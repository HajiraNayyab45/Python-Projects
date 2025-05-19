
import tkinter as tk
import random

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("600x550")
        self.root.configure(bg="#f8f9fa")

        self.words_with_hints = [
            ("python", "A popular programming language."),
            ("hangman", "A classic word guessing game."),
            ("developer", "Someone who writes code."),
            ("rainbow", "Appears after it rains."),
            ("challenge", "Something difficult that tests you.")
        ]
        self.word_to_guess, self.hint = random.choice(self.words_with_hints)
        self.guessed_word = ["_"] * len(self.word_to_guess)
        self.guessed_letters = set()
        self.max_attempts = 6
        self.attempts = 0

        # Canvas Frame
        self.canvas = tk.Canvas(self.root, width=250, height=250, bg="white", bd=2, relief="groove")
        self.canvas.pack(pady=20)

        # Word display
        self.word_label = tk.Label(self.root, text=" ".join(self.guessed_word),
                                   font=("Helvetica", 24, "bold"), bg="#f8f9fa", fg="#343a40")
        self.word_label.pack(pady=5)

        # Hint
        self.hint_label = tk.Label(self.root, text=f"💡 Hint: {self.hint}",
                                   font=("Helvetica", 13), bg="#f8f9fa", fg="#6c757d")
        self.hint_label.pack()

        # Attempts
        self.attempts_label = tk.Label(self.root, text=f"❌ Incorrect guesses: {self.attempts} / {self.max_attempts}",
                                       font=("Helvetica", 13), bg="#f8f9fa", fg="red")
        self.attempts_label.pack(pady=5)

        # Guessed letters
        self.guessed_label = tk.Label(self.root, text="🔠 Guessed Letters: ",
                                      font=("Helvetica", 12), bg="#f8f9fa")
        self.guessed_label.pack()

        # Input section
        input_frame = tk.Frame(self.root, bg="#f8f9fa")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Enter a letter:", font=("Helvetica", 14), bg="#f8f9fa").pack(side=tk.LEFT)
        self.letter_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=3)
        self.letter_entry.pack(side=tk.LEFT, padx=5)

        self.submit_button = tk.Button(self.root, text="✅ Submit", command=self.check_guess,
                                       font=("Helvetica", 13), bg="#0d6efd", fg="white", width=12)
        self.submit_button.pack(pady=8)

        # Message label
        self.message_label = tk.Label(self.root, text="", font=("Helvetica", 14), bg="#f8f9fa")
        self.message_label.pack()

        # Exit button
        self.exit_button = tk.Button(self.root, text="🚪 Exit Game", command=self.root.quit,
                                     font=("Helvetica", 12), bg="#dc3545", fg="white", width=12)
        self.exit_button.pack(pady=10)

        self.draw_hangman()

    def draw_hangman(self):
        self.canvas.delete("all")
        # Gallows
        self.canvas.create_line(20, 230, 180, 230)       # Base
        self.canvas.create_line(100, 230, 100, 50)       # Pole
        self.canvas.create_line(100, 50, 180, 50)        # Top bar
        self.canvas.create_line(180, 50, 180, 80)        # Rope

        # Body parts
        if self.attempts >= 1:
            self.canvas.create_oval(160, 80, 200, 120)   # Head
        if self.attempts >= 2:
            self.canvas.create_line(180, 120, 180, 170)  # Body
        if self.attempts >= 3:
            self.canvas.create_line(180, 130, 150, 150)  # Left arm
        if self.attempts >= 4:
            self.canvas.create_line(180, 130, 210, 150)  # Right arm
        if self.attempts >= 5:
            self.canvas.create_line(180, 170, 150, 200)  # Left leg
        if self.attempts >= 6:
            self.canvas.create_line(180, 170, 210, 200)  # Right leg

    def check_guess(self):
        guess = self.letter_entry.get().lower()
        self.letter_entry.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            self.message_label.config(text="⚠️ Please enter a single valid letter.")
            return

        if guess in self.guessed_letters:
            self.message_label.config(text="⛔ You already guessed that letter.")
            return

        self.guessed_letters.add(guess)
        self.guessed_label.config(text="🔠 Guessed Letters: " + ", ".join(sorted(self.guessed_letters)))

        if guess in self.word_to_guess:
            for i, letter in enumerate(self.word_to_guess):
                if letter == guess:
                    self.guessed_word[i] = guess
            self.word_label.config(text=" ".join(self.guessed_word))
            self.message_label.config(text="✅ Correct guess!")

            if "_" not in self.guessed_word:
                self.message_label.config(text="🎉 You won! Well done.")
                self.submit_button.config(state=tk.DISABLED)
        else:
            self.attempts += 1
            self.message_label.config(text="❌ Incorrect guess!")
            self.attempts_label.config(text=f"❌ Incorrect guesses: {self.attempts} / {self.max_attempts}")
            self.draw_hangman()

            if self.attempts >= self.max_attempts:
                self.message_label.config(text=f"💀 Game Over! The word was: {self.word_to_guess}")
                self.submit_button.config(state=tk.DISABLED)

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
