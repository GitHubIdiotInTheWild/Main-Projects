import tkinter as tk
import tkinter.font as tkfont
import threading
import urllib.request
import json
import re
import pygame
import os

# ---------------- CONFIG ----------------
API_KEY    = "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"
MODEL      = "google/gemma-3-27b-it"
SOUND_DIR  = r"C:\Users\HP\Documents\GitHub\Main-Projects\python\other"
SP_SOUND   = os.path.join(SOUND_DIR, "SPRank.ogg")
NORM_SOUND = os.path.join(SOUND_DIR, "NormalRank.wav")
VOLUME     = 0.35
# ----------------------------------------

pygame.mixer.init()

def play_rank_sound(rank):
    try:
        path = SP_SOUND if rank in ("S", "P") else NORM_SOUND
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(VOLUME)
        pygame.mixer.music.play()
    except:
        pass

RANK_ORDER = ["P", "S", "A", "B", "C", "D", "F"]

RANKS = [
    ("P", "#FFD700", "Immaculate. Just, perfect. Flawless. Impeccable. Faultless. Unblemished. Spotless. Stainless. Pristine. Irreproachable."),
    ("S", "#FF4444", "Great!!!"),
    ("A", "#FF8800", "Good!"),
    ("B", "#FFDD00", "Serviceable"),
    ("C", "#44CC44", "Bad but whatever you can improve"),
    ("D", "#4488FF", "Very bad"),
    ("F", "#888888", "How did you even do something this shit."),
]

RANK_COLORS = {r[0]: r[1] for r in RANKS}

SYSTEM_PROMPT_GENERAL = """You are a fair but direct achievement ranker. Honest and a little dry, but never cruel.
Rate the portfolio with ONE rank: P, S, A, B, C, D, or F

P: Once-in-a-generation. Almost never given.
S: Exceptional. Genuinely rare and impressive.
A: Clearly above average. Good work.
B: Solid. Gets the job done.
C: Mediocre. Room to grow.
D: Below expectations. Needs work.
F: Genuinely poor showing.

Respond ONLY in this JSON, no markdown:
{"rank": "X", "reasoning": "2-3 sentence honest but fair assessment"}"""

SYSTEM_PROMPT_GAME = """You are a video game performance ranker. Be direct and ACTUALLY CALIBRATED — not needlessly harsh.

CRITICAL RULES — read carefully:
- A style score like 45000 in a game like ULTRAKILL is INSANE. That is S tier. Do not give it C.
- A time of 20 seconds for a level is blazing fast. That is S tier unless context says otherwise.
- 11 million kills is absurd. That is S tier.
- Only give C or below for genuinely mediocre or bad performance.
- You are rating relative to what a SKILLED player could achieve. Extraordinary numbers = extraordinary rank.
- Be stingy with ranks that AREN'T deserved, but give high ranks when the numbers genuinely warrant it.

Categories:
- style: creativity, flair, score. High style score = high rank. Low/no style = low rank.
- kills: kill count and efficiency. More kills faster = better.
- time: completion speed. Faster = better.

Rank each: S, A, B, C, D, or F (NOT P).

Respond ONLY in this JSON, no markdown:
{"style": "X", "kills": "X", "time": "X", "style_reason": "1-2 sentences", "kills_reason": "1-2 sentences", "time_reason": "1-2 sentences"}"""

BG     = "#0a0a0a"
FG     = "#e0e0e0"
ACCENT = "#1a1a1a"
BORDER = "#2a2a2a"

def call_api_general(achievements, callback):
    def run():
        try:
            payload = json.dumps({
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT_GENERAL},
                    {"role": "user", "content": f"Rate these achievements:\n{achievements}"}
                ],
                "max_tokens": 300, "temperature": 0.8
            }).encode()
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=payload,
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                text = re.sub(r"```json|```", "", data["choices"][0]["message"]["content"]).strip()
                result = json.loads(text)
                callback(result["rank"].upper(), result["reasoning"], None)
        except Exception as e:
            callback("ERROR", str(e), None)
    threading.Thread(target=run, daemon=True).start()

