# Instructions

## Workflow

This is a solo project — don't create feature branches, worktrees, or pull requests to land changes. Edit files directly on `main` and leave them uncommitted. Only run `git add`/`git commit`/`git push` if explicitly instructed to in that turn.

## Running the tests

Tests use pytest and must be run from the project root using the virtual environment:

```bash
.venv/bin/python -m pytest tests/ -q --tb=short

`-q --tb=short` keeps output minimal to reduce context usage. If a test fails, rerun it individually with `-v` for more detail:

```bash
.venv/bin/python -m pytest tests/test_gate.py::GateTestCase::test_name -v
```
```

## Quantum circuit diagrams

Circuit diagrams are typeset with [Qcircuit](https://github.com/CQuIC/qcircuit), a LaTeX/Xy-pic package. Jupyter's MathJax cannot render it inline, so diagrams are rendered **at edit time** — never at notebook runtime — and referenced from markdown cells as static images. Each diagram is a pair of files in `images/`:

- `images/<name>.tex` — the Qcircuit source. **This is the only file you edit.**
- `images/<name>.svg` — the render. Never hand-edit it, and never try to parse or reverse-engineer it; the `.tex` file is the readable form of the diagram.

Rendering is strictly one-way, `.tex` → `.svg`, via the helper in the repo root:

```bash
python3 render_qcircuit.py <name>          # renders images/<name>.tex -> images/<name>.svg
python3 render_qcircuit.py --check         # verifies every .svg matches its .tex source
```

Requires a local LaTeX install with the `qcircuit` package, plus `dvisvgm` (both come with MacTeX/TeX Live).

### Keeping source and render in sync

The `.tex` and `.svg` for a given name must always correspond. Concretely:

- **Whenever you create or edit an `images/*.tex` file, immediately re-run `python3 render_qcircuit.py <name>`** in the same change. Never leave an edited `.tex` with a stale `.svg`.
- After any task that touched circuit diagrams, run `python3 render_qcircuit.py --check` and fix anything it reports before finishing.
- Never modify an `.svg` directly — if a diagram is wrong, fix the `.tex` and re-render.
- Never delete one file of the pair without the other.

(`--check` re-renders each `.tex` and compares canonicalised SVG output, so it is a reliable pass/fail, not a heuristic.)

### Adding or editing a diagram

1. Write the `\Qcircuit` body to `images/<name>.tex` (kebab-case `<name>`, unique in `images/`) — one row per qubit wire, `&`-separated columns, every row except the last ending in `\\`. Every row must have the **same number of columns**; pad with `\qw` where nothing happens on that wire.
2. Render it: `python3 render_qcircuit.py <name>`.
3. Reference it from a notebook markdown cell:

   ```html
   <img src="images/<name>.svg" alt="<what the circuit does, wire by wire>" width="420"/>
   ```

### Qcircuit macro cheat-sheet

| Macro | Meaning |
|---|---|
| `\qw` | plain wire segment (fills an empty column) |
| `\gate{H}` | boxed single-qubit gate (any label: `\gate{X}`, `\gate{U_f}`) |
| `\lstick{a: \ket{0}}` | label at the left end of a wire (contents are math mode; `\ket` comes from the `braket` package) |
| `\ctrl{n}` | control dot, with the vertical line reaching the gate *n* rows below (`\ctrl{-2}` = 2 rows above) |
| `\targ` | CNOT target ⊕ — goes in the **same column** as its `\ctrl` |
| `\meter` | measurement box; wires that are not measured just end with `\qw` |
| `\multigate{n}{U}` | gate box spanning this wire and the *n* wires below; put `\ghost{U}` in the same column on each covered wire |
| `\cw` | classical (double) wire, for after a `\meter` |

Column/row spacing is set by `@C=1em @R=1em` in the template inside `render_qcircuit.py`. Full reference: [Qcircuit tutorial PDF](https://physics.unm.edu/CQuIC/Qcircuit/Qtutorial.pdf) — but the table above covers everything used in this repo.

If rendering fails, the script raises with the tail of the LaTeX log. The usual causes are a missing `\\` between rows, rows with unequal column counts, or a misspelled macro.

### Example

`images/bell-state-circuit.tex` (rendered to `images/bell-state-circuit.svg` by `python3 render_qcircuit.py bell-state-circuit`) is a Bell-pair preparation and measurement circuit:

```latex
\lstick{\ket{0}} & \gate{H} & \ctrl{1} & \qw & \meter \\
\lstick{\ket{0}} & \qw      & \targ    & \qw & \meter
```

<img src="images/bell-state-circuit.svg" alt="Bell state preparation circuit: H on qubit 1 then CNOT onto qubit 2, both measured" width="300"/>

## Spelling

- **Schrödinger** refers to [Erwin Schrödinger](https://en.wikipedia.org/wiki/Erwin_Schrödinger). Correct any misspellings.
- **Heisenberg** refers to [Werner Heisenberg](https://en.wikipedia.org/wiki/Werner_Heisenberg). Correct any misspellings.

## Glossary

- **Hadamard** refers to the Hadamard gate as used in quantum computing: [Hadamard transform — Quantum computing applications](https://en.wikipedia.org/wiki/Hadamard_transform#Quantum_computing_applications).

- **Deutsch** refers to [David Deutsch](https://en.wikipedia.org/wiki/David_Deutsch).

- **Jozsa** refers to [Richard Jozsa](https://en.wikipedia.org/wiki/Richard_Jozsa).
