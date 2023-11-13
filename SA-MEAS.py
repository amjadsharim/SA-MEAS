import tkinter as tk
# from tkinter import ttk
from tkinter import scrolledtext
import sympy
import pyttsx3
import speech_recognition as sr
import re
# Initialize the speech recognition object
r = sr.Recognizer()
# Initialize the text-to-speech engin
engine = pyttsx3.init()


# Function to convert the equation to sympy form i.e. 2*x**2+x*1 etc-
def convert_equation_sympy(input_equation):
    # get the input from entry widgets
    input_equation = entry.get().strip()  # Remove leading and trailing spaces
    
    # Identify the distinct variables used in the equation
    variables_set = set(filter(str.isalpha, input_equation))
    variables = "".join(variables_set)

    # Split the equation using regular expression to capture '+', '-', and '='
    terms = re.split(r'([-+=]=?)', input_equation.replace(" ", ""))
    # Remove empty strings and trim spaces
    terms = [term.strip() for term in terms if term.strip()]
    
    output_equation = []

    for term in terms:
        # Check if there is a variable with any power
        if any(f'{var}^' in term for var in variables):
            for var in variables:
                if f'{var}^' in term:
                    # Check if there is a constant along with variable^power
                    power_index = term.find(f'{var}^') + len(f'{var}^')
                    power_str = ''
                    while power_index < len(term) and term[power_index].isdigit():
                        power_str += term[power_index]
                        power_index += 1
                    
                    if power_str and (power_index >= len(term) or term[power_index] != '*'):
                        power = int(power_str)
                        coefficient_str = term.replace(f'{var}^{power}', '')
                        if coefficient_str.isdigit() or (coefficient_str.startswith('-') and coefficient_str[1:].isdigit()):
                            coefficient = coefficient_str
                            output_equation.append(f'{coefficient}*{var}**{power}')
                        else:
                            output_equation.append(f'1*{var}**{power}')
        
        # Check if there is a variable squared
        elif any(f'{var}^2' in term for var in variables):
            for var in variables:
                if f'{var}^2' in term:
                    # Check if there is a constant along with variable^2
                    coefficient_str = term.replace(var, '').replace(f'^2', '')
                    if coefficient_str.isdigit() or (coefficient_str.startswith('-') and coefficient_str[1:].isdigit()):
                        coefficient = coefficient_str
                        output_equation.append(f'{coefficient}*{var}**2')
                    else:
                        output_equation.append(f'1*{var}**2')
        # Check if there is a variable without squared
        elif any(f'{var}' in term and '*' not in term for var in variables):
            for var in variables:
                if f'{var}' in term and '*' not in term:
                    # Check if there is a constant along with variable
                    coefficient_str = term.replace(var, '')
                    if coefficient_str.isdigit() or (coefficient_str.startswith('-') and coefficient_str[1:].isdigit()):
                        coefficient = coefficient_str
                        output_equation.append(f'{coefficient}*{var}')
                    else:
                        output_equation.append(f'1*{var}')
        else:
            output_equation.append(term)
            
    result = ' '.join(output_equation).replace('^', '**')
    return result