def call_api_game(achievements, callback):
    def run():
        try:
            payload = json.dumps({
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT_GAME},
                    {"role": "user", "content": f"Rate this video game performance:\n{achievements}"}
                ],
                "max_tokens": 400, "temperature": 0.8
            }).encode()
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=payload,
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                text = re.sub(r"```json|```", "", data["choices"][0]["message"]["content"]).strip()
                result = json.loads(text)
                sr = result["style"].upper()
                kr = result["kills"].upper()
                tr = result["time"].upper()
                sorted_ranks = sorted([sr, kr, tr], key=lambda x: RANK_ORDER.index(x) if x in RANK_ORDER else 6)
                final = sorted_ranks[1]
                if sr == "S" and kr == "S" and tr == "S":
                    final = "P"
                callback(final, None, {
                    "style": sr, "kills": kr, "time": tr,
                    "style_reason": result.get("style_reason",""),
                    "kills_reason": result.get("kills_reason",""),
                    "time_reason": result.get("time_reason",""),
                })
        except Exception as e:
            callback("ERROR", str(e), None)
    threading.Thread(target=run, daemon=True).start()


class FlashBox(tk.Canvas):
    """A canvas that flashes white then fades to transparent over 1.5s."""
    def __init__(self, parent, width, height, **kwargs):
        super().__init__(parent, width=width, height=height,
                         bg=BG, highlightthickness=0, **kwargs)
        self._rect = self.create_rectangle(0, 0, width, height, fill=BG, outline="")
        self._alpha = 0
        self._fading = False

    def flash(self):
        self._alpha = 255
        self._fading = True
        self._fade_step()

    def _fade_step(self):
        if not self._fading or self._alpha <= 0:
            self._alpha = 0
            self._fading = False
            self.itemconfig(self._rect, fill=BG)
            return
        # interpolate white -> BG
        ratio = self._alpha / 255
        r = int(0x0a + (0xff - 0x0a) * ratio)
        g = int(0x0a + (0xff - 0x0a) * ratio)
        b = int(0x0a + (0xff - 0x0a) * ratio)
        color = f"#{r:02x}{g:02x}{b:02x}"
        self.itemconfig(self._rect, fill=color)
        self._alpha = max(0, self._alpha - 8)
        self.after(50, self._fade_step)


