import tkinter as tk
from tkinter import messagebox

def fibonacci_generator(n):
    """
    Generate a Fibonacci sequence of n numbers.

    :param n: Number of terms in the Fibonacci sequence
    :return: A generator yielding Fibonacci numbers
    """
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

def generate_fibonacci():
    try:
        terms = int(entry.get())
        if terms <= 0:
            raise ValueError("Number of terms must be a positive integer.")
        sequence = list(fibonacci_generator(terms))
        output_label.config(text="Fibonacci Sequence:\n" + ", ".join(map(str, sequence)))
    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))

def exit_app():
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Fibonacci Generator")
root.geometry("500x400")
root.resizable(False, False)


# Header Section
header_frame = tk.Frame(root, bg="#4CAF50", pady=10)
header_frame.pack(fill="x")
header_label = tk.Label(header_frame, text="Fibonacci Generator", font=("Arial", 24, "bold"), bg="#4CAF50", fg="white")
header_label.pack()

# Input section
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

input_label = tk.Label(input_frame, text="Enter the number of terms:", font=("Arial", 12))
input_label.grid(row=0, column=0, padx=5, pady=5)

entry = tk.Entry(input_frame, font=("Arial", 12), width=20)
entry.grid(row=0, column=1, padx=5, pady=5)


# Generate button
generate_button = tk.Button(root, text="Generate", command=generate_fibonacci , width=30)
generate_button.pack(pady=10)

# Output section
output_label = tk.Label(root, text="", font=("Arial", 12), wraplength=450, justify="left", fg="green")
output_label.pack(pady=20)

# Exit button
exit_button = tk.Button(root, text="Exit", font=("Arial", 12), command=exit_app, bg="red", fg="white", width=15 )
exit_button.pack(pady=10)

# Run the application
root.mainloop()