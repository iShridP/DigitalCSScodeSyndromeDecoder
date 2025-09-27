# CSS Quantum Error Correction (QEC) Syndrome Decoder – Digital Implementation

## Overview

This project implements a **digital syndrome decoder** for arbitrary CSS (Calderbank-Shor-Steane) quantum error-correcting codes. The decoder is capable of handling popular examples like:

- Steane \([7,1,3]\) code  
- Shor \([9,1,3]\) code
- Five-qubit error correcting \([5,1,3]\) code
- Other custom CSS codes defined via their stabilizer check matrices  

The decoder automatically generates the **lookup tables (LUTs)** for single-qubit error correction **based on the input stabilizer (Check) matrices** and produces **VHDL modules** that can be synthesized on hardware implementations such as an FPGA. 

A corresponding **testbench** can be used for local simulation and verification of the decoder.

---

## Features

- **Fully parameterizable**: Works for any number of qubits and stabilizer generators.  
- **Automated LUT generation**: Produces error-to-syndrome mappings for both X and Z errors.  
- **VHDL code generation**: Generates RTL-ready files for FPGA implementation:  
  - `Syndrome_Decoder.vhd` – main decoder module  
  - `DUT.vhdl` – device under test wrapper  
  - `Testbench.vhdl` – testbench for simulation  
- **Supports single-qubit error correction** and no-error cases.  
- **Python Generating Code**: Generate_Files.py automatically generates all vhd/vhdl files according to provided check_matrix

## How to use:

- Edit the Check_Matrix.txt file with the Check matrix of custom CSS code implementation
- Edit the tracefile if required for local simulations
- Run Generate_Files.py
- The three custom VHDL codes will be generated
- For analysis through Quartus: ensure Tracefile.txt is valid according to Code testcases, compile Testbench+Tracefile is added, and that DUT is set as top level entity

