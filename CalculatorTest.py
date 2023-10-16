#this is a list of all the functions in the math module just for refrence ¯\_(ツ)_/¯
"""
__doc__
__loader__ 
__name__   
__package__
__spec__   
acos       
acosh      
asin       
asinh      
atan       
atan2      
atanh      
ceil       
comb       
copysign   
cos        
cosh       
degrees    
dist       
e
erf        
erfc       
exp        
expm1      
fabs       
factorial  
floor      
fmod       
frexp      
fsum       
gamma      
gcd        
hypot      
inf        
isclose    
isfinite   
isinf      
isnan      
isqrt      
lcm        
ldexp      
lgamma     
log        
log10      
log1p
log2
modf
nan
nextafter
perm
pi
pow
prod
radians
remainder
sin
sinh
sqrt
tan
tanh
tau
trunc
ulp
"""
from math import *
import sys
#this is a list containing all the valid math operations. This is because we dont want the user to run malicious code
#anything not in this list will not be allowed to run in the eval() function, thus preventing malicious code execution
safe_list = ['acos', 'asin', 'atan', 'atan2', 'ceil', 'cos','cosh', 'degrees', 'e', 'exp', 'fabs', 'floor','fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10','modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt','tan', 'tanh', 'factorial','ln','custlg','asinh','atanh','acosh']

#however the eval() function wants a dict with key string values like "sin" whose value is the builtin sin function ¯\_(ツ)_/¯


tolerance = pow(10,-15)

def ln(inputNum):
    return log(inputNum)

def custlg(inputNum):
    return log10(inputNum)

safeDict = {}
for safe_key in safe_list: #populating the dict
    safeDict[safe_key] = locals().get(safe_key)
#google has a lot of versions of pi so i decided to use a few of them just incase :-)
safeDict["π"] = pi
safeDict["𝝅"] = pi
safeDict["𝝿"] = pi
safeDict["pi"] = pi

def showExpressions():
    print("Allowed Expressions: ")
    print("| ", end="")
    for item in safe_list:
        print(item, end=" | ")


#the trig and hyp functions start with these letters so we will add a ' * ' before it to make the string actually usable
specialLetters = ["a","s","c","t"]
specialFunctions = ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh']

def isSpecialLetter(inputLetter):
    if inputLetter in specialLetters:
        return True
    else:
        return False
def isFunction(inputString):
    if inputString in specialFunctions:
        return True
    else:
        return False
def tempOutput(inputList):
    outputStr = ""
    for i in inputList:
        outputStr += i
    print(outputStr)
if __name__ == "__main__":
    print(radians(1))
    #CLI SECTION
    print("\nThis is an example expression: ")
    print("Please note that variables must be written in UPPERCASE inorder for the caluclator to work correctly")
    print("10 * X * Y +  5 * Y + X + X ** 2 , where X = 2 and Y = 5")

    while True:
        userInput = input("Please enter expression to solve: ")
        addedLetters = []
        for letter in userInput:
            addedLetters.append(letter)

        index = 0
        while index <= len(addedLetters) - 1:
            try:
                if addedLetters[index].isnumeric() == True and addedLetters[index + 1].isalpha() == True and addedLetters[index + 1].isupper():
                    print("first condition")
                    addedLetters.insert(index + 1, " * ")

                elif addedLetters[index].isalpha() == True and addedLetters[index + 1].isalpha() == True and addedLetters[index + 1].isupper():
                    print("second condition")
                    addedLetters.insert(index + 1, " * ")
                                
                elif addedLetters[index].isupper() == True and addedLetters[index].isalpha() == True and isSpecialLetter(addedLetters[index + 1]) == True:
                    print("third condition")
                    addedLetters.insert(index + 1, " * ")

                elif addedLetters[index].isalpha() == True and addedLetters[index].islower() == True and isFunction(addedLetters[index + 1 : index + 4]) == True:
                    print("fourth condition")
                    addedLetters.insert(index + 1, " * ")
                    tempOutput(addedLetters)
                    
                elif (addedLetters[index] == ")" or addedLetters[index].isnumeric() == True) and isSpecialLetter(addedLetters[index + 1]) == True:
                    print("fifth condition")
                    addedLetters.insert(index + 1, " * ")
                    tempOutput(addedLetters)

                elif addedLetters[index] == ")" and addedLetters[index + 1].isnumeric() == True:
                    print("sixth condition")
                    addedLetters.insert(index + 3, " * ")
                    tempOutput(addedLetters)
                    
                elif (addedLetters[index].isnumeric() == True or addedLetters[index].isupper == True) and addedLetters[index + 1] == "(":
                    print("seventh condition")
                    addedLetters.insert(index + 1, " * ")
                    tempOutput(addedLetters)
                print(f"Current Index: {index} | Current len: {len(addedLetters)}")

                if addedLetters[index] == "|":
                    expression = ""
                    for letter in addedLetters:
                        expression+=letter
                    expression = expression.replace("|", "abs(", 1).replace("|", ")", 1)
                    newList = []
                    for i in expression:
                        newList.append(i)
                    addedLetters = newList
                    index += 1
                    #note...if we have a number OR constant before trig/hyp function, then insert ' * '
                index+=1

            except Exception as E:
                #Detailed Mode
                #print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                
                #Get this over with mode
                break


        newUserInput = ""
        for i in addedLetters:
            newUserInput += i
        print(f"THIS IS THE NEW USER INPUT: {newUserInput}")
        try:
            answer = eval(newUserInput,safeDict)
            #if isclose(answer, 0, rel_tol=tolerance, abs_tol=tolerance):
                #answer = 0
            print(f"Answer: {answer}")

        except Exception as e:
            print("ERROR: ")
            print(e)

        """for item in addedLetters:
            safeDict.pop(item)
        addedLetters.clear()"""
        #  Degrees not supported yet ¯\_(ツ)_/¯ but will be with a GUI
        #  radians() function will be used to convert degrees to radians when a GUI is added


