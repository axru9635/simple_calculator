
import argparse, traceback, sys
import calculator as calc
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

    [execute_command(command) for command in commands ]
        
        
def read_input_commands_file(input_file: str) -> Generator[str, None, None]:
    """
    Reads commands input file and return the 
    commands as a generator to be iterated
    """

    with open(input_file) as fh: 
        for line in fh.readlines():
            yield line.rstrip()


def execute_command(command: str) -> None:
    """
    Tries to run commands as they were written in the
    input file and prints the result or errors
    """

    result: str

    try:
        command_parsing = command.split(' ')
        command_type = command_parsing.pop(0)
        if  calc.Types.DEF == command_type: 
            result = calc.define_variable(command_parsing)

        elif calc.Types.CLEAR == command_type:
            result = calc.clear_defined_variables()

        elif calc.Types.CALC == command_type:
            result = calc.evaluate_expression(command_parsing)
        else:
            raise calc.CommandNotFoundError(command_type)
    
    except calc.CommandNotFoundError:
        traceback.print_exc()
        sys.exit()

    except Exception:
        print( f"The command given: \"{command}\" caused an error: " )
        traceback.print_exc()
        sys.exit()

    else: 
        # Success!
        print(result)


if __name__ == "__main__":
    word_calculator_main()

