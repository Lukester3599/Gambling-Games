import tkinter as tk
import random
import threading
import time

# GamblingGame is the main window for the gambling game GUI
class GamblingGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gambling Game")  # Set window title
        self.geometry("400x300")     # Set window size
        self.money = 1000            # Player's starting money
        self.bet = 0                 # Current bet amount
        self.number = 0              # The number to guess
        self.create_widgets()        # Set up all GUI widgets
        self.update_money_display()  # Show starting money

    def create_widgets(self):
        # Label to display current money
        self.money_label = tk.Label(self, text="", font=("Arial", 16))
        self.money_label.pack(pady=10)

        # Entry and button for placing a bet
        self.bet_label = tk.Label(self, text="Place your bet:")
        self.bet_label.pack()
        self.bet_entry = tk.Entry(self)
        self.bet_entry.pack()
        self.bet_entry.bind('<Return>', self.on_bet_entry_return)  # Dedicated handler for Enter key
        self.bet_button = tk.Button(self, text="Place Bet", command=self.place_bet)
        self.bet_button.pack(pady=5)

        # Entry and button for making a guess (hidden until bet is placed)
        self.guess_label = tk.Label(self, text="Your guess (1-10):")
        self.guess_entry = tk.Entry(self)
        self.guess_entry.bind('<Return>', self.on_guess_entry_return)  # Dedicated handler for Enter key
        self.guess_button = tk.Button(self, text="Guess", command=self.make_guess)
        self.guess_label.pack_forget()
        self.guess_entry.pack_forget()
        self.guess_button.pack_forget()

        # Label to show results and messages
        self.result_label = tk.Label(self, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        # Label for the rolling animation
        self.animation_label = tk.Label(self, text="", font=("Arial", 20))
        self.animation_label.pack(pady=10)

    def update_money_display(self):
        # Update the money display label
        self.money_label.config(text=f"Money: ${self.money}")

    def place_bet(self):
        # Called when the user clicks 'Place Bet'
        try:
            bet = int(self.bet_entry.get())
        except ValueError:
            self.result_label.config(text="Enter a valid number for your bet!")
            return
        if bet <= 0:
            self.result_label.config(text="Bet must be positive!")
            return
        if bet > self.money:
            self.result_label.config(text="You cannot bet more than you have!")
            return
        self.bet = bet
        self.money -= bet
        self.update_money_display()
        self.result_label.config(text="Bet placed! Now guess the number.")
        self.bet_entry.delete(0, tk.END)
        self.bet_button.config(state=tk.DISABLED)
        self.show_guess_widgets()
        self.number = random.randint(1, 10)  # Random number to guess
        self.animation_label.config(text="?")
        self.guess_entry.focus_set()  # Move focus to guess entry

    def show_guess_widgets(self):
        # Show guess entry and button
        self.guess_label.pack()
        self.guess_entry.pack()
        self.guess_button.pack()

    def hide_guess_widgets(self):
        # Hide guess entry and button
        self.guess_label.pack_forget()
        self.guess_entry.pack_forget()
        self.guess_button.pack_forget()

    def make_guess(self):
        # Called when the user clicks 'Guess'
        try:
            guess = int(self.guess_entry.get())
        except ValueError:
            self.result_label.config(text="Enter a valid number for your guess!")
            return
        if not (1 <= guess <= 10):
            self.result_label.config(text="Guess must be between 1 and 10!")
            return
        self.guess_entry.delete(0, tk.END)
        self.hide_guess_widgets()
        # Start the rolling animation in a separate thread
        threading.Thread(target=self.roll_animation, args=(guess,)).start()

    def roll_animation(self, guess):
        # Show a rolling animation before revealing the number
        for _ in range(10):
            n = random.randint(1, 10)
            self.animation_label.config(text=str(n))
            time.sleep(0.1)
        self.animation_label.config(text=str(self.number))
        # After animation, show the result
        self.after(100, lambda: self.show_result(guess))

    def show_result(self, guess):
        # Show win/loss message and update money
        if guess == self.number:
            winnings = self.bet * 2
            self.money += winnings
            self.result_label.config(text=f"Congratulations! You won ${winnings}!")
        else:
            self.result_label.config(text=f"You lost! The number was {self.number}. You now have ${self.money}.")
        self.update_money_display()
        self.bet_button.config(state=tk.NORMAL)
        if self.money == 0:
            self.result_label.config(text="You have run out of money. Game over!")
            self.bet_button.config(state=tk.DISABLED)
        self.animation_label.config(text="")
        self.bet_entry.focus_set()  # Focus back to bet entry after result

    def on_bet_entry_return(self, event):
        # Only trigger place_bet if focus is on bet_entry
        if event.widget == self.bet_entry:
            self.place_bet()
            return "break"  # Prevent further propagation

    def on_guess_entry_return(self, event):
        # Only trigger make_guess if focus is on guess_entry
        if event.widget == self.guess_entry:
            self.make_guess()
            return "break"  # Prevent further propagation

# Start the game if this file is run directly
if __name__ == "__main__":
    app = GamblingGame()
    app.mainloop()
