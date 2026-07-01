BraKet as an inner product describing the transition probability, the probability of taking the ket state and it measuring as the bra state. Explain that better in terms of projectors. For the z+ projector, we can view it as the ket being projected onto ket(0) and then asking what the inner product is between the state and the projection onto ket(0).
Explanation for how observables are transformed by gates.

From the Heisenburg state we should be able to quickly generate the overall Schrodinger state. Add some functions which accept a list of qubits and output the overall state.

sympy's evaluate_pauli_product does not simplify products of labelled Pauli matrices (sympy issue #26745). We work around this with evaluate_labelled_pauli_product in sympy_pauli.py. Track the upstream issue and remove the workaround if it is ever fixed.

The |0⟩ projector is ½(I + σ_z) = ((1 0)(0 0)). Initialising every qubit to |0⟩ means all Z-observables start in the +1 eigenstate, so no Z measurement ever produces a surprise — all the interesting variation in measurement outcomes comes from the X observables. Explain this when introducing global state initialisation.
