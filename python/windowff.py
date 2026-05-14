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
        allowed_chars = set("0123456789+-*/() ")
        for c in expr:
            if c not in allowed_chars:
                return None

        result = eval(expr)

        if isinstance(result, float):
            if result.is_integer():
                result = int(result)

        return result

    except:
        return None

# ---------------- variables ----------------

variables = {}

def resolve_vars(expr):
    new_expr = expr

    for var_name in variables:
        var_value = str(variables[var_name])
        new_expr = new_expr.replace(var_name, var_value)

    return new_expr

# ---------------- functions ----------------

functions = {}

def parse_function_call(expr):
    match = re.match(r"([a-zA-Z]\w*)\((.*)\)", expr)

    if match is None:
        return None

    func_name = match.group(1)
    func_arg = match.group(2).strip()

    if func_name not in functions:
        return None

    return func_name, func_arg

# ---------------- sound ----------------

pygame.mixer.init()
type_sound = pygame.mixer.Sound("type.wav")

# ---------------- state ----------------

debug_uses = 0

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
    "WHY?!",
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

label = tk.Label(container, text="Enter input:", font=FONT, bg="black", fg="#bffcff")
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

    if log_running:
        if len(log_queue) == 0:
            return

    if len(log_queue) == 0:
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
    global debug_uses

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
            left_side, right_side = raw.split("=", 1)

            func_header = left_side
            func_body = right_side.strip()

            func_name, func_params = func_header.split("(", 1)
            func_name = func_name.strip()

            func_params = func_params.replace(")", "").strip()

            functions[func_name] = (func_params, func_body)

            log(f"{func_name} defined")
            return

        except:
            log("NAN")
            return

    # ---------------- function call ----------------

    parsed = parse_function_call(raw)

    if parsed is not None:
        func_name = parsed[0]
        func_arg = parsed[1]

        func_params, func_body = functions[func_name]

        param_name = func_params.split(",")[0].strip()

        replaced_body = func_body.replace(param_name, func_arg)

        replaced_body = resolve_vars(replaced_body)

        result = eval_expression(replaced_body)

        if result is None:
            log("NAN")
        else:
            if is_debug:
                debug_uses += 1
                log(f"{func_name}({func_arg}) = {result}")
            else:
                log(f"{func_name}({func_arg}) = {result}")

        return

    # ---------------- variable assignment ----------------

    if "=" in raw:
        try:
            var_name, var_value = raw.split("=", 1)

            var_name = var_name.strip()
            var_value = resolve_vars(var_value.strip())

            evaluated = eval_expression(var_value)

            if evaluated is None:
                try:
                    evaluated = int(var_value)
                except:
                    log("NAN")
                    return

            variables[var_name] = evaluated

            log(f"{var_name} = {evaluated}")
            return

        except:
            log("NAN")
            return

    # ---------------- expression ----------------

    processed = resolve_vars(raw)

    expr_result = eval_expression(processed)

    if expr_result is not None:
        if is_debug:
            debug_uses += 1
            log(f"D {raw} = {expr_result}")
        else:
            log(f"{raw} = {expr_result}")
        return

    # ---------------- factorial ----------------

    try:
        number = int(raw)
    except:
        log("NAN")
        return

    result = factorial(number)

    if number >= 1000:
        log(random.choice(roasts_1000))
        return

    if number > 100:
        roll = random.random()

        if roll < 0.05:
            log(f"ok this might break your pc: {result}")
        elif roll < 0.25:
            log(f"Factorial digit count of {number}: {len(str(result))}")
        else:
            log(random.choice(roasts))
        return

    if is_debug:
        debug_uses += 1
        log(f"D Factorial {number} = {result}")
    else:
        log(f"Factorial of {number} = {result}")

window.mainloop()