class App:
    def __init__(self, root):
        self.root = root
        self.mode = tk.StringVar(value="general")
        root.title("Achievement Ranker")
        root.configure(bg=BG)
        root.attributes("-fullscreen", True)
        root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
        root.bind("<F11>", lambda e: root.attributes("-fullscreen", True))

        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()

        try:
            self.font_title = tkfont.Font(family="VCR OSD Mono", size=24, weight="bold")
            self.font_label = tkfont.Font(family="VCR OSD Mono", size=11)
            self.font_rank  = tkfont.Font(family="VCR OSD Mono", size=100, weight="bold")
            self.font_small = tkfont.Font(family="VCR OSD Mono", size=9)
            self.font_sub   = tkfont.Font(family="VCR OSD Mono", size=16, weight="bold")
        except:
            self.font_title = tkfont.Font(family="Courier", size=24, weight="bold")
            self.font_label = tkfont.Font(family="Courier", size=11)
            self.font_rank  = tkfont.Font(family="Courier", size=100, weight="bold")
            self.font_small = tkfont.Font(family="Courier", size=9)
            self.font_sub   = tkfont.Font(family="Courier", size=16, weight="bold")

        # Main scroll canvas
        main = tk.Frame(root, bg=BG)
        main.pack(expand=True, fill="both")

        tk.Label(main, text="ACHIEVEMENT RANKER", font=self.font_title, bg=BG, fg=FG).pack(pady=(30,2))
        tk.Label(main, text="list your achievements. get destroyed.", font=self.font_small, bg=BG, fg="#444444").pack(pady=(0,14))

        mode_frame = tk.Frame(main, bg=BG)
        mode_frame.pack(pady=(0,10))
        tk.Label(mode_frame, text="MODE:", font=self.font_small, bg=BG, fg="#555555").pack(side="left", padx=(0,8))
        for val, lbl in [("general","GENERAL"), ("game","VIDEO GAME")]:
            tk.Radiobutton(mode_frame, text=lbl, variable=self.mode, value=val,
                           font=self.font_small, bg=BG, fg="#888888",
                           selectcolor=BG, activebackground=BG, activeforeground=FG,
                           command=self._on_mode_change).pack(side="left", padx=8)

        iw = min(800, sw - 80)
        input_frame = tk.Frame(main, bg=BORDER, padx=1, pady=1)
        input_frame.pack(padx=40)
        inner = tk.Frame(input_frame, bg=ACCENT)
        inner.pack()
        self.text = tk.Text(inner, height=6, width=iw//9, bg=ACCENT, fg=FG,
                            insertbackground=FG, relief="flat",
                            font=self.font_label, padx=14, pady=10,
                            wrap="word", bd=0)
        self.text.pack()
        self._set_placeholder()
        self.text.bind("<FocusIn>", self._clear_placeholder)
        self._placeholder_active = True

        self.btn = tk.Button(main, text="[ RANK ME ]", font=self.font_label,
                             bg="#111111", fg=FG, activebackground="#1e1e1e",
                             activeforeground=FG, relief="flat", bd=0,
                             cursor="hand2", pady=12, command=self.submit)
        self.btn.pack(padx=40, fill="x", pady=(2,0), ipadx=0)
        self.btn.bind("<Enter>", lambda e: self.btn.config(bg="#1e1e1e"))
        self.btn.bind("<Leave>", lambda e: self.btn.config(bg="#111111"))

        # P rank gold box (hidden until P is awarded)
        self.p_outer = tk.Frame(main, bg=BG)
        self.p_outer.pack(pady=(24,0))
        self.p_box = tk.Frame(self.p_outer, bg="#FFD700", padx=20, pady=10)
        self.p_rank_label = tk.Label(self.p_box, text="P", font=self.font_rank, bg="#FFD700", fg="white")
        self.p_rank_label.pack()

        # Normal rank label
        self.rank_frame = tk.Frame(main, bg=BG)
        self.rank_frame.pack()
        self.rank_var = tk.StringVar(value="?")
        self.rank_label = tk.Label(self.rank_frame, textvariable=self.rank_var,
                                   font=self.font_rank, bg=BG, fg="#2a2a2a")
        self.rank_label.pack()

        # Flash overlay for final rank
        self.final_flash = FlashBox(main, width=200, height=130)
        # not packed — we place it via place() over rank

        self.rank_name_var = tk.StringVar(value="")
        tk.Label(main, textvariable=self.rank_name_var, font=self.font_label, bg=BG, fg="#555555").pack()

        # Sub ranks
        self.sub_frame = tk.Frame(main, bg=BG)
        self.sub_frame.pack(pady=(12,0))
        self.sub_labels = {}
        self.sub_flashes = {}
        for cat in ["STYLE", "KILLS", "TIME"]:
            col = tk.Frame(self.sub_frame, bg=BG)
            col.pack(side="left", padx=30)
            tk.Label(col, text=cat, font=self.font_small, bg=BG, fg="#444444").pack()
            # Use a Canvas so we can draw both flash rect and text on same layer
            fb = tk.Canvas(col, width=50, height=42, bg=BG, highlightthickness=0)
            fb.pack()
            fb._rect  = fb.create_rectangle(0, 0, 50, 42, fill=BG, outline="")
            fb._text  = fb.create_text(25, 21, text="-", font=self.font_sub, fill="#333333")
            fb._alpha = 0
            fb._fading = False
            def _flash_start(canvas=fb):
                canvas._alpha = 255
                canvas._fading = True
                _fade(canvas)
            def _fade(canvas):
                if not canvas._fading or canvas._alpha <= 0:
                    canvas._alpha = 0
                    canvas._fading = False
                    canvas.itemconfig(canvas._rect, fill=BG)
                    return
                ratio = canvas._alpha / 255
                r = int(0x0a + (0xff - 0x0a) * ratio)
                g = int(0x0a + (0xff - 0x0a) * ratio)
                b = int(0x0a + (0xff - 0x0a) * ratio)
                canvas.itemconfig(canvas._rect, fill=f"#{r:02x}{g:02x}{b:02x}")
                canvas._alpha = max(0, canvas._alpha - 8)
                canvas.after(50, lambda c=canvas: _fade(c))
            fb.flash = _flash_start
            rv = tk.StringVar(value="")
            rl = tk.Label(col, textvariable=rv, font=self.font_small, bg=BG, fg="#444444",
                          wraplength=200, justify="center")
            rl.pack()
            self.sub_labels[cat.lower()] = (fb, rv)
            self.sub_flashes[cat.lower()] = fb

        self.reason_var = tk.StringVar(value="")
        tk.Label(main, textvariable=self.reason_var, font=self.font_small,
                 bg=BG, fg="#666666", wraplength=700, justify="center").pack(pady=(12,0), padx=40)

        legend = tk.Frame(main, bg=BG)
        legend.pack(pady=(18,0))
        for rank, color, _ in RANKS:
            tk.Label(legend, text=rank, font=self.font_label, bg=BG, fg=color).pack(side="left", padx=7)

        self.status_var = tk.StringVar(value="")
        tk.Label(main, textvariable=self.status_var, font=self.font_small,
                 bg=BG, fg="#333333").pack(pady=(8,0))

        tk.Label(main, text="ESC = exit fullscreen  |  F11 = fullscreen",
                 font=self.font_small, bg=BG, fg="#222222").pack(pady=(4,0))

    def _set_placeholder(self):
        ph = ("e.g.\n- won a regional spelling bee\n- benched 60kg once\n- finished a game on normal difficulty"
              if self.mode.get() == "general" else
              "e.g.\n- game: ULTRAKILL\n- level: 1-1\n- kills: 47, no deaths\n- time: 3:24\n- style: 45000")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", ph)
        self.text.config(fg="#333333")
        self._placeholder_active = True

    def _on_mode_change(self):
        self._set_placeholder()
        self._reset_display()

    def _clear_placeholder(self, event):
        if self._placeholder_active:
            self.text.delete("1.0", "end")
            self.text.config(fg=FG)
            self._placeholder_active = False

    def _reset_display(self):
        self.rank_var.set("?")
        self.rank_label.config(fg="#2a2a2a")
        self.rank_name_var.set("")
        self.reason_var.set("")
        self.p_box.pack_forget()
        self.rank_label.pack()
        for cat in ["style","kills","time"]:
            fb, rv = self.sub_labels[cat]
            fb.itemconfig(fb._text, text="-", fill="#333333")
            rv.set("")

    def submit(self):
        achievements = self.text.get("1.0", "end").strip()
        if not achievements or self._placeholder_active:
            self.status_var.set("type something first.")
            return
        self.btn.config(state="disabled", text="[ RANKING... ]")
        self._reset_display()
        self.status_var.set("consulting the judges...")
        if self.mode.get() == "general":
            call_api_general(achievements, self._on_result)
        else:
            call_api_game(achievements, self._on_result)

    def _on_result(self, rank, reasoning, sub):
        self.root.after(0, lambda: self._display(rank, reasoning, sub))

    def _display(self, rank, reasoning, sub):
        self.btn.config(state="normal", text="[ RANK ME ]")
        self.status_var.set("")
        if rank == "ERROR":
            self.status_var.set(f"error: {reasoning[:80]}")
            return
        color = RANK_COLORS.get(rank, "#888888")
        rank_info = next((r for r in RANKS if r[0] == rank), None)
        if sub:
            self._reveal_sub(["style","kills","time"], 0, sub, rank, color, rank_info)
        else:
            self._show_final(rank, color, rank_info, reasoning)

    def _reveal_sub(self, cats, idx, sub, final_rank, final_color, rank_info):
        if idx < len(cats):
            cat = cats[idx]
            fb, rv = self.sub_labels[cat]
            r = sub[cat]
            c = RANK_COLORS.get(r, "#888888")
            fb.itemconfig(fb._text, text=r, fill=c)
            rv.set(sub.get(f"{cat}_reason",""))
            fb.flash()
            self.root.after(800, lambda: self._reveal_sub(cats, idx+1, sub, final_rank, final_color, rank_info))
        else:
            self.root.after(600, lambda: self._show_final(final_rank, final_color, rank_info, None))

    def _show_final(self, rank, color, rank_info, reasoning):
        play_rank_sound(rank)
        if rank == "P":
            self.rank_label.pack_forget()
            self.p_box.pack(in_=self.p_outer)
            self.p_box.config(bg="#FFD700")
            self.p_rank_label.config(bg="#FFD700")
        else:
            self.p_box.pack_forget()
            self.rank_label.pack()
            self.rank_var.set(rank)
            self.rank_label.config(fg=color)
        if rank_info:
            self.rank_name_var.set(rank_info[2])
        if reasoning:
            self.reason_var.set(f'"{reasoning}"')
        self._flash(rank, color, 0)

    def _flash(self, rank, color, n):
        if n >= 6:
            if rank == "P":
                self.p_box.config(bg="#FFD700")
                self.p_rank_label.config(bg="#FFD700")
            else:
                self.rank_label.config(fg=color)
            return
        if rank == "P":
            c = "#FFD700" if n % 2 == 0 else BG
            self.p_box.config(bg=c)
            self.p_rank_label.config(bg=c)
        else:
            c = color if n % 2 == 0 else BG
            self.rank_label.config(fg=c)
        self.root.after(80, lambda: self._flash(rank, color, n+1))


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()