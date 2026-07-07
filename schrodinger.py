from itertools import product

from sympy import sqrt, zeros, simplify, expand, eye
from sympy.physics.matrices import msigma
from sympy.physics.quantum import TensorProduct

from measurement import expectation_in_zero_state
from sympy_pauli import evaluate_labelled_pauli_product

# Every qubit starts in |0>, so the whole system starts in the pure state |0...0>.
# Any n-qubit density matrix can be written as a sum over Pauli strings:
#
#   rho = (1/2^n) * sum_{P1,...,Pn in {I,X,Y,Z}} <P1 x ... x Pn> * (P1 x ... x Pn)
#
# Since evolution is a homomorphism (U†(A B)U = (U†AU)(U†BU)), a Pauli string
# evolves to the product of each qubit's evolved observable, so
# <P1(t) x ... x Pn(t)> is just <0...0| P1(t) P2(t) ... Pn(t) |0...0>, which
# expectation_in_zero_state already knows how to compute from the qubits'
# (Heisenberg-picture) x/y/z observables.
_AXIS_MATRIX = {None: eye(2), 'x': msigma(1), 'y': msigma(2), 'z': msigma(3)}


def density_matrix(qubits):
    """
    Reconstruct the overall Schrodinger-picture density matrix from a list of
    Heisenberg-picture qubits, given that every qubit started in |0...0>.

    qubits: list of every Qubit in the system, in the order that should index
            the tensor product (and hence the rows/columns of the matrix)
    """
    all_labels = [str(qubit.qubitid) for qubit in qubits]
    dim = 2 ** len(qubits)
    rho = zeros(dim, dim)

    for axes in product(_AXIS_MATRIX, repeat=len(qubits)):
        operator = 1
        for qubit, axis in zip(qubits, axes):
            if axis is not None:
                operator *= getattr(qubit, axis)
        operator = evaluate_labelled_pauli_product(expand(operator))

        expectation = expectation_in_zero_state(operator, all_labels)
        if expectation == 0:
            continue

        term = None
        for axis in axes:
            matrix = _AXIS_MATRIX[axis]
            term = matrix if term is None else TensorProduct(term, matrix)

        rho += expectation * term

    return rho / dim


def state_vector(qubits):
    """
    Extract a ket (up to an overall global phase) for a list of
    Heisenberg-picture qubits, given that every qubit started in |0...0>.

    The reconstructed density matrix rho = |psi><psi| is pure, so any nonzero
    diagonal entry rho[j, j] = |psi_j|^2 lets us read off column j, which is
    psi * conj(psi_j). Dividing by sqrt(rho[j, j]) pins psi_j to be real and
    positive, fixing the global phase.
    """
    rho = density_matrix(qubits)
    dim = rho.shape[0]

    for j in range(dim):
        diagonal = simplify(rho[j, j])
        if diagonal != 0:
            return simplify(rho[:, j] / sqrt(diagonal))

    raise ValueError("Density matrix is zero; cannot extract a state vector.")
