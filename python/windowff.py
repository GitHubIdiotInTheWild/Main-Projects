import tkinter as tk
import random

def factorial(num):
    fact = 1
    for i in range(1, num + 1):
        fact *= i
    return fact

debug_uses = 0
reboot_done = False

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

FONT = ("VCR OSD Mono", 12)

# TYPEWRITER LOG
def log(text, i=0):
    if i == 0:
        output.config(text="")

    if i <= len(text):
        output.config(text=text[:i] + "│")  # thin cursor
        window.after(25, lambda: log(text, i + 1))  # faster typing
    else:
        output.config(text=text)


def process():
    global debug_uses, reboot_done

    raw = entry.get().strip()

    if raw.startswith("debugsilent "):
        try:
            num = int(raw.split()[1])
        except:
            log("invalid input")
            return

        fact = factorial(num)
        log(str(fact))
        return

    if raw.startswith("debug "):
        try:
            num = int(raw.split()[1])
        except:
            log("invalid input")
            return

        debug_uses += 1
        fact = factorial(num)

        log(f"DEBUGMODE-Factorial of {num} = {fact}")

        if debug_uses == 10:
            log(f"File code unstable. Factorial = {fact}")
            return

        if debug_uses == 11 and not reboot_done:
            log("Detected instability... Promptly restarting.")

            def stage2():
                log("Reloading factorialfinder.py")

                def maybe_fail():
                    if random.random() < 0.1:
                        log("Failed to compile code. Retrying...")
                        window.after(1000, stage3)
                    else:
                        stage3()

                def stage3():
                    log("Successfully reloaded! Now patching...")

                    def stage4():
                        log("Patched! Will not happen again. Enjoy the free math :)")

                    window.after(2500, stage4)

                window.after(500, maybe_fail)

            window.after(500, stage2)

            reboot_done = True

        return

    try:
        num = int(raw)
    except:
        log("NAN, please insert a valid number.")
        return

    if num < 0:
        log("Negative factorial is NOT this universe's problem.")
        return

    fact = factorial(num)

    if num == 1337:
        log("Factorial = Elite.")
        return

    if num > 100:
        roll = random.random()

        if roll < 0.05:
            log(f"Unlucky, your PC might break. Factorial of {num} = {fact}")

        elif roll < 0.25:
            log(f"WHY? Factorial digit count of {num} = {len(str(fact))}")

        else:
            log(random.choice(roasts))
    else:
        log(f"Factorial of {num} = {fact}")


window = tk.Tk()
window.title("factorial finder")
window.geometry("500x300")

frame = tk.Frame(window)
frame.place(relx=0.5, rely=0.5, anchor="center")

label = tk.Label(frame, text="Enter a number:", font=FONT)
label.pack(pady=5)

entry = tk.Entry(frame, width=30, font=FONT)
entry.pack(pady=5)

button = tk.Button(frame, text="run", command=process, font=FONT)
button.pack(pady=5)

output = tk.Label(frame, text="", font=FONT, wraplength=400)
output.pack(pady=15)

window.mainloop()