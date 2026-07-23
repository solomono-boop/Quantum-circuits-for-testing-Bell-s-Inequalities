import cirq

# function 1: def exp_value(n_00, n_11, n_01, n_10) -> calculates expected value or E(x, y)
#n_00= number of times Alice measured 0 and Bob measured 0
#n_11= number of times Alice measured 1 and Bob measured 1
#n_10= number of times Alice measured 1 and Bob measured 0
#n_01= number of times Alice measured 0 and Bob measured 1
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
