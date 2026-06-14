import unittest
from sympy import eye
from sympy.physics.matrices import msigma
from sympy.physics.quantum import TensorProduct
from sympy.physics.paulialgebra import Pauli
from qubit import Qubit
from gates_multi import cnot

class CnotMatrixTestCase(unittest.TestCase):

    # CNOT matrix is it's own transpose
    cnotmatrix = TensorProduct((eye(2) + msigma(3)) / 2, eye(2)) + TensorProduct((eye(2) - msigma(3)) / 2, msigma(1))
    # from sympy import Matrix
    # cnotmatrix = Matrix([
    #     [1, 0, 0, 0],
    #     [0, 1, 0, 0],
    #     [0, 0, 0, 1],
    #     [0, 0, 1, 0]
    # ])
    cnotpauli = ((1 + Pauli(3, label="control")) / 2) + (((1 - Pauli(3, label="control")) * Pauli(1, label="target")) / 2)

    # The Deutsch and Hayden paper uses this arrangement, which applies the X
    # rotation if the control qubit z-observable has an eigenvalue of 1, which
    # doesn't fit with the normal convention of making a rotation when the
    # eigenvalue is -1.
    # This is because in point (4) on the paper, we're considering eigenvalue -1 to be "0"
    # in the computational basis, which is opposite to what has become normal convention.
    #reversedcnotmatrix = TensorProduct((eye(2) - msigma(3)) / 2, eye(2)) + TensorProduct((eye(2) + msigma(3)) / 2, msigma(1))

    def test_gate_definition_matches_pauli_arithmetic(self):
        control_qubit = Qubit.qubit_time_0("control")
        target_qubit = Qubit.qubit_time_0("target")

        # Use evolve with the pauli expression
        control_qubit_after_evolve = control_qubit.evolve(self.cnotpauli)
        target_qubit_after_evolve = target_qubit.evolve(self.cnotpauli)

        # Use the gate definition with hardcoded (faster) behaviour
        (control_qubit_after_gate, target_qubit_after_gate) = cnot(control_qubit, target_qubit)

        # Verify that the end result is the same to prove that the hardcoded
        # behaviour represents the Pauli-based transformation
        assert control_qubit_after_evolve == control_qubit_after_gate
        assert target_qubit_after_evolve == target_qubit_after_gate


    def test_control_x_observable(self):
        control_x = TensorProduct(msigma(1), eye(2))

        result = self.cnotmatrix * control_x * self.cnotmatrix

        expected_result = TensorProduct(msigma(1), msigma(1))

        self.assertEqual(expected_result, result)

    def test_control_y_observable(self):
        control_y = TensorProduct(msigma(2), eye(2))

        result = self.cnotmatrix * control_y * self.cnotmatrix

        expected_result = TensorProduct(msigma(2), msigma(1))

        self.assertEqual(expected_result, result)

    def test_control_z_observable(self):
        control_z = TensorProduct(msigma(3), eye(2))

        result = self.cnotmatrix * control_z * self.cnotmatrix

        expected_result = TensorProduct(msigma(3), eye(2))

        self.assertEqual(expected_result, result)

    def test_target_x_observable(self):
        target_x = TensorProduct(eye(2), msigma(1))

        result = self.cnotmatrix * target_x * self.cnotmatrix

        expected_result = TensorProduct(eye(2), msigma(1))

        self.assertEqual(expected_result, result)

    def test_target_y_observable(self):
        target_y = TensorProduct(eye(2), msigma(2))

        result = self.cnotmatrix * target_y * self.cnotmatrix

        expected_result = TensorProduct(msigma(3), msigma(2))

        self.assertEqual(expected_result, result)

    def test_target_z_observable(self):
        target_z = TensorProduct(eye(2), msigma(3))

        result = self.cnotmatrix * target_z * self.cnotmatrix

        expected_result = TensorProduct(msigma(3), msigma(3))

        self.assertEqual(expected_result, result)
