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

The pipeline is `latex` then `dvisvgm --no-fonts` (glyphs become paths, so the
SVG displays without TeX fonts installed). Both ship with MacTeX/TeX Live.
"""
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


def _run(cmd, cwd):
    """Run a compile step, surfacing the tool's log tail if it fails."""
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        tail = "\n".join((result.stdout + result.stderr).splitlines()[-30:])
        raise RuntimeError(f"{cmd[0]} failed:\n{tail}")


def render_svg(body: str) -> bytes:
    """Compile a \\Qcircuit body and return the SVG bytes."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "circuit.tex").write_text(TEMPLATE % body.strip())

        _run(
            ["latex", "-interaction=nonstopmode", "-halt-on-error", "circuit.tex"],
            cwd=tmp_path,
        )
        _run(
            ["dvisvgm", "--no-fonts", "-Z", str(ZOOM), "-o", "circuit.svg", "circuit.dvi"],
            cwd=tmp_path,
        )
        return (tmp_path / "circuit.svg").read_bytes()


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
