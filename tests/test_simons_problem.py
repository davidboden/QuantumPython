import unittest

from simons_problem import (
    SECRET,
    TRUTH_TABLE,
    classical_output,
    collision_output,
)


def _xor(x, s):
    return format(int(x, 2) ^ int(s, 2), f"0{len(x)}b")


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
