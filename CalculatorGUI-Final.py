#This is the frontend of the CalculatorTest backend
#(It's not really now. Its a mess of backend and frontend and alot of other things lmao.)
#(But it was fun.)
#This is supposed to be a scientific calculator

import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from sympy import var,sympify,Eq,symbols,solve
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import CalculatorTest as CALC
import UNIT_CONVERSION_FINAL as UC
import math 

#CalculatorTest library created by Aly Mohamed Elsharkawy 320220040
##############################################################################
#Belal here.
#I got the code from Aly 5/2/2023
#and started implementing the features i made in another file here 
#already implemented grahping in the university today 2/5/2023
#and started implementing other features now at 6:00 PM
##############################################################################
"""""
                Aly Mohamed Elsharkawy (320220040) SEC 2
                Belal Mohamed Elsayed Salem (320220015) SEC 1
                Hazem Ahmed Saadallah Mohammed(320220035) SEC 2
                """


#This contains all the important color codes to make the calculator look stylish
styleDict = {"SMALL_FONT_STYLE": ("Segoe UI",18),"LARGE_FONT_STYLE": ("Segoe UI",45),"DIGIT_FONT_STYLE": ("Segoe UI",27,"bold"),"DEFAULT_FONT_STYLE": ("Segoe UI",23),"UNIT_FONT_STYLE": ("Segoe UI",16),"LIGHT_GRAY": "#F5F5F5","WHITE": "#FFFFFF","LABEL_COLOR": "#25265E","OFF_WHITE": "#F8FAFF","LIGHT_BLUE": "#CCEDFF","MS_LIGHT_GRAY": "#3b3b3b","MS_DARK_GRAY": "#323232","MS_LIGHT_BLUE": "#76b9ed","MS_BACKGROUND_GREY": "#202020"}

