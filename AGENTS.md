# Instructions

## Running the tests

Tests use pytest and must be run from the project root using the virtual environment:

```bash
.venv/bin/python -m pytest tests/ -q --tb=short

`-q --tb=short` keeps output minimal to reduce context usage. If a test fails, rerun it individually with `-v` for more detail:

```bash
.venv/bin/python -m pytest tests/test_gate.py::GateTestCase::test_name -v
```
```

## Spelling

- **Schrödinger** refers to [Erwin Schrödinger](https://en.wikipedia.org/wiki/Erwin_Schrödinger). Correct any misspellings.
- **Heisenberg** refers to [Werner Heisenberg](https://en.wikipedia.org/wiki/Werner_Heisenberg). Correct any misspellings.

## Glossary

- **Hadamard** refers to the Hadamard gate as used in quantum computing: [Hadamard transform — Quantum computing applications](https://en.wikipedia.org/wiki/Hadamard_transform#Quantum_computing_applications).

- **Deutsch** refers to [David Deutsch](https://en.wikipedia.org/wiki/David_Deutsch).

- **Jozsa** refers to [Richard Jozsa](https://en.wikipedia.org/wiki/Richard_Jozsa).
