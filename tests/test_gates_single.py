import unittest
from qubit import Qubit
from gates_single import hadamard
from sympy.physics.paulialgebra import Pauli
from sympy.physics.matrices import msigma
from sympy import sqrt, Matrix

class SingleGateTestCase(unittest.TestCase):

    hadamardmatrix = 1/sqrt(2) * Matrix([
        [ 1,  1],
        [ 1, -1]
    ])

    def test_hadmard_gate(self):
        """
        Check that the hadamard gate has the same effect on the observables as evaluating
        U† * observable * U (conjugate transpose on the left).
        In this case U† = U because the Hadamard is real and symmetric.
        """
        hadamard_gate_pauli = 1/sqrt(2) * (Pauli(1, label="a") + Pauli(3, label="a"))

        a = Qubit.qubit_time_0("a")
        a_after_hadamard_gate = hadamard(a)
        a_after_hadamard_pauli = a.evolve(hadamard_gate_pauli)

        self.assertEqual(
            a_after_hadamard_gate,
            a_after_hadamard_pauli
        )

    def test_hadamard_x_observable_matrix(self):
        result = self.hadamardmatrix.H * msigma(1) * self.hadamardmatrix

        expected_result = msigma(3)

        self.assertEqual(expected_result, result)

    def test_hadamard_y_observable_matrix(self):
        result = self.hadamardmatrix.H * msigma(2) * self.hadamardmatrix

        expected_result = -msigma(2)

        self.assertEqual(expected_result, result)

    def test_hadamard_z_observable_matrix(self):
        result = self.hadamardmatrix.H * msigma(3) * self.hadamardmatrix

        expected_result = msigma(1)

        self.assertEqual(expected_result, result)
