
import abc, traceback, sys


class _Variables(dict):
    """ 
    Works as an interface for user defined variables 
    that extends pythons standard dictionary e.g.
    by adding a method that in a simplified way
    returns a variable name from a value
    """
    
    class VariableNameNotFoundError(Exception):
        "Variable name not found"
        pass

    def __getitem__(self, key) -> int:
        """ adds raising of custom error """
        if key not in self.keys():
            raise self.VariableNameNotFoundError
        else: 
            return super().__getitem__(key) 

    def key_from_value(self,value: int) -> str:
        """
        a method that in a simplified way
        returns a variable name from a value
        """
        try:
            return list(self.keys())[list(self.values()).index(value)]  
        except ValueError:
            raise self.VariableNameNotFoundError("Variable name not found")


class CalculatorCommand:
    """ 
    Base class for all calculator commands.

    Implements a "run" abstract method overrided in children
    that is executed on instantiation and 
    hence executes in children instances,
    customized for their specific command.

    Also contains attributes for type 
    """

    class Types:
        """ Defines the allowed command types for the calculator """
        DEF = "def"
        CLEAR = "clear"
        CALC = "calc"

    class DefaultRightHandSides:
        """ Defines the allowed operator types for the calculator """
        UNKNOWN ='unknown'
        # ...

    class Result:
        """ 
        Container class for the command result which 
        is a string. Adds some typesafeing.
        """
        
        def __str__(self):
            return self.text 

        class ResultError(Exception):
            "The type of a commond result must be of string type"
            pass

        def __init__(self,text: str):
            
            if not isinstance(text, str):
                raise self.ResultError
            else:
                self.text = text


    class CalculatorCommandError(Exception):
        "Base class not meant to be instantiated"
        pass

    
    class CommandNotFoundError(Exception):
        """ Handles when the type of command is not recognized """
        
        def __init__(self, command_name):
            msg = f"The command type \"{command_name}\" is not found  " 
            super().__init__(msg)


    def __init__(self,command = None):

        self.TYPE: self.Types
        self.result: self.Result

        if command is None:
            self.run()
        
        else:
            self.run(command )

    
    def __str__(self):
        return self.result.text
        
    @abc.abstractmethod
    def run(self):
        """
        Ment to be overridden and customized for the 
        child classe's specific command. 
        """
    
        raise self.CalculatorCommandError
    

class ClearVariables(CalculatorCommand):
    """ clear all user defined variables """

    def run(self) -> str:
        
        self.TYPE = self.Types.DEF 
        
        _defined_variables.clear()

        self.result = self.Result("All variables cleared")  
        
    
class DefineVariable(CalculatorCommand):
    """ Defines a stored variable """

    def run(self, expression: list) -> str:
        variable_name = expression.pop(0)
        variable_value = expression.pop(0)

        _defined_variables[variable_name] = int(variable_value)

        self.result = self.Result(f"Defined variable: {variable_name}, with value: {variable_value} ")
    

class EvaluateExpression(CalculatorCommand):
    """ 
    Tries to calculate an expression and
    determing a defined variable name as the right 
    hand side corresponding to that resulting value
    """

    class _Operators:
        """ Defines the allowed operator types for the calculator """
        PLUS = '+'
        MINUS = '-'
        EQUALS = '='

    def run(self, expression: list) -> str:

        sum: int
        right_hand_side_answer_word: str
        left_hand_side_expression_text : str
        
        expression.remove(self._Operators.EQUALS)

        left_hand_side_expression_text = ' '.join( expression)

        try:
            
            sum = self._calculate(expression)  
            right_hand_side_answer_word = _defined_variables.key_from_value(sum)
        
        except _defined_variables.VariableNameNotFoundError:

            right_hand_side_answer_word = self.DefaultRightHandSides.UNKNOWN


        self.result = self.Result(f"{left_hand_side_expression_text} = {right_hand_side_answer_word}" )
    

    def _calculate(self,expression: list) -> int:
        """ Calculates a given mathematical expression """

        sum = int(_defined_variables[expression.pop(0)]) # it will always start with the first variable
            
        for itemIndex in range(0,len(expression)-1,2):
            operator = expression.pop(0)
            variable = expression.pop(0)
            
            if self._Operators.PLUS == operator:
                sum = sum + _defined_variables[variable]

            elif self._Operators.MINUS == operator:
                sum = sum - _defined_variables[variable]

        return sum


class CalulatorCommandFactory:
    """
    Creates command instances of different types. 
    The commands will run on instantiation and return
    a command result, which contains a result or informatic text
    from the execution, also does some initial parsing of the command
    """

    @staticmethod
    def create(command) -> CalculatorCommand:
        """ Tries to create a specific command """

        try:
           
            parsed_expression = command.split(' ')
            command_type = parsed_expression.pop(0)

            if  CalculatorCommand.Types.DEF == command_type: 
                return DefineVariable(parsed_expression)

            elif CalculatorCommand.Types.CLEAR == command_type:
                return ClearVariables()

            elif CalculatorCommand.Types.CALC == command_type:
                return EvaluateExpression(parsed_expression)

            else:
                raise CalculatorCommand.CommandNotFoundError
        
        except CalculatorCommand.CommandNotFoundError:
            traceback.print_exc()
            sys.exit()

        except Exception:
            print( f"The command given: \"{command}\" caused an error: " )
            traceback.print_exc()
            sys.exit()



_defined_variables = _Variables()

