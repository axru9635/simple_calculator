import sys

inputFile = sys.argv[1]

inputLines = []
outputList = []

definedVariables = {}

# uncommnet on submssion
# for line in sys.stdin:
#     inputLines.append(line.rstrip())

# comment on submission
with open(inputFile) as fh: 
   for line in fh.readlines():
       inputLines.append(line.rstrip() )

for commandLine in inputLines:

    commandToParse = commandLine.split(' ')
    commandType = commandToParse.pop(0)
    outputExpression = ' '.join(commandToParse)
    
    if commandType == 'clear':
        definedVariables.clear()

    elif commandType == 'def':
        definedVariables[commandToParse.pop(0)] = int(commandToParse.pop(1))

    elif commandType == 'calc':
        sum = 0
        commandVariables = []
        answer = ''
        
        [commandVariables.append(item) for item in commandToParse if item not in ['+','-','='] ]
        
        if not all(var in definedVariables for var in commandVariables):
            answer = 'unknown'
            
        else:
            sum = definedVariables[commandToParse.pop(0)] # it will always start with the first variable
            
            for itemIndex in range(0,len(commandToParse)-1,2):
                operator = commandToParse.pop(0)
                variable = commandToParse.pop(0)
                
                if operator == '+':
                    sum = sum + definedVariables[variable]
                elif  operator == '-':
                    sum = sum - definedVariables[variable]
                
            if not sum in definedVariables.values():
                answer = "unknown"    
            else:
                answer = list(definedVariables.keys())[list(definedVariables.values()).index(sum)]

        outputList.append( outputExpression + ' ' + answer)

# Final 
[print(outputLine) for outputLine in outputList]
