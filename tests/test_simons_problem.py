import unittest

from sympy import expand
from sympy.physics.paulialgebra import Pauli

from gates_single import hadamard
from qubit import Qubit
from simons_problem import (
    SECRET,
    TRUTH_TABLE,
    classical_output,
    collision_output,
    oracle,
)
from sympy_pauli import evaluate_labelled_pauli_product


def _xor(x, s):
    return format(int(x, 2) ^ int(s, 2), f"0{len(x)}b")


def _sx(label):
    return Pauli(1, label=label)


def _sz(label):
    return Pauli(3, label=label)


class SimonsTruthTableTestCase(unittest.TestCase):
    """The truth table itself is two-to-one with period s = 110."""

    def test_two_to_one_with_period_s(self):
        for x, y in TRUTH_TABLE.items():
            self.assertEqual(
                TRUTH_TABLE[_xor(x, SECRET)], y,
                f"f({x}) and f({x} XOR {SECRET}) should agree",
            )

    def test_only_x_and_x_xor_s_collide(self):
        for x, y in TRUTH_TABLE.items():
            sharers = {other for other, z in TRUTH_TABLE.items() if z == y}
            self.assertEqual(sharers, {x, _xor(x, SECRET)})


class SimonsOracleClassicalTestCase(unittest.TestCase):
    """The oracle circuit reproduces the truth table on every classical input."""

    def test_all_eight_classical_inputs(self):
        for x, expected in TRUTH_TABLE.items():
            self.assertEqual(classical_output(x), expected, f"f({x})")


class SimonsOracleSuperpositionTestCase(unittest.TestCase):
    """Each colliding pair, prepared as (|x> + |x XOR s>)/sqrt(2), leaves the
    output register in the single shared value f(x)."""

    def test_colliding_pairs_collapse_to_shared_output(self):
        for b in (0, 1):
            for c in (0, 1):
                x = f"0{b}{c}"
                partner = _xor(x, SECRET)
                output = collision_output(b, c)
                self.assertEqual(output, TRUTH_TABLE[x], f"pair {x}/{partner}")
                self.assertEqual(output, TRUTH_TABLE[partner], f"pair {x}/{partner}")


class SimonsObservablesTestCase(unittest.TestCase):
    """After Hadamarding a, b, c and running the oracle — the "measure the
    output right after the oracle" picture from 102 SimonsProblem.ipynb — each
    qubit's evolved Z observable equals the hardcoded Pauli expression the
    notebook quotes (extended to a, b, c, t, which the notebook leaves implicit)."""

    def test_z_observables_match_hardcoded_expressions(self):
        qa, qb, qc = (Qubit.qubit_time_0(label) for label in "abc")
        qd, qe, qf = (Qubit.qubit_time_0(label) for label in "def")
        qt = Qubit.qubit_time_0("t")
        qa, qb, qc = hadamard(qa), hadamard(qb), hadamard(qc)
        qa, qb, qc, qd, qe, qf, qt = oracle(qa, qb, qc, qd, qe, qf, qt)
        evolved = dict(a=qa, b=qb, c=qc, d=qd, e=qe, f=qf, t=qt)

        sx, sz = _sx, _sz
        expected = {
            # the first Hadamard sends Z -> X; the oracle uses a, b, c only as
            # controls, so their Z observable is otherwise untouched
            "a": sx("a"),
            "b": sx("b"),
            "c": sx("c"),
            # d = 1 ^ a ^ b ^ c
            "d": -sx("a") * sx("b") * sx("c") * sz("d") * sz("t"),
            # e = c
            "e": sx("c") * sz("e"),
            # f = (1 ^ a ^ b) & (1 ^ c) -- the nonlinear bit built by the Toffoli
            "f": sz("f") / 2 * ((1 - sx("c")) - sx("a") * sx("b") * sz("t") * (1 + sx("c"))),
            # ancilla left dirty at t = 1 ^ a ^ b
            "t": -sx("a") * sx("b") * sz("t"),
        }

        for label, expr in expected.items():
            self.assertEqual(
                evolved[label].z,
                evaluate_labelled_pauli_product(expand(expr)),
                f"Z observable for qubit {label}",
            )
