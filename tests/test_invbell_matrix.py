import unittest
from sympy import sqrt, Matrix, eye, simplify, transpose
from sympy.physics.matrices import msigma
from sympy.physics.quantum import TensorProduct

class InvbellMatrixTestCase(unittest.TestCase):

    # CNOT matrix is its own transpose
    cnotmatrix = Matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ])

    hadamardmatrix = 1/sqrt(2) * Matrix([
        [ 1,  1], 
        [ 1, -1]
    ])

    hadamardthencnotmatrix = simplify(cnotmatrix * TensorProduct(hadamardmatrix, eye(2)))

    def test_control_x_observable(self):
        control_x = TensorProduct(msigma(1), eye(2))

        result = transpose(self.hadamardthencnotmatrix) * control_x * self.hadamardthencnotmatrix

        expected_result = TensorProduct(msigma(3), msigma(1))

        self.assertEqual(expected_result, result)

    def test_control_y_observable(self):
        control_y = TensorProduct(msigma(2), eye(2))

        result = transpose(self.hadamardthencnotmatrix) * control_y * self.hadamardthencnotmatrix

        expected_result = -TensorProduct(msigma(2), msigma(1))

        self.assertEqual(expected_result, result)

    def test_control_z_observable(self):
        control_z = TensorProduct(msigma(3), eye(2))

        result = transpose(self.hadamardthencnotmatrix) * control_z * self.hadamardthencnotmatrix

        expected_result = TensorProduct(msigma(1), eye(2))

        self.assertEqual(expected_result, result)

    def test_target_x_observable(self):
        target_x = TensorProduct(eye(2), msigma(1))

        result = transpose(self.hadamardthencnotmatrix) * target_x * self.hadamardthencnotmatrix

        expected_result = TensorProduct(eye(2), msigma(1))

        self.assertEqual(expected_result, result)

    def test_target_y_observable(self):
        target_y = TensorProduct(eye(2), msigma(2))

        result = transpose(self.hadamardthencnotmatrix) * target_y * self.hadamardthencnotmatrix

        expected_result = TensorProduct(msigma(1), msigma(2))

        self.assertEqual(expected_result, result)

    def test_target_z_observable(self):
        target_z = TensorProduct(eye(2), msigma(3))

        result = transpose(self.hadamardthencnotmatrix) * target_z * self.hadamardthencnotmatrix

        expected_result = TensorProduct(msigma(1), msigma(3))

        self.assertEqual(expected_result, result)
