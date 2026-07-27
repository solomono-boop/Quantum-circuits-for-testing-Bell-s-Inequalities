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

#function 2: add noise to every qubit in a circuit
def add_noise(circuit,noise_probability):
    noisy_circuit=cirq.Circuit()
    for moment in circuit:
        #keep the originial quantum gates
        noisy_circuit.append(moment)
        #add depolairzing noise after every operation
        for operation in moment.operations:
            for qubit in operation.qubits:
                noisy_circuit.append(cirq.depolarize(noise_probability).on(qubit))
    return noisy_circuit

# function 3: def chsh_value(x, y, z, d) --> calculates CHSH value
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

#functio, 4: creates a histogram showing measurment outcomes
#00,01,10,and 11 for Alice and Bob
def plot_measurement_histogram(counts,title):
     #Convert Cirq's interger states into binary numbers so its easier to see the combinations 
        states=["00","01","10","11"]
        occurances=[counts.get(0,0),counts.get(1,0),counts.get(2,0),counts.get(3,0),]
    
        #creating histogram:
        plt.bar(states,occurances,color="#ff69b4")
        plt.xlabel("Measurement State (Alice,Bob)")
        plt.ylabel("Occurances")
        plt.title(title) #i did this so that way we could clarify each time what graph it was showing with a different title :)
        plt.show()

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

#creates the four CHSH circuits starting from a chosen initial state (for expirement where we change chosen state)
#initial_state is a string: "00","01","10", or "11"

def create_chsh_circuits(initial_state):
    a=cirq.NamedQubit("Alice")
    b=cirq.NamedQubit("Bob")
    circuits=[]

    #circuit 1: A, B
    circuit1=cirq.Circuit()

    #set initial state
    if initial_state[0]=="1":
        circuit1.append(cirq.X(a))

    if initial_state[1]=="1":
        circuit1.append(cirq.X(b))

    #create a bell pair
    circuit1.append(cirq.H(a))
    circuit1.append(cirq.CNOT(a,b))

   
    circuit1.append(cirq.ry(np.pi/4)(b)) #bob measurement angle =45 degrees
    circuit1.append(cirq.measure(a,b,key="result"))

    #circuit 2: A, B'
    circuit2=cirq.Circuit()
    #set initial state
    if initial_state[0]=="1":
        circuit2.append(cirq.X(a))
    
    if initial_state[1]=="1":
        circuit2.append(cirq.X(b))
    
    #create a bell pair
    circuit2.append(cirq.H(a))
    circuit2.append(cirq.CNOT(a,b))
    circuit2.append(cirq.ry(-np.pi/4)(b)) #bob measurement angle =-45 degrees
    circuit2.append(cirq.measure(a,b,key="result"))

    #circuit 3: A', B
    circuit3=cirq.Circuit()
    #set initial state
    if initial_state[0]=="1":
        circuit3.append(cirq.X(a))
    
    if initial_state[1]=="1":
        circuit3.append(cirq.X(b))
    
    #create a bell pair
    circuit3.append(cirq.H(a))
    circuit3.append(cirq.CNOT(a,b))
    circuit3.append(cirq.ry(np.pi/2)(a)) #alice measurement angle =90 degrees
    circuit3.append(cirq.ry(np.pi/4)(b)) #bob measurement angle =45 degrees
    circuit3.append(cirq.measure(a,b,key="result"))

    #circuit 4: A', B'
    circuit4=cirq.Circuit()
    #set initial state
    if initial_state[0]=="1":
        circuit4.append(cirq.X(a))
    
    if initial_state[1]=="1":
        circuit4.append(cirq.X(b))
    
    #create a bell pair
    circuit4.append(cirq.H(a))
    circuit4.append(cirq.CNOT(a,b))
    circuit4.append(cirq.ry(np.pi/2)(a)) #alice measurement angle =90 degrees
    circuit4.append(cirq.ry(-np.pi/4)(b)) #bob measurement angle =-45 degrees
    circuit4.append(cirq.measure(a,b,key="result"))

    circuits.append(circuit1)
    circuits.append(circuit2)
    circuits.append(circuit3)
    circuits.append(circuit4)

    return circuits
   

#testing how CHSH values changes with different numbers of repeitions
rep_values=[50,100,500,1000,2500,5000]
#testing different noise values as well
noise_values=[0.00,0.01,0.03,0.05,0.10]
noise_results=[]
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

