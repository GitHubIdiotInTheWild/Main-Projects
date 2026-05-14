import tkinter as tk
import random
import pygame
import re
import math
import os
import sys

# ---------------- resource path ----------------

def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

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

# ---------------- trig + math functions ----------------

def apply_trig(expr):
    def safe_eval(x):
        try:
            return float(eval(x.replace("^", "**")))
        except:
            return 0

    expr = re.sub(r"sqrt\(([^)]+)\)", lambda m: str(math.sqrt(safe_eval(m.group(1)))), expr)
    expr = re.sub(r"log\(([^)]+)\)", lambda m: str(math.log10(safe_eval(m.group(1)))), expr)
    expr = re.sub(r"sin\(([^)]+)\)", lambda m: str(math.sin(math.radians(safe_eval(m.group(1))))), expr)
    expr = re.sub(r"cos\(([^)]+)\)", lambda m: str(math.cos(math.radians(safe_eval(m.group(1))))), expr)
    expr = re.sub(r"tan\(([^)]+)\)", lambda m: str(math.tan(math.radians(safe_eval(m.group(1))))), expr)

    return expr

# ---------------- expression system ----------------

def eval_expression(expr):
    allowed_chars = set("0123456789+-*/()^. ")

    for c in expr:
        if c not in allowed_chars:
            return None

    try:
        expr = expr.replace("^", "**")
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
type_sound = pygame.mixer.Sound(resource_path("type.wav"))

# ---------------- state ----------------

COLOR_DEF = "#ffd700"   # gold
COLOR_EXPR = "#b388ff"  # royal purple
COLOR_FACT = "#ff6b6b"  # light red
debug_uses = 0
log_queue = []
log_running = False

# ---------------- colors ----------------

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
entry.bind("<Return>", lambda event: process())

output = tk.Label(container, text="", font=FONT, bg="black", fg="#bffcff", wraplength=900)
output.pack(pady=20)

run_btn = tk.Button(container, text="Give output", font=FONT, bg="#00e5ff", fg="black", command=lambda: process())
run_btn.pack(pady=10)

set_color()

# hide main UI until boot sequence finishes
container.place_forget()

# ---------------- boot sequence ----------------

boot_label = tk.Label(window, text="", font=FONT, bg="black", fg="#00ffff", wraplength=760)
boot_label.place(relx=0.5, rely=0.5, anchor="center")

def lerp_color(c1, c2, t):
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"

def fade_in_app(step=0, steps=30):
    t = step / steps
    label.config(fg=lerp_color("#000000", "#bffcff", t))
    entry.config(bg=lerp_color("#000000", "#ffffff", t))
    output.config(fg=lerp_color("#000000", BASE_COLOR, t))
    run_btn.config(bg=lerp_color("#000000", "#00e5ff", t))
    if step < steps:
        window.after(33, lambda: fade_in_app(step + 1, steps))

def type_boot(text, on_done, i=0):
    if i <= len(text):
        boot_label.config(text=text[:i] + ("▍" if i < len(text) else ""))
        try:
            type_sound.play()
        except:
            pass
        window.after(25, lambda: type_boot(text, on_done, i + 1))
    else:
        boot_label.config(text=text)
        on_done()

def boot_step_3_done():
    msg = "Activation success! Sentience gained. Bringing interface to main application."
    def after_last():
        window.after(1800, launch_app)
    type_boot(msg, after_last)

def boot_step_2_done():
    window.after(7000, boot_step_3_done)

def boot_step_1_done():
    msg = "Activation failed. Promptly restarting..."
    type_boot(msg, boot_step_2_done)

def boot_step_0_done():
    window.after(3000, lambda: type_boot("Loading complete! Activating...", boot_step_1_done))

# ---------------- logo sequence ----------------

logo_canvas = None

