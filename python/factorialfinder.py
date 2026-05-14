import random
import sys

## variable num is the number selected by user
## variable fact is the factorial of variable num
## "{len(str(fact))}" is the amount of digits in variable fact

raw = input("Enter any number: ")

# debug mode
if raw.startswith("debug "):
    num = int(raw.split(" ")[1])

    if num < 0:
        print("Negative factorial is NOT this universe's problem..")
        sys.exit()

    fact = 1
    for i in range(1, num + 1):
        fact *= i

    print(f"{fact}")
    sys.exit()

num = int(raw)

if num < 0:
    print("Negative factorial is NOT this universe's problem..")
    sys.exit()

fact = 1
for i in range(1, num + 1):
    fact *= i

no = [
    "What will you even use this for?",
    "Do you really think this is necessary?",
    "This is way overkill, but okay.",
    "Why are you like this?",
    "Your CPU will kill itself if I revealed this to you",
    "why tho",
    "bro??",
    "???",
    "Explain.",
    "Explain yourself."
]

if num == 1337:
    print("Factorial of {num} = Elite")
    sys.exit()

if num > 100:
    roll = random.random()

    if roll < 0.05:
        print(f"Wow, you're pretty unlucky. Your PC is gonna kill itself, maybe help it after this or turn it off? Factorial of {num} = {fact}")
    elif roll < 0.25:
        print(f"WHY? Factorial of {num} has {len(str(fact))} digits, if you need it somehow.")
    else:
        print(random.choice(no))
else:
    print(f"Factorial of {num} = {fact}")