#noise expirement
print()
print("Noise Expirement")
print("--------------------")
reps=2500
for noise in noise_values:
    noisy1=add_noise(circuit1,noise)
    noisy2=add_noise(circuit2,noise)
    noisy3=add_noise(circuit3,noise)
    noisy4=add_noise(circuit4,noise)

    counts1=sim_run(noisy1,reps)
    counts2=sim_run(noisy2,reps)
    counts3=sim_run(noisy3,reps)
    counts4=sim_run(noisy4,reps)

    E_AB=get_exp_value(counts1)
    E_AB_prime = get_exp_value(counts2)
    E_A_prime_B = get_exp_value(counts3)
    E_A_prime_B_prime = get_exp_value(counts4)

    S=chsh_value(E_AB,E_AB_prime,E_A_prime_B,E_A_prime_B_prime)

    noise_results.append(S)
    print("Noise =",noise)
    print("CHSH=",S)

#Testing different starting states
starting_states=["00","01","10","11"]
starting_state_results=[]

for state in starting_states:
    print("--------------")
    print("Starting state: ",state)

    circuits=create_chsh_circuits(state)
    counts1=sim_run(circuits[0],2500)
    counts2=sim_run(circuits[1],2500)
    counts3=sim_run(circuits[2],2500)
    counts4=sim_run(circuits[3],2500)

    E_AB= get_exp_value(counts1)
    E_AB_prime= get_exp_value(counts2)
    E_A_prime_B= get_exp_value(counts3)
    E_A_prime_B_prime= get_exp_value(counts4)

    S=chsh_value(E_AB,E_AB_prime,E_A_prime_B,E_A_prime_B_prime)
    starting_state_results.append(S)
    print("CHSH Value: ",S)


#Create CHSH vs reps graph
plt.plot(rep_values,chsh_results,marker="*",color="#ff69b4",label="Simulated CHSH value")
plt.axhline(y=2,color="#3D3D3D",linestyle="--",label="Classical Limit of 2")
plt.axhline(y=2*np.sqrt(2),color="#898989",linestyle="--",label="Tsirelson's bound (2√2)")
plt.title("CHSH Value vs Number of Measurement")
plt.xlabel("Number of repeititions")
plt.ylabel("CHSH value")
plt.legend()
plt.show()


#Create CHSH vs noise graph
plt.figure() #adds new plot for this
plt.plot(noise_values,noise_results,marker="*",color="#ff69b4",label="Simulated CHSH value")
plt.axhline(y=2,color="#3D3D3D",linestyle="--", label="Classical Limit (2)")
plt.axhline(y=2*np.sqrt(2),color="#898989",linestyle="--", label="Tsirelson's Bound (2√2)")
plt.title("CHSH Value vs Noise")
plt.xlabel("Noise Probability")
plt.ylabel("CHSH Value")
plt.legend()
plt.show()

#Simple measurement circuit histogram plot
#we want no noise and repitions set at the base amount (2500)
histogram_reps=2500 #just in case we wanted reps something else at a different place i made another variable just for this here
#running circuit (w/o noise)
hist_counts1=sim_run(circuit1,histogram_reps)
hist_counts2=sim_run(circuit2,histogram_reps)
hist_counts3=sim_run(circuit3,histogram_reps)
hist_counts4=sim_run(circuit4,histogram_reps)
#plot results 
plot_measurement_histogram(hist_counts1,"Measurement Results: E(A,B)")
plot_measurement_histogram(hist_counts2,"Measurement Results: E(A,B')")
plot_measurement_histogram(hist_counts3,"Measurement Results: E(A',B)")
plot_measurement_histogram(hist_counts4,"Measurement Results: E(A',B')")

#Create different starting state plot
plt.figure()
plt.bar(starting_states,starting_state_results,color="#ff69b4")
plt.axhline(y=2,color="#3D3D3D", linestyle="--", label="Classical Limit (2)")
plt.axhline(y=2*np.sqrt(2),color="#898989",linestyle="--",label="Tsirelson's bound (2√2)")
plt.xlabel("Initial State")
plt.ylabel("CHSH Value (S)")
plt.title("CHSH Value for Different Initial States")
plt.legend()
plt.show()