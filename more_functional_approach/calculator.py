
""" A module that contains variables and defines commands """

_defined_variables = {}


class Types():
    """ Defines the allowed command types for the calculator """
    DEF = "def"
    CLEAR = "clear"
    CALC = "calc"


class _Operators():
    """ Defines the allowed operator types for the calculator """
    PLUS = '+'
    MINUS = '-'
    EQUALS = '='


class _DefaultResults:
    """
    Defines the standard answer if a calculation 
    resulted in a value with no corresponding variable
    """

    UNKNOWN ='unknown'

class CommandNotFoundError(Exception):
    """ Handles when the type of command is not recognized """

    def __init__(self):
        pass
    
    def __init__(self, command_name: str):
       msg = f"The command type \"{command_name}\" is not found  " 
       super().__init__(msg)


def clear_defined_variables() -> str:
    """ Command: clear all user defined variables """
    
    _defined_variables.clear()

    return "All variables cleared"


def define_variable(expression: list) -> str:
    """ Command: Defines a stored variable """

    variable_name = expression.pop(0)
    variable_value = expression.pop(0)

    _defined_variables[variable_name] = int(variable_value)

    return f"Defined variable: {variable_name}, with value: {variable_value} "


def evaluate_expression(expression: list) -> str:
    """ 
    Command: Tries to calculate an expression and
    determing a defined variable name as the right 
    hand side corresponding to that resulting value
    """

    sum = 0
    right_hand_side_answer_word: str
    left_hand_side_expression_text : str
    
    expression.remove(_Operators.EQUALS)

    left_hand_side_expression_text = ' '.join(expression)

    
    if _any_variables_missing_value(expression):
        right_hand_side_answer_word = _DefaultResults.UNKNOWN
    
    else:
        right_hand_side_answer_word = _calculate(expression)

        if not sum in _defined_variables.values():
            right_hand_side_answer_word = _DefaultResults.UNKNOWN

        else:
            right_hand_side_answer_word = _value_to_variable_name(sum)


    return f"{left_hand_side_expression_text} = {right_hand_side_answer_word}"


def _any_variables_missing_value(expression: list) -> bool:
    """ 
    Checks is there are any variables (variable names) 
    in the expression that 
    """

    variables = []

    [variables.append(item) for item in expression if item not in dir(_Operators) ]
    
    if not all(var in _defined_variables for var in variables):
        return True
    
    else:
        return False
    

def _calculate(expression: list) -> int:
    """ Calculates a given mathematical expression """

    sum = _defined_variables[expression.pop(0)] # it will always start with the first variable
        
    for itemIndex in range(0,len(expression)-1,2):
        operator = expression.pop(0)
        variable = expression.pop(0)
        
        if _Operators.PLUS == operator:
            sum = sum + _defined_variables[variable]

        elif _Operators.MINUS == operator:
            sum = sum - _defined_variables[variable]


def _value_to_variable_name(value: int) -> list:
    """ 
    Uses a dictionary \"backwards\" i.e. 
    given a value, it returns the corresponding variable name
    """
    
    return list(_defined_variables.keys())[list(_defined_variables.values()).index(value)]



