import tkinter as tk
import random
import time

def factorial(num):
    fact = 1
    for i in range(1, num + 1):
        fact *= i
    return fact

debug_uses = 0
reboot_done = False

def log(text):
    output.config(text=text)

def normal_calc():
    global debug_uses, reboot_done

    raw = entry.get()

    try:
        num = int(raw)
    except:
        log("bro that’s not a number")
        return

    if num < 0:
        log("Negative factorial is NOT this universe's problem..")
        return

    fact = factorial(num)

    if num == 1337:
        log("Factorial = Elite")
        return

    if num > 100:
        roll = random.random()

        if roll < 0.05:
            log(f"unlucky. factorial = {fact}")

        elif roll < 0.25:
            log(f"WHY? digits = {len(str(fact))}")

        else:
            log(random.choice(roasts))
    else:
        log(f"Factorial = {fact}")

def debug():
    global debug_uses, reboot_done

    raw = entry.get()

    try:
        num = int(raw.split()[-1])
    except:
        log("debug needs a number bro")
        return

    debug_uses += 1
    fact = factorial(num)

    log(f"DEBUG factorial of {num} = {fact}")

    if debug_uses == 10:
        log("File code unstable.")

    elif debug_uses == 11 and not reboot_done:
        log("Detected rising instability... Promptly restarting.")
        window.update()
        time.sleep(1)

        log("Reloading factorialfinder.py")
        window.update()

        if random.random() < 0.1:
            time.sleep(1)
            log("Failed to compile code. Retrying...")
            window.update()

        time.sleep(3)
        log("Successfully reloaded! Now patching...")

        time.sleep(2)
        log("Patched! Will not happen again. Enjoy the free math :)")

        reboot_done = True

def debugsilent():
    raw = entry.get()

    try:
        num = int(raw.split()[-1])
    except:
        log("debugsilent needs a number")
        return

    fact = factorial(num)
    log(str(fact))

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

window = tk.Tk()
window.title("factorial finder")
window.geometry("400x250")

entry = tk.Entry(window, width=30)
entry.pack(pady=10)

tk.Button(window, text="calculate", command=normal_calc).pack()
tk.Button(window, text="debug", command=debug).pack()
tk.Button(window, text="debugsilent", command=debugsilent).pack()

output = tk.Label(window, text="", wraplength=350)
output.pack(pady=20)

window.mainloop()