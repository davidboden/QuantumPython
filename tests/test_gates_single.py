import unittest
from qubit import Qubit
from gates_single import hadamard, xrotation, xrotation_pauli_expression, yrotation, yrotation_pauli_expression, zrotation, zrotation_pauli_expression
from sympy.physics.paulialgebra import Pauli
from sympy.physics.matrices import msigma
from sympy import sqrt, Matrix, I

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

    def test_xrotation_gate(self):
        """
        Check that the xrotation gate has the same effect on the observables as evaluating
        U† * observable * U (conjugate transpose on the left).
        See xrotation_pauli_expression in gates_single.py for the derivation of the expression.
        The evolve result contains half-angle expressions; simplify reduces them to cos(θ)/sin(θ).
        """
        from sympy import Symbol, simplify
        theta = Symbol('theta', real=True)
        u        = xrotation_pauli_expression(theta, label="a")
        u_dagger = xrotation_pauli_expression(-theta, label="a")

        a = Qubit.qubit_time_0("a")
        a_after_xrotation_gate  = xrotation(a, theta)
        a_after_xrotation_pauli = a.evolve(u, u_dagger)

        self.assertEqual(simplify(a_after_xrotation_gate.x - a_after_xrotation_pauli.x), 0)
        self.assertEqual(simplify(a_after_xrotation_gate.y - a_after_xrotation_pauli.y), 0)
        self.assertEqual(simplify(a_after_xrotation_gate.z - a_after_xrotation_pauli.z), 0)

    def test_yrotation_gate(self):
        """
        Check that the yrotation gate has the same effect on the observables as evaluating
        U† * observable * U (conjugate transpose on the left).
        See yrotation_pauli_expression in gates_single.py for the derivation of the expression.
        The evolve result contains half-angle expressions; simplify reduces them to cos(θ)/sin(θ).
        """
        from sympy import Symbol, simplify
        theta = Symbol('theta', real=True)
        u        = yrotation_pauli_expression(theta, label="a")
        u_dagger = yrotation_pauli_expression(-theta, label="a")

        a = Qubit.qubit_time_0("a")
        a_after_yrotation_gate  = yrotation(a, theta)
        a_after_yrotation_pauli = a.evolve(u, u_dagger)

        self.assertEqual(simplify(a_after_yrotation_gate.x - a_after_yrotation_pauli.x), 0)
        self.assertEqual(simplify(a_after_yrotation_gate.y - a_after_yrotation_pauli.y), 0)
        self.assertEqual(simplify(a_after_yrotation_gate.z - a_after_yrotation_pauli.z), 0)

    def test_zrotation_gate(self):
        """
        Check that the zrotation gate has the same effect on the observables as evaluating
        U† * observable * U (conjugate transpose on the left).
        See zrotation_pauli_expression in gates_single.py for the derivation of the expression.
        The evolve result contains half-angle expressions; simplify reduces them to cos(θ)/sin(θ).
        """
        from sympy import Symbol, simplify
        theta = Symbol('theta', real=True)
        u        = zrotation_pauli_expression(theta, label="a")
        u_dagger = zrotation_pauli_expression(-theta, label="a")

        a = Qubit.qubit_time_0("a")
        a_after_zrotation_gate  = zrotation(a, theta)
        a_after_zrotation_pauli = a.evolve(u, u_dagger)

        self.assertEqual(simplify(a_after_zrotation_gate.x - a_after_zrotation_pauli.x), 0)
        self.assertEqual(simplify(a_after_zrotation_gate.y - a_after_zrotation_pauli.y), 0)
        self.assertEqual(simplify(a_after_zrotation_gate.z - a_after_zrotation_pauli.z), 0)
