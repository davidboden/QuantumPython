import unittest

from qubit import Qubit
from sympy import simplify

class QubitTestCase(unittest.TestCase):
    def test_qubit_simplify(self):
        """
        Check that simplifying a qubit observable with sin squared plus cos squared
        simplifies the observable to just 1.
        """
        from sympy import Symbol, cos, sin
        aa = Symbol('aa')
        a1 = Qubit(7, sin(aa)**2 + cos(aa)**2, 1, 1)

        self.assertEqual(a1.x, sin(aa)**2 + cos(aa)**2)

        a2 = simplify(a1)

        self.assertEqual(a2.x, 1)
