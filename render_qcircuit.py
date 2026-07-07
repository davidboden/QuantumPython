#!/usr/bin/env python3
"""Render a Qcircuit (https://github.com/CQuIC/qcircuit) diagram to a PNG.

Qcircuit is a LaTeX package (Xy-pic based) for typesetting quantum circuit
diagrams. It is not something Jupyter's MathJax can render inline, so the
workflow here is: write the `\\Qcircuit{...}` body, compile it standalone
with `latex`, rasterise the DVI with `dvipng`, then embed the resulting PNG
in a notebook markdown cell the same way the other images/ assets are used.

Usage:
    python render_qcircuit.py <output-name> <circuit.tex>

`<circuit.tex>` should contain just the body passed to `\\Qcircuit`, e.g.:

    \\lstick{\\ket{0}} & \\gate{H} & \\ctrl{1} & \\qw & \\meter \\\\
    \\lstick{\\ket{0}} & \\qw      & \\targ    & \\qw & \\meter

The rendered PNG is written to images/<output-name>.png.
"""
import shutil
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
DPI = 300


def render(body: str, output_name: str) -> Path:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        tex_file = tmp_path / "circuit.tex"
        tex_file.write_text(TEMPLATE % body.strip())

        subprocess.run(
            ["latex", "-interaction=nonstopmode", "-halt-on-error", tex_file.name],
            cwd=tmp_path,
            check=True,
            capture_output=True,
        )

        dvi_file = tmp_path / "circuit.dvi"
        png_file = tmp_path / "circuit.png"
        subprocess.run(
            ["dvipng", "-D", str(DPI), "-T", "tight", "-o", png_file.name, dvi_file.name],
            cwd=tmp_path,
            check=True,
            capture_output=True,
        )

        IMAGES_DIR.mkdir(exist_ok=True)
        dest = IMAGES_DIR / f"{output_name}.png"
        shutil.copy(png_file, dest)
        return dest


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    output_name, circuit_tex_path = sys.argv[1], Path(sys.argv[2])
    body = circuit_tex_path.read_text()
    dest = render(body, output_name)
    print(f"Wrote {dest}")


if __name__ == "__main__":
    main()
