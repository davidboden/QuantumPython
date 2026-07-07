from sympy import Rational
from sympy.physics.paulialgebra import Pauli
from sympy_pauli import evaluate_labelled_pauli_product
from qubit import Qubit


def expectation_in_zero_state(expr, labels):
    """
    Compute the expectation value of a Pauli expression in the |00...0> state.
    In |0>, each qubit has Z expectation = 1 and X, Y expectation = 0.
    """
    result = expr
    for label in labels:
        result = result.subs(Pauli(3, label=label), 1)
        result = result.subs(Pauli(1, label=label), 0)
        result = result.subs(Pauli(2, label=label), 0)
    return result


def _substitute_z(qubit, measured_label, z_value):
    """Replace the Z Pauli of the measured qubit with a scalar in all observables."""
    return Qubit(
        qubit.qubitid,
        evaluate_labelled_pauli_product(qubit.x.subs(Pauli(3, label=measured_label), z_value)),
        evaluate_labelled_pauli_product(qubit.y.subs(Pauli(3, label=measured_label), z_value)),
        evaluate_labelled_pauli_product(qubit.z.subs(Pauli(3, label=measured_label), z_value)),
    )


def measure_z(branches, measured_label, all_labels):
    """
    Measure the Z observable of the qubit with the given label.

    Each branch (probability, qubits) splits into two new branches:
      - outcome +1: probability *= ½(1 + <Z>), Z Pauli of measured qubit → 1
      - outcome -1: probability *= ½(1 - <Z>), Z Pauli of measured qubit → -1

    The measured qubit's Z Pauli is substituted with the scalar outcome throughout
    all qubits' observables, collapsing the entanglement. Branches with zero
    probability are dropped.

    branches:       list of (prob, tuple of Qubit)
    measured_label: label string of the qubit to measure
    all_labels:     list of all qubit label strings (needed to evaluate expectation value)
    """
    new_branches = []
    for prob, qubits in branches:
        measured_qubit = next(q for q in qubits if str(q.qubitid) == measured_label)
        z_exp = expectation_in_zero_state(measured_qubit.z, all_labels)

        prob_plus  = prob * Rational(1, 2) * (1 + z_exp)
        prob_minus = prob * Rational(1, 2) * (1 - z_exp)

        if prob_plus != 0:
            new_branches.append((
                prob_plus,
                tuple(_substitute_z(q, measured_label, 1) for q in qubits)
            ))
        if prob_minus != 0:
            new_branches.append((
                prob_minus,
                tuple(_substitute_z(q, measured_label, -1) for q in qubits)
            ))

    return new_branches
