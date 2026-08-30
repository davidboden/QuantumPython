import unittest
from sympy import eye, expand, conjugate, transpose, Matrix
from sympy.physics.matrices import msigma
from sympy.physics.quantum import TensorProduct
from qubit import Qubit
from gates_multi import toffoli, toffoli_pauli_expression
from tests.pauli_matrix import pauli_expr_to_matrix

I2 = eye(2)

LABELS = ("control1", "control2", "target")


def _to_matrix(expr):
    return pauli_expr_to_matrix(expr, LABELS)


def _embed(*mats):
    """A single-qubit operator per slot, tensored into the 3-qubit space."""
    return TensorProduct(*mats)


class ToffoliMatrixTestCase(unittest.TestCase):

    # Toffoli (CCNOT) matrix (its own transpose), hardcoded in the |0> = +1
    # Z-eigenvalue convention: X fires on the target only when both controls are
    # |1> (the final 2x2 block).
    toffolimatrix = Matrix([
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 1, 0],
    ])

    def test_toffoli_matrix_is_self_adjoint(self):
        # Real and symmetric, so the conjugate transpose is the matrix itself.
        # That means matrix evolution U_dagger * O * U can safely use U for both
        # factors, matching Qubit.evolve's default and gates_multi's claim that
        # CCNOT^2 = I.
        self.assertEqual(transpose(conjugate(self.toffolimatrix)), self.toffolimatrix)
        self.assertEqual(self.toffolimatrix * self.toffolimatrix, eye(8))

    def test_pauli_expression_matches_hardcoded_matrix(self):
        # gates_multi.toffoli_pauli_expression, as an 8x8 matrix, is the
        # hardcoded Toffoli.
        self.assertEqual(
            _to_matrix(toffoli_pauli_expression(*LABELS)),
            self.toffolimatrix,
        )

    def test_gate_definition_matches_pauli_arithmetic(self):
        control1 = Qubit.qubit_time_0("control1")
        control2 = Qubit.qubit_time_0("control2")
        target = Qubit.qubit_time_0("target")

        u = toffoli_pauli_expression("control1", "control2", "target")

        control1_after_evolve = control1.evolve(u)
        control2_after_evolve = control2.evolve(u)
        target_after_evolve = target.evolve(u)

        (control1_after_gate, control2_after_gate, target_after_gate) = toffoli(
            control1, control2, target
        )

        assert control1_after_evolve == control1_after_gate
        assert control2_after_evolve == control2_after_gate
        assert target_after_evolve == target_after_gate

    def _assert_matrix_evolution_matches_gate(self, slot_index, component):
        qubits = [Qubit.qubit_time_0(label) for label in LABELS]

        mats = [I2, I2, I2]
        mats[slot_index] = msigma({"x": 1, "y": 2, "z": 3}[component])
        observable = _embed(*mats)

        # Self-adjoint, so U_dagger == U.
        evolved = (self.toffolimatrix * observable * self.toffolimatrix).applyfunc(expand)

        gate_result = toffoli(*qubits)[slot_index]
        from_gate = _to_matrix(getattr(gate_result, component))

        self.assertEqual(evolved, from_gate)

    def test_control1_x_observable(self):
        self._assert_matrix_evolution_matches_gate(0, "x")

    def test_control1_y_observable(self):
        self._assert_matrix_evolution_matches_gate(0, "y")

    def test_control1_z_observable(self):
        self._assert_matrix_evolution_matches_gate(0, "z")

    def test_control2_x_observable(self):
        self._assert_matrix_evolution_matches_gate(1, "x")

    def test_control2_y_observable(self):
        self._assert_matrix_evolution_matches_gate(1, "y")

    def test_control2_z_observable(self):
        self._assert_matrix_evolution_matches_gate(1, "z")

    def test_target_x_observable(self):
        self._assert_matrix_evolution_matches_gate(2, "x")

    def test_target_y_observable(self):
        self._assert_matrix_evolution_matches_gate(2, "y")

    def test_target_z_observable(self):
        self._assert_matrix_evolution_matches_gate(2, "z")
