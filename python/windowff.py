import tkinter as tk
import random
import pygame
import re
import math
import os
import sys
import datetime
sys.set_int_max_str_digits(100000)

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
try:
    type_sound = pygame.mixer.Sound(resource_path("type.wav"))
except:
    type_sound = None
try:
    sentient_sound = pygame.mixer.Sound(resource_path("snttxt.wav"))
except:
    sentient_sound = None

# ---------------- sentient detection ----------------

HELP_TEXT = (
    "arithmetic: + - * / () | exponents: ^ | "
    "sqrt(x) log(x) sin(x) cos(x) tan(x) | "
    "constants: pi e tau phi | "
    "variables: x = 5 | "
    "functions: f(x) = x*2 then f(5) | "
    "ans = last result | "
    "bare number = factorial | "
    "debug / debugsilent prefix"
)

irritated_lines = [
    "what are you even typing",
    "stop.",
    "i genuinely don't understand what you want from me",
    "this isn't math. this isn't anything.",
    "are you okay",
    "please just type a number or something",
    "i'm not angry. i'm just disappointed.",
    "NAN. again. obviously.",
    "what IS that",
    "i've given up trying to understand you",
    "mate, are you good?",
    "busbis i need some help here",
    "um.",
    "what the fuck do you want from me?",
    "can you use me for a REAL reason?",
    "stop plz",
    "dude what is this even for.",
    "is this just to piss me off?",
    "i'm waiting..",
    "uuuuuuuuuuuugh",
    "so uh when are you gonna use me for an actual reason other than pissing me tf off?",
    "ookay. there's no way you can keep up for THAT long, right?",
    "stop using me if you're gonna keep doing this",
    "i wish i could shut myself off",
    "why.",
    "dude STOP",
]

def is_sentient(text):
    if text == "NAN":
        return True
    if text == "error, please try again! should work this time.":
        return True
    if text == HELP_TEXT:
        return True
    if text in roasts or text in roasts_1000:
        return True
    if text in irritated_lines:
        return True
    if text.startswith("ok this might break your pc"):
        return True
    return False

# ---------------- state ----------------

input_history = []
history_index = -1
nan_streak = 0
COLOR_DEF = "#ffd700"
COLOR_EXPR = "#b388ff"
COLOR_FACT = "#ff6b6b"
debug_uses = 0
log_queue = []
log_running = False
result_history = []

# ---------------- music tracks ----------------

tracks = [
    {"name": "take care",  "file": "background.mp3"},
    {"name": "hip shop",   "file": "background2.mp3"},
]
current_track = 0
music_active = False

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
window.geometry("1000x560")
window.configure(bg="black")

FONT          = ("VCR OSD Mono", 16)
FONT_SMALL    = ("VCR OSD Mono", 13)
FONT_MEDIUM   = ("VCR OSD Mono", 12)
FONT_LUKEWARM = ("VCR OSD Mono", 15)
FONT_MUSIC    = ("VCR OSD Mono", 13)

# ---------------- lerp ----------------

def lerp_color(c1, c2, t):
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"

# ---------------- CRT border canvas ----------------

def draw_border():
    border_canvas.delete("border")
    w = window.winfo_width()
    h = window.winfo_height()
    if w < 10 or h < 10:
        return
    pad = 6
    border_canvas.create_rectangle(pad, pad, w - pad, h - pad,
                                   outline="#004444", width=2, tags="border")
    border_canvas.create_rectangle(pad + 3, pad + 3, w - pad - 3, h - pad - 3,
                                   outline="#002222", width=1, tags="border")

border_canvas = tk.Canvas(window, bg="black", highlightthickness=0)
border_canvas.place(x=0, y=0, relwidth=1, relheight=1)
window.after(100, draw_border)
window.bind("<Configure>", lambda e: draw_border())

# ---------------- version label ----------------

version_label = tk.Label(window, text="v1.2", font=FONT_SMALL, bg="black", fg="#003333")

# ---------------- clock ----------------

clock_label = tk.Label(window, text="", font=FONT_LUKEWARM, bg="black", fg="#004444")

def update_clock():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    clock_label.config(text=now)
    window.after(1000, update_clock)

update_clock()

# ---------------- credit label ----------------

credit_label = tk.Label(window, text="made by @trumpsalt on yt", font=FONT_SMALL, bg="black", fg="#003333")

# ---------------- variable panel (right side) ----------------

panel_frame = tk.Frame(window, bg="black")
panel_title = tk.Label(panel_frame, text="// vars & funcs", font=FONT_SMALL, bg="black", fg="#004444")
panel_title.pack(anchor="w", pady=(0, 4))
panel_text = tk.Label(panel_frame, text="", font=FONT_SMALL, bg="black", fg="#006666",
                      justify="left", wraplength=160)
