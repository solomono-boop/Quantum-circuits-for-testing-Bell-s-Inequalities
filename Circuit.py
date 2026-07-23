import cirq

c = cirq.Circuit()
q0 = cirq.NamedQubit("qubit")
c.append(cirq.H(q0))
print(c)