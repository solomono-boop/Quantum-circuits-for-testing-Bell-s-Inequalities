import cirq

# function 1: def exp_value(n_00, n_11, n_01, n_10) -> calculates expected value or E(x, y)

#n_11= number of times Alice measured 1 and Bob measured 1
#n_10= number of times Alice measured 1 and Bob measured 0
#n_01= number of times Alice measured 0 and Bob measured 1
#n_00= number of times Alice measured 0 and Bob measured 0

def exp_value(n_00,n_11,n_01,n_10):

    #calculate the total number of measurements taken
    total_measurements=n_00+n_11+n_01+n_10

    #avoids dividing by zero if no measurements taken 
    if total_measurements==0:
        return 0
    
    #Apply correlation value formula:
    #E(x,y)=(n_00+n_11-n_01-n_10)/(n_00+n_11+n_01+n_10)
    correlation=(n_00+n_11-n_01-n_10)/total_measurements
    return correlation

# function 2: def chsh_value(x, y, z, d) --> calculates CHSH value
#x= E(A,B)
#y= E(A,B')
#z= E(A',B)
#d= E(A',B')
def chsh_value(x,y,z,d):
    #Apply CHSH inequality formula:
    #S=|E(A,B) + E(A,B') + E(A',B) - E(A',B')|
    S=abs(x+y+z-d)
    return S

#first entangled circuit with A, B
a = cirq.NamedQubit("q0")
b = cirq.NamedQubit("q1")
circuit1 = cirq.Circuit()
circuit1.append(cirq.H(a))
circuit1.append(cirq.CNOT(a, b))
circuit1.append((cirq.Y ** 0.25)(b))
circuit1.append(cirq.measure(a,b))

#second entangled circuit with A, B'
a = cirq.NamedQubit("q0")
b_dash = cirq.NamedQubit("q1")
circuit2 = cirq.Circuit()
circuit2.append(cirq.H(a))
circuit2.append(cirq.CNOT(a, b_dash))
circuit2.append((cirq.Y ** (-0.25))(b_dash))
circuit2.append(cirq.measure(a, b_dash))

#third entangled circuit with A', B
a_dash = cirq.NamedQubit("q0")
b = cirq.NamedQubit("q1")
circuit3 = cirq.Circuit()
circuit3.append(cirq.H(a_dash))
circuit3.append(cirq.CNOT(a_dash, b))
circuit3.append((cirq.Y ** (0.5))(a_dash))
circuit3.append(cirq.measure(a_dash, b))

#fourth entangled circuit with A', B'
a_dash = cirq.NamedQubit("q0")
b_dash = cirq.NamedQubit("q1")
circuit4 = cirq.Circuit()
circuit4.append(cirq.H(a_dash))
circuit4.append(cirq.CNOT(a_dash, b_dash))
circuit4.append((cirq.Y ** (0.5))(a_dash))
circuit4.append((cirq.Y ** (-0.25))(b_dash))
circuit4.append(cirq.measure(a_dash, b_dash))

#run simulations on the circuit 
#create histogram on each qubit value
#n_11 = count_through the histogram*(+1)
#n_01 = count_through the histogram*(-1)
#n_00 = count_through the histogram*(+1)
#n_10 = count_through the histogram*(-1)
#call exp_value function apply to the circuit
#store the exp_values for the circuit
#do lines 11-17 4 times for each circuit

#call chsh function using each exp_value
