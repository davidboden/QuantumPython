# SymPy usage

We use SymPy to manipulate symbolic algebra to explain how algorithms update qubits over time. Keeping the algebra intact rather than performing matrix calculations and just examining the result allows us to see the working-out that's going on within the algorithm rather than just the results of the algorithm.

## Conjugate transpose: `.H`

`.H` is a property on SymPy `Matrix` objects that returns the **conjugate transpose** — equivalent to `.T.conjugate()` combined. It is the standard linear algebra notation for the Hermitian adjoint, also written $U^\dagger$.

For matrices with real entries (such as the Hadamard gate), `.H` gives the same result as `.T`. The reason to use `.H` over `.T` is correctness for the general case: if a gate has complex entries (such as the Y Pauli or any phase gate), `.T` gives the wrong answer while `.H` gives the right one.

In the context of the Heisenberg picture, the transformed observable is $O' = U^\dagger O U$, written in code as:

```python
U.H * observable * U
```
