from sympy import sqrt, Matrix, Transpose, Symbol

hadamard = 1/sqrt(2) * Matrix([[1, 1], [1, -1]])
zstate1 = Matrix([[1], [0]])
zstate2 = Matrix([[0], [1]])
xstate1 = 1/sqrt(2) * Matrix([[1], [1]])
xstate2 = 1/sqrt(2) * Matrix([[1], [-1]])
xprojector1 = xstate1 * Transpose(xstate1)
xprojector2 = xstate2 * Transpose(xstate2)
zprojector1 = zstate1 * Transpose(zstate1)
zprojector2 = zstate2 * Transpose(zstate2)
xobservable = (1 * xprojector1) + (-1 * xprojector2)
zobservable = (1 * zprojector1) + (-1 * zprojector2)
state = Matrix([[Symbol("a")], [Symbol("b")]])
