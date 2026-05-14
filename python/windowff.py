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
    "pi": "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679",
    "π": "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679",
    "e": "2.7182818284590452353602874713526624977572470936999595749669676277240763303535475945713821785251664274",
    "tau": "6.2831853071795864769252867665590057683943387987502116419498891846156328125724179972576696506842341340",
    "phi": "1.6180339887498948482045868343656381177203091798057628621354486227052604628189024497072072041893911374"
}

def apply_constants(expr):
    for k, v in constants.items():
        expr = expr.replace(k, v)
    return expr

# ---------------- trig ----------------

def apply_trig(expr):
    def safe_eval(x):
        try:
            return float(eval(x))
        except:
            return 0

    expr = re.sub(r"sin\(([^)]+)\)", lambda m: str(math.sin(math.radians(safe_eval(m.group(1))))), expr)
    expr = re.sub(r"cos\(([^)]+)\)", lambda m: str(math.cos(math.radians(safe_eval(m.group(1))))), expr)
    expr = re.sub(r"tan\(([^)]+)\)", lambda m: str(math.tan(math.radians(safe_eval(m.group(1))))), expr)

    return expr

# ---------------- expression system ----------------

def eval_expression(expr):
    allowed_chars = set("0123456789+-*/() .")

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
    for name in variables:
        expr = expr.replace(name, str(variables[name]))
    return expr

# ---------------- ANS ----------------

ans = 0

def apply_ans(expr):
    return expr.replace("ans", str(ans))

def display_expr(expr):
    return apply_ans(expr)

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

# ---------------- COLORS (fixed, stable) ----------------

BASE_COLOR = "#00ffff"

def set_color():
    output.config(fg=BASE_COLOR)

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

set_color()

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
            set_color()
            finish()

    def finish():
        global log_running
        log_running = False
        run_log_queue()

    type_step()

# ---------------- MAIN ----------------

def process():
    global debug_uses, ans

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
        replaced = apply_ans(replaced)
        replaced = apply_constants(replaced)
        replaced = apply_trig(replaced)

        result = eval_expression(replaced)

        if result is None:
            log("NAN")
        else:
            ans = result
            log(f"{func_name}({display_expr(arg_string)}) = {result}")

        return

    # ---------------- variable assignment ----------------

    if "=" in raw:
        try:
            name, value = raw.split("=", 1)

            name = name.strip()
            value = apply_ans(resolve_vars(value.strip()))

            evaluated = eval_expression(value)

            if evaluated is None:
                try:
                    evaluated = int(value)
                except:
                    log("NAN")
                    return

            variables[name] = evaluated
            ans = evaluated
            log(f"{name} = {evaluated}")
            return

        except:
            log("NAN")
            return

    # ---------------- expression ----------------

    expr = apply_ans(resolve_vars(raw))
    expr = apply_constants(expr)
    expr = apply_trig(expr)

    result = eval_expression(expr)

    if result is not None:
        ans = result
        log(f"{display_expr(raw)} = {result}")
        return

    # ---------------- factorial (FIXED) ----------------

    try:
        num = int(apply_ans(raw))
    except:
        log("NAN")
        return

    fact = factorial(num)
    ans = fact

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