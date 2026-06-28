from sympy import cos, sin, I
from sympy.physics.paulialgebra import Pauli
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

# The X-rotation matrix has imaginary off-diagonal entries:
#
#   U_x(θ) = [[ cos(θ/2)    i·sin(θ/2) ],    =  cos(θ/2) · [[1, 0],  +  i·sin(θ/2) · [[0, 1],
#              [ i·sin(θ/2)  cos(θ/2)   ]]                    [0, 1]]                    [1, 0]]
#
#           = cos(θ/2) · I  +  i·sin(θ/2) · Pauli(1)
#
# σ_x = [[0,1],[1,0]] is real, so SymPy's Pauli(1) needs no convention adjustment.
# The adjoint U† is obtained by negating θ (i.e. xrotation_pauli_expression(-theta, label)).
def xrotation_pauli_expression(theta, label):
    return cos(theta/2) + I * sin(theta/2) * Pauli(1, label=label)

# Not self-adjoint: rotation by theta around the x-axis; adjoint is xrotation(qubit, -theta)
def xrotation(qubit: Qubit, theta):
    return qubit.with_observables(
        qubit.x,
        cos(theta) * qubit.y + sin(theta) * qubit.z,
        cos(theta) * qubit.z - sin(theta) * qubit.y
    )

# The Y-rotation matrix is purely real:
#
#   R_y(θ) = [[ cos(θ/2)  -sin(θ/2) ],    =  cos(θ/2) · [[1, 0],  +  sin(θ/2) · [[ 0, -1],
#              [ sin(θ/2)   cos(θ/2) ]]                    [0, 1]]                  [ 1,  0]]
#
#           = cos(θ/2) · I  +  sin(θ/2) · σ_y_real
#
# where σ_y_real = [[0,-1],[1,0]] is the real-form Pauli used in the notebooks.
# SymPy's Pauli(2) uses the standard complex form σ_y = [[0,-i],[i,0]], so
# σ_y_real = -i · Pauli(2). Substituting:
#
#   R_y(θ) = cos(θ/2) · I  -  i·sin(θ/2) · Pauli(2)
#
# The -i is an artifact of SymPy's complex convention, not a physical sign choice.
# The adjoint U† is obtained by negating θ (i.e. yrotation_pauli_expression(-theta, label)).
def yrotation_pauli_expression(theta, label):
    return cos(theta/2) - I * sin(theta/2) * Pauli(2, label=label)

# Not self-adjoint: rotation by theta around the y-axis; adjoint is yrotation(qubit, -theta)
def yrotation(qubit: Qubit, theta):
    return qubit.with_observables(
        cos(theta) * qubit.x + sin(theta) * qubit.z,
        qubit.y,
        cos(theta) * qubit.z - sin(theta) * qubit.x
    )

# The Z-rotation matrix has imaginary diagonal entries:
#
#   U_z(θ) = [[ cos(θ/2)+i·sin(θ/2)   0                   ],    =  cos(θ/2) · [[1, 0],  +  i·sin(θ/2) · [[ 1,  0],
#              [ 0                       cos(θ/2)-i·sin(θ/2)]]                    [0, 1]]                    [ 0, -1]]
#
#           = cos(θ/2) · I  +  i·sin(θ/2) · Pauli(3)
#
# σ_z = [[1,0],[0,-1]] is real, so SymPy's Pauli(3) needs no convention adjustment.
# The adjoint U† is obtained by negating θ (i.e. zrotation_pauli_expression(-theta, label)).
def zrotation_pauli_expression(theta, label):
    return cos(theta/2) + I * sin(theta/2) * Pauli(3, label=label)

# Not self-adjoint: rotation by theta around the z-axis; adjoint is zrotation(qubit, -theta)
def zrotation(qubit: Qubit, theta):
    return qubit.with_observables(
        cos(theta) * qubit.x + sin(theta) * qubit.y,
        cos(theta) * qubit.y - sin(theta) * qubit.x,
        qubit.z
    )
