from sympy import Add, Mul, Pow
from sympy.physics.quantum import TensorProduct
from sympy.physics.paulialgebra import Pauli
# Hopefully the sympy evaluate_pauli_product function will be updated with this behaviour.
# If that happens, we can remove this definition and close this issue:
# https://github.com/sympy/sympy/issues/26745
# If you don't need the extra simplification you can just use sympy's evaluate_pauli_product(...)
def evaluate_labelled_pauli_product(arg):
    '''Help function to evaluate Pauli matrices product
    with symbolic objects.

    Parameters
    ==========

    arg: symbolic expression that contains Paulimatrices

    Examples
    ========

    >>> from sympy.physics.paulialgebra import Pauli, evaluate_pauli_product
    >>> from sympy import I
    >>> evaluate_pauli_product(I*Pauli(1)*Pauli(2))
    -sigma3

    >>> from sympy.abc import x
    >>> evaluate_pauli_product(x**2*Pauli(2)*Pauli(1))
    -I*x**2*sigma3
    '''
    start = arg
    end = arg

    if isinstance(arg, Pow) and isinstance(arg.args[0], Pauli):
        if arg.args[1].is_odd:
            return arg.args[0]
        else:
            return 1

    if isinstance(arg, Add):
        return Add(*[evaluate_labelled_pauli_product(part) for part in arg.args])

    if isinstance(arg, TensorProduct):
        return TensorProduct(*[evaluate_labelled_pauli_product(part) for part in arg.args])

    elif not(isinstance(arg, Mul)):
        return arg

    while not start == end or start == arg and end == arg:
        start = end

        tmp = start.as_coeff_mul()
        # Keeping track of the labelled Paulis separately is the main difference
        sigma_products_by_label = {}
        com_product = 1
        keeper = 1

        def add_sigma_product(p: Pauli):
            if (sigma_products_by_label.get(p.label)):
                sigma_products_by_label[p.label] *= p
            else:
                sigma_products_by_label[p.label] = p

        def flatten_sigma_product():
            sigma_product = 1
            sigma_products_by_label
            for label in sorted(sigma_products_by_label):
                sigma_product *= sigma_products_by_label[label]

            sigma_products_by_label.clear()

            return sigma_product

        for el in tmp[1]:
            if isinstance(el, Pauli):
                add_sigma_product(el)
            elif not el.is_commutative:
                if isinstance(el, Pow) and isinstance(el.args[0], Pauli):
                    if el.args[1].is_odd:
                        add_sigma_product(el.args[0])
                elif isinstance(el, TensorProduct):
                    keeper = keeper*flatten_sigma_product()*\
                        TensorProduct(
                            *[evaluate_labelled_pauli_product(part) for part in el.args]
                        )
                else:
                    keeper = keeper*flatten_sigma_product()*el
            else:
                com_product *= el
        end = tmp[0]*keeper*flatten_sigma_product()*com_product
        if end == arg: break
    return end
