from qubit import Qubit

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
