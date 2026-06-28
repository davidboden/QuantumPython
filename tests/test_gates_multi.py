import unittest
from qubit import Qubit
from gates_single import hadamard
from gates_multi import cnot, cnot_pauli_expression, bell, invbell

class MultiGateTestCase(unittest.TestCase):

    def test_cnot_pauli_expression(self):
        """
        Check that cnot_pauli_expression has the same effect on each qubit's observables
        as the cnot function when applied via evolve.
        CNOT is self-adjoint so evolve takes a single argument.
        """
        c = Qubit.qubit_time_0("control")
        t = Qubit.qubit_time_0("target")

        u = cnot_pauli_expression("control", "target")

        c_after_pauli = c.evolve(u)
        t_after_pauli = t.evolve(u)

        (c_after_cnot, t_after_cnot) = cnot(c, t)

        self.assertEqual(c_after_pauli, c_after_cnot)
        self.assertEqual(t_after_pauli, t_after_cnot)

    def test_bell_same_as_cnot_hadamard(self):
        """
        Bell function should give the same results as cnot then hadamard of control.
        """
        c = Qubit.qubit_time_0("con")
        t = Qubit.qubit_time_0("tar")

        (c_after_bell, t_after_bell) = bell(c, t)

        (c_after_cnot, t_after_cnot) = cnot(c, t)
        c_after_hadamard = hadamard(c_after_cnot)

        self.assertEqual(
            c_after_bell,
            c_after_hadamard
        )

        self.assertEqual(
            t_after_bell,
            t_after_cnot
        )

    def test_invbell_same_as_hadamard_cnot(self):
        """
        Inverse bell function should give the same results as hadamard of control then cnot.
        """
        c = Qubit.qubit_time_0("con")
        t = Qubit.qubit_time_0("tar")

        (c_after_invbell, t_after_invbell) = invbell(c, t)

        (c_after_combination, t_after_combination) = cnot(hadamard(c), t)

        self.assertEqual(
            c_after_invbell,
            c_after_combination
        )

        self.assertEqual(
            t_after_invbell,
            t_after_combination
        )

    def test_bell_invbell_is_identity(self):
        c = Qubit.qubit_time_0("con")
        t = Qubit.qubit_time_0("tar")
        (c_after_bell, t_after_bell) = bell(c, t)
        (c_after_invbell, t_after_invbell) = invbell(c_after_bell, t_after_bell)

        self.assertEqual(
            c_after_invbell,
            c
        )

        self.assertEqual(
            t_after_invbell,
            t
        )
