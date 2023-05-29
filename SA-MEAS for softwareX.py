import tkinter as tk
import sympy
import pyttsx3
import speech_recognition as sr

# Function to analyze expression
def analyze_expression(expr):
    # Convert the expression string to a SymPy expression object
    expr = sympy.sympify(expr)

    # Create a symbol for the variable in the expression
    x = sympy.symbols('x')
    
    # Get the factors of the expression
    factors = sympy.factor(expr)
    
    # Get the terms of the expression
    terms = sympy.expand(expr).args
    
    # Get the constants in the expression
    constants = [str(term) for term in terms if not term.free_symbols]
    
    # Get the variables in the expression
    variables = [str(symbol) for symbol in expr.free_symbols]
    
    # Get the type of expression
    if len(variables) == 1:
        if sympy.degree(expr) == 2:
            expr_type = 'Quadratic'
        else:
            expr_type = 'Linear'
    else:
        expr_type = 'Multivariable'
    
    # Get the solutions of the expression
    solutions = []
    if len(variables) == 1:
        solutions = sympy.solve(expr, x)
    
    # Create a string summary of the expression analysis
    summary = f"Expression: {expr}\nSummary:\nExpression Type: {expr_type}\nTotal Terms: {len(terms)}\nFactors: {[str(factor) for factor in factors.args]}\nConstants: {', '.join(constants)}\nVariables: {', '.join(variables)}\nSolutions: {', '.join([str(s) for s in solutions])}"
    
    # Print the summary
    print(summary)
    
    # Speak the summary
    engine = pyttsx3.init()
    engine.say(summary)
    engine.runAndWait()

# Function to get expression using speech recognition
def get_expression():
    with sr.Microphone() as source:
        print("Speak an expression:")
        audio = r.listen(source)
        
    try:
        expr = r.recognize_google(audio)
        entry.delete(0, tk.END)
        entry.insert(0, expr)
        analyze_expression(expr)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Create the GUI
root = tk.Tk()
root.title("SA-MEAS")
root.geometry("500x300")

# Create the input label and entry
label = tk.Label(root, text="Enter an expression:")
label.pack(pady=10)
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Create the analyze button
analyze_button = tk.Button(root, text="Analyze", command=lambda: analyze_expression(entry.get()))
analyze_button.pack(pady=10)

# Create the speech input button
speech_button = tk.Button(root, text="Speak", command=get_expression)
speech_button.pack(pady=10)

root.mainloop()