#----------------------------------------------------------------------------------------
# the function use to speak and anlyze the equ or expression
def analyze_and_speak_input(input_str):
    
    # get the input from the cover equ sympy function 
    input_str = convert_equation_sympy(input_equation=())
    if not input_str:
        speak_message("Please input to Analyze.")
        # Update the output_text widget with the summary
        output_text.config(state=tk.NORMAL)  # Set the widget to normal state to allow editing
        output_text.delete(1.0, tk.END)  # Clear previous content in the widget
        output_text.insert(tk.END, "Please input to Analyze")  # Insert the new summary into the widget
        output_text.config(state=tk.DISABLED)  # Disable editing of the widget to make it read-only
        # Update the display
        output_text.update_idletasks()
        # print("Please input to analyze.")
        return
    
    try:
        equation_parts = input_str.split("=")
        if len(equation_parts) == 2:
            
            # Identify the distinct variables used in the equation
            variables_set = set(filter(str.isalpha, input_str))
            var = "".join(variables_set)
            variable = sympy.symbols(var)
            # If there is more than one variable, print a message and return
            if len(variables_set) > 1:
                speak_message("Equation with multiple variables are not supported for solving.")
                # Update the output_text widget with the summary
                output_text.config(state=tk.NORMAL)  # Set the widget to normal state to allow editing
                output_text.delete(1.0, tk.END)  # Clear previous content in the widget
                output_text.insert(tk.END, "Equation with multiple variables are not supported for solving.")  # Insert the new summary into the widget
                output_text.config(state=tk.DISABLED)  # Disable editing of the widget to make it read-only
                # Update the display
                output_text.update_idletasks()
                # print("Equations with multiple variables are not supported for solving.")
                return
    
            # If the equation is in the form x^2 + x + 1 = 0
            lhs, rhs = equation_parts[0], equation_parts[1]
            # Convert the equation to a SymPy expression
            lhs_expr = sympy.sympify(lhs)
            rhs_expr = sympy.sympify(rhs)
            
            # Create the equation expression
            expr = lhs_expr - rhs_expr
            
            degree = max(sympy.degree(lhs_expr, variable), sympy.degree(rhs_expr, variable))
            
            solution = sympy.solve(expr, variable)
            
            if solution:
                if degree == 0:
                    equation_type = "Constant"
                elif degree == 1:
                    equation_type = "Linear"
                elif degree == 2:
                    equation_type = "Quadratic"
                elif degree == 3:
                    equation_type = "Cubic"
                else:
                    equation_type = f"{degree}-degree"
                summary = f"Input: {entry.get().strip()} \nType: {equation_type} Equation \nSolutions: {variable} = {solution} "
                    
            else:
                summary = f"No solution found for the {equation_type.lower()} equation: {input_str}"
            
        else:
            result = sympy.sympify(input_str)
            summary = f"Expression: {entry.get().strip()}\nResult: {result}"
        
    # except (sympy.SympifyError, ValueError):
        # print(f"Invalid input: {input_str}")
        
        # to anlyze equation and expresson
        if '=' in input_str:    
            # Analyze the equation
            lhs, rhs = input_str.split('=')
            lhs_expr = sympy.sympify(lhs.strip())
            rhs_expr = sympy.sympify(rhs.strip())
        
            terms_lhs = lhs_expr.as_ordered_terms()
            terms_rhs = rhs_expr.as_ordered_terms()
        
            factors_lhs = [str(term.as_ordered_factors()) for term in terms_lhs]
            factors_rhs = [str(term.as_ordered_factors()) for term in terms_rhs]
        
            constants_lhs = [str(term) for term in terms_lhs if term.is_constant()]
            constants_rhs = [str(term) for term in terms_rhs if term.is_constant()]
            
            variables_lhs = [str(variable) for variable in lhs_expr.free_symbols]
            variables_rhs = [str(variable) for variable in rhs_expr.free_symbols]
            
            summary += "\n\nAnalysis of the Equation:\n"
            summary += "Terms     in LHS : " + ", ".join([str(term) for term in terms_lhs]) + "\n"
            summary += "Terms     in RHS : " + ", ".join([str(term) for term in terms_rhs]) + "\n"
            summary += "Factors   in LHS : " + ", ".join(factors_lhs)   + "\n"
            summary += "Factors   in RHS : " + ", ".join(factors_rhs)   + "\n"
            summary += "Constants in LHS : " + ", ".join(constants_lhs) + "\n"
            summary += "Constants in RHS : " + ", ".join(constants_rhs) + "\n"
            summary += "Variables in LHS : " + ", ".join(variables_lhs) + "\n"
            summary += "Variables in RHS : " + ", ".join(variables_rhs)
        
        else:
            # analyze the expression
            exp       = input_str
            expr      = sympy.sympify(exp.strip())
            terms     = expr.as_ordered_terms()
            factors   = [str(term.as_ordered_factors()) for term in terms]
            constants = [str(term) for term in terms if term.is_constant()]
            variables = [str(variable) for variable in expr.free_symbols]
            
            summary += "\n\nAnalysis of the Expressions:\n"
            summary += "Terms     : " + ", ".join([str(term) for term in terms]) + "\n"
            summary += "Factors   : " + ", ".join(factors) + "\n"
            summary += "Constants : " + ", ".join(constants) + "\n"
            summary += "Variables : " + ", ".join(variables)
            
        # Print the summary
        print(summary)
    
    except (sympy.SympifyError, ValueError):
        
        print(f"Invalid input: {input_str}")
        summary = f"Invalid input: {input_str}"
    
    # Update the output_text widget with the summary
    output_text.config(state=tk.NORMAL)  # Set the widget to normal state to allow editing
    output_text.delete(1.0, tk.END)  # Clear previous content in the widget
    output_text.insert(tk.END, summary)  # Insert the new summary into the widget
    output_text.config(state=tk.DISABLED)  # Disable editing of the widget to make it read-only
    # Update the display
    output_text.update_idletasks()
    # Speak the summary
    speak_message(summary)  
    
# # Example usage:
# input_equation = "x^2 + 2x = 0"
# output_equation = convert_equation_sympy(input_equation)
# analyze_and_speak_input(output_equation)
# # print("Converted Equation:", output_equation)

