import tkinter as tk
import random
import pygame

# ---------------- math ----------------

def factorial(num):
    fact = 1
    for i in range(1, num + 1):
        fact *= i
    return fact

# ---------------- expression system ----------------

def eval_addition(expr):
    if any(c.isalpha() for c in expr):
        return None

    if "+" not in expr:
        return None

    try:
        parts = expr.split("+")
        nums = [int(p.strip()) for p in parts]
        return nums, sum(nums)
    except:
        return None

# ---------------- sound ----------------

pygame.mixer.init()
type_sound = pygame.mixer.Sound("type.wav")

# ---------------- state ----------------

debug_uses = 0
reboot_done = False

log_queue = []
log_running = False

roasts = [
    "What are you even doing?",
    "This is really unnecessary.",
    "You really typed THAT in huh?",
    "Why are you like this?",
    "Your CPU is suffering silently",
    "Okay, but WHY though??",
    "What?",
    "Why?",
    "How?",
    "by spu7nix.",
    "Please stop",
    "This is cursed behavior.",
    "Explain yourself.",
    "Explain.",
    "Let's talk about this..",
    "uhh, what the hell?"
    "Busbis would hate you for this.",
    "Shh....",
    "no. just no.",
    "Nuh uh.",
    "No.",
    "I'm not gonna do that.",
    "Nah.",
    "Ehhhhh..."
]

# ---------------- window ----------------

window = tk.Tk()
window.title("Sentient Mathematics")
window.geometry("800x450")
window.configure(bg="black")

FONT = ("VCR OSD Mono", 16)

container = tk.Frame(window, bg="black")
container.place(relx=0.5, rely=0.5, anchor="center")

label = tk.Label(container, text="Enter a number:", font=FONT, bg="black", fg="#bffcff")
label.pack(pady=10)

entry = tk.Entry(container, font=FONT, bg="white", fg="black", insertbackground="black", width=30)
entry.pack(pady=10)

output = tk.Label(container, text="", font=FONT, bg="black", fg="#bffcff", wraplength=900)
output.pack(pady=20)

button = tk.Button(container, text="run", font=FONT, bg="#00e5ff", fg="black", command=lambda: process())
button.pack(pady=10)

# ---------------- log system ----------------

def log(text):
    log_queue.append(text)
    run_log_queue()

def run_log_queue():
    global log_running

    if log_running or not log_queue:
        return

    log_running = True
    text = log_queue.pop(0)

    def type_step(i=0):
        if i <= len(text):
            output.config(text=text[:i] + "▏")

            try:
                type_sound.play()
            except:
                pass

            window.after(25, lambda: type_step(i + 1))
        else:
            output.config(text=text)
            window.after(120, finish)

    def finish():
        global log_running
        log_running = False
        run_log_queue()

    type_step()

# ---------------- idk ----------------

def process():
    global debug_uses, reboot_done

    raw = entry.get().strip()

    # ---------------- Debug mode ----------------

    is_debug = False
    is_silent = False

    if raw.startswith("debugsilent "):
        is_debug = True
        is_silent = True
        raw = raw.replace("debugsilent ", "", 1)

    elif raw.startswith("debug "):
        is_debug = True
        raw = raw.replace("debug ", "", 1)

    # ---------------- addition ----------------

    add = eval_addition(raw)
    if add is not None:
        nums, total = add

        if is_debug:
            debug_uses += 1

            if is_silent:
                log(str(total))
            else:
                log(f"D {nums} = {total}")
        else:
            log(f"{raw} = {total}")

        return

    # ---------------- factorials ----------------

    try:
        num = int(raw)
    except:
        log("NAN")
        return

    fact = factorial(num)

    # ---------------- rsystem----------------

    if num > 100:
        roll = random.random()

        if roll < 0.05:
            log(f"ok this might break your pc: {fact}")

        elif roll < 0.25:
            log(f"digits: {len(str(fact))}")

        else:
            log(random.choice(roasts))

        return

    # ---------------- outputs ----------------

    if is_debug:
        debug_uses += 1
        if is_silent:
            log(str(fact))
        else:
            log(f"D factorial {num} = {fact}")
    else:
        log(f"Factorial = {fact}")

window.mainloop()