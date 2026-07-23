import cirq

# function 1: def exp_value(n_00, n_11, n_01, n_10) -> calculates expected value or E(x, y)
# function 2: def chsh_value(x, y, z, d) --> calculates CHSH value

#first entangled circuit with A, B
#second entangled circuit with A, B'
#third entangled circuit with A', B
#fourth entangled circuit with A', B'

#run simulations on the circuit 
#create histogram on each qubit value
#n_11 = count_through the histogram*(+1)
#n_01 = count_through the histogram*(-1)
#n_00 = count_through the histogram*(+1)
#n_10 = count_through the histogram*(-1)
#call exp_value function apply to each circuit
#do lines 11-17 4 times for each circuit

#store the exp_values for each circuit
#call chsh function using each exp_value
