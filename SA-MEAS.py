import tkinter as tk
import sympy
import pyttsx3
import speech_recognition as sr

# Initialize the speech recognition object
r = sr.Recognizer()

# Function to analyze expression
def analyze_expression(expr):
    try:
        # Split the equation into left-hand and right-hand sides
        lhs, rhs = expr.split('=')
        
        # Convert the left-hand and right-hand sides to SymPy expressions
        lhs_expr = sympy.sympify(lhs.strip())  # Remove leading/trailing whitespace
        rhs_expr = sympy.sympify(rhs.strip())  # Remove leading/trailing whitespace
        
        # Create an equation object
        equation = sympy.Eq(lhs_expr, rhs_expr)
        
        # Analyze the equation as needed
        # ...

        # Print the equation and its properties
        print(f"Equation: {equation}")
        # ...

    except ValueError:
        print("Invalid equation format. Please use 'left-hand side = right-hand side' format.")

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
