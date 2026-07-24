import cirq
import matplotlib.pyplot as plt
import numpy as np

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

#runs simulations on the circuit 
def sim_run(circuit, reps):
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=reps)
    counts = result.histogram(key="result")
    #Creating the histogram: COMMENTED OUT
    #We wanted it to be obvious how many occurances happen per each state hence why we did it this way

    #Convert Cirq's interger states into binary numbers so its easier to see the combinations 
    #states=["00","01","10","11"]
    #occurances=[counts.get(0,0),counts.get(1,0),counts.get(2,0),counts.get(3,0),]

    #creating histogram:
   #plt.bar(states,occurances,color="#ff69b4")
    #plt.xlabel("Measurement State (Alice,Bob)")
    #plt.ylabel("Occurances")
    #plt.title("Qubit Measurement Results")
    #plt.show()
    return counts

#def get_exp_value(count_of_each_value) 
#n_11 = count..*(+1)
#n_01 = count..*(-1)
#n_00 = count..*(+1)
#n_10 = count..*(-1)
def get_exp_value(counts):
    n_00=counts.get(0,0)
    n_01=counts.get(1,0)
    n_10=counts.get(2,0)
    n_11=counts.get(3,0)
    return exp_value(n_00,n_11,n_01,n_10)


#first entangled circuit with A, B
a = cirq.NamedQubit("q0")
b = cirq.NamedQubit("q1")
circuit1 = cirq.Circuit()
circuit1.append(cirq.H(a))
circuit1.append(cirq.CNOT(a, b))
circuit1.append((cirq.ry(np.pi/4)(b)))
circuit1.append(cirq.measure(a,b, key="result"))

#second entangled circuit with A, B'
a = cirq.NamedQubit("q0")
b_dash = cirq.NamedQubit("q1")
circuit2 = cirq.Circuit()
circuit2.append(cirq.H(a))
circuit2.append(cirq.CNOT(a, b_dash))
circuit2.append((cirq.ry(-(np.pi/4)))(b_dash))
circuit2.append(cirq.measure(a, b_dash, key="result"))

#third entangled circuit with A', B
a_dash = cirq.NamedQubit("q0")
b = cirq.NamedQubit("q1")
circuit3 = cirq.Circuit()
circuit3.append(cirq.H(a_dash))
circuit3.append(cirq.CNOT(a_dash, b))
circuit3.append(cirq.ry(np.pi/2)(a_dash))
circuit3.append(cirq.ry(np.pi/4)(b))
circuit3.append(cirq.measure(a_dash, b, key="result"))

#fourth entangled circuit with A', B'
a_dash = cirq.NamedQubit("q0")
b_dash = cirq.NamedQubit("q1")
circuit4 = cirq.Circuit()
circuit4.append(cirq.H(a_dash))
circuit4.append(cirq.CNOT(a_dash, b_dash))
circuit4.append((cirq.ry(np.pi/2))(a_dash))
circuit4.append((cirq.ry(-(np.pi/4)))(b_dash))
circuit4.append(cirq.measure(a_dash, b_dash, key="result"))

#testing how CHSH values changes with different numbers of repeitions
rep_values=[50,100,500,1000,2500,5000]
#stores CHSH value for each repitiion amount
chsh_results=[]
#run expirement for each repition amount
for reps in rep_values:
    counts1=sim_run(circuit1,reps)
    counts2=sim_run(circuit2,reps)
    counts3=sim_run(circuit3,reps)
    counts4=sim_run(circuit4,reps)
    #store the exp_values for the circuit
    E_AB= get_exp_value(counts1)
    E_AB_prime= get_exp_value(counts2)
    E_A_prime_B= get_exp_value(counts3)
    E_A_prime_B_prime= get_exp_value(counts4)
    #call chsh function using each exp_value
    S=chsh_value(E_AB,E_AB_prime,E_A_prime_B,E_A_prime_B_prime)
    #saving result
    chsh_results.append(S)
    print("Repetitions: ",reps)
    print("E(A,B):", E_AB)
    print("E(A,B'):", E_AB_prime)
    print("E(A',B):", E_A_prime_B)
    print("E(A',B'):", E_A_prime_B_prime)
    print("CHSH value: ",S)
    print("---------------")

#Create CHSH graph
plt.plot(rep_values,chsh_results,marker="*",color="#ff69b4",label="Simulated CHSH value")
plt.axhline(y=2,color="#3D3D3D",linestyle="--",label="Classical Limit of 2")
plt.axhline(y=2*np.sqrt(2),color="#898989",linestyle="--",label="Tsirelson's bound (2√2)")
plt.title("CHSH Value vs Number of Measurement")
plt.xlabel("Number of repeititions")
plt.ylabel("CHSH value")
plt.legend()
plt.show()
