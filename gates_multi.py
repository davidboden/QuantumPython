from sympy import Rational, expand
from sympy.physics.paulialgebra import Pauli
from qubit import Qubit

# CNOT applies X to the target when the control is |1⟩ (the −1 eigenstate of Z_c).
# Decomposing by the control's eigenstates:
#
#   CNOT = |0⟩⟨0|_c ⊗ I_t  +  |1⟩⟨1|_c ⊗ X_t
#
# Substituting |0⟩⟨0| = ½(I + Z_c) and |1⟩⟨1| = ½(I − Z_c):
#
#   CNOT = ½(I + Z_c) ⊗ I_t  +  ½(I − Z_c) ⊗ X_t
#        = ½(1  +  Z_c  +  X_t  −  Z_c·X_t)
#
# Self-adjoint (CNOT² = I), so the same expression serves as both U and U†.
def cnot_pauli_expression(control_label, target_label):
    Zc = Pauli(3, label=control_label)
    Xt = Pauli(1, label=target_label)
    return Rational(1, 2) * (1 + Zc + Xt - Zc * Xt)

# In the Deutsch and Hayden paper, the relationships are listed as:
# control: control.x * target.x,  control.y * target.x,  control.z
# target:  target.x,             -control.z * target.y,  -control.z * target.z
# However, we've chosen to represent |0> with the 1 eigenvalue so the relationships are:
# control: control.x * target.x,  control.y * target.x,  control.z
# target:  target.x,              control.z * target.y,  control.z * target.z
# Self-adjoint: CNOT² = I
def cnot(control: Qubit, target: Qubit):
    return (
        control.with_observables(control.x * target.x, control.y * target.x, control.z),
        target.with_observables(target.x, control.z * target.y, control.z * target.z)
    )

# Self-adjoint status unknown: three-qubit gate from Deutsch and Hayden; not yet verified
def ttransformation(k: Qubit, l: Qubit, m: Qubit):
    return (
        k.with_observables(-k.x * m.x, -k.y * m.x, k.z),
        l.with_observables(k.z * l.x * m.z, k.z * l.y * m.z, l.z),
        m.with_observables(-l.z * m.x, k.z * l.z * m.y, -k.z * m.z)
    )

# Deutsch / Hayden  paper has:
# control: control.z, -control.y * target.x,  control.x * target.x
# target:  target.x , -control.z * target.y, -control.z * target.z
# Using the |0> = 1 eigenvalue convention removes the negatives on the target qubit
# control: control.z, -control.y * target.x,  control.x * target.x
# target:  target.x ,  control.z * target.y,  control.z * target.z
# Not self-adjoint: bell and invbell are adjoints of each other (bell = H·CNOT, invbell = CNOT·H)
def bell(control: Qubit, target: Qubit):
    return (
        control.with_observables(control.z, -control.y * target.x, control.x * target.x),
        target.with_observables(target.x, control.z * target.y, control.z * target.z)
    )

# Toffoli (CCNOT) flips the target when both controls are |1⟩ (the −1 eigenstate of Z).
# Decomposing by the controls' eigenstates:
#
#   CCNOT = (1 − |1⟩⟨1|_1 ⊗ |1⟩⟨1|_2) ⊗ I_t  +  |1⟩⟨1|_1 ⊗ |1⟩⟨1|_2 ⊗ X_t
#
# Substituting |1⟩⟨1| = ½(I − Z):
#
#   CCNOT = 1 − ¼(1 − Z1 − Z2 + Z1·Z2)·(1 − X_t)
#
# Self-adjoint (CCNOT² = I), so the same expression serves as both U and U†.
def toffoli_pauli_expression(control1_label, control2_label, target_label):
    Z1 = Pauli(3, label=control1_label)
    Z2 = Pauli(3, label=control2_label)
    Xt = Pauli(1, label=target_label)
    return 1 - Rational(1, 4) * (1 - Z1 - Z2 + Z1 * Z2) * (1 - Xt)

# Toffoli is not a Clifford gate, so conjugating a control's X/Y observable produces a
# sum of Pauli terms rather than a single Pauli monomial (unlike cnot/bell/invbell below).
# with_observables accepts arbitrary expressions, so this is still representable; the
# terms must be expanded before passing them in, since with_observables/evaluate_labelled_pauli_product
# only groups Paulis by label within an already-expanded sum of products.
# Self-adjoint: CCNOT² = I
def toffoli(control1: Qubit, control2: Qubit, target: Qubit):
    control1_target_factor = Rational(1, 2) * (1 + control2.z + target.x - control2.z * target.x)
    control2_target_factor = Rational(1, 2) * (1 + control1.z + target.x - control1.z * target.x)
    target_factor = Rational(1, 2) * (1 + control1.z + control2.z - control1.z * control2.z)
    return (
        control1.with_observables(
            expand(control1.x * control1_target_factor),
            expand(control1.y * control1_target_factor),
            control1.z
        ),
        control2.with_observables(
            expand(control2.x * control2_target_factor),
            expand(control2.y * control2_target_factor),
            control2.z
        ),
        target.with_observables(
            target.x,
            expand(target.y * target_factor),
            expand(target.z * target_factor)
        )
    )

# Deutsch / Hayden  paper has:
# control: control.z * target.x, -control.y * target.x, control.x
# target:  targetx,              -control.x * target.y, -control.x * target.z
# Using the |0> = 1 eigenvalue convention removes the negatives on the target qubit
# control: control.z * target.x, -control.y * target.x, control.x
# target:  targetx,               control.x * target.y, control.x * target.z
# Not self-adjoint: bell and invbell are adjoints of each other (bell = H·CNOT, invbell = CNOT·H)
def invbell(control: Qubit, target: Qubit):
    return (
        control.with_observables(control.z * target.x, -control.y * target.x, control.x),
        target.with_observables(target.x,  control.x * target.y,  control.x * target.z)
    )