class Calculator:
    #constructor...This is pretty important for defining basic properties
    def __init__(self):
        #basic initializations and creating the window
        self.width = 630
        self.height = 667
        self.window = tk.Tk()
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.resizable(0,0)
        self.window.title("General Purpose Calculator")
        self.window.config(bg=styleDict["MS_BACKGROUND_GREY"])
        self.currentExpression = ""
        self.totalExpression = ""
        self.temp = {}
        self.canvas_frame=None
        self.specialLetters = ["a","s","c","t"]
        self.specialFunctions = ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh']


        
        #this is for managing the creation and destruction of the hyp and tri menus and constant menu
        self.hypExists = False
        self.triExists = False
        self.constantExist = False
        self.hypButtons = []
        self.triButtons = []
        self.constantButtons = []

        #variable for tracking whether the calculator is in radian or degrees mode
        #by default it will be rad because the built in trig and hyp functions in all programming languages use radians
        self.isRad = True
        self.isInverse = False

        #for adding mode menu
        self.menuManager = tk.Menu(self.window)
        self.window.config(menu=self.menuManager)


        #adding mode menu and misc menu and their options
        modeMenu = tk.Menu(self.menuManager)
        miscMenu = tk.Menu(self.menuManager)

        self.menuManager.add_cascade(label="Mode",menu=modeMenu)
        self.menuManager.add_cascade(label="Credits",menu=miscMenu)

        modeMenu.add_command(label="Scientific Calculator", command=self.goToScientific)
        #modeMenu.add_command(label="Complex", command=self.goToComplex)
        #modeMenu.add_command(label="Base-N", command=self.goToBaseN)
        modeMenu.add_command(label="2D Graphing", command=self.graphingMode)
        modeMenu.add_command(label="SLE Solver",command=self.calc_SOE)
        modeMenu.add_command(label="Quadratic Equation Solver",command=self.Quadritic_ready)
        modeMenu.add_command(label="Cubic Equation Solver",command=self.cubic_ready)
        modeMenu.add_command(label="Base-N Converter",command=self.baseN_ready)
        modeMenu.add_command(label="Unit Conversion", command=self.getConversionReady)
        #modeMenu.add_command(label="Matrix",command=self.goToMatrix)
        modeMenu.add_command(label="Quit",command=self.terminateApp)

        miscMenu.add_command(label="View Credits", command=self.showCredits)

        #to prevent user from closing too many brackets
        self.bracketsList = []


        #initialzing the 2 main display and button labels
        self.displayFrame = self.createDisplayFrame()
        self.buttonsFrame = self.createButtonsFrame()
        self.equals_button = self.createEqualsButton()
        self.buttonsFrame.config(borderwidth=3)

        #Scientific constants
        self.scientificConstants = {
            'π': 3.141592653589793,         # PI
            'e': 2.718281828459045,         # Euler's number
            'ħ': 6.62607015*(10**-34),      # Planck constant
            'k': 8.9875517923*(10**9),      # Coulomb constant
            'me': 9.1093837015*(10**-31),   # Electron mass
            'mp': 1.67262192369*(10**-27),  # Proton mass
            'mn': 1.67492749804*(10**-27),  # Neutron mass
            'μ': 1.883531627*(10**-28),     # Muon mass
            'a₀': 5.291772086*(10**-11),   # Bohr radius
            'μN': 5.0507837461*(10**-27),  # Nuclear magneton
            'μB': 9.2740100783*(10**-24),  # Bohr magneton
            'α': 7.2973525693*(10**-3),     # Fine-Structure Constant
            're': 2.8179403262*(10**-15),   # Classical electron radius
            'λc': 2.42631023867*(10**-12), # Compton Wavelength
            'γp': 267522209.9,             # Gyromagnetic ratio
            'λcp': 1.321409845*(10**-15),  # Proton Compton Wavelength
            'λcn': 1.319590895*(10**-15),  # Neutron Compton Wavelength
            'G': 6.67430*(10**-11),         # Newtonian constant of gravitation
            'R∞': 10973731.57,              # Rydberg constant
            'u': 1.66053906660*(10**-27),   # Atomic mass constant
            'μp': 1.410606662*(10**-26),   # Proton magnetic moment
            'μe': -9.2847647043*(10**-24), # Electron magnetic moment
            'μn': -9.6623641*(10**-27),    # Neutron magnetic moment
            'μμ': -4.49044786*(10**-26),   # Muon magnetic moment
            'F': 96485.3399,               # Faraday constant
            'NA': 6.02214179*(10**23),      # Avogadro constant
            'k': 1.3806504*(10**-23),       # Boltzmann constant
            'Vm': 0.022413996,              # Molar volume of ideal gas
            'R': 8.314472,                  # Molar gas constant
            'σ': 5.6704*(10**-8),           # Stefan-Boltzmann constant
            'ε₀': 8.854187817*(10**-12),   # Electric constant
            'μ₀': 1.256637061*(10**-6),    # Magnetic constant
            'Φ₀': 2.067833667*(10**-15),   # Magnetic
            'G₀': 7.7480917*(10**-5),       # Conductance quantum
            'Z₀': 376.7303135,              # Characteristic impedance of vacuum
            't': 273.15,                    # Celsius temperature
            'atm': 101325,                  # Standard atmosphere
            'c': 3*(10**8),                 # Speed of light in vacuum
            'e': -1.602176634*(10**-19),    # Charge of electron
            'e₀': 8.8541878128*(10**-12),   # Vacuum permittivity
            'h': 6.62607015*(10**-34),      # Planck constant
            'hbar': 1.054571817*(10**-34),  # Reduced Planck constant
        }
        self.scientificConstantsList = list(self.scientificConstants.keys())

        #expanding each button to occupy whole screen
        #initially 5Rx4C
        
        self.FixButtonSize()

        #all capital letters in english language for keyboard input
        self.capitalLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        #al lowercase letters for keyboard input
        self.lowerCaseletters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        #digits and their grid positions
        self.digits = {7: (5, 2), 8: (5, 3), 9: (5, 4),4: (6, 2), 5: (6, 3), 6: (6, 4),1: (7,2), 2: (7, 3), 3: (7, 4), 0: (8, 3), '.': (8, 4)}

        #just a simple dict for making the output look nice instead of 3^4 its 3⁴
        self.numericPowers = {"^0": "⁰", "^1": "¹", "^2": "²", "^3" : "³" , "^4" : "⁴", "^5" : "⁵", "^6" : "⁶" , "^7" : "⁷" , "^8" : "⁸", "^9": "⁹"}

        #just a simple dict for making the output look nice instead of 3^X its 3ˣ
        self.alphaPowers = {"A": "ᴬ", "B": "ᴮ", "C" : "ᶜ", "D" : "ᴰ", "E" : "ᴱ", "F" : "ᶠ", "G" : "ᴳ", "H" : "ᴴ", "I" : "ᴵ", "J" : "ᴶ", "K" : "ᴷ", "L" : "ᴸ", "M" : "ᴹ",  "N" : "ᴺ", "O" : "ᴼ", "P" : "ᴾ", "Q" : "ᵠ", "R" : "ᴿ", "S" : "ˢ", "T" : "ᵀ", "U" : "ᵁ", "V" : "ⱽ", "W" : "ᵂ", "X" : "ˣ", "Y" : "ʸ", "Z" : "ᶻ"} 

        #exist purely to help automate things
        self.wordButtons = ["TRI", "HYP","GRP","CST","RAD"]
        self.logExpoButtons = ["log(𝒙)","ln(𝒙)"]

        #allowed operations and their unicode alternatives
        
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.extraOperations = {"√":"sqrt","log":"custlg","²" : "**2", "³" : "**3", "⁰": "**0", "⁴": "**4", "⁵": "**5", "⁶": "**6", "⁷": "**7", "⁸":"**8","⁹":"**9"}

        self.converstionButtons = []
        self.allowedConversion = ["Length","Area","Volume", "Close"]

        #This part is for the unit conversions
        self.lengthConversionValues =  ['n/a','cm', 'dm', 'feet', 'inch', 'km', 'm', 'mi', 'mm', 'nm', 'nmi', 'pm', 'um', 'yd']
        self.lengthConversionNames = ['select unit','centimeters', 'decimeters', 'feet', 'inches', 'kilometers', 'meters', 'miles', 'millimeters', 'nanometers', 'nautical miles', 'picometers', 'micrometers', 'yards']
        for index in range(len(self.lengthConversionNames)):
            self.lengthConversionNames[index] = self.lengthConversionNames[index].title()

        self.areaConversionNames = ['select unit','square centimeters', 'square decimeters', 'square feet', 'square inches', 'square kilometers', 'square meters', 'square miles', 'square millimeters', 'square nanometers', 'square nautical miles', 'square picometers', 'square micrometers', 'square yards', 'close']
        self.areaConversionValues = ['n/a','cm**2', 'dm**2', 'feet**2', 'inch**2', 'km**2', 'm**2', 'mi**2', 'mm**2', 'nm**2', 'nmi**2', 'pm**2', 'um**2', 'yd**2']
        for index in range(len(self.areaConversionNames)):
            self.areaConversionNames[index] = self.areaConversionNames[index].title()

        self.volumeConversionNames = ['select unit','cubic centimeters', 'cubic decimeters', 'cubic feet', 'cubic inches', 'cubic kilometers', 'cubic meters', 'cubic miles', 'cubic millimeters', 'cubic nanometers', 'cubic nautical miles', 'cubic picometers', 'cubic micrometers', 'cubic yards']
        self.volumeConversionValues = ['n/a','cm**3', 'dm**3', 'feet**3', 'inch**3', 'km**3', 'm**3', 'mi**3', 'mm**3', 'nm**3', 'nmi**3', 'pm**3', 'um**3', 'yd**3']
        for index in range(len(self.volumeConversionNames)):
            self.volumeConversionNames[index] = self.volumeConversionNames[index].title()

        #creating the 2 main current expression and total expression labels
        self.totalExpressionLabel, self.currentExpressionLabel = self.createDisplayLabels()

        #creating the operator buttons
        self.createOperatorButtons()

        #creating the clear button
        self.createClearButton()

        #creating the digit buttons
        self.createDigitButtons()

        #creating the equals button
        #equals button is now a property of the calculator itself

        #creating the square button
        self.createSquareButton()

        #creating reciprocoral button
        self.createReciprocoralButton()

        #creating the square root button
        self.createSquareRootButton()

        #bind the keyboard to the calculator
        self.bindKeys()

        #creating delete button
        self.createDeleteButton()

        #creating extra word buttons
        self.createWordButtons()

        #creating brackets buttons
        self.createBracketButtons()

        #creating factorialButton
        self.createFactorialButton()

        #creating absolute button
        self.createAbsoluteButton()

        #creating logarithmic button
        self.createLogButtons()

        #creating inverse button
        self.createInverseButton()

        #creating exponential button
        self.createExpoButton()

    def FixButtonSize(self,columnNumInput=6):
        for rowNum in range(1,9):
            self.buttonsFrame.rowconfigure(rowNum,weight=1)
        
        for columnNum in range (1,columnNumInput):
            self.buttonsFrame.columnconfigure(columnNum, weight=1)
    
    def showCredits(self):
        newWindow = tk.Tk()
        newWindow.title("Scientific Calculator Credits")
        newWindow.geometry("800x180")
        creditsLabel = tk.Label(newWindow,text="""              The Scientific Calculator was Created by\n 
                Aly Mohamed Elsharkawy (320220040)
                Belal Mohamed Elsayed Salem (320220015) 
                Hazem Ahmed Saadallah Mohammed(320220035)\n
                                """, font=("Segoe UI", 14, "bold"))
        creditsLabel.pack(expand=True,fill=tk.BOTH,padx=5,pady=5)


    #I dont think i need to explain xD
    def terminateApp(self):
        quit()
    

    #modes are scientific, complex, base-n, SLE, matrix, 2D graph
    def goToScientific(self):
        self.window.unbind("=")
        self.window.bind("<Return>", lambda event: self.evaluate())
        self.equals_button.config(command=self.evaluate)
        self.leaveConversionMode()

    """def goToSLE(self):
        self.window.destroy()
        BelalsCalculator = BC.CalculatorBelal()
        BelalsCalculator.run()"""


    def graphingMode(self):
        self.currentExpression=""
        self.update_label()
        self.totalExpression="Y = "
        self.update_total_label()


        #we change the equal button and return key command to the next step
        self.equals_button.configure(command=lambda: self.create_graph_frame(self.totalExpression))
        self.window.bind("<Return>", lambda event: self.create_graph_frame(self.totalExpression))


    def create_graph_frame(self,equation):
        #create the canvas frame
        print("we are now in the freaking graph window!")
        self.totalExpression = self.totalExpression.replace("Y","")
        self.totalExpression = self.totalExpression.replace("=","")
        if self.currentExpression != "":
            self.totalExpression = self.totalExpression + self.currentExpression
        
        self.update_total_label()
        print(f"Expression going to CALC: {self.totalExpression}")
        self.switchExponents()

        equation = self.totalExpression

        
        equation = self.parseCleanly(equation)

        canvas = tk.Frame(self.window)
        #assign it to be a property of the calc itself
        self.canvas_frame = canvas

        #we go into the graphfunction2D and pass to it things
        #and the frame
        #the function is down in the implementation
        graph = self.graphfuncsin2D(equation)
        if graph == "error":
            self.currentExpression="Error"
            self.update_label()
        else:
            self.temp["GGG"] = graph
            self.window.geometry("900x667")
            canvas.pack(pady=667,padx=200,side="left",expand=True,fill="y")
        

        var =tk.IntVar() #to wait fora click on the equals button
        self.equals_button.configure(command=lambda: var.set(1))
        self.window.bind("<Return>", lambda event: var.set(1))
        self.equals_button.wait_variable(var)
        self.clear()
        self.graphingMode()
        
    


    def graphfuncsin2D(self,func :str,x1=-5,x2=5): 
        X = var('X')
        try:
            expr = sympify(func)
        except:
            return "error"

        values = np.linspace(x1,x2,100)
        temp = []
        for value in values:
            te = expr.subs(X,value)
            if '*I' in str(te):
                new_values = np.linspace(0,x2,100)
                for val in new_values:
                    te = expr.subs(X,val)
                    temp.append(te)
                    values = new_values
                break
            temp.append(te)


        y = np.array(temp)

        fig,ax=plt.subplots()
        canvas = FigureCanvasTkAgg(fig,master=self.window)
        plt.axhline(0,color='0')
        plt.axvline(0,color='0')

        plt.plot(values,y)
        
        plt.xlabel("X axis")
        plt.ylabel("Y axis")
        plt.title("Graph")
        canvas.get_tk_widget().pack()
        return canvas
    
    def calc_SOE(self):
        self.currentExpression = ""
        self.update_label()
        self.totalExpression = "How many equations? (1,2,3)"
        self.update_total_label()
        self.equals_button.configure(command=self.Check_Noe)
        self.window.bind("<Return>", lambda event: self.Check_Noe())

        #second step
    def Check_Noe(self):
        
        NoE = self.currentExpression
        try: 

           if int(NoE) > 3 or int(NoE) < 1:
            self.totalExpression = "Must be 1, 2 or 3 eqs"
            self.update_total_label()
            self.currentExpression = ""
            self.update_label()
           else:
            self.currentExpression = ""
            self.update_label()
            self.store_equs(NoE)
        except:
            self.totalExpression=""
            self.update_total_label()
            self.currentExpression="Error"
            self.update_label()
        

        #third step
    def store_equs(self,NoE):
        list_of_eqs = []
        button = tk.Button(self.buttonsFrame, text = "=", fg = styleDict["WHITE"], bg=styleDict["MS_DARK_GRAY"], font=styleDict["DEFAULT_FONT_STYLE"], borderwidth=2,command=lambda x="=": self.addOperator(x))
        button.grid(row=1,column=1,padx=2,pady=2,stick=tk.NSEW,columnspan=1)
        self.window.bind("=", lambda event: self.addOperator("="))
        self.temp["string_equal_temp"] = button
        for num in range(1,int(NoE) + 1):
            var =tk.IntVar() #to wait fora click on the equals button
            self.equals_button.configure(command=lambda: var.set(1))
            self.window.bind("<Return>", lambda event: var.set(1))
            self.totalExpression = f"Enter Eq.{str(num)}: "
            self.update_total_label()
            self.equals_button.wait_variable(var)
            if self.currentExpression != "":
                self.totalExpression = self.totalExpression + self.currentExpression
            self.update_total_label()
            print(f"Expression going to CALC: {self.totalExpression}")
            self.switchExponents()
            self.totalExpression = self.parseCleanly(self.totalExpression)
            list_of_eqs.append(self.totalExpression)
            self.currentExpression = ""
            self.update_label()

        self.totalExpression = "Answer"
            
        try:
            sol = self.solveFuncs(tuple(list_of_eqs),NoE=NoE) #we pass the list as a tuple to the implementaion of solveFuncs
        except Exception as e:
            self.currentExpression = "Error"
            self.update_label()
        else:
            self.show_eq_solution(sol,NoE) #if no error happens we pass the solution to this function
                                           #to properly show the solution

        finally:

            self.update_total_label()

    def solveFuncs(self,expr,NoE):
        NoE = int(NoE)
        if NoE == 1:
            X = symbols("X")
            eqs = self._fixequs(expr)
            sol = solve(eqs,(X))
            for key in sol:
                sol[key] = round(sol[key],2)
            return sol

        elif NoE == 2:
            X,Y = symbols("X Y")
            eqs = self._fixequs(expr)
            sol = solve(eqs,(X,Y))
            for key in sol:
                sol[key] = round(sol[key],2)
            return sol
            

        elif NoE == 3:
            X,Y,Z = symbols("X Y Z")
            eqs = self._fixequs(expr)
            
            sol = solve(eqs,(X,Y,Z))
            for key in sol:
                sol[key] = round(sol[key],2)
                
            return sol
            

        #final step
    def show_eq_solution(self,sol,NoE):
        var = tk.IntVar()
        self.equals_button.config(command=lambda: var.set(1))
        keys = []
        for key in sol:
            keys.append(key)
        NoE = int(NoE)
        if NoE == 1:
            
            self.currentExpression = f"X = {str(sol[keys[0]])[:5]}"
            self.update_label()
        elif NoE == 2:
            self.currentExpression = f"X = {str(sol[keys[0]])[:5]}"
            self.update_label()
            self.equals_button.wait_variable(var)
            self.currentExpression = f"Y = {str(sol[keys[1]])[:5]}"
            self.update_label()
        elif NoE == 3:
            self.currentExpression = f"X = {str(sol[keys[0]])[:5]}"
            self.update_label()
            self.equals_button.wait_variable(var)
            self.currentExpression = f"Y = {str(sol[keys[1]])[:5]}"
            self.update_label()
            self.equals_button.wait_variable(var)
            self.currentExpression = f"Z = {str(sol[keys[2]])[:5]}"
            self.update_label()

    def _fixequs(self,expr):
        eqs  = []
        num=1
        for equ in expr:
            equ = equ.replace(f"Enter Eq.{num}: ","")
            print(equ)
            temp = equ
            final,value = [x.strip() for x in temp.split("=")]
            eqs.append(Eq(sympify(final),float(value)))
            num += 1
        eqs = tuple(eqs)
        return eqs
    

    def baseN_ready(self):
        self.currentExpression=""
        self.update_label()
        self.totalExpression="Enter Base from"
        self.update_total_label()
        var = tk.IntVar()
        self.equals_button.configure(command=lambda: var.set(1))
        self.window.bind("<Return>", lambda event: var.set(1))
        self.equals_button.wait_variable(var)
        N_from = self.currentExpression
        if int(N_from) > 36:
            self.totalExpression = "Base N can't be higher than 36"
            self.currentExpression= ""
            self.update_total_label()
            self.equals_button.wait_variable(var)
            self.baseN_ready()
        if int(N_from) <= 0:
            self.totalExpression = "Base N can't be less than 0"
            self.currentExpression= ""
            self.update_total_label()
            self.equals_button.wait_variable(var)
            self.baseN_ready()

        self.currentExpression=""
        self.update_label()
        self.totalExpression="Enter Base to"
        self.update_total_label()
        self.equals_button.wait_variable(var)
        N_to = self.currentExpression

        if int(N_to) > 36:
            self.totalExpression = "Base N can't be higher than 36"
            self.currentExpression= ""
            self.update_total_label()
            self.equals_button.wait_variable(var)
            self.baseN_ready()
        if int(N_to) <= 0:
            self.totalExpression = "Base N can't be less than 0"
            self.currentExpression= ""
            self.update_total_label()
            self.equals_button.wait_variable(var)
            self.baseN_ready()


        self.currentExpression=""
        self.update_label()
        self.totalExpression="Enter number"
        self.update_total_label()
        self.equals_button.wait_variable(var)
        num = self.currentExpression
        self.totalExpression="Answer"
        self.update_total_label()
        try:
            self.currentExpression = self.base_N(N_from,num,N_to)
        except:
            self.currentExpression = "Error"
        finally:
            self.update_label()
            self.equals_button.configure(command=self.baseN_ready)
            self.window.bind("<Return>", lambda event: self.baseN_ready())





    def decimal_to_N(self,num, base):
        if int(base) > 36:
            return "err_000"
        num_str = ""
        num = int(num)
        base = int(base)
        while num > 0:
            if (num % base) < 9:
                num_str += str(num % base)
            else:
                num_str += chr(ord('A') + int(num % base) - 10)
            num //= base
        num_str = num_str[::-1]
        return num_str


    def N_to_decimal(self,num, base):
        if int(base) > 36:
            return "err_000"
        dec_num = 0
        base = int(base)
        ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
        ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        dig_list = list()
        for i in range(len(num)):
            if num[i] in ascii_lowercase[:base - 10]:
                dig_list.append(int(ascii_lowercase.index(num[i]) + 10))
            elif num[i] in ascii_uppercase[base - 10]:
                dig_list.append((ascii_uppercase.index(num[i]) + 10))
            elif num[i] in "0123456789":
                dig_list.append(int(num[i]))
            else:
                print("Error:\"", num[i], "\"out of base", base, "digites")
                return "err001"
        for i in range(len(dig_list)):
            dec_num += base**(len(dig_list) -1 -i) * int(dig_list[i])
        return dec_num


    def base_N(self,old_N, num, new_N):
        return self.decimal_to_N(self.N_to_decimal(num, old_N), new_N)

    def isSpecialLetter(self,inputLetter):
        if inputLetter in self.specialLetters:
            return True
        else:
            return False
    def isFunction(self,inputString):
        if inputString in self.specialFunctions:
            return True
        else:
            return False
        

    def Quadritic_ready(self):
        
        constanslist = ['a','b','c']

        self.totalExpression=f"{str(constanslist[0])}X\u00b2+{str(constanslist[1])}X+{str(constanslist[2])}"
        self.update_total_label()
        self.currentExpression = ""
        self.update_label()

        var =tk.IntVar() #to wait fora click on the equals button
        self.equals_button.configure(command=lambda: var.set(1))
        self.window.bind("<Return>", lambda event: var.set(1))
        

        for i in range(0,3):

            constanslist[i] = constanslist[i].upper()
            self.totalExpression=f"{str(constanslist[0])}X\u00b2+{str(constanslist[1])}X+{str(constanslist[2])}"
            self.update_total_label()
            self.equals_button.wait_variable(var)
            constanslist[i] = self.currentExpression

            self.currentExpression = ""
            self.update_label()
            if i == 2:
                self.totalExpression=f"{str(constanslist[0])}X\u00b2+{str(constanslist[1])}X+{str(constanslist[2])}"
                self.update_total_label()
        try:
            self.solveQuadritic(float(constanslist[0]),float(constanslist[1]),float(constanslist[2]))
        except:
            self.currentExpression="Error"
            self.update_label()
        finally:
            self.equals_button.configure(command=self.Quadritic_ready)
            self.window.bind("<Return>", lambda event: self.Quadritic_ready())

    def solveQuadritic(self,a,b,c):
        d = (b**2) - (4*a*c)
        print(d)
        x1= (-b-math.sqrt(d)/(2*a))
        x2= (-b+math.sqrt(d)/(2*a))
        self.currentExpression = f"X1 = {str(x1)[:6]}"
        self.update_label()
        var = tk.IntVar()
        self.equals_button.configure(command=lambda: var.set(1))
        self.window.bind("<Return>", lambda event: var.set(1))
        self.equals_button.wait_variable(var)
        print("here")
        self.currentExpression = f"X2 = {str(x2)[:6]}"
        self.update_label()


    def cubic_ready(self):
        constanslist = ['a','b','c','d']

        self.totalExpression=f"{str(constanslist[0])}X\u00b2+{str(constanslist[1])}X+{str(constanslist[2])}"
        self.update_total_label()
        self.currentExpression = ""
        self.update_label()

        var =tk.IntVar() #to wait fora click on the equals button
        self.equals_button.configure(command=lambda: var.set(1))
        self.window.bind("<Return>", lambda event: var.set(1))
        

        for i in range(0,4):

            constanslist[i] = constanslist[i].upper()
            self.totalExpression=f"{str(constanslist[0])}X\u00b3+{str(constanslist[1])}X\u00b2+{str(constanslist[2])}+{str(constanslist[3])}"
            self.update_total_label()
            self.equals_button.wait_variable(var)
            constanslist[i] = self.currentExpression

            self.currentExpression = ""
            self.update_label()
            if i == 3:
                self.totalExpression=f"{str(constanslist[0])}X\u00b2+{str(constanslist[1])}X+{str(constanslist[2])}+{str(constanslist[3])}"
                self.update_total_label()
        try:
            self.solveCubic(float(constanslist[0]),float(constanslist[1]),float(constanslist[2]),float(constanslist[3]))
        except:
            self.currentExpression = "Error"
            self.update_label()
        finally:
            self.equals_button.configure(command=self.cubic_ready)
            self.window.bind("<Return>", lambda event: self.cubic_ready())

    def solveCubic(self,a,b,c,d):
        solutions = list()
        p = (3 * a * c - b ** 2) / (3 * a ** 2)
        q = (2 * b ** 3 - 9 * a * b * c + 27 * a ** 2 * d) / (27 * a ** 3)
        alpha = self.cbrt(-q / 2 + math.sqrt((q / 2) ** 2 + (p / 3) ** 3))
        beta = self.cbrt(-q / 2 - math.sqrt((q / 2) ** 2 + (p / 3) ** 3))
        for i in alpha:
            for j in beta:
                if abs((i * j) + p / 3) <= 0.00001:
                    x = i + j - b / (3 * a)
                    solutions.append(x)

        self.currentExpression = f"X1 = {str(solutions[0])[:6]}"
        self.update_label()
        var = tk.IntVar()
        self.equals_button.configure(command=lambda: var.set(1))
        self.window.bind("<Return>", lambda event: var.set(1))
        self.equals_button.wait_variable(var)
        print(solutions)
        print("here")
        self.currentExpression = f"X2 = {str(solutions[1])[:6]}"
        self.update_label()
        self.equals_button.wait_variable(var)
        print("here")
        self.currentExpression = f"X3 = {str(solutions[2])[:6]}"
        self.update_label()

    def cbrt(self,polynomial):
        solution = set()
        root1 = polynomial ** (1 / 3)
        root2 = (polynomial ** (1 / 3)) * (-1 / 2 + (math.sqrt(3) * 1j) / 2)
        root3 = (polynomial ** (1 / 3)) * (-1 / 2 - (math.sqrt(3) * 1j) / 2)
        solution.update({root1, root2, root3})
        return solution



    def parseCleanly(self,stringToParse):
        
        addedLetters = []
        for letter in stringToParse:
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
                                
                elif addedLetters[index].isupper() == True and addedLetters[index].isalpha() == True and self.isSpecialLetter(addedLetters[index + 1]) == True:
                    #print("third condition")
                    addedLetters.insert(index + 1, " * ")

                elif addedLetters[index].isalpha() == True and addedLetters[index].islower() == True and self.isFunction(addedLetters[index + 1 : index + 4]) == True:
                    #print("fourth condition")
                    addedLetters.insert(index + 1, " * ")
                    #tempOutput(addedLetters)
                    
                elif (addedLetters[index] == ")" or addedLetters[index].isnumeric() == True) and self.isSpecialLetter(addedLetters[index + 1]) == True:
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
                index+=1  

            except Exception as E:
            #Detailed Mode
            #print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            
            #Get this over with mode
                break         
            newUserInput = ""
        for i in addedLetters:
            newUserInput += i
        return newUserInput
    
    def updateDropdowns(self, event):
        print("Updating dropdowns")
        conversion_mode = self.conversionModeVar.get()
        input_mode = self.inputModeVar.get()
        output_mode = self.outputModeVar.get()

        if conversion_mode == "Close" or input_mode == "Close" or output_mode == "Close":
            self.leaveConversionMode()
        if conversion_mode == "Length":
            self.inputDropDownMenu["menu"].delete(0,"end")
            for item in self.lengthConversionNames:
                command= tk._setit(self.inputModeVar, item)
                self.inputDropDownMenu["menu"].add_command(label=item, command = command)
            self.outputModeMenu["menu"].delete(0,"end")
            for item in self.lengthConversionNames:
                command= tk._setit(self.outputModeVar, item)
                self.outputModeMenu["menu"].add_command(label=item, command = command)
        elif conversion_mode == "Area":
            self.inputDropDownMenu["menu"].delete(0,"end")
            for item in self.areaConversionNames:
                command= tk._setit(self.inputModeVar, item)
                self.inputDropDownMenu["menu"].add_command(label=item, command = command)
            self.outputModeMenu["menu"].delete(0,"end")
            for item in self.areaConversionNames:
                command= tk._setit(self.outputModeVar, item)
                self.outputModeMenu["menu"].add_command(label=item, command = command)
        elif conversion_mode == "Volume":
            self.inputDropDownMenu["menu"].delete(0,"end")
            for item in self.volumeConversionNames:
                command= tk._setit(self.inputModeVar, item)
                self.inputDropDownMenu["menu"].add_command(label=item, command = command)
            self.outputModeMenu["menu"].delete(0,"end")
            for item in self.volumeConversionNames:
                command= tk._setit(self.outputModeVar, item)
                self.outputModeMenu["menu"].add_command(label=item, command = command)
        self.inputModeVar.set("Select Unit")
        self.outputModeVar.set("Select Unit")

    def getConversionReady(self):
        self.equals_button.configure(command= self.unitConversion)
        self.window.unbind("=")
        self.window.bind("<Return>", lambda event: self.unitConversion())
        self.destroyHypButtons()
        self.destroyTriButtons()
        self.inputModeVar = tk.StringVar()
        self.inputModeVar.set(self.lengthConversionNames[0])
        self.conversionModeVar = tk.StringVar()
        self.conversionModeVar.set(self.allowedConversion[0])
        self.outputModeVar = tk.StringVar()
        self.outputModeVar.set(self.lengthConversionNames[0])
        self.inputDropDownMenu = tk.OptionMenu(self.buttonsFrame,self.inputModeVar, *self.lengthConversionNames,command=self.closeChecker)
        self.inputDropDownMenu.config(bg=styleDict["MS_DARK_GRAY"],fg=styleDict["WHITE"],borderwidth=2,font=styleDict["UNIT_FONT_STYLE"],height=2)
        self.inputDropDownMenu.config(bg=styleDict["MS_DARK_GRAY"],fg=styleDict["WHITE"],borderwidth=2,font=styleDict["UNIT_FONT_STYLE"],height=2)
        self.inputDropDownMenu.grid(row=1,column=1,columnspan=2,padx=5,pady=5,stick=tk.NSEW,rowspan=1)
        self.converstionButtons.append(self.inputDropDownMenu)

        self.outputModeMenu = tk.OptionMenu(self.buttonsFrame,self.outputModeVar, *self.lengthConversionNames,command=self.closeChecker)
        self.outputModeMenu.config(bg=styleDict["MS_DARK_GRAY"],fg=styleDict["WHITE"],borderwidth=2,font=styleDict["UNIT_FONT_STYLE"],height=2)
        self.outputModeMenu.grid(row=1,column=4,columnspan=2,padx=5,pady=5,stick=tk.NSEW,rowspan=1)
        self.converstionButtons.append(self.outputModeMenu)

        conversionModeMenu = tk.OptionMenu(self.buttonsFrame,self.conversionModeVar, *self.allowedConversion,command=self.updateDropdowns)
        conversionModeMenu.config(bg=styleDict["MS_DARK_GRAY"],fg=styleDict["WHITE"],borderwidth=2,font=styleDict["DEFAULT_FONT_STYLE"],height=2)
        conversionModeMenu.grid(row=1,column=3,columnspan=1,padx=5,pady=5,stick=tk.NSEW,rowspan=1)
        self.converstionButtons.append(conversionModeMenu)

    def closeChecker(self,event):
        conversion_mode = self.conversionModeVar.get()
        if conversion_mode == "Close":
            self.leaveConversionMode()
    
    def swtichForUnitConv(self,input):
        if self.conversionModeVar.get() == "Length":
            index = self.lengthConversionNames.index(input)
            return self.lengthConversionValues[index]
        
        if self.conversionModeVar.get() == "Area":
            index = self.areaConversionNames.index(input)
            return self.areaConversionValues[index]
        
        if self.conversionModeVar.get() == "Volume":
            index = self.volumeConversionNames.index(input)
            return self.volumeConversionValues[index]


    """
    self.totalExpression = ""
        print(self.currentExpression)
        #scientific notation currently enabled
        if len(self.currentExpression) >= 10 and float(self.currentExpression) >= 1000000000 and self.currentExpression != "Syntax Error" and self.currentExpression != "Variables Error" and self.currentExpression != "Overflow Error" and self.currentExpression != "Zero Division Error":
            self.currentExpression = "{:.10e}".format(float(self.currentExpression))
        self.update_label()
        self.update_total_label()"""

    def unitConversion(self):
        if self.conversionModeVar.get() == "Length":
            print(self.swtichForUnitConv(self.inputModeVar.get()),self.swtichForUnitConv(self.outputModeVar.get()),int(self.currentExpression),False)
            self.currentExpression = UC.unit_convert.length(self.swtichForUnitConv(self.inputModeVar.get()),(self.swtichForUnitConv(self.outputModeVar.get())),float(self.currentExpression),False)
            self.totalExpression = ""
            self.update_label()
            self.update_total_label()
            self.currentExpression = ""

        elif self.conversionModeVar.get() == "Area":
            self.currentExpression = UC.unit_convert.area(self.swtichForUnitConv(self.inputModeVar.get()),self.swtichForUnitConv(self.outputModeVar.get()),float(self.currentExpression),False)
            self.totalExpression = ""
            self.update_label()
            self.update_total_label()
            self.currentExpression = ""
        
        elif self.conversionModeVar.get() == "Volume":
            self.currentExpression = UC.unit_convert.valume(self.swtichForUnitConv(self.inputModeVar.get()),self.swtichForUnitConv(self.outputModeVar.get()),float(self.currentExpression),False)
            self.totalExpression = ""
            self.update_label()
            self.update_total_label()
            self.currentExpression = ""


    def leaveConversionMode(self):
        for item in self.converstionButtons:
            item.destroy()

    def goToBaseN(self):
        pass

    def goTo2DGraphing(self):
        self.window.destroy()
        #start ready state here
        

    def bindKeys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        self.window.bind("<BackSpace>", lambda event: self.deleteButtonAction())
        self.window.bind("<Delete>", lambda event: self.clear())
        self.window.bind("(", lambda event: self.addLeftBracket())
        self.window.bind(")", lambda event: self.addRightBracket())
        self.window.bind("^",lambda event, operator="^": self.addOperator(operator))

        
    
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.addToCurrentExpression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.addOperator(operator))

        self.window.bind("!", lambda event, operator=key: self.factorialize())

        for letter in self.capitalLetters:
            self.window.bind(letter, lambda event, operator=letter: self.addOperator(operator))
        
        for letter in self.lowerCaseletters:
            self.window.bind(letter, lambda event, operator=letter: self.addOperator(operator))
    
    #frame functions here
    def createDisplayFrame(self):
        frame = tk.Frame(self.window,height=221, bg=styleDict["LIGHT_GRAY"])
        frame.pack(expand=True, fill="both",pady=50,side="top")
        return frame
    
    def createButtonsFrame(self):
        frame = tk.Frame(self.window)
        frame.config(bg=styleDict["MS_BACKGROUND_GREY"])
        frame.pack(expand=True,fill="both",side="right")
        return frame
    

    #all the important labels are created here
    def createDisplayLabels(self):
        totalExpressionLabel = tk.Label(self.displayFrame,text=self.totalExpression,anchor=tk.E, bg=styleDict["MS_BACKGROUND_GREY"],fg=styleDict["WHITE"],padx=24,font=styleDict["SMALL_FONT_STYLE"])
        totalExpressionLabel.pack(expand=True,fill="both")

        currentExpressionLabel = tk.Label(self.displayFrame,text=self.currentExpression,anchor=tk.E, bg=styleDict["MS_BACKGROUND_GREY"],fg=styleDict["WHITE"],padx=24,font=styleDict["LARGE_FONT_STYLE"])
        currentExpressionLabel.pack(expand=True,fill="both")

        return totalExpressionLabel,currentExpressionLabel
    
    #label updaters
    def update_total_label(self):
        expression = self.totalExpression
        for operator,symbol in self.operations.items():
            expression = expression.replace(operator, f" {symbol} ")
        self.totalExpressionLabel.config(text=expression)
        print(f"Updated total label: {expression}")

    
    def update_label(self):
        self.currentExpressionLabel.config(text=self.currentExpression)

    def addToCurrentExpression(self,inputVal):
        self.currentExpression += str(inputVal)
        self.update_label()
     
    def switchExtraOperations(self):
        expression = self.totalExpression
        for operator,symbol in self.extraOperations.items():
            expression = expression.replace(operator, f"{symbol}")

        #commented out for experimental reasons
        #for operator,symbol in self.numericPowers.items():
            #expression = expression.replace(operator, f"{symbol}")
        self.totalExpressionLabel.config(text=expression)
        self.totalExpression = expression
        print(f"Updated total with swtiched operations: {expression}")
    
    def switchExponents(self):
        expression = self.totalExpression
        for operator,symbol in self.extraOperations.items():
            expression = expression.replace(operator, f"{symbol}")
        self.totalExpressionLabel.config(text=expression)
        self.totalExpression = expression
        print(f"Updated total with swtiched operations (EXPONENTS ONLY): {expression}")

    def addOperator(self,operator):
        self.currentExpression += str(operator)
        self.totalExpression += self.currentExpression
        self.currentExpression = ""
        self.update_total_label()
        self.update_label()
    
    def deleteButtonAction(self):
        if len(self.currentExpression) != 0:
            tempExpression = self.currentExpression[:len(self.currentExpression) - 1]
            self.currentExpression = tempExpression
            self.update_label()
        else:
            tempExpression = self.totalExpression[:len(self.totalExpression) - 1]
            self.totalExpression = tempExpression
            self.update_total_label()

    def addOperatorExponent(self,operator):
        self.currentExpression += str(operator)
        self.totalExpression += self.currentExpression
        self.currentExpression = ""
        self.switchExponents()
        self.update_total_label()
        #self.update_label()
    
    def addLeftBracket(self):
        self.currentExpression += str("(")
        self.totalExpression += self.currentExpression
        self.currentExpression = ""
        self.bracketsList.append("(")
        self.update_total_label()
        self.update_label()
    
    def addRightBracket(self):
        if len(self.bracketsList) != 0:
            self.currentExpression += str(")")
            self.totalExpression += self.currentExpression
            self.currentExpression = ""
            self.bracketsList.pop()
            self.update_total_label()
            self.update_label()
    
    #function to clear screen
    def clear(self):
        self.currentExpression = ""
        self.totalExpression = ""
        self.update_label()
        self.update_total_label()
        self.FixButtonSize()
        #self.window.unbind("=")
        #self.window.bind("<Return>", lambda event: self.evaluate())
        #self.equals_button.config(command=self.evaluate)

        self.window.geometry(f"{self.width}x{self.height}")
        for key in self.temp:
            try:
                self.temp[key].destroy()
            except:
                self.temp[key].get_tk_widget().destroy()

        if self.canvas_frame != None:
            self.canvas_frame.pack_forget()
        

    #function to evalute string
    def evaluate(self):
        self.totalExpression += self.currentExpression
        print(f"This is total expression: {self.totalExpression}")
        self.switchExtraOperations()
        self.switchExponents()
        self.update_total_label()
        self.totalExpression = self.totalExpression.replace("^","**")
        print(f"Expression going to CALC: {self.totalExpression}")
        self.currentExpression = CALC.evaluateWithParsing(self.totalExpression)
        self.totalExpression = ""
        print(self.currentExpression)
        #scientific notation currently enabled
        if len(self.currentExpression) >= 10 and float(self.currentExpression) >= 1000000000 and self.currentExpression != "Syntax Error" and self.currentExpression != "Variables Error" and self.currentExpression != "Overflow Error" and self.currentExpression != "Zero Division Error":
            self.currentExpression = "{:.10e}".format(float(self.currentExpression))
        self.update_label()
        self.update_total_label()

    """def square(self):
        self.currentExpression += str("²")
        self.totalExpression += self.currentExpression
        self.currentExpression = ""
        self.update_total_label()
        self.update_label()
        #if self.currentExpression != "":
            #self.currentExpression = CALC.evaluateWithParsing(f"({self.currentExpression})**2")
            #self.update_label()"""

    
    def factorialize(self):
        firstIteration = CALC.evaluateWithParsing(f"{self.currentExpression}")
        print(firstIteration)
        self.currentExpression = CALC.evaluateWithParsing(f"factorial({firstIteration})")
        #scientific notation currently enabled
        if len(self.currentExpression) >= 10 and float(self.currentExpression) >= 1000000000 and self.currentExpression != "Syntax Error" and self.currentExpression != "Variables Error" and self.currentExpression != "Overflow Error" and self.currentExpression != "Zero Division Error":
            self.currentExpression = "{:.10e}".format(float(self.currentExpression))
        self.update_label()
    
    def addOperatorWithBrackets(self,operator):
        self.currentExpression += str(operator)
        self.totalExpression += self.currentExpression
        self.currentExpression = ""
        self.bracketsList.append("(")
        self.update_total_label()
        self.update_label()
    
    def addOperatorTrigonometric(self,operator):
        if self.isRad == True:
            self.currentExpression += str(operator)
            self.totalExpression += self.currentExpression
            self.currentExpression = ""
            self.bracketsList.append("(")
            self.update_total_label()
            self.update_label()

        if self.isRad == False:
            self.currentExpression += f"{operator}radians("
            self.totalExpression += self.currentExpression
            self.currentExpression = ""
            self.bracketsList.append("(")
            self.bracketsList.append("(")
            self.update_total_label()
            self.update_label()

        #if self.currentExpression != "":
            #self.currentExpression = CALC.evaluateWithParsing(f"({self.currentExpression})**0.5")
            #self.update_label()

    #button functions are here
    def createDigitButtons(self):
        for digit, gridLocation in self.digits.items():
            button = tk.Button(self.buttonsFrame,text=str(digit),bg = styleDict["MS_LIGHT_GRAY"], fg=styleDict["WHITE"],borderwidth=2,font=styleDict["DIGIT_FONT_STYLE"], command=lambda x=digit: self.addToCurrentExpression(x))
            button.grid(row=gridLocation[0], column=gridLocation[1], sticky=tk.NSEW,columnspan=1,padx=2,pady=2)
        
    def createOperatorButtons(self):
        counterVar = 4
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttonsFrame, text=symbol,fg=styleDict["OFF_WHITE"],bg=styleDict["MS_DARK_GRAY"],font=styleDict["DEFAULT_FONT_STYLE"],borderwidth=2, command= lambda x=operator: self.addOperator(x))
            button.grid(row=counterVar, column=5,stick=tk.NSEW,columnspan=1,padx=2,pady=2)
            counterVar+=1

        #creating plus-minus button
        button = tk.Button(self.buttonsFrame,text="\u00b1",bg = styleDict["MS_LIGHT_GRAY"], fg=styleDict["WHITE"],borderwidth=2,font=styleDict["DIGIT_FONT_STYLE"], command=lambda x="-": self.addToCurrentExpression(x))
        button.grid(row=8, column=2, sticky=tk.NSEW,columnspan=1,padx=2,pady=2)
        
    def createClearButton(self):
        button = tk.Button(self.buttonsFrame, text="C",fg=styleDict["WHITE"],bg=styleDict["MS_DARK_GRAY"],font=styleDict["DEFAULT_FONT_STYLE"], command= self.clear,borderwidth=2)
        button.grid(row=3, column=4,stick=tk.NSEW,columnspan=1,padx=2,pady=2)
    
    def createDeleteButton(self):
        button = tk.Button(self.buttonsFrame, text="⌫",fg=styleDict["WHITE"],bg=styleDict["MS_DARK_GRAY"],font=styleDict["DEFAULT_FONT_STYLE"],borderwidth=2, command=self.deleteButtonAction)
        button.grid(row=3, column=5,stick=tk.NSEW,columnspan=1,padx=2,pady=2)
    
    def createReciprocoralButton(self):
        button = tk.Button(self.buttonsFrame, text="1/𝒙",fg=styleDict["WHITE"],bg=styleDict["MS_DARK_GRAY"],font=styleDict["DEFAULT_FONT_STYLE"],borderwidth=2,command=lambda x="1/(": self.addOperatorWithBrackets(x))
        button.grid(row=3, column=2,stick=tk.NSEW,columnspan=1,padx=2,pady=2)
    
    def createFactorialButton(self):
        button = tk.Button(self.buttonsFrame, text="𝒏!",fg=styleDict["WHITE"],bg=styleDict["MS_DARK_GRAY"],font=styleDict["DEFAULT_FONT_STYLE"],borderwidth=2,command=self.factorialize)
        button.grid(row=4, column=4,stick=tk.NSEW,columnspan=1,padx=2,pady=2)
    
    def createAbsoluteButton(self):
        button = tk.Button(self.buttonsFrame, text="|𝒙|",fg=styleDict["WHITE"],bg=styleDict["MS_DARK_GRAY"],font=styleDict["DEFAULT_FONT_STYLE"],borderwidth=2,command=lambda x="|": self.addOperator(x))
        button.grid(row=3, column=3,stick=tk.NSEW,columnspan=1,padx=2,pady=2)
    
    def createInverseButton(self):
        button = tk.Button(self.buttonsFrame, text="REG",fg=styleDict["WHITE"],bg=styleDict["MS_DARK_GRAY"],font=styleDict["DEFAULT_FONT_STYLE"],borderwidth=2)
        button.config(command=lambda x=button: self.inverseButtonBehaviour(x))
        button.grid(row=3, column=1,stick=tk.NSEW,columnspan=1,padx=2,pady=2)

    def createWordButtons(self):
        commands = [self.createTriButtons, self.createHypButtons, self.graphingMode, self.createConstantButtons, self.radButtonBehaviour]
        counterVar = 1
        for word in self.wordButtons:
            button = tk.Button(self.buttonsFrame, text=word,fg=styleDict["WHITE"],bg=styleDict["MS_DARK_GRAY"],font=styleDict["DEFAULT_FONT_STYLE"],borderwidth=2,command=commands[counterVar - 1])
            button.grid(row=2, column=counterVar,stick=tk.NSEW,columnspan=1,padx=2,pady=2)
            counterVar+=1
            if word == "RAD":
                break
        radButton = tk.Button(self.buttonsFrame, text=word,fg=styleDict["WHITE"],bg=styleDict["MS_DARK_GRAY"],font=styleDict["DEFAULT_FONT_STYLE"],borderwidth=2)
        radButton.config(command=lambda x=radButton: self.radButtonBehaviour(x))
        radButton.grid(row=2, column=5,stick=tk.NSEW,columnspan=1,padx=2,pady=2)
    
    def createBracketButtons(self):
        #left bracket
        button = tk.Button(self.buttonsFrame, text="(",fg=styleDict["WHITE"],bg=styleDict["MS_DARK_GRAY"],font=styleDict["DEFAULT_FONT_STYLE"],borderwidth=2,command=self.addLeftBracket)
        button.grid(row=4, column=2,stick=tk.NSEW,columnspan=1,padx=2,pady=2)

        #right bracket
        button = tk.Button(self.buttonsFrame, text=")",fg=styleDict["WHITE"],bg=styleDict["MS_DARK_GRAY"],font=styleDict["DEFAULT_FONT_STYLE"],borderwidth=2,command=self.addRightBracket)
        button.grid(row=4, column=3,stick=tk.NSEW,columnspan=1,padx=2,pady=2)

    def createLogButtons(self):
        counterVar = 7
        ops = ["log(","ln("]
        secondCounter = 0
        for word in self.logExpoButtons:
            button = tk.Button(self.buttonsFrame, text=word,fg=styleDict["WHITE"],bg=styleDict["MS_DARK_GRAY"],font=styleDict["DEFAULT_FONT_STYLE"],borderwidth=2,command = lambda x=ops[secondCounter]: self.addOperatorWithBrackets(x))
            button.grid(row=counterVar, column=1,stick=tk.NSEW,columnspan=1,padx=2,pady=2)
            counterVar+=1
            secondCounter+=1
    
    def createExpoButton(self):
        button = tk.Button(self.buttonsFrame, text="𝒙ʸ",fg=styleDict["WHITE"],bg=styleDict["MS_DARK_GRAY"],font=styleDict["DEFAULT_FONT_STYLE"],borderwidth=2,command=lambda x="^": self.addOperatorExponent(x))
        button.grid(row=6, column=1,stick=tk.NSEW,columnspan=1,padx=2,pady=2)

    def createSquareButton(self):
        button = tk.Button(self.buttonsFrame, text="𝒙\u00b2",fg=styleDict["WHITE"],bg=styleDict["MS_DARK_GRAY"],font=styleDict["DEFAULT_FONT_STYLE"], command= lambda x="²": self.addOperator(x),borderwidth=2)
        button.grid(row=4, column=1,stick=tk.NSEW,columnspan=1,padx=2,pady=2)
    
    def createSquareRootButton(self):
        button = tk.Button(self.buttonsFrame, text="\u221a𝒙",fg=styleDict["WHITE"],bg=styleDict["MS_DARK_GRAY"],font=styleDict["DEFAULT_FONT_STYLE"], command= lambda x="√(": self.addOperatorWithBrackets(x),borderwidth=2)
        button.grid(row=5, column=1,stick=tk.NSEW,columnspan=1,padx=2,pady=2)

    def createConstantButtons(self):
        if self.constantExist == False:
            counterVar = 0
            self.width *= 2
            self.window.geometry(f"{self.width}x{self.height}")
            self.FixButtonSize(12)
            for rowN in range(2,9):
                for columnN in range(6,12):
                    try:
                        print(f"row: {rowN} | column: {columnN}")
                        button = tk.Button(self.buttonsFrame, text=self.scientificConstantsList[counterVar],fg=styleDict["WHITE"],bg=styleDict["MS_DARK_GRAY"],font=styleDict["DEFAULT_FONT_STYLE"],borderwidth=2,command=lambda x=f"{self.scientificConstants[self.scientificConstantsList[counterVar]]}": self.addToCurrentExpression(x))
                        button.grid(row=rowN, column=columnN,stick=tk.NSEW,columnspan=1,padx=2,pady=2)
                        self.constantButtons.append(button)
                        counterVar+=1
                    except:
                        button = tk.Button(self.buttonsFrame,text="Close",fg=styleDict["WHITE"],bg=styleDict["MS_DARK_GRAY"],font=styleDict["DEFAULT_FONT_STYLE"],borderwidth=2,command=self.destroyConstantButtons)
                        button.grid(row=rowN, column=columnN,stick=tk.NSEW,columnspan=1,padx=2,pady=2)
                        self.constantButtons.append(button)
                        counterVar+=1
                        break

            button = tk.Button(self.buttonsFrame,fg=styleDict["WHITE"],bg=styleDict["MS_DARK_GRAY"],font=styleDict["DEFAULT_FONT_STYLE"],borderwidth=2,state=tk.DISABLED)
            button.grid(row=8, column=11,stick=tk.NSEW,columnspan=1,padx=2,pady=2)
            self.constantButtons.append(button)
            self.constantExist = True
            if self.triExists == True:
                for columnVar in range(5,12):
                    blankButton = tk.Button(self.buttonsFrame, fg = styleDict["WHITE"], bg=styleDict["MS_DARK_GRAY"], font=styleDict["DEFAULT_FONT_STYLE"], borderwidth=2,state=tk.DISABLED)
                    blankButton.grid(row=1,column=columnVar,stick=tk.NSEW,padx=2,pady=2,columnspan=1)
                    self.triButtons.append(blankButton)
            elif self.hypExists == True:
                for columnVar in range(5,12):
                    blankButton = tk.Button(self.buttonsFrame, fg = styleDict["WHITE"], bg=styleDict["MS_DARK_GRAY"], font=styleDict["DEFAULT_FONT_STYLE"], borderwidth=2,state=tk.DISABLED)
                    blankButton.grid(row=1,column=columnVar,stick=tk.NSEW,padx=2,pady=2,columnspan=1)
                    self.hypButtons.append(blankButton)

          
    def destroyConstantButtons(self):
        if self.constantExist == True:

            self.width //= 2
            self.window.geometry(f"{self.width}x{self.height}")
            for button in self.constantButtons:
                button.destroy()
            for columnNum in range(6,12):
                self.buttonsFrame.columnconfigure(columnNum,weight=0)
            self.constantExist = False
                
    def radButtonBehaviour(self,thisButton):
        self.isRad = not self.isRad
        if self.isRad == True:
            thisButton.config(text="RAD")
        if self.isRad == False:
            thisButton.config(text = "DEG")
    
    def inverseButtonBehaviour(self,thisButton):
        if self.triExists == False and self.hypExists == False:
            self.isInverse = not self.isInverse
            if self.isInverse == True:
                thisButton.config(text="INV")
            if self.isInverse == False:
                thisButton.config(text="REG")

    #This entire section is going to be dedicated to the hyp and tri menus
    def createTriButtons(self):
        if self.triExists == False and self.hypExists == False:
            closeButton = tk.Button(self.buttonsFrame, text = "Clear", fg = styleDict["WHITE"], bg=styleDict["MS_DARK_GRAY"], font=styleDict["DEFAULT_FONT_STYLE"], borderwidth=2,command = self.destroyTriButtons)
            closeButton.grid(row=1,column=4,stick=tk.NSEW,padx=2,pady=2,columnspan=1)
            self.triButtons.append(closeButton)

            blankButton = tk.Button(self.buttonsFrame, fg = styleDict["WHITE"], bg=styleDict["MS_DARK_GRAY"], font=styleDict["DEFAULT_FONT_STYLE"], borderwidth=2,state=tk.DISABLED)
            blankButton.grid(row=1,column=5,stick=tk.NSEW,padx=2,pady=2,columnspan=1)
            self.triButtons.append(blankButton)
            if self.constantExist == True:
                for columnVar in range(5,12):
                    blankButton = tk.Button(self.buttonsFrame, fg = styleDict["WHITE"], bg=styleDict["MS_DARK_GRAY"], font=styleDict["DEFAULT_FONT_STYLE"], borderwidth=2,state=tk.DISABLED)
                    blankButton.grid(row=1,column=columnVar,stick=tk.NSEW,padx=2,pady=2,columnspan=1)
                    self.triButtons.append(blankButton)

        if self.triExists == False and self.hypExists == False and self.isInverse == False:
            texts = ["sin(𝒙)", "cos(𝒙)", "tan(𝒙)"]
            names = ["sin", "cos", "tan"]
            columnVar = 1
            for funcName in texts:
                button = tk.Button(self.buttonsFrame, text = funcName, fg = styleDict["WHITE"], bg=styleDict["MS_DARK_GRAY"], font=styleDict["DEFAULT_FONT_STYLE"], borderwidth=2,command=lambda x=f"{names[texts.index(funcName)]}(": self.addOperatorTrigonometric(x))
                button.grid(row=1,column=columnVar,padx=2,pady=2,stick=tk.NSEW,columnspan=1)
                columnVar+=1
                self.triButtons.append(button)
            self.triExists = True

        elif self.triExists == False and self.hypExists == False and self.isInverse == True:
            texts = ["sin⁻¹(𝒙)", "cos⁻¹(𝒙)", "tan⁻¹(𝒙)"]
            names = ["sin", "cos", "tan"]
            columnVar = 1
            for funcName in texts:
                button = tk.Button(self.buttonsFrame, text = funcName, fg = styleDict["WHITE"], bg=styleDict["MS_DARK_GRAY"], font=styleDict["DEFAULT_FONT_STYLE"], borderwidth=2,command=lambda x=f"a{names[texts.index(funcName)]}(": self.addOperatorWithBrackets(x))
                button.grid(row=1,column=columnVar,padx=2,pady=2,stick=tk.NSEW,columnspan=1)
                columnVar+=1
                self.triButtons.append(button)
                self.triExists = True
    
    def destroyTriButtons(self):
        if self.triExists == True and self.hypExists == False:
            for function in self.triButtons:
                function.destroy()
            self.triExists = False
    
    def createHypButtons(self):
        if self.hypExists == False and self.triExists == False:
            closeButton = tk.Button(self.buttonsFrame, text = "Clear", fg = styleDict["WHITE"], bg=styleDict["MS_DARK_GRAY"], font=styleDict["DEFAULT_FONT_STYLE"], borderwidth=2,command = self.destroyHypButtons)
            closeButton.grid(row=1,column=4,stick=tk.NSEW,padx=2,pady=2,columnspan=1)
            self.hypButtons.append(closeButton)

            blankButton = tk.Button(self.buttonsFrame, fg = styleDict["WHITE"], bg=styleDict["MS_DARK_GRAY"], font=styleDict["DEFAULT_FONT_STYLE"], borderwidth=2,state=tk.DISABLED)
            blankButton.grid(row=1,column=5,stick=tk.NSEW,padx=2,pady=2,columnspan=1)
            self.hypButtons.append(blankButton)
            if self.constantExist == True:
                for columnVar in range(5,12):
                    blankButton = tk.Button(self.buttonsFrame, fg = styleDict["WHITE"], bg=styleDict["MS_DARK_GRAY"], font=styleDict["DEFAULT_FONT_STYLE"], borderwidth=2,state=tk.DISABLED)
                    blankButton.grid(row=1,column=columnVar,stick=tk.NSEW,padx=2,pady=2,columnspan=1)
                    self.hypButtons.append(blankButton)

        if self.hypExists == False and self.triExists == False and self.isInverse == False:
            texts = ["sinh(𝒙)", "cosh(𝒙)", "tanh(𝒙)"]
            names = ["sinh","cosh","tanh"]
            columnVar = 1
            for funcName in texts:
                button = tk.Button(self.buttonsFrame, text = funcName, fg = styleDict["WHITE"], bg=styleDict["MS_DARK_GRAY"], font=styleDict["DEFAULT_FONT_STYLE"], borderwidth=2,command=lambda x=f"{names[texts.index(funcName)]}(": self.addOperatorWithBrackets(x))
                button.grid(row=1,column=columnVar,padx=2,pady=2,stick=tk.NSEW,columnspan=1)
                columnVar+=1
                self.hypButtons.append(button)
                self.hypExists = True
        elif self.hypExists == False and self.triExists == False and self.isInverse == True:
            texts = ["sinh⁻¹(𝒙)", "cosh⁻¹(𝒙)", "tanh⁻¹(𝒙)"]
            names = ["sinh","cosh","tanh"]
            columnVar = 1
            for funcName in texts:
                button = tk.Button(self.buttonsFrame, text = funcName, fg = styleDict["WHITE"], bg=styleDict["MS_DARK_GRAY"], font=styleDict["DEFAULT_FONT_STYLE"], borderwidth=2,command=lambda x=f"a{names[texts.index(funcName)]}(": self.addOperatorWithBrackets(x))
                button.grid(row=1,column=columnVar,padx=2,pady=2,stick=tk.NSEW,columnspan=1)
                columnVar+=1
                self.hypButtons.append(button)
                self.hypExists = True
    
    def destroyHypButtons(self):
        if self.hypExists == True:
            for function in self.hypButtons:
                function.destroy()
            self.hypExists = False

    def createEqualsButton(self):
        button = tk.Button(self.buttonsFrame, text="=",fg=styleDict["WHITE"],bg=styleDict["MS_LIGHT_BLUE"],font=styleDict["DEFAULT_FONT_STYLE"],command=self.evaluate,borderwidth=2)
        button.grid(row=8, column=5,stick=tk.NSEW,columnspan=1,padx=2,pady=2)
        return button

    #running functions here
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calcObj = Calculator()
    calcObj.run()