#-----------------------------------------------------------------------------------   
# Function to get input using speech recognition
def get_input():
    speak_message("Please Speak Expression correctly")
    
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        input_text = r.recognize_google(audio)
        entry.delete(0, tk.END)
        entry.insert(0, input_text)
        analyze_and_speak_input(input_text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service: {e}")


# Mapping characters to words for speaking
SPEAK_MAPPING = {
    '!': 'excalamtion mark',
    '$': 'dollar sign',
    '^': 'power',
    '(': 'small bracket open',
    ')': 'small bracket close',
    '-': 'minus',
    '{': 'curly brace open',
    '}': 'curly brace close',
    '[': 'square bracket open',
    ']': 'square bracket close',
    '|': 'or',
    ':': 'colon',
    ';': 'semi colon',
    '"': 'double quote',
    "'": "signle quote",
    '<': 'less than',
    '>': 'greater than',
    '?': 'quetsion mark',
    ',': 'comma',
    '.': 'dot',
    ' ': 'space',  
    'Shift_L': 'Shift left',
    'Shift_R': 'Shift right',
    'Control_L': 'Ctrl left',
    'Control_R': 'Ctrl right',
    'Alt_L': 'Alt left',
    'Alt_R': 'Alt right',
    'Caps_Lock': 'Caps Lock'    
    # Add more mappings as needed
}

# Function to speak a message
def speak_message(message):
    engine.say(message)
    engine.runAndWait()
    
# Function to handle keypress event
shift_spoken = True  # Variable to track if Shift has been spoken

def on_keypress(event):
    global shift_spoken  # Access the global variable shift_spoken
    input_char = event.keysym  # Get the pressed key directly from event.keysym
    
    # Check if the Shift key is pressed
    shift_pressed = (event.state & 1) != 0
    
    current_text = entry.get()  # Get the current text in the entry widget
    split_text = list(current_text)
    
    if input_char == 'Return':  # Check if Enter key is pressed
        speak_message('Enter')  # Speak "Enter" when Enter key is pressed
        # Handle special cases
        # Check if current_text contains any words from SPEAK_MAPPING
        matched_special_chars = [value for key, value in SPEAK_MAPPING.items() if key in current_text]
        if current_text:
            # Replace special characters with their spoken equivalents
            for key, value in SPEAK_MAPPING.items():
                current_text = current_text.replace(key, value)
            speak_message(f"The input is: {current_text}")
            speak_message(f"To Analyze press ctrl A. To clear press ctrl C.")
        else:
            speak_message("The input is: Empty")  # Speak "The input is: Empty" when input is empty
            
    elif input_char == 'BackSpace':  # Check if Backspace key is pressed
        if current_text:
            removed_char = split_text[-1]
            if removed_char in SPEAK_MAPPING:
                speak_message(f"Backspace remove: {SPEAK_MAPPING[removed_char]}")
            else:
                speak_message(f"Backspace remove: {removed_char}")
            # Remove the last character from the input text
            entry.delete(len(split_text)+1 - 1, tk.END)  # Delete the last character from the entry widget
        else:
            speak_message("Backspace remove: nothing")  # Speak "Backspace remove: nothing" when nothing to remove

    elif input_char in SPEAK_MAPPING:
        # Speak the special key name only if Shift is not already spoken
        if not shift_spoken or input_char != 'Shift_L' and input_char != 'Shift_R':
            speak_message(SPEAK_MAPPING[input_char])
            shift_spoken = True  # Set shift_spoken to True when Shift is spoken
        # If Shift is pressed, speak it only once
        if input_char.startswith('Shift') and shift_pressed:
            return
        
    elif input_char not in ['Shift_L', 'Shift_R', 'Control_L', 'Control_R']:  # Ignore Shift and Ctrl keys
        # If Shift is pressed, speak it only once
        if shift_pressed:
            speak_message('Shift')
            # Check if the input_char corresponds to a special character when Shift is pressed
            if input_char in SPEAK_MAPPING:
                input_char = SPEAK_MAPPING[input_char]
            else:
                # If not a special character, convert the input_char to uppercase
                input_char = input_char.upper()
        if input_char in SPEAK_MAPPING:
            speak_message(SPEAK_MAPPING[input_char])  # Speak the corresponding special character
        else:
            speak_message(input_char)  # Speak the pressed key if not found in the mapping



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Create the GUI
root = tk.Tk()
root.title("SA-MEAS")
root.geometry("600x500")
# root.configure(bg="aqua")  # Set the background color to light red

# Create labels, entry, and buttons using standard Tkinter widgets
label1 = tk.Label(root, text="Welcome to SA-MEAS!", font=("Arial", 14), pady=10, fg="dark blue")
label1.pack()

label2 = tk.Label(root, text="Enter an Expression or Equation", font=("Arial", 12), fg="dark blue")
label2.pack()

label3 = tk.Label(root, text="Formate: ax^2+bx+c=0 or ax+b=0", font=("Arial", 10), fg="silver")
label3.pack()

entry = tk.Entry(root, width=30, font=("Arial", 11), )
entry.pack()

# Frame to hold the buttons and pack them side by side
button_frame = tk.Frame(root)
button_frame.pack()

analyze_button = tk.Button(button_frame, text="Analyze (ctrl+A)", command=lambda: analyze_and_speak_input(entry.get()), font=("Arial", 12), bg="dark red", fg="white")
analyze_button.pack(side="left", padx=10, pady=10)

speech_button = tk.Button(button_frame, text="Speak (ctrl+s)", command=get_input, font=("Arial", 12), bg="dark blue", fg="white")
speech_button.pack(side="left", padx=10, pady=10)

label6 = tk.Label(root, text="---Guide lines---\n\nGuidelines : Ctr+G\n\nHear Input  : Enter\n\nClear Input : Ctrl+C\n\nSpeaking    : Ctrl+S\n\nAnalyze        : Ctrl+A\n\nExit         : Ctrl+E", font=("Arial", 9), padx=1, pady=0, bg="dimgrey" ,fg="snow", bd=1, relief=tk.SOLID, anchor="ne", justify=tk.LEFT)
label6.pack(side="left", fill="both", padx=10, pady=46)


label4 = tk.Label(root, text="Output Screen", font=("Arial", 14), pady=10, fg="dark blue")
label4.pack()

# Create a Text widget with a vertical scroll bar
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=14, font=("Arial", 11), bg="white", bd=1, relief=tk.SOLID)
output_text.pack()
output_text.config(state=tk.DISABLED)  # Disable editing in the ScrolledText widget

