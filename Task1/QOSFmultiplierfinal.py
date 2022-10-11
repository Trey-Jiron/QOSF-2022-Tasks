# -*- coding: utf-8 -*-
"""
2x2 bit quantum multiplier for QOSF quantum cohort task 1

@author: Trey Jiron
"""
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer, IBMQ
from numpy import pi

#creates a quantum circuit with 4 classical registers. also load in the provider and back end.
qreg_q = QuantumRegister(11, 'q')
creg_c = ClassicalRegister(4, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
IBMQ.load_account() #Load your own IBM account
provider = IBMQ.get_provider(group=) #enter your own provider here
backend = provider.get_backend('ibmq_qasm_simulator')

valid_input = False #used to make sure the input from user is vaild

# multipler function proper, takes two inputs A and B and intilize them into bits, uses circuit to multiply them, then turns the answer from binary to interger
# This is in the from of AxB = C where A and B are 3 bit number and C is a 4 bit number
def multiplier(A,B):
    #These two blocks turn A and B into binary form by using not gates to turn the qubits in |1> state for the requited bits
    # the bits are as follows A0 = q0, A1 = q1, B0=q2, and B1=q3
    if A == 0:
        pass
    elif A == 1:
        circuit.x(qreg_q[0])
    elif A == 2:
        circuit.x(qreg_q[1])
    elif A == 3:
        circuit.x(qreg_q[0])
        circuit.x(qreg_q[1])
    
    if B == 0:
        pass
    elif B == 1:
        circuit.x(qreg_q[2])
    elif B == 2:
        circuit.x(qreg_q[3])
    elif B == 3:
        circuit.x(qreg_q[2])
        circuit.x(qreg_q[3])
    # The quantum circuit proper, diagram is in the pdf, use the measured classical bits as the bits for C. c0 = C0, c1 = C1, c2=C2, c3 = C3
    # where lower case c is the classical bit and the upper case C corsponds the the binary bits for the number C
    circuit.ccx(qreg_q[0], qreg_q[3], qreg_q[9])
    circuit.ccx(qreg_q[0], qreg_q[2], qreg_q[10])
    circuit.ccx(qreg_q[1], qreg_q[2], qreg_q[8])
    circuit.ccx(qreg_q[1], qreg_q[3], qreg_q[7])
    circuit.ccx(qreg_q[8], qreg_q[9], qreg_q[4])
    circuit.cx(qreg_q[9], qreg_q[8])
    circuit.ccx(qreg_q[4], qreg_q[7], qreg_q[5])
    circuit.swap(qreg_q[1], qreg_q[8])
    circuit.swap(qreg_q[3], qreg_q[5])
    circuit.cx(qreg_q[7], qreg_q[4])
    circuit.swap(qreg_q[0], qreg_q[10])
    circuit.measure(qreg_q[1], creg_c[1])
    circuit.swap(qreg_q[2], qreg_q[4])
    circuit.measure(qreg_q[0], creg_c[0])
    circuit.measure(qreg_q[3], creg_c[3])
    circuit.measure(qreg_q[2], creg_c[2])
    
    job = execute(circuit, backend, shots=1) #excutes the job on the backend, no more than 1 shot is needed for the simulator but if implemented on a real
                                             #device increase shots to reduce chance of wrong answer from error. 
                                             
    #This block gets the result from the job, counts the results and finds the most common result and uses that as the final answer
    results = job.result()
    counts = results.get_counts()
    product = counts.most_frequent()

    #This block converts the answer from the job from binary to interger from, returns an error if not one of the listed results.
    # note that there are some numbers that cannot be the product of multiplication of 2 2 bit numbers, such as 7, so they are not listed
    if product == '0000':
        number = 0
    elif product == '0001':
        number = 1
    elif product == '0010':
        number = 2
    elif product == '0011':
        number = 3
    elif product == '0100':
        number = 4
    elif product == '0110':
        number = 6
    elif product == '1000':
        number = 8
    elif product == '1001':
        number = 9
    else:
        print("Error")
        
    return(number) #Final result is then returned

# this part asks the user to enter numbers to be multiplied by
print("This is a 2X2 bit multiplier for a quantum circuit. It can multiply AXB where A and B are numbers between and including 0 and 3.")

#These 2 blocks ask for the numbers for A and B, and make sure they are 2 bit numbers
while not valid_input:
    print("Please type in number for A between and including, 0 and 3.")
    A_input = input()
    A_input = int(A_input)
    
    if A_input > 3 or A_input < 0:
        print("Please type in a number between and including, 0 and 3.")
    else:
        valid_input = True

valid_input = False
while not valid_input:
    print("Please type in number for B between and including, 0 and 3.")
    B_input = input()
    B_input = int(B_input)
    if B_input > 3 or B_input < 0:
        print("Please type in a number between and including, 0 and 3.")
    else:
        valid_input = True

#runs the multpiler function with the inputs from the user
answer = multiplier(A_input, B_input)

#prints the final answer
print('The answer of', A_input, 'X', B_input, 'is:', answer)

#can print out circuit if you want
#print(circuit)

#waits for input before closing
input()