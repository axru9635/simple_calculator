
import argparse
import calculator as calc
from calculator import CalulatorCommandFactory
from typing import Generator

def word_calculator_main() -> None:
    """
    Takes command line input parameter and runs 
    the calculator for the commands from input content.
    """

    program_description = \
    "This is a calculator that solely uses varible names. \
    Expressions are caclulated using variable names and \
    right hand side results are given in corresponding variable \
    name if it exists otherwise unknown."

    parser = argparse.ArgumentParser(description=program_description)
    
    parser.add_argument('input_filename')
    args = parser.parse_args()

    commands = read_input_commands_file(args.input_filename)

    [print(CalulatorCommandFactory.create(command) ) for command in commands]

        
def read_input_commands_file(input_file) -> Generator[str, None, None]:
    """
    Reads commands input file and return the 
    commands as a generator to be iterated
    """

    with open(input_file) as fh: 
        for line in fh.readlines():
            yield line.rstrip()


if __name__ == "__main__":
    word_calculator_main()