label5 = tk.Label(root, text="Note: This Interface is builf for Blind Peoples to type or speak equation or expression \n and find the solution easily with speak facility.", font=("Arial", 9), pady=10, fg="silver")
label5.pack()


# Function to exit GUI by ctrl+e
def exit_shortcut(event):
    speak_message("Exit")
    root.destroy()
# Bind Ctrl + E to the exit_shortcut function
root.bind_all("<Control-e>", exit_shortcut)

# Function to handle speak by ctrl and s
def get_input_shortcut(event):
    get_input()
# Bind Ctrl + s to the get_input_shortcut function
root.bind_all("<Control-s>", get_input_shortcut)

# Function to handle the Ctrl + A shortcut
def analyze_shortcut(event):
    analyze_and_speak_input(entry.get())
# Bind Ctrl + A to the analyze_shortcut function
root.bind_all("<Control-a>", analyze_shortcut)

# Function to clear by ctrl and c
def clear_shortcut(event):
    entry.delete(0, tk.END)  # Clear the text in the entry widget
    speak_message("The input is cleared")
# Bind the get_input_shortcut function to a specific key combination (e.g., Ctrl+C)
root.bind_all("<Control-c>", clear_shortcut)

# Function to get input (speak)
def guideline_shortcut(event):
    speak_message("Welcome to Guide lines. This interface is specially designed for blind peoples to find the solution of mathematical equations by Hearing:")
    speak_message("The interface consists of Input Box to input equation, Two buttons Analyze and Speak to Analyze and input by speak and Output text box for the output")
    speak_message("Input expression or equation by typing. type the letters and symbols with sounds")
    speak_message("Input expression or equation by Speaking. Press control and s then Speak the equation or exprsion correctly")
    speak_message("Press enter to listen the equation or expression you input")
    speak_message("Press control and A to analyze the terms, factor, constants and variables")
    speak_message("Thank you. Lets Start Now")
# Bind the get_input_shortcut function to a specific key combination (e.g., Ctrl+C)
root.bind_all("<Control-g>", guideline_shortcut)

# for key press events 
entry.bind("<KeyPress>", on_keypress)

# Set focus on the entry widget
entry.focus_set()

# Schedule the function to speak the welcome message after the GUI is fully ready
root.after(1, lambda: [root.update_idletasks(), root.after(1200, speak_message("Welcome to SA-MEAS! Please enter an expression or equation by speaking or typing. listen guidelines by pressing Ctrl and G or Exit by Ctrl and E."))])

# Set focus on the root window after the main loop
root.focus_force()

# Start the main loop
root.mainloop()




