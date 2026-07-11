#!/usr/bin/env python3
r"""Render Qcircuit (https://github.com/CQuIC/qcircuit) diagrams to SVG.

Qcircuit is a LaTeX package (Xy-pic based) for typesetting quantum circuit
diagrams. Jupyter's MathJax cannot render it inline, so diagrams are rendered
at edit time and referenced from notebooks as static `<img>` tags.

Each diagram is a pair of files in images/:

    images/<name>.tex   the source — the body passed to \Qcircuit (edit this)
    images/<name>.svg   the render (never edit this; regenerate it)

The .tex file contains one row per qubit wire, `&`-separated columns, rows
ending in `\\`, e.g.:

    \lstick{\ket{0}} & \gate{H} & \ctrl{1} & \qw & \meter \\
    \lstick{\ket{0}} & \qw      & \targ    & \qw & \meter

Rendering is one-way, .tex -> .svg:

    python3 render_qcircuit.py <name>     render images/<name>.tex
    python3 render_qcircuit.py --check    verify every .svg matches its .tex

The pipeline is `latex` then `dvisvgm --no-fonts`. `latex` ships with
MacTeX/TeX Live. `dvisvgm` must be Homebrew's build (`brew install dvisvgm`),
not the older one bundled with MacTeX: qcircuit's `\meter` gate draws its
needle with a PostScript special, and MacTeX's dvisvgm (2.3.5) isn't linked
against Ghostscript, so it silently drops that special and the needle renders
as a jagged staircase of tiny rectangles instead of a smooth diagonal line.
Homebrew's dvisvgm is linked against Ghostscript and renders it correctly.
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

TEMPLATE = r"""
\documentclass[border=2pt]{standalone}
\usepackage{braket}
\usepackage{qcircuit}
\begin{document}
\Qcircuit @C=1em @R=1em {
%s
}
\end{document}
"""

REPO_ROOT = Path(__file__).resolve().parent
IMAGES_DIR = REPO_ROOT / "images"
ZOOM = 1.5  # scale factor from TeX's natural size to a comfortable screen size

# Homebrew's dvisvgm isn't part of the Homebrew texlive keg, so its bundled
# kpathsea resolves TEXMFROOT relative to its own install dir and can't find
# texlive's PostScript header files (tex.pro etc.) needed to process the
# \meter needle's PostScript special. Point it at Homebrew texlive's tree
# explicitly, via the stable unversioned `opt` symlink.
_TEXLIVE_SHARE = Path("/opt/homebrew/opt/texlive/share")
_DVISVGM_ENV = {
    **os.environ,
    "TEXMFCNF": str(_TEXLIVE_SHARE / "texmf-dist" / "web2c"),
    "TEXMFROOT": str(_TEXLIVE_SHARE),
} if _TEXLIVE_SHARE.exists() else os.environ


def _run(cmd, cwd, env=None) -> str:
    """Run a compile step, surfacing the tool's log tail if it fails.

    Returns the combined stdout+stderr on success, so callers can inspect it
    for warnings even when the command didn't fail.
    """
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)
    output = result.stdout + result.stderr
    if result.returncode != 0:
        tail = "\n".join(output.splitlines()[-30:])
        raise RuntimeError(f"{cmd[0]} failed:\n{tail}")
    return output


def render_svg(body: str, capture_log: bool = False):
    """Compile a \\Qcircuit body and return the SVG bytes.

    If capture_log is True, returns (svg_bytes, log) instead, where log is
    the combined latex + dvisvgm output (including any warnings).
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "circuit.tex").write_text(TEMPLATE % body.strip())

        log = _run(
            ["latex", "-interaction=nonstopmode", "-halt-on-error", "circuit.tex"],
            cwd=tmp_path,
        )
        log += _run(
            ["dvisvgm", "--no-fonts", "-Z", str(ZOOM), "-o", "circuit.svg", "circuit.dvi"],
            cwd=tmp_path,
            env=_DVISVGM_ENV,
        )
        svg_bytes = (tmp_path / "circuit.svg").read_bytes()
        return (svg_bytes, log) if capture_log else svg_bytes


def render(name: str) -> Path:
    """Render images/<name>.tex to images/<name>.svg."""
    tex_file = IMAGES_DIR / f"{name}.tex"
    dest = IMAGES_DIR / f"{name}.svg"
    dest.write_bytes(render_svg(tex_file.read_text()))
    return dest


def _canonical(svg: bytes):
    """Canonical form for comparing renders.

    dvisvgm emits the glyph <path> definitions inside <defs> in a
    nondeterministic order, so sort those lines; everything else (the <use>
    and <rect> drawing elements) is order-significant and kept as is.
    """
    lines = svg.decode().splitlines()
    glyphs = sorted(line for line in lines if line.startswith("<path "))
    rest = [line for line in lines if not line.startswith("<path ")]
    return glyphs, rest


def check() -> int:
    """Verify every images/*.tex renders to exactly its committed .svg."""
    failures = 0
    tex_files = sorted(IMAGES_DIR.glob("*.tex"))
    if not tex_files:
        print(f"No .tex circuit sources found in {IMAGES_DIR}")
        return 1
    for tex_file in tex_files:
        svg_file = tex_file.with_suffix(".svg")
        if not svg_file.exists():
            print(f"STALE  {svg_file.name}: missing — run: python3 render_qcircuit.py {tex_file.stem}")
            failures += 1
            continue
        if _canonical(render_svg(tex_file.read_text())) != _canonical(svg_file.read_bytes()):
            print(f"STALE  {svg_file.name}: does not match {tex_file.name} — run: python3 render_qcircuit.py {tex_file.stem}")
            failures += 1
        else:
            print(f"ok     {svg_file.name}")
    return 1 if failures else 0


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    if sys.argv[1] == "--check":
        sys.exit(check())
    dest = render(sys.argv[1])
    print(f"Wrote {dest}")


if __name__ == "__main__":
    main()