#GUI FUNCTIONS SECTION
#This is for the GUI. This is a high level function that automates all the shenanigans of the eval function()
def evaluate(inputString):
    try:
        answer = eval(userInput,safeDict)
        return answer
        
    except Exception as e:
        print("ERROR: ")
        print(e)

def evaluateWithParsing(userInput):
    addedLetters = []
    for letter in userInput:
        addedLetters.append(letter)

    if len(addedLetters) == 0:
        return ""
    index = 0
    while index <= len(addedLetters) - 1:
        try:
            if addedLetters[index].isnumeric() == True and addedLetters[index + 1].isalpha() == True and addedLetters[index + 1].isupper():
                #print("first condition")
                addedLetters.insert(index + 1, " * ")

            elif addedLetters[index].isalpha() == True and addedLetters[index + 1].isalpha() == True and addedLetters[index + 1].isupper():
                #print("second condition")
                addedLetters.insert(index + 1, " * ")
                            
            elif addedLetters[index].isupper() == True and addedLetters[index].isalpha() == True and isSpecialLetter(addedLetters[index + 1]) == True:
                #print("third condition")
                addedLetters.insert(index + 1, " * ")

            elif addedLetters[index].isalpha() == True and addedLetters[index].islower() == True and isFunction(addedLetters[index + 1 : index + 4]) == True:
                #print("fourth condition")
                addedLetters.insert(index + 1, " * ")
                #tempOutput(addedLetters)
                
            elif (addedLetters[index] == ")" or addedLetters[index].isnumeric() == True) and isSpecialLetter(addedLetters[index + 1]) == True:
                #print("fifth condition")
                addedLetters.insert(index + 1, " * ")
                #tempOutput(addedLetters)

            elif addedLetters[index] == ")" and addedLetters[index + 1].isnumeric() == True:
                #print("sixth condition")
                addedLetters.insert(index + 3, " * ")
                #tempOutput(addedLetters)
                
            elif (addedLetters[index].isnumeric() == True or addedLetters[index].isupper() == True) and addedLetters[index + 1] == "(" and addedLetters[index - 3] != "g":
                #print("seventh condition")
                addedLetters.insert(index + 1, " * ")
                #tempOutput(addedLetters)
            #note...if we have a number OR constant before trig/hyp function, then insert ' * '

            if addedLetters[index] == "|":
                expression = ""
                for letter in addedLetters:
                    expression+=letter
                expression = expression.replace("|", "abs(", 1).replace("|", ")", 1)
                newList = []
                for i in expression:
                    newList.append(i)
                addedLetters = newList
                index += 1
            
            index += 1
            
        except Exception as E:
            #Detailed Mode
            #print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            
            #Get this over with mode
            break


    newUserInput = ""
    for i in addedLetters:
        newUserInput += i
    try:
        answer = eval(newUserInput,safeDict)
        if isclose(answer, 0, rel_tol=tolerance, abs_tol=tolerance):
            answer = 0
        return str(answer)
    except SyntaxError:
        return "Syntax Error"
    except ZeroDivisionError:
        return "Zero Division Error"
    except OverflowError:
        return "Overflow Error"
    except Exception as e:
        return "Variables Error"

def addVariable(letter, value):
    if letter not in safeDict.keys():
        safeDict[letter] = value

def removeVariable(letter):
    if letter in dict.keys():
        safeDict.pop(letter)

def accessVariable(letter):
    return safeDict.get(letter)