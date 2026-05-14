import tkinter as tk
import random
import pygame
import re
import math

# ---------------- math ----------------

def factorial(num):
    fact = 1
    for i in range(1, num + 1):
        fact *= i
    return fact

# ---------------- constants ----------------

constants = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
    "phi": (1 + 5 ** 0.5) / 2
}

def apply_constants(expr):
    for k in constants:
        expr = expr.replace(k, str(constants[k]))
    return expr

# ---------------- trig ----------------

def apply_trig(expr):
    try:
        expr = re.sub(r"sin\(([^)]+)\)", lambda m: str(math.sin(math.radians(eval(m.group(1))))), expr)
        expr = re.sub(r"cos\(([^)]+)\)", lambda m: str(math.cos(math.radians(eval(m.group(1))))), expr)
        expr = re.sub(r"tan\(([^)]+)\)", lambda m: str(math.tan(math.radians(eval(m.group(1))))), expr)
    except:
        pass
    return expr

# ---------------- expression system ----------------

def eval_expression(expr):
    expr = apply_constants(expr)
    expr = apply_trig(expr)

    allowed_chars = set("0123456789+-*/() ")

    for c in expr:
        if c not in allowed_chars:
            return None

    try:
        result = eval(expr)

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return result
    except:
        return None

# ---------------- variables ----------------

variables = {}

def resolve_vars(expr):
    new_expr = expr
    for name in variables:
        new_expr = new_expr.replace(name, str(variables[name]))
    return new_expr

# ---------------- functions ----------------

functions = {}

def parse_function_call(expr):
    match = re.match(r"([a-zA-Z]\w*)\((.*)\)", expr)

    if not match:
        return None

    name = match.group(1)
    args = match.group(2)

    if name not in functions:
        return None

    return name, args


def split_args(arg_string):
    args = []
    current = ""
    depth = 0

    for c in arg_string:
        if c == "," and depth == 0:
            args.append(current.strip())
            current = ""
        else:
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
            current += c

    if current:
        args.append(current.strip())

    return args

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

label = tk.Label(container, text="enter input", font=FONT, bg="black", fg="#bffcff")
label.pack(pady=10)

entry = tk.Entry(container, font=FONT, bg="white", fg="black", insertbackground="black", width=30)
entry.pack(pady=10)

output = tk.Label(container, text="", font=FONT, bg="black", fg="#bffcff", wraplength=900)
output.pack(pady=20)

tk.Button(container, text="run", font=FONT, bg="#00e5ff", fg="black", command=lambda: process()).pack(pady=10)

# ---------------- fade (ADD ON ONLY) ----------------

def fade(text):
    steps = 6

    def step(i=0):
        if i <= steps:
            shade = int(255 * (i / steps))
            color = f"#{shade:02x}{shade:02x}ff"
            output.config(text=text, fg=color)
            window.after(30, lambda: step(i + 1))
        else:
            output.config(text=text, fg="#bffcff")

    step()

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
            fade(text)
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
            left, right = raw.split("=", 1)
            func_name, params = left.split("(", 1)

            func_name = func_name.strip()
            params = params.replace(")", "").strip()
            func_body = right.strip()

            functions[func_name] = (params, func_body)

            log(f"{func_name} defined")
            return
        except:
            log("NAN")
            return

    # ---------------- function call ----------------

    parsed = parse_function_call(raw)

    if parsed is not None:
        func_name, arg_string = parsed

        param_string, func_body = functions[func_name]

        param_names = [p.strip() for p in param_string.split(",")]
        arg_values = split_args(arg_string)

        replaced = func_body

        for i in range(min(len(param_names), len(arg_values))):
            replaced = replaced.replace(param_names[i], arg_values[i])

        replaced = resolve_vars(replaced)

        result = eval_expression(replaced)

        if result is None:
            log("NAN")
        else:
            log(f"{func_name}({arg_string}) = {result}")

        return

    # ---------------- variable assignment ----------------

    if "=" in raw:
        try:
            name, value = raw.split("=", 1)

            name = name.strip()
            value = resolve_vars(value.strip())

            evaluated = eval_expression(value)

            if evaluated is None:
                try:
                    evaluated = int(value)
                except:
                    log("NAN")
                    return

            variables[name] = evaluated
            log(f"{name} = {evaluated}")
            return

        except:
            log("NAN")
            return

    # ---------------- expression ----------------

    expr = resolve_vars(raw)

    result = eval_expression(expr)

    if result is not None:
        log(f"{raw} = {result}")
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
        log(f"D Factorial {num} = {fact}")
    else:
        log(f"Factorial of {num} = {fact}")

window.mainloop()