import random

x = random.randint(1, 100)
print(x)
guessed_num = int(input("Guess the number: "))

while x != guessed_num:
    if x > guessed_num:
        int(input("Guess Higher: "))
    if x < guessed_num:
        int(input("Guess Lower: "))

if x == guessed_num:
    print("You have Guessed Number")