def show_logo():
    global logo_canvas

    w = window.winfo_width() or 800
    h = window.winfo_height() or 450
    cx     = w // 2
    base_y = h // 2

    logo_canvas = tk.Canvas(window, bg="black", highlightthickness=0)
    logo_canvas.place(x=0, y=0, relwidth=1, relheight=1)

    LOGO_FONT = ("Share Tech Mono", 30)
    GAP = 46

    def y1(cy): return cy - GAP // 2
    def y2(cy): return cy + GAP // 2 + 8

    glow_off = [(-1,0),(1,0),(0,-1),(0,1)]

    g1 = [logo_canvas.create_text(cx+dx, y1(base_y)+dy, text="sentient",     font=LOGO_FONT, fill="#000000") for dx,dy in glow_off]
    g2 = [logo_canvas.create_text(cx+dx, y2(base_y)+dy, text="mathematics.", font=LOGO_FONT, fill="#000000") for dx,dy in glow_off]
    m1 = logo_canvas.create_text(cx, y1(base_y), text="sentient",     font=LOGO_FONT, fill="#000000")
    m2 = logo_canvas.create_text(cx, y2(base_y), text="mathematics.", font=LOGO_FONT, fill="#000000")

    def place_at(cy):
        for item,(dx,dy) in zip(g1, glow_off): logo_canvas.coords(item, cx+dx, y1(cy)+dy)
        for item,(dx,dy) in zip(g2, glow_off): logo_canvas.coords(item, cx+dx, y2(cy)+dy)
        logo_canvas.coords(m1, cx, y1(cy))
        logo_canvas.coords(m2, cx, y2(cy))

    def set_colors(t):
        gc = lerp_color("#000000", "#002929", t)
        mc = lerp_color("#000000", "#00ffff", t)
        for item in g1 + g2: logo_canvas.itemconfig(item, fill=gc)
        logo_canvas.itemconfig(m1, fill=mc)
        logo_canvas.itemconfig(m2, fill=mc)

    SLIDE = 155
    rest_cy = base_y - SLIDE

    startup_sound = None
    try:
        startup_sound = pygame.mixer.Sound(resource_path("startup.wav"))
        startup_sound.set_volume(0)
        startup_sound.play()
    except:
        pass

    music_path = resource_path("background.mp3")
    music_loaded = False
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0)
        pygame.mixer.music.play(-1)
        music_loaded = True
        print(f"[music] loaded and playing: {music_path}")
    except Exception as e:
        print(f"[music] failed to load: {e} | path: {music_path}")

    def fade_in_music(step=0, steps=60):
        if music_loaded:
            pygame.mixer.music.set_volume(step / steps)
        if step < steps:
            window.after(50, lambda: fade_in_music(step + 1, steps))

    def fade_in_logo(step=0, steps=25):
        t = step / steps
        set_colors(t)
        if startup_sound:
            try: startup_sound.set_volume(t)
            except: pass
        if step < steps:
            window.after(30, lambda: fade_in_logo(step + 1, steps))
        else:
            fade_in_music()
            animate()

    def animate(phase=0.0, elapsed=0):
        place_at(base_y + math.sin(phase) * 5)
        if elapsed < 3500:
            window.after(40, lambda: animate(phase + 0.08, elapsed + 40))
        else:
            slide_up(0)

    def slide_up(step, steps=22):
        t = 1 - (1 - step / steps) ** 3
        place_at(base_y - SLIDE * t)
        if step < steps:
            window.after(25, lambda: slide_up(step + 1, steps))
        else:
            window.after(600, finish_logo)

    def finish_logo():
        ui_y = y2(rest_cy) + 50
        container.place(x=cx, y=ui_y, anchor="n")
        container.lift()
        label.config(fg="#000000")
        entry.config(bg="#000000")
        output.config(fg="#000000")
        run_btn.config(bg="#000000")
        fade_in_app()

    fade_in_logo()

def launch_app():
    boot_label.place_forget()
    show_logo()

def start_boot():
    type_boot("Loading...", boot_step_0_done)

window.after(1800, start_boot)

# ---------------- log system ----------------

def log(text, color="#00ffff"):
    log_queue.append((text, color))
    run_log_queue()

def run_log_queue():
    global log_running

    if log_running or not log_queue:
        return

    log_running = True
    text, color = log_queue.pop(0)

    def type_step(i=0):
        if i <= len(text):
            output.config(text=text[:i] + "▍", fg=color)
            try:
                type_sound.play()
            except:
                pass
            window.after(25, lambda: type_step(i + 1))
        else:
            output.config(text=text, fg=color)
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

    # ---------------- function definition ----------------

    func_def = re.match(r"([a-zA-Z]\w*)\(([^)]*)\)\s*=\s*(.+)", raw)
    if func_def:
        func_name = func_def.group(1)
        param_str = func_def.group(2)
        func_body = func_def.group(3).strip()
        param_names = [p.strip() for p in param_str.split(",") if p.strip()]
        functions[func_name] = (param_names, func_body)
        log(f"{func_name}({param_str}) defined", COLOR_DEF)
        return

    # ---------------- function call ----------------

    parsed = parse_function_call(raw)

    if parsed is not None:
        func_name, arg_string = parsed

        if func_name not in functions:
            log("NAN", COLOR_EXPR)
            return

        param_names, func_body = functions[func_name]

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
            log("NAN", COLOR_EXPR)
            return

        ans = result
        log(f"{func_name}({display_expr(arg_string)}) = {result}", COLOR_EXPR)
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
                    log("NAN", COLOR_EXPR)
                    return

            variables[name] = evaluated
            ans = evaluated
            log(f"{name} = {evaluated}", COLOR_DEF)
            return

        except:
            log("NAN", COLOR_EXPR)
            return

    # ---------------- expression ----------------

    expr = resolve_vars(raw)
    expr = apply_ans(expr)
    expr = apply_constants(expr)
    expr = apply_trig(expr)

    # ---------------- bare number = factorial (historical behavior) ----------------

    if raw.strip().isdigit():
        num = int(raw)
        fact = factorial(num)
        ans = fact

        if num >= 1000:
            log(random.choice(roasts_1000), COLOR_FACT)
            return

        if num > 100:
            roll = random.random()
            if roll < 0.05:
                log(f"ok this might break your pc: {fact}", COLOR_FACT)
            elif roll < 0.25:
                log(f"Factorial digit count of {num}: {len(str(fact))}", COLOR_FACT)
            else:
                log(random.choice(roasts), COLOR_FACT)
            return

        log(f"Factorial of {num} = {fact}", COLOR_FACT)
        return

    # ---------------- normal expression ----------------

    result = eval_expression(expr)

    if result is not None:
        ans = result
        log(f"{raw} = {result}", COLOR_EXPR)
        return

    # ---------------- factorial fallback ----------------

    try:
        raw_fixed = apply_ans(raw)
        num = eval_expression(raw_fixed)
        if num is None:
            log("NAN", COLOR_EXPR)
            return
        num = int(num)
    except:
        log("NAN", COLOR_EXPR)
        return

    fact = factorial(num)
    ans = fact

    if num >= 1000:
        log(random.choice(roasts_1000), COLOR_FACT)
        return

    if num > 100:
        roll = random.random()
        if roll < 0.05:
            log(f"ok this might break your pc: {fact}", COLOR_FACT)
        elif roll < 0.25:
            log(f"Factorial digit count of {num}: {len(str(fact))}", COLOR_FACT)
        else:
            log(random.choice(roasts), COLOR_FACT)
        return

    if is_debug:
        debug_uses += 1
        log(f"D Factorial {num} = {fact}", COLOR_FACT)
    else:
        log(f"Factorial of {num} = {fact}", COLOR_FACT)

window.mainloop()
## script end :