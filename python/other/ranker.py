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

SYSTEM_PROMPT_GENERAL = """You are a brutally honest but fair achievement ranker. You are harsh and darkly funny, but you actually evaluate things correctly.
Rate the overall achievement portfolio with ONE rank: P, S, A, B, C, D, or F

Rank definitions:
P: Once-in-a-generation perfection. Almost never given.
S: Exceptional. Rare. Genuinely impressive.
A: Genuinely good. Above average.
B: Solid. Serviceable. Fine.
C: Below average. Mediocre but not catastrophic.
D: Bad. You should be embarrassed.
F: Genuinely pathetic. How.

Be harsh and funny in your reasoning but actually give a fair rank. Don't inflate, don't deflate — be honest.
Respond ONLY in this exact JSON, no markdown:
{"rank": "X", "reasoning": "2-3 sentence brutal but fair roast"}"""

SYSTEM_PROMPT_GAME = """You are a brutally honest but fair video game performance ranker. Rate 3 categories.
Be harsh and funny but ACTUALLY fair — if the numbers are insane, reflect that in the rank.

Categories:
- style: creativity, flair, risk-taking, combos. Raw quantity = bad. Skill expression = good.
- kills: kill count and efficiency relative to what's expected for that game/level. 11 million kills = absurd = high rank.
- time: speed relative to a reasonable expectation. 2 seconds for anything = either a glitch, skip, or godlike = reflect that.

Rank each: S, A, B, C, D, or F (NOT P — calculated separately).
Be stingy but not delusional. Absurd numbers deserve absurd ranks.

Respond ONLY in this exact JSON, no markdown:
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
                "max_tokens": 300, "temperature": 0.85
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
                "max_tokens": 400, "temperature": 0.85
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


class App:
    def __init__(self, root):
        self.root = root
        self.mode = tk.StringVar(value="general")
        root.title("Achievement Ranker")
        root.configure(bg=BG)
        root.geometry("640x800")
        root.resizable(False, False)

        try:
            self.font_title = tkfont.Font(family="VCR OSD Mono", size=20, weight="bold")
            self.font_label = tkfont.Font(family="VCR OSD Mono", size=10)
            self.font_rank  = tkfont.Font(family="VCR OSD Mono", size=80, weight="bold")
            self.font_small = tkfont.Font(family="VCR OSD Mono", size=8)
            self.font_sub   = tkfont.Font(family="VCR OSD Mono", size=13, weight="bold")
        except:
            self.font_title = tkfont.Font(family="Courier", size=20, weight="bold")
            self.font_label = tkfont.Font(family="Courier", size=10)
            self.font_rank  = tkfont.Font(family="Courier", size=80, weight="bold")
            self.font_small = tkfont.Font(family="Courier", size=8)
            self.font_sub   = tkfont.Font(family="Courier", size=13, weight="bold")

        tk.Label(root, text="ACHIEVEMENT RANKER", font=self.font_title, bg=BG, fg=FG).pack(pady=(24,2))
        tk.Label(root, text="list your achievements. get destroyed.", font=self.font_small, bg=BG, fg="#444444").pack(pady=(0,12))

        mode_frame = tk.Frame(root, bg=BG)
        mode_frame.pack(pady=(0,10))
        tk.Label(mode_frame, text="MODE:", font=self.font_small, bg=BG, fg="#555555").pack(side="left", padx=(0,8))
        for val, lbl in [("general","GENERAL"), ("game","VIDEO GAME")]:
            tk.Radiobutton(mode_frame, text=lbl, variable=self.mode, value=val,
                           font=self.font_small, bg=BG, fg="#888888",
                           selectcolor=BG, activebackground=BG, activeforeground=FG,
                           command=self._on_mode_change).pack(side="left", padx=6)

        input_frame = tk.Frame(root, bg=BORDER, padx=1, pady=1)
        input_frame.pack(padx=28, fill="x")
        inner = tk.Frame(input_frame, bg=ACCENT)
        inner.pack(fill="x")
        self.text = tk.Text(inner, height=7, bg=ACCENT, fg=FG,
                            insertbackground=FG, relief="flat",
                            font=self.font_label, padx=12, pady=10,
                            wrap="word", bd=0)
        self.text.pack(fill="x")
        self._set_placeholder()
        self.text.bind("<FocusIn>", self._clear_placeholder)
        self._placeholder_active = True

        self.btn = tk.Button(root, text="[ RANK ME ]", font=self.font_label,
                             bg="#111111", fg=FG, activebackground="#1e1e1e",
                             activeforeground=FG, relief="flat", bd=0,
                             cursor="hand2", pady=10, command=self.submit)
        self.btn.pack(padx=28, fill="x", pady=(2,0))
        self.btn.bind("<Enter>", lambda e: self.btn.config(bg="#1e1e1e"))
        self.btn.bind("<Leave>", lambda e: self.btn.config(bg="#111111"))

        # P rank gold box
        self.p_frame = tk.Frame(root, bg=BG)
        self.p_frame.pack(pady=(20,0))
        self.p_box = tk.Frame(self.p_frame, bg="#FFD700", padx=18, pady=8)
        self.p_rank_label = tk.Label(self.p_box, text="P", font=self.font_rank, bg="#FFD700", fg="white")
        self.p_rank_label.pack()

        # Normal rank display
        self.rank_frame = tk.Frame(root, bg=BG)
        self.rank_frame.pack()
        self.rank_var = tk.StringVar(value="?")
        self.rank_label = tk.Label(self.rank_frame, textvariable=self.rank_var,
                                   font=self.font_rank, bg=BG, fg="#2a2a2a")
        self.rank_label.pack()

        self.rank_name_var = tk.StringVar(value="")
        tk.Label(root, textvariable=self.rank_name_var, font=self.font_label, bg=BG, fg="#555555").pack()

        # Sub ranks (game mode)
        self.sub_frame = tk.Frame(root, bg=BG)
        self.sub_frame.pack(pady=(8,0))
        self.sub_labels = {}
        for cat in ["STYLE", "KILLS", "TIME"]:
            col = tk.Frame(self.sub_frame, bg=BG)
            col.pack(side="left", padx=14)
            tk.Label(col, text=cat, font=self.font_small, bg=BG, fg="#444444").pack()
            lv = tk.StringVar(value="-")
            lbl = tk.Label(col, textvariable=lv, font=self.font_sub, bg=BG, fg="#333333")
            lbl.pack()
            rv = tk.StringVar(value="")
            rl = tk.Label(col, textvariable=rv, font=self.font_small, bg=BG, fg="#444444",
                          wraplength=160, justify="center")
            rl.pack()
            self.sub_labels[cat.lower()] = (lv, lbl, rv)

        self.reason_var = tk.StringVar(value="")
        tk.Label(root, textvariable=self.reason_var, font=self.font_small,
                 bg=BG, fg="#666666", wraplength=560, justify="center").pack(pady=(10,0), padx=28)

        legend = tk.Frame(root, bg=BG)
        legend.pack(pady=(16,0))
        for rank, color, _ in RANKS:
            tk.Label(legend, text=rank, font=self.font_label, bg=BG, fg=color).pack(side="left", padx=5)

        self.status_var = tk.StringVar(value="")
        tk.Label(root, textvariable=self.status_var, font=self.font_small,
                 bg=BG, fg="#333333").pack(pady=(6,0))

    def _set_placeholder(self):
        ph = ("e.g.\n- won a regional spelling bee\n- benched 60kg once\n- finished a game on normal difficulty"
              if self.mode.get() == "general" else
              "e.g.\n- game: ULTRAKILL\n- level: 1-1\n- kills: 47, no deaths\n- time: 3:24\n- style: railcoined 3 enemies")
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
            lv, lbl, rv = self.sub_labels[cat]
            lv.set("-")
            lbl.config(fg="#333333")
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
            # reveal sub ranks one by one, then final
            cats = ["style", "kills", "time"]
            self._reveal_sub(cats, 0, sub, rank, color, rank_info)
        else:
            # general mode: just show final after flash
            self._show_final(rank, color, rank_info, reasoning)

    def _reveal_sub(self, cats, idx, sub, final_rank, final_color, rank_info):
        if idx < len(cats):
            cat = cats[idx]
            lv, lbl, rv = self.sub_labels[cat]
            r = sub[cat]
            c = RANK_COLORS.get(r, "#888888")
            lv.set(r)
            lbl.config(fg=c)
            rv.set(sub.get(f"{cat}_reason",""))
            self.root.after(700, lambda: self._reveal_sub(cats, idx+1, sub, final_rank, final_color, rank_info))
        else:
            # all subs shown, now show final after a pause
            self.root.after(500, lambda: self._show_final(final_rank, final_color, rank_info, None))

    def _show_final(self, rank, color, rank_info, reasoning):
        play_rank_sound(rank)

        if rank == "P":
            self.rank_label.pack_forget()
            self.p_box.pack(in_=self.p_frame)
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
            c = "#FFD700" if n % 2 == 0 else "#aa8800"
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