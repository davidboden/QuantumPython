import unittest

from sympy import simplify, sqrt, Matrix, Symbol, exp, I

from qubit import Qubit
from gates_single import hadamard, zrotation
from gates_multi import cnot
from schrodinger import density_matrix, state_vector


class SchrodingerTestCase(unittest.TestCase):
    def test_product_zero_state(self):
        """Two untouched qubits should reconstruct as |00>."""
        c = Qubit.qubit_time_0("c")
        t = Qubit.qubit_time_0("t")

        vec = state_vector([c, t])

        self.assertEqual(vec, Matrix([[1], [0], [0], [0]]))

    def test_density_matrix_of_zero_state_is_projector(self):
        c = Qubit.qubit_time_0("c")
        t = Qubit.qubit_time_0("t")

        rho = density_matrix([c, t])

        expected = Matrix([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        self.assertEqual(simplify(rho), expected)

    def test_bell_state(self):
        """Hadamard on the control followed by CNOT should give (|00> + |11>)/sqrt(2)."""
        c = Qubit.qubit_time_0("c")
        t = Qubit.qubit_time_0("t")

        c, t = cnot(hadamard(c), t)

        vec = simplify(state_vector([c, t]))

        self.assertEqual(vec, Matrix([[sqrt(2) / 2], [0], [0], [sqrt(2) / 2]]))

    def test_state_vector_picks_up_relative_phase(self):
        """A Z-rotation after Hadamard should leave a relative phase of exp(i*theta) between |0> and |1>."""
        theta = Symbol('theta', real=True)

        q = Qubit.qubit_time_0("a")
        q = zrotation(hadamard(q), theta)

        vec = simplify(state_vector([q]))

        ratio = simplify(vec[0] / vec[1])
        self.assertEqual(simplify(ratio.rewrite(exp)), exp(I * theta))

    def test_state_vector_is_normalised(self):
        c = Qubit.qubit_time_0("c")
        t = Qubit.qubit_time_0("t")

        c, t = cnot(hadamard(c), t)

        vec = simplify(state_vector([c, t]))

        norm_squared = simplify((vec.T * vec.conjugate())[0, 0])
        self.assertEqual(norm_squared, 1)