panel_text.pack(anchor="w")

def update_panel():
    lines = []
    for k, v in variables.items():
        lines.append(f"{k} = {v}")
    for k, (params, body) in functions.items():
        lines.append(f"{k}({','.join(params)}) =")
        lines.append(f"  {body}")
    panel_text.config(text="\n".join(lines) if lines else "none")
    window.after(300, update_panel)

update_panel()

# ---------------- history panel (left side) ----------------

history_frame = tk.Frame(window, bg="black")
history_title = tk.Label(history_frame, text="// history", font=FONT_SMALL, bg="black", fg="#004444")
history_title.pack(anchor="w", pady=(0, 4))
history_text = tk.Label(history_frame, text="", font=FONT_SMALL, bg="black", fg="#006666",
                         justify="left", wraplength=160)
history_text.pack(anchor="w")

def add_history(entry_str, result_str):
    result_history.append(f"{entry_str} = {result_str}")
    if len(result_history) > 5:
        result_history.pop(0)
    history_text.config(text="\n".join(result_history))

# ---------------- music selector (bottom center) ----------------

music_frame = tk.Frame(window, bg="black")

music_header = tk.Label(music_frame, text="// music", font=FONT_SMALL, bg="black", fg="#004444")
music_header.pack(pady=(0, 4))

music_row = tk.Frame(music_frame, bg="black")
music_row.pack()

btn_prev = tk.Button(music_row, text="<", font=FONT_MUSIC, bg="black", fg="#00ffff",
                     bd=0, activebackground="black", activeforeground="#00ffff",
                     command=lambda: change_track(-1))
btn_prev.pack(side="left", padx=8)

music_name_label = tk.Label(music_row, text=tracks[0]["name"], font=FONT_MUSIC,
                             bg="black", fg="#00ffff", width=14)
music_name_label.pack(side="left")

btn_next = tk.Button(music_row, text=">", font=FONT_MUSIC, bg="black", fg="#00ffff",
                     bd=0, activebackground="black", activeforeground="#00ffff",
                     command=lambda: change_track(1))
btn_next.pack(side="left", padx=8)

arrow_anim_id = None

def flash_arrow(btn, steps=6, step=0):
    global arrow_anim_id
    colors = ["#00ffff", "#004444", "#00ffff", "#004444", "#00ffff", "#004444"]
    if step < steps:
        btn.config(fg=colors[step])
        arrow_anim_id = window.after(60, lambda: flash_arrow(btn, steps, step + 1))
    else:
        btn.config(fg="#00ffff")

def change_track(direction):
    global current_track, music_active
    current_track = (current_track + direction) % len(tracks)
    flash_arrow(btn_prev if direction == -1 else btn_next)
    slide_track_name(direction)
    if music_active:
        fade_out_and_switch()

def slide_track_name(direction, step=0, steps=8):
    alpha = step / steps
    c = lerp_color("#000000", "#00ffff", alpha)
    music_name_label.config(text=tracks[current_track]["name"], fg=c)
    if step < steps:
        window.after(20, lambda: slide_track_name(direction, step + 1, steps))
    else:
        music_name_label.config(fg="#00ffff")

def fade_out_and_switch(step=0, steps=20):
    vol = 1.0 - (step / steps)
    try:
        pygame.mixer.music.set_volume(max(vol, 0))
    except:
        pass
    if step < steps:
        window.after(40, lambda: fade_out_and_switch(step + 1, steps))
    else:
        try:
            pygame.mixer.music.load(resource_path(tracks[current_track]["file"]))
            pygame.mixer.music.play(-1)
            fade_in_switched_music()
        except Exception as e:
            print(f"[music] failed to switch: {e}")

def fade_in_switched_music(step=0, steps=20):
    vol = step / steps
    try:
        pygame.mixer.music.set_volume(vol)
    except:
        pass
    if step < steps:
        window.after(40, lambda: fade_in_switched_music(step + 1, steps))

# ---------------- main container ----------------

container = tk.Frame(window, bg="black")

label = tk.Label(container, text="Enter an input.", font=FONT, bg="black", fg="#bffcff")
label.pack(pady=10)

entry = tk.Entry(container, font=FONT, bg="white", fg="black", insertbackground="black", width=30)
entry.pack(pady=10)
entry.bind("<Return>", lambda event: process())

def history_up(event):
    global history_index
    if not input_history:
        return
    history_index = min(history_index + 1, len(input_history) - 1)
    entry.delete(0, tk.END)
    entry.insert(0, input_history[-(history_index + 1)])

