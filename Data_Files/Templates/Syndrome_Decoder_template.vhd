--Syndrome Detector

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all; 
library work;
use work.Gates.all;

entity syndrome_decoder is
port(syn : in std_logic_vector({number of stab-1} downto 0); e_x, e_z : out std_logic_vector({number of qubits-1} downto 0)); 
end syndrome_decoder;

architecture struct of syndrome_decoder is

type lut_type_z is array (0 to {2^number of z stab-1}) of std_logic_vector({number of qubits-1} downto 0);
type lut_type_x is array (0 to {2^number of x stab-1}) of std_logic_vector({number of qubits-1} downto 0);

constant LUT_e_x : lut_type_z := (
--LUT_cases_x
);

constant LUT_e_z : lut_type_x := (
--LUT_cases_y
);

begin
e_x <= LUT_e_x(to_integer(unsigned(syn({number of x stab-1} downto 0))));
e_z <= LUT_e_z(to_integer(unsigned(syn({number of stab-1} downto {number of x stab}))));
end struct;