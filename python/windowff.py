import tkinter as tk
import random
import pygame

# ---------------- math ----------------

def factorial(num):
    fact = 1
    for i in range(1, num + 1):
        fact *= i
    return fact

# ---------------- addition ----------------

def try_addition(expr):
    if any(c.isalpha() for c in expr):
        return None

    if "+" not in expr:
        return None

    try:
        parts = expr.split("+")
        nums = [int(p.strip()) for p in parts]
        return expr + " = " + str(sum(nums))
    except:
        return None

# ---------------- sound ----------------

pygame.mixer.init()
type_sound = pygame.mixer.Sound("type.wav")

# ---------------- state ----------------

debug_uses = 0
reboot_done = False
is_corrupted = False

log_queue = []
log_running = False

# ---------------- window ----------------

window = tk.Tk()
window.title("factorial finder")
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

# ---------------- MAIN ----------------

def process():
    global debug_uses, reboot_done, is_corrupted

    raw = entry.get().strip()

    # debug silent
    if raw.startswith("debugsilent "):
        try:
            num = int(raw.split()[1])
            log(str(factorial(num)))
        except:
            log("invalid input")
        return

    # debug mode
    if raw.startswith("debug "):
        try:
            num = int(raw.split()[1])
        except:
            log("invalid input")
            return

        debug_uses += 1
        fact = factorial(num)

        log(f"DFactorial of {num} = {fact}")

        # corruption trigger
        if debug_uses == 10:
            is_corrupted = True
            log("File code unstable.")
            return

        # reboot arc
        if debug_uses == 11 and not reboot_done:
            reboot_done = True

            log("Detected instability... restarting.")
            log("Reloading factorialfinder.py")

            def step2():
                if random.random() < 0.1:
                    log("Failed to compile code. Retrying...")
                    window.after(2900, step3)
                else:
                    step3()

            def step3():
                log("Successfully reloaded! Now patching...")

                def step4():
                    global is_corrupted
                    is_corrupted = False
                    log("Patched! Will not happen again. Enjoy the free math :)")

                window.after(2500, step4)

            window.after(1700, step2)

        return

    # addition FIRST
    add_result = try_addition(raw)
    if add_result is not None:
        log(add_result)
        return

    # normal number
    try:
        num = int(raw)
    except:
        log("NAN")
        return

    log(f"Factorial = {factorial(num)}")

window.mainloop()