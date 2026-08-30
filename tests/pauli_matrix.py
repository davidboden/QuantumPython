"""Shared test helper: convert a labelled-Pauli expression into a matrix."""
from sympy import eye, expand, zeros
from sympy.physics.matrices import msigma
from sympy.physics.quantum import TensorProduct
from sympy.physics.paulialgebra import Pauli

I2 = eye(2)


def pauli_expr_to_matrix(expr, labels):
    """Turn a labelled-Pauli expression into a 2**len(labels) square matrix.

    Each Pauli(n, label=L) becomes msigma(n) in L's tensor slot (ordered as
    `labels`); every other slot is the identity. The expression is expanded to a
    sum of products first, and each labelled Pauli is assumed to appear at most
    once per term per label (as guaranteed by evaluate_labelled_pauli_product).
    """
    expr = expand(expr)
    dimension = 2 ** len(labels)
    total = zeros(dimension, dimension)
    for term in expr.as_ordered_terms():
        coeff, factors = term.as_coeff_mul()
        slots = {label: I2 for label in labels}
        for factor in factors:
            base, exponent = factor.as_base_exp()
            if isinstance(base, Pauli):
                matrix = I2 if exponent % 2 == 0 else msigma(base.i)
                slots[base.label] = slots[base.label] * matrix
            else:
                coeff = coeff * factor
        total = total + coeff * TensorProduct(*[slots[label] for label in labels])
    return total.applyfunc(expand)
