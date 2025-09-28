--Syndrome Detector

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all; 
library work;
use work.Gates.all;

entity syndrome_decoder is
port(syn : in std_logic_vector(5 downto 0); e_x, e_z : out std_logic_vector(6 downto 0)); 
end syndrome_decoder;

architecture struct of syndrome_decoder is

type lut_type_z is array (0 to 7) of std_logic_vector(6 downto 0);
type lut_type_x is array (0 to 7) of std_logic_vector(6 downto 0);

constant LUT_e_x : lut_type_z := (
"0000000",
"0000100",
"0000010",
"0010000",
"0000001",
"0100000",
"0001000",
"1000000"

);

constant LUT_e_z : lut_type_x := (
"0000000",
"0000100",
"0000010",
"0010000",
"0000001",
"0100000",
"0001000",
"1000000"

);

begin
e_x <= LUT_e_x(to_integer(unsigned(syn(2 downto 0))));
e_z <= LUT_e_z(to_integer(unsigned(syn(5 downto 3))));
end struct;