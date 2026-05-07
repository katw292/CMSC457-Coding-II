from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

# Return a quantum circuit on 3 qubits and 3 classical bits
# 1. Create a GHZ state \ket{000}+\ket{111} starting from \ket{000}
# 2. Apply X gate on the 0th qubit to get \ket{100}+\ket{011}
# 3. Measure everything
# Note: the result will be either "100" or "011" due to Qiskit's bit order
def ghz_x_meas():
	qc = QuantumCircuit(3, 3)
	QuantumCircuit()
	qc.h(0)
	qc.cx(0, 1)
	qc.cx(0, 2)
	qc.x(0)
	qc.measure([0,1,2], [0,1,2])
	return qc

# Return a quantum circuit on 1 qubit
# Apply an X gate if input x is True
# Similarly for Z gate
def superdense_alice(x, z):
	qc = QuantumCircuit(1)
	if x:
		qc.x(0)
	if z:
		qc.z(0)
	return qc

# Return a quantum circuit on 2 qubits and 2 classical bits
def superdense_bob():
	qc = QuantumCircuit(2,2)
	qc.cx(0, 1)
	qc.h(0)
	qc.measure([0,1], [0,1])
	return qc

# Return Alice's quantum circuit
# qreg: register of 2 qubits
# creg: register of 2 bits
def teleport_alice(qreg: QuantumRegister, creg: ClassicalRegister):
	qc = QuantumCircuit(qreg, creg)
	qc.cx(0, 1)
	qc.h(qreg[0])
	qc.measure([0,1], [0,1])
	return qc

# Return Charlie's quantum circuit
# qreg: register of 2 qubits
# creg: register of 2 bits
# Assume the 0th qubit is above the 1st qubit.
# Match the indices when measuring. (That is, qreg[0] goes into creg[0].)
def swap_charlie(qreg: QuantumRegister, creg: ClassicalRegister):
	qc = QuantumCircuit(qreg,creg)
	qc.cx(0, 1)
	qc.h(qreg[0])
	qc.measure([0,1], [0,1])
	return qc

# Return Alice's quantum circuit
# qreg: register of 1 qubit
# creg: register of 2 bits
def swap_alice(qreg: QuantumRegister, creg: ClassicalRegister):
  qc = QuantumCircuit(qreg,creg)
  with qc.if_test((creg[0], 1)):
    qc.z(qreg[0])
  with qc.if_test((creg[1], 1)):
    qc.x(qreg[0])
  return qc

# Output a classical syndrome string based on the error Pauli
# Pauli: One of "X", "XZ", or "Z".
# Wire: A number between 1 and 5.
# Example mappings:
# error_to_syndrome("X", 1) -> "00011"
# error_to_syndrome("X", 3) -> "11000"
# error_to_syndrome("XZ", 3) -> "11101"
def error_to_syndrome(pauli, wire):
	table = {
        ("X", 1): "00011",
        ("X", 2): "00110",
        ("X", 3): "11000",
        ("X", 4): "01100",
        ("X", 5): "10001",

        ("Z", 1): "10100",
        ("Z", 2): "01010",
        ("Z", 3): "00101",
        ("Z", 4): "10010",
        ("Z", 5): "01001",

				("XZ", 1): "10111",
        ("XZ", 2): "11011",
        ("XZ", 3): "11101",
        ("XZ", 4): "11110",
        ("XZ", 5): "01111",
    }

	syndrome = table[(pauli, wire)]
	return syndrome

# Output a quantum circuit that measures with respect to a Pauli operator
# data: register of 5 qubits
# ancilla: register of 1 qubit
# creg: classical register of 1 bit
# synd: A string representing a 5-qubit Pauli operator; e.g. "XZZXI".
# You can assume there will be no "Y" operator in any qubit.
def measure_one_syndrome(data, ancilla, creg, synd):
	qc = QuantumCircuit(data, ancilla, creg)
	for i in range(5):
		if synd[i] == "X":
			qc.h(data[i])
			qc.cx(data[i], ancilla[0])
			qc.h(data[i])
		elif synd[i] == "Z":
			qc.cx(data[i], ancilla[0])
	qc.measure(ancilla[0], creg[0])
	return qc
