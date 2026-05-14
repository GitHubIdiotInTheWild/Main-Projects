import tkinter as tk
import random
import pygame

def factorial(num):
    fact = 1
    for i in range(1, num + 1):
        fact *= i
    return fact


pygame.mixer.init()
type_sound = pygame.mixer.Sound("type.wav")

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

BG = "#000000"
FG = "#bffcff"
ENTRY_BG = "#ffffff"
ENTRY_FG = "#000000"
ACCENT = "#00e5ff"

BASE_FONT_SIZE = 14


def get_font(size):
    return ("Consolas", size)


def log(text, i=0):
    if i == 0:
        output.config(text="")

    if i <= len(text):
        output.config(text=text[:i] + "┃")

        try:
            type_sound.play()
        except:
            pass

        window.after(25, lambda: log(text, i + 1))
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

        log(str(factorial(num)))
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
            log("File code unstable.")
            return

        if debug_uses == 11 and not reboot_done:
            log("Detected instability... restarting.")

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
            log(f"Unlucky, your PC might break. Factorial = {fact}")
        elif roll < 0.25:
            log(f"WHY? digits = {len(str(fact))}")
        else:
            log(random.choice(roasts))
    else:
        log(f"Factorial = {fact}")


def resize(event):
    # scale font based on window size
    size = max(10, int(event.width / 60))

    f = get_font(size)

    label.config(font=f)
    entry.config(font=f)
    button.config(font=f)
    output.config(font=f)


window = tk.Tk()
window.title("factorial finder")
window.configure(bg=BG)
window.state("zoomed")

window.bind("<Configure>", resize)

label = tk.Label(window, text="Enter a number:", bg=BG, fg=FG)
label.pack(pady=10)

entry = tk.Entry(window, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ENTRY_FG)
entry.pack(pady=10, ipadx=20, ipady=5)

button = tk.Button(window, text="run", command=process, bg=ACCENT, fg="black")
button.pack(pady=10)

output = tk.Label(window, text="", bg=BG, fg=FG, wraplength=900, justify="center")
output.pack(pady=20)

window.mainloop()