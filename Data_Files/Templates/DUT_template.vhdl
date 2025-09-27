--DUT
library ieee;
use ieee.std_logic_1164.all;

entity DUT is
   port(input_vector: in std_logic_vector({number of stab-1} downto 0);
       	output_vector: out std_logic_vector({2_number of qubits-1} downto 0));
end entity;

architecture DutWrap of DUT is
	Component syndrome_decoder is
		port(SYN : in std_logic_vector({number of stab-1} downto 0);
			  E_X,E_Z   : out std_logic_vector({number of qubits-1} downto 0));
	end component syndrome_decoder;
begin
   add_instance: syndrome_decoder port map (
	SYN => input_vector({number of stab-1} downto 0), 
	E_X => output_vector({2_number of qubits-1} downto {number of qubits}),
	E_Z => output_vector({number of qubits-1} downto 0)
	);
end DutWrap;