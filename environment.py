from qubit import Qubit


class Environment:
    """An isolated register of qubits representing one possibility.

    Two Environments never share qubit objects, so gates applied while
    building one cannot leak into another. This is what lets several
    equally-likely measurement outcomes be collected and compared as
    genuinely independent possibilities, rather than accidentally sharing
    state through reused qubit variables.
    """

    def __init__(self, *labels):
        self.qubits = {label: Qubit.qubit_time_0(label) for label in labels}

    def __getitem__(self, label):
        return self.qubits[label]

    def __setitem__(self, label, qubit):
        self.qubits[label] = qubit

    def z_observables(self, *labels):
        """The Z observable of each named qubit, as currently evolved."""
        return {label: self.qubits[label].z for label in labels}
