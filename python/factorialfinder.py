import random
import sys
import time

def factorial(num):
    fact = 1
    for i in range(1, num + 1):
        fact *= i
    return fact

debug_uses = 0
reboot_done = False

while True:
    raw = input("Enter any number: ")

    # debug silent mode
    if raw.startswith("debugsilent "):
        num = int(raw.split(" ")[1])

        debug_uses += 1  # now counts toward corruption

        fact = factorial(num)
        print(fact)
        continue

    # normal debug mode
    if raw.startswith("debug "):
        num = int(raw.split(" ")[1])

        debug_uses += 1

        fact = factorial(num)

        print(f"Factorial of {num} = {fact}")

        if debug_uses == 10:
            print("File code unstable.")

        elif debug_uses == 11 and not reboot_done:
            print("Detected rising instability, promptly restarting.")
            time.sleep(0.5)

            print("Reloading factorialfinder.py")

            # small chance of failure event
            if random.random() < 0.1:
                print("Failed to compile code. Retrying...")
                time.sleep(1.5)

            time.sleep(3)
            print("factorialfinder.py successfully reloaded! Patching...")

            time.sleep(2)
            print("Patched! Will not happen again. Enjoy your free math :)")

            reboot_done = True

        continue

    num = int(raw)

    if num < 0:
        print("Negative factorial is NOT this universe's problem..")
        continue

    fact = factorial(num)

    roasts = [
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
        continue

    if num > 100:
        roll = random.random()

        if roll < 0.05:
            print(f"Wow, you're pretty unlucky. Your PC is gonna kill itself. Factorial of {num} = {fact}")

        elif roll < 0.25:
            print(f"WHY? Factorial of {num} has {len(str(fact))} digits, if you need it somehow.")

        else:
            print(random.choice(roasts))
    else:
        print(f"Factorial of {num} = {fact}")