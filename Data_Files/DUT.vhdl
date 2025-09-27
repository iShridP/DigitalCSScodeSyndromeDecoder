--DUT
library ieee;
use ieee.std_logic_1164.all;

entity DUT is
   port(input_vector: in std_logic_vector(5 downto 0);
       	output_vector: out std_logic_vector(13 downto 0));
end entity;

architecture DutWrap of DUT is
	Component syndrome_decoder is
		port(SYN : in std_logic_vector(5 downto 0);
			  E_X,E_Z   : out std_logic_vector(6 downto 0));
	end component syndrome_decoder;
begin

   -- input/output vector element ordering is critical,
   -- and must match the ordering in the trace file!
   add_instance: syndrome_decoder port map (
	SYN => input_vector(5 downto 0), 
	E_X => output_vector(13 downto 7),
	E_Z => output_vector(6 downto 0)
	);
end DutWrap;