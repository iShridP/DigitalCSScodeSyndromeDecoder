import json
import math

import os
print(os.getcwd())

script_dir = os.path.dirname(os.path.abspath(__file__))  # folder of the script

#CSS code implementation variables:
#import the check matrix for the CSS code
Check_Matrix = []

with open(os.path.join(script_dir, "Check_Matrix.txt"),'r') as f:
    for line in f:
        row = list(map(int, line.strip().split()))
        if row != []:
            Check_Matrix.append(row)

with open(os.path.join(script_dir, "Stabiliser_Details.txt"), "r") as f:
    line = f.readline().strip()

number_of_stabilizer_generators = int(len(Check_Matrix))
number_of_X_stabilizer_generators = int(line.split()[-1])
number_of_Z_stabilizer_generators = number_of_stabilizer_generators  - number_of_X_stabilizer_generators

number_of_qubits = int(len(Check_Matrix[0])/2)

# Print matrix
print("Check Matrix:")
for row in Check_Matrix:
    print(row)

def matrix_mult(H,e): # Me (mod 2)
    output = []
    for row in H:
        if e == 0:
            element = 0 
        else:
            element = row[e-1]
        output.append(element%2) #mod 2

    return int(''.join(map(str, output)),2)

#compute the LUT elements
#for e_x or e_z = [0,0, .. 1, ... 0,0] of length (number_of_qubits):
#s_z = H_z * e_X^T (mod 2)
#then LUT is sequence of e_X indexed according to its s_z
#same logic for e_Z and s_x

#H is of form [[H_z, 0], [0, H_x]] since its CSS code 

#Extract H_z: Top left of Check Matrix H, (number_of_Z_stabilizer_generators) rows and (number_of_qubits) columns
H_z = []
curr_row = []
for j in range(number_of_Z_stabilizer_generators):
    for i in range(number_of_qubits):
        curr_row.append(Check_Matrix[j][i])
    H_z.append(curr_row)
    curr_row = []

print("Z Stabilizer Matrix:")
for row in H_z:
    print(row)


#Similar for H_x: bottom right
H_x = []
curr_row = []
for j in range(number_of_X_stabilizer_generators):
    for i in range(number_of_qubits):
        curr_row.append(Check_Matrix[j+number_of_Z_stabilizer_generators][i+number_of_qubits])
    H_x.append(curr_row)
    curr_row = []

print("X Stabilizer Matrix:")
for row in H_x:
    print(row)


#Now we generate the LUT conditions

#LUT_e_x --> index according to s_z
#e_x^T can take N+1 values with error at Nth qubit or no error

s_x_index = []
s_z_index = []

for i in range(number_of_qubits+1):
    s_x_index.append([matrix_mult(H_x,i),(1 << (i-1)) if i != 0 else 0])
    s_z_index.append([matrix_mult(H_z,i),(1 << (i-1)) if i != 0 else 0])

#now s_z and s_x indexes are indexed accordingly to e_x and e_z

s_x_sorted = sorted(s_x_index, key=lambda row: row[0])
s_z_sorted = sorted(s_z_index, key=lambda row: row[0])

#now we ready to make LUT. each element of s_sorted is the error string e_X or e_Z sorted acc to syndrome value (as required in LUT)

LUT_x_string = ""
LUT_z_string = ""

def bin_to_bitstring(value: int) -> str:
    value = int(value)
    return format(value, f'0{number_of_qubits}b')

for error_index in range(number_of_qubits + 1):
    if error_index != number_of_qubits:
        LUT_z_string+=(f"\"{bin_to_bitstring((s_x_sorted[error_index][1]))}\",\n")
        LUT_x_string+=(f"\"{bin_to_bitstring((s_z_sorted[error_index][1]))}\",\n")
    else:
        LUT_x_string+=(f"\"{bin_to_bitstring((s_z_sorted[error_index][1]))}\"\n")
        LUT_z_string+=(f"\"{bin_to_bitstring((s_x_sorted[error_index][1]))}\"\n")

#define required inputs:
number_of_stabilizer_generators_minus_one = str(number_of_stabilizer_generators - 1)
number_of_X_stabilizer_generators_minus_one = str(number_of_X_stabilizer_generators - 1)
number_of_Z_stabilizer_generators_minus_one = str(number_of_Z_stabilizer_generators - 1)
number_of_qubits_minus_one = str(number_of_qubits -1)
two_number_of_qubits = str(2*number_of_qubits)
two_number_of_Z_stabilizer_generators_minus_one = str(int(math.pow(2,number_of_Z_stabilizer_generators))-1)
two_number_of_X_stabilizer_generators_minus_one = str(int(math.pow(2,number_of_X_stabilizer_generators))-1)
two_number_of_qubits_minus_one = str(int(two_number_of_qubits) -1)
two_power_z_stab_minus_one = str(int(math.pow(2,number_of_Z_stabilizer_generators))-1)
two_power_x_stab_minus_one = str(int(math.pow(2,number_of_X_stabilizer_generators))-1)


replace = {} #dictionary
replace["{number of stab-1}"] = number_of_stabilizer_generators_minus_one
replace["{number of stab}"] = str(number_of_stabilizer_generators)
replace["{2_number of qubits}"] = two_number_of_qubits
replace["{2_number of qubits-1}"] = two_number_of_qubits_minus_one
replace["{number of qubits-1}"] = number_of_qubits_minus_one
replace["{number of qubits}"] = str(number_of_qubits)
replace["{2^number of z stab-1}"] = two_number_of_Z_stabilizer_generators_minus_one
replace["{2^number of x stab-1}"] = two_number_of_X_stabilizer_generators_minus_one
replace["--LUT_cases_x"] = LUT_x_string
replace["--LUT_cases_y"] = LUT_z_string
replace["{number of x stab-1}"] = number_of_X_stabilizer_generators_minus_one
replace["{number of x stab}"] = str(number_of_X_stabilizer_generators)

#Read templates and make new file:
with open(os.path.join(script_dir,"Data_Files/Templates/Syndrome_Decoder_template.vhd"), "r") as f:
    syndrome_template = f.read()

with open(os.path.join(script_dir,"Data_Files/Templates/Testbench_template.vhdl"),'r') as f:
    testbench_template = f.read()

with open(os.path.join(script_dir,"Data_Files/Templates/DUT_template.vhdl"),'r') as f:
    DUT_template = f.read()

syndrome_out = syndrome_template
testbench_out = testbench_template
DUT_out = DUT_template
for key, value in replace.items():
    syndrome_out = syndrome_out.replace(key, value)
    testbench_out = testbench_out.replace(key,value)
    DUT_out = DUT_out.replace(key,value)

with open(os.path.join(script_dir,"Data_Files/Syndrome_Decoder.vhd"), "w") as f:
    f.write(syndrome_out)
with open(os.path.join(script_dir,"Data_Files/DUT.vhdl"),"w") as f:
    f.write(DUT_out)
with open(os.path.join(script_dir,"Data_Files/Testbench.vhdl"),"w") as f:
    f.write(testbench_out)

print()
print("Successfully created new QEC code syndrome decoder files")