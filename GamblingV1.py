import random
import time

money = 1000
print(f"You have ${money} to start with.")

while money > 0:
    try:
        bet = int(input("Place your bet (0 to quit): "))
    except ValueError:
        print("You must enter a valid number!")
        continue
    if bet == 0:
        print("You chose to quit the game.")
        break
    if bet > money:
        print("You cannot bet more than you have!")
        continue
    if bet < 0:
        print("You cannot bet a negative amount!")
        continue
    money -= bet
    print(f"You placed a bet of ${bet}. You now have ${money} left.")
    print("Choosing a number between 1 and 10!")
    number = random.randint(1, 10)
    time.sleep(1)  # Pause for suspense
    print("The number has been chosen. Make your guess!")
    guess = int(input("Your guess: "))
    if guess != number:
        print()
        print(f"You lost! The number was {number}. You now have ${money}.")
    else:
        print()
        print(f"Congratulations! You won ${bet * 2}!")
        money += bet * 2
        print(f"You now have ${money}.")
    print()  # Blank line for readability

if money == 0:
    print("You have run out of money. Game over!")
