from sympy import Matrix, sqrt, UnevaluatedExpr
ket_zero = Matrix([[1], [0]])
ket_one = Matrix([[0], [1]])
ket_plus = UnevaluatedExpr(1/sqrt(2)) * Matrix([[1], [1]])
ket_minus = UnevaluatedExpr(1/sqrt(2)) * Matrix([[1], [-1]])
bra_zero = ket_zero.T
bra_one = ket_one.T
bra_plus = ket_plus.T
bra_minus = ket_minus.T

projector_z_zero = ket_zero * bra_zero
projector_z_one = ket_one * bra_one
projector_x_plus = ket_plus * bra_plus
projector_x_minus = ket_minus * bra_minus
