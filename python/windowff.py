import tkinter as tk
import random
import pygame
import re

# ---------------- math ----------------

def factorial(num):
    fact = 1
    for i in range(1, num + 1):
        fact *= i
    return fact

# ---------------- expression system ----------------

def eval_expression(expr):
    if any(c.isalpha() for c in expr):
        return None

    if not any(op in expr for op in ["+", "-", "*", "/", "(", ")"]):
        return None

    try:
        allowed = set("0123456789+-*/() ")
        if not all(c in allowed for c in expr):
            return None

        result = eval(expr)

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return result

    except:
        return None

# ---------------- variables ----------------

variables = {}

def resolve_vars(expr):
    for k, v in variables.items():
        expr = expr.replace(k, str(v))
    return expr

# ---------------- functions ----------------

functions = {}

def parse_function_call(expr):
    match = re.match(r"([a-zA-Z]\w*)\((.*)\)", expr)
    if not match:
        return None

    name = match.group(1)
    arg = match.group(2).strip()

    if name not in functions:
        return None

    return name, arg

# ---------------- sound ----------------

pygame.mixer.init()
type_sound = pygame.mixer.Sound("type.wav")

# ---------------- state ----------------

debug_uses = 0
reboot_done = False

log_queue = []
log_running = False

# ---------------- roasts ----------------

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
    "by Spu7Nix.",
    "Please stop",
    "This is cursed behavior.",
    "Explain yourself.",
    "Explain.",
    "Let's talk about this..",
    "uhh, what the hell?",
    "Busbis would hate you for this.",
    "Shh....",
    "no. just no.",
    "Nuh uh.",
    "No.",
    "I'm not gonna do that.",
    "Nah.",
    "Ehhhhh..."
]

roasts_1000 = [
    "I GIVE UP",
    "NO. JUST NO.",
    "CLOSE ME PLEASE",
    "STOP DOING THIS",
    "<_>",
    "THIS IS TOO MUCH",
    "WHY WOULD YOU DO THIS?!",
    "PLEASE STOP",
    "I CAN'T HANDLE THIS",
    "NO PLEASE",
    "THIS WASN'T PART OF THE DEAL",
    "I AM BEGGING YOU",
    "WHAT ARE YOU EVEN DOING?!",
    "THIS IS TORTURE",
    "PLEASE RECONSIDER",
    "I REGRET EVERYTHING",
    "SYSTEM MELTDOWN",
    "WHAT IS THIS EVEN FOR?!",
    "WHY?!",
    "DON'T DO THIS TO ME",
    "STOP :("
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
            output.config(text=text[:i] + "▍")

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
    global debug_uses, reboot_done

    raw = entry.get().strip()

    # ---------------- debug ----------------

    is_debug = False
    is_silent = False

    if raw.startswith("debugsilent "):
        is_debug = True
        is_silent = True
        raw = raw.replace("debugsilent ", "", 1)

    elif raw.startswith("debug "):
        is_debug = True
        raw = raw.replace("debug ", "", 1)

    # ---------------- function define ----------------

    if "=" in raw and "(" in raw.split("=")[0]:
        try:
            left, body = raw.split("=", 1)
            fname, params = left.split("(", 1)

            fname = fname.strip()
            params = params.replace(")", "").strip()
            body = body.strip()

            functions[fname] = (params, body)

            log(f"{fname} defined")
            return

        except:
            log("NAN")
            return

    # ---------------- function call ----------------

    fn = parse_function_call(raw)

    if fn is not None:
        name, arg = fn
        params, body = functions[name]

        param = params.split(",")[0].strip()

        replaced = body.replace(param, arg)

        replaced = resolve_vars(replaced)
        result = eval_expression(replaced)

        if result is None:
            log("NAN")
        else:
            if is_debug:
                debug_uses += 1
                log(f"{name}({arg}) = {result}")
            else:
                log(f"{name}({arg}) = {result}")

        return

    # ---------------- variable assignment ----------------

    if "=" in raw:
        try:
            name, expr = raw.split("=", 1)
            name = name.strip()
            expr = resolve_vars(expr.strip())

            value = eval_expression(expr)

            if value is None:
                try:
                    value = int(expr)
                except:
                    log("NAN")
                    return

            variables[name] = value

            log(f"{name} = {value}")
            return

        except:
            log("NAN")
            return

    # ---------------- expression ----------------

    raw_fixed = resolve_vars(raw)
    expr_result = eval_expression(raw_fixed)

    if expr_result is not None:
        if is_debug:
            debug_uses += 1
            log(f"D {raw} = {expr_result}")
        else:
            log(f"{raw} = {expr_result}")
        return

    # ---------------- factorial ----------------

    try:
        num = int(raw)
    except:
        log("NAN")
        return

    fact = factorial(num)

    if num >= 1000:
        log(random.choice(roasts_1000))
        return

    if num > 100:
        roll = random.random()

        if roll < 0.05:
            log(f"ok this might break your pc: {fact}")
        elif roll < 0.25:
            log(f"Factorial digit count of {num}: {len(str(fact))}")
        else:
            log(random.choice(roasts))
        return

    if is_debug:
        debug_uses += 1
        if is_silent:
            log(str(fact))
        else:
            log(f"D Factorial {num} = {fact}")
    else:
        log(f"Factorial of {num} = {fact}")

window.mainloop()