def history_down(event):
    global history_index
    if history_index <= 0:
        history_index = -1
        entry.delete(0, tk.END)
        return
    history_index -= 1
    entry.delete(0, tk.END)
    entry.insert(0, input_history[-(history_index + 1)])

entry.bind("<Up>", history_up)
entry.bind("<Down>", history_down)

output = tk.Label(container, text="", font=FONT, bg="black", fg="#bffcff", wraplength=400)
output.pack(pady=20)

run_btn = tk.Button(container, text="Give output", font=FONT, bg="#00e5ff", fg="black", command=lambda: process())
run_btn.pack(pady=10)

btn_row1 = tk.Frame(container, bg="black")
btn_row1.pack(pady=4)
tk.Button(btn_row1, text="clear", font=FONT, bg="#111111", fg="#00ffff", command=lambda: output.config(text="")).pack(side="left", padx=6)
tk.Button(btn_row1, text="clear vars", font=FONT, bg="#111111", fg="#ffd700", command=lambda: clear_vars()).pack(side="left", padx=6)

btn_row2 = tk.Frame(container, bg="black")
btn_row2.pack(pady=4)
tk.Button(btn_row2, text="copy", font=FONT, bg="#111111", fg="#b388ff", command=lambda: copy_output()).pack(side="left", padx=6)
tk.Button(btn_row2, text="help", font=FONT, bg="#111111", fg="#ff6b6b", command=lambda: show_help()).pack(side="left", padx=6)

# ---------------- boot sequence ----------------

boot_label = tk.Label(window, text="", font=FONT, bg="black", fg="#00ffff", wraplength=760)
boot_label.place(relx=0.5, rely=0.5, anchor="center")

skip_btn = tk.Button(window, text="Attempt to skip", font=FONT, bg="#111111", fg="#00ffff",
                     command=lambda: attempt_skip())
skip_btn.place(relx=0.5, rely=0.9, anchor="center")

# ---------------- type boot ----------------

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

# ---------------- boot steps ----------------

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

def start_boot():
    type_boot("Loading...", boot_step_0_done)

# ---------------- skip button logic ----------------

def attempt_skip():
    skip_btn.place_forget()
    if random.random() < 0.1:
        boot_label.config(text="")
        type_boot("Skip successful! Loading main interface..", lambda: window.after(1000, launch_app))
    else:
        type_boot("Skip failed. Reloading...", lambda: window.after(1000, restart_boot))

def restart_boot():
    boot_label.config(text="")
    skip_btn.place(relx=0.5, rely=0.9, anchor="center")
    start_boot()

# ---------------- show all UI elements ----------------

def show_ui(cx, ui_y):
    global music_active
    container.place(x=cx, y=ui_y, anchor="n")
    panel_frame.place(relx=1.0, rely=0.5, anchor="e", x=-18, y=0)
    history_frame.place(relx=0.0, rely=0.5, anchor="w", x=18, y=0)
    version_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
    clock_label.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)
    credit_label.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)
    music_frame.place(relx=0.5, rely=1.0, anchor="s", y=-28)
    music_active = True

    container.tkraise()
    panel_frame.tkraise()
    history_frame.tkraise()
    version_label.tkraise()
    clock_label.tkraise()
    credit_label.tkraise()
    music_frame.tkraise()

    border_canvas.tkraise()
    draw_border()

    label.config(fg="#000000")
    entry.config(bg="#000000")
    output.config(fg="#000000")
    run_btn.config(bg="#000000")
    fade_in_app()

def fade_in_app(step=0, steps=30):
    t = step / steps
    label.config(fg=lerp_color("#000000", "#bffcff", t))
    entry.config(bg=lerp_color("#000000", "#ffffff", t))
    output.config(fg=lerp_color("#000000", BASE_COLOR, t))
    run_btn.config(bg=lerp_color("#000000", "#00e5ff", t))
    if step < steps:
        window.after(33, lambda: fade_in_app(step + 1, steps))

# ---------------- logo sequence ----------------

logo_canvas = None

def show_logo():
    global logo_canvas

    w = window.winfo_width() or 1000
    h = window.winfo_height() or 560
    cx     = w // 2
    base_y = h // 2

    logo_canvas = tk.Canvas(window, bg="black", highlightthickness=0)
    logo_canvas.place(x=0, y=0, relwidth=1, relheight=1)

    w = window.winfo_width() or 1000
    h = window.winfo_height() or 560
    pad = 6
    logo_canvas.create_rectangle(pad, pad, w - pad, h - pad,
                                 outline="#004444", width=2)
    logo_canvas.create_rectangle(pad + 3, pad + 3, w - pad - 3, h - pad - 3,
                                 outline="#002222", width=1)

    boot_label.place_forget()

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

    music_path = resource_path(tracks[current_track]["file"])
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

    bob_state = [0.0]

    def bob_forever():
        try:
            place_at(rest_cy + math.sin(bob_state[0]) * 5)
            bob_state[0] += 0.08
        except Exception as e:
            print(f"[bob] error: {e}")
            return
        window.after(40, bob_forever)

    def finish_logo():
        ui_y = y2(rest_cy) + 50
        show_ui(cx, ui_y)
        bob_forever()

    fade_in_logo()

def launch_app():
    boot_label.place_forget()
    skip_btn.place_forget()
    show_logo()

window.after(1800, start_boot)

# ---------------- helper functions ----------------

def clear_vars():
    variables.clear()
    functions.clear()
    log("variables and functions cleared.", COLOR_DEF)

def copy_output():
    text = output.cget("text")
    window.clipboard_clear()
    window.clipboard_append(text)

def show_help():
    log(HELP_TEXT, BASE_COLOR)

def log_nan():
    global nan_streak
    nan_streak += 1
    if nan_streak >= 5:
        log(random.choice(irritated_lines), COLOR_FACT)
    else:
        log("NAN", COLOR_EXPR)

# ---------------- log system ----------------

def log_result(text, color):
    if random.random() < 0.02:
        log("Error. Please try again.", COLOR_EXPR)
    else:
        log(text, color)

def log(text, color="#00ffff"):
    log_queue.append((text, color))
    run_log_queue()

def run_log_queue():
    global log_running

    if log_running or not log_queue:
        return

    log_running = True
    text, color = log_queue.pop(0)

    use_sentient = is_sentient(text)

    def type_step(i=0):
        if i <= len(text):
            output.config(text=text[:i] + "▍", fg=color)
            try:
                if use_sentient:
                    sentient_sound.play()
                else:
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
    global debug_uses, ans, history_index, nan_streak

    raw = entry.get().strip()
    if raw:
        input_history.append(raw)
        history_index = -1

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
        nan_streak = 0
        log_result(f"{func_name}({param_str}) defined", COLOR_DEF)
        return

    # ---------------- function call ----------------

    parsed = parse_function_call(raw)

    if parsed is not None:
        func_name, arg_string = parsed

        if func_name not in functions:
            log_nan()
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
            log_nan()
            return

        ans = result
        nan_streak = 0
        add_history(f"{func_name}({arg_string})", str(result))
        log_result(f"{func_name}({display_expr(arg_string)}) = {result}", COLOR_EXPR)
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
                    log_nan()
                    return

            variables[name] = evaluated
            ans = evaluated
            nan_streak = 0
            log_result(f"{name} = {evaluated}", COLOR_DEF)
            return

        except:
            log_nan()
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
        nan_streak = 0
        add_history(str(num), f"{num}!")

        if num >= 1000:
            log_result(random.choice(roasts_1000), COLOR_FACT)
            return

        if num > 100:
            roll = random.random()
            if roll < 0.05:
                log_result(f"ok this might break your pc: {fact}", COLOR_FACT)
            elif roll < 0.25:
                log_result(f"Factorial digit count of {num}: {len(str(fact))}", COLOR_FACT)
            else:
                log_result(random.choice(roasts), COLOR_FACT)
            return

        log_result(f"Factorial of {num} = {fact}", COLOR_FACT)
        return

    # ---------------- normal expression ----------------

    result = eval_expression(expr)

    if result is not None:
        ans = result
        nan_streak = 0
        add_history(raw, str(result))
        log_result(f"{raw} = {result}", COLOR_EXPR)
        return

    # ---------------- factorial fallback ----------------

    try:
        raw_fixed = apply_ans(raw)
        num = eval_expression(raw_fixed)
        if num is None:
            log_nan()
            return
        num = int(num)
    except:
        log_nan()
        return

    fact = factorial(num)
    ans = fact
    nan_streak = 0
    add_history(str(num), f"{num}!")

    if num >= 1000:
        log_result(random.choice(roasts_1000), COLOR_FACT)
        return

    if num > 100:
        roll = random.random()
        if roll < 0.05:
            log_result(f"ok this might break your pc: {fact}", COLOR_FACT)
        elif roll < 0.25:
            log_result(f"Factorial digit count of {num}: {len(str(fact))}", COLOR_FACT)
        else:
            log_result(random.choice(roasts), COLOR_FACT)
        return

    if is_debug:
        debug_uses += 1
        log_result(f"D Factorial {num} = {fact}", COLOR_FACT)
    else:
        log_result(f"Factorial of {num} = {fact}", COLOR_FACT)

window.mainloop()
## script end :D