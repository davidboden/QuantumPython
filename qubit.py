from sympy import Basic, Expr, simplify, expand, I
from sympy.physics.paulialgebra import Pauli
from sympy_pauli import evaluate_labelled_pauli_product

class Qubit(Basic):
    def __new__(cls, qubitid: int, x: Expr, y: Expr, z: Expr):
        obj = super().__new__(cls, x, y, z)
        obj.qubitid = qubitid
        return obj
    
    def _eval_simplify(self, **kwargs):
        return Qubit(
            self.qubitid,
            simplify(self.args[0]),
            simplify(self.args[1]),
            simplify(self.args[2])
        )
    
    def with_observables(self, x, y, z):
        return Qubit(
            self.qubitid,
            evaluate_labelled_pauli_product(x),
            evaluate_labelled_pauli_product(y),
            evaluate_labelled_pauli_product(z)
        )
    
    def with_xz_observables(self, x, z):
        return Qubit(
            self.qubitid,
            evaluate_labelled_pauli_product(x),
            # Calculate the Y observable using the X and Z observables
            # Could have also used: -I * z * x
            evaluate_labelled_pauli_product(I * x * z),
            evaluate_labelled_pauli_product(z)
        )
    
    # The conjugate transpose of all the pauli matrices is the same as the original matrix
    def evolve(self, expr: Expr):
        return Qubit(
            self.qubitid,
            evaluate_labelled_pauli_product(expand(expr * self.x * expr)),
            evaluate_labelled_pauli_product(expand(expr * self.y * expr)),
            evaluate_labelled_pauli_product(expand(expr * self.z * expr))
        )
    
    def expand_and_simplify(self):
        return Qubit(
            self.qubitid,
            evaluate_labelled_pauli_product(expand(self.x)),
            evaluate_labelled_pauli_product(expand(self.y)),
            evaluate_labelled_pauli_product(expand(self.z))
        )

    @property
    def x(self):
        return self.args[0]

    @property
    def y(self):
        return self.args[1]

    @property
    def z(self):
        return self.args[2]

    def __repr__(self):
        return f"Qubit({self.qubitid}, {self.x}, {self.y}, {self.z})"
    
    def __eq__(self, other):
        return (
            self.qubitid == other.qubitid and
            self.x == other.x and
            self.y == other.y and
            self.z == other.z
        )
    
    @staticmethod
    def qubit_time_0(qubitid):
        qn = str(qubitid)
        return Qubit(qubitid, Pauli(1, label=qn), Pauli(2, label=qn), Pauli(3, label=qn))
    
    # We'll typically display just the X and Z observables; the Y observable can be derived from the X and Z.
    def _latex(self, printer):
        return f"Qubit_{self.qubitid}(X={printer.doprint(self.x)}, Z={printer.doprint(self.z)})"

