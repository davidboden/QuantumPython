"""Simon's problem — the worked $n = 3$, $s = 110$ example.

The oracle computes

    f(x1, x2, x3) = ( 1 ^ x1 ^ x2 ^ x3,   x3,   (1 ^ x1 ^ x2) & (1 ^ x3) )

which is two-to-one with period s = 110: flipping x1 and x2 together leaves
the output unchanged. Input bits x1 x2 x3 are carried by qubits a, b, c; the
output bits f1 f2 f3 land on qubits d, e, f; t is a scratch ancilla.

The narrative lives in "102 SimonsProblem.ipynb"; tests/test_simons_problem.py
verifies the oracle on every classical input and on the colliding superpositions.
"""
from sympy.physics.paulialgebra import Pauli
from qubit import Qubit
from gates_single import hadamard, qnot
from gates_multi import cnot, toffoli

# f(x1 x2 x3) -> y1 y2 y3 for the s = 110 example (Wikipedia's Simon's problem).
TRUTH_TABLE = {
    "000": "101", "001": "010", "010": "000", "011": "110",
    "100": "000", "101": "110", "110": "101", "111": "010",
}

SECRET = "110"

_LABELS = "abcdeft"


def oracle(qa, qb, qc, qd, qe, qf, qt):
    """Heisenberg-evolve the seven qubits through the s = 110 oracle circuit.

    Built from CNOTs plus a single Toffoli, which supplies the AND that the
    nonlinear output bit f3 needs and that a CNOT-only circuit cannot produce.
    """
    qt = qnot(qt)
    qa, qt = cnot(qa, qt)
    qb, qt = cnot(qb, qt)
    qt, qd = cnot(qt, qd)
    qc, qd = cnot(qc, qd)
    qc, qe = cnot(qc, qe)
    qt, qf = cnot(qt, qf)
    qt, qc, qf = toffoli(qt, qc, qf)
    return qa, qb, qc, qd, qe, qf, qt


def measure_z(z_observable, bits):
    """Read a bit from an evolved Z observable evaluated on a basis state.

    ``bits`` maps qubit label -> 0/1. Z = +1 for |0>, Z = -1 for |1>; a qubit
    prepared in a definite basis state has X = Y = 0.
    """
    substitutions = {}
    for label, bit in bits.items():
        substitutions[Pauli(1, label=label)] = 0
        substitutions[Pauli(2, label=label)] = 0
        substitutions[Pauli(3, label=label)] = 1 - 2 * bit
    return 0 if z_observable.subs(substitutions) == 1 else 1


def _fresh_register():
    qa, qb, qc = (Qubit.qubit_time_0(label) for label in "abc")
    qd, qe, qf = (Qubit.qubit_time_0(label) for label in "def")
    qt = Qubit.qubit_time_0("t")
    return qa, qb, qc, qd, qe, qf, qt


def _read_output(qd, qe, qf):
    bits = {label: 0 for label in _LABELS}
    return "".join(str(measure_z(q.z, bits)) for q in (qd, qe, qf))


def classical_output(x):
    """Run the oracle on the computational-basis input x = "x1x2x3" and return
    the output register d e f as a 3-character bit string."""
    x1, x2, x3 = (int(bit) for bit in x)
    qa, qb, qc, qd, qe, qf, qt = _fresh_register()

    if x1:
        qa = qnot(qa)
    if x2:
        qb = qnot(qb)
    if x3:
        qc = qnot(qc)

    qa, qb, qc, qd, qe, qf, qt = oracle(qa, qb, qc, qd, qe, qf, qt)
    return _read_output(qd, qe, qf)


def collision_output(b, c):
    """Prepare (|0,b,c> + |1,~b,c>)/sqrt(2) — a pair of inputs differing by
    s = 110 — run it through the oracle, and return the (definite) output
    register. Both branches share an output, so the result is a single value."""
    qa, qb, qc, qd, qe, qf, qt = _fresh_register()

    if b:
        qb = qnot(qb)
    if c:
        qc = qnot(qc)
    qa = hadamard(qa)
    qa, qb = cnot(qa, qb)

    qa, qb, qc, qd, qe, qf, qt = oracle(qa, qb, qc, qd, qe, qf, qt)
    return _read_output(qd, qe, qf)
