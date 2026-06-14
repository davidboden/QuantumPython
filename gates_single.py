from sympy import cos, sin
from qubit import Qubit

# Self-adjoint: H² = I
def hadamard(qubit: Qubit):
    return qubit.with_observables(qubit.z, -qubit.y, qubit.x)

# Self-adjoint: Pauli X, X² = I. Note: identical transformation to xrot.
def qnot(qubit: Qubit):
    return qubit.with_observables(qubit.x, -qubit.y, -qubit.z)

# Self-adjoint: Pauli X, X² = I. Note: identical transformation to qnot.
def xrot(qubit: Qubit):
    return qubit.with_observables(qubit.x, -qubit.y, -qubit.z)

# Self-adjoint: Pauli Y, Y² = I
def yrot(qubit: Qubit):
    return qubit.with_observables(-qubit.x, qubit.y, -qubit.z)

# Self-adjoint: Pauli Z, Z² = I
def zrot(qubit: Qubit):
    return qubit.with_observables(-qubit.x, -qubit.y, qubit.z)

# Not self-adjoint: rotation by theta around the x-axis; adjoint is xrotation(qubit, -theta)
def xrotation(qubit: Qubit, theta):
    return qubit.with_observables(
        qubit.x,
        cos(theta) * qubit.y + sin(theta) * qubit.z,
        cos(theta) * qubit.z - sin(theta) * qubit.y
    )

# Not self-adjoint: rotation by theta around the y-axis; adjoint is yrotation(qubit, -theta)
def yrotation(qubit: Qubit, theta):
    return qubit.with_observables(
        cos(theta) * qubit.x + sin(theta) * qubit.z,
        qubit.y,
        cos(theta) * qubit.z - sin(theta) * qubit.x
    )
