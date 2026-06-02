import tkinter as tk
import tkinter.font as tkfont
import threading
import urllib.request
import urllib.error
import json
import re

# ---------------- CONFIG ----------------
API_KEY = "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"
MODEL   = "google/gemma-3-27b-it"
# ----------------------------------------

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

SYSTEM_PROMPT = """You are an achievement ranker. The user will give you a list of achievements.
You must rate the overall achievement portfolio with a single rank:
P, S, A, B, C, D, or F

Rank definitions:
P (golden): Immaculate. Just, perfect. Flawless. Impeccable. Faultless.
S (red): Great!!!
A (orange): Good!
B (yellow): Serviceable
C (green): Bad but whatever you can improve
D (blue): Very bad
F (gray): How did you even do something this shit.

Respond ONLY in this exact JSON format, nothing else, no markdown:
{"rank": "X", "reasoning": "your reasoning here (2-3 sentences max, be brutally honest and funny)"}"""

BG = "#0a0a0a"
FG = "#e0e0e0"
ACCENT = "#222222"
BORDER = "#333333"

def call_api(achievements, callback):
    def run():
        try:
            payload = json.dumps({
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Rate these achievements:\n{achievements}"}
                ],
                "max_tokens": 300,
                "temperature": 0.8
            }).encode()

            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {API_KEY}",
                }
            )

            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                text = data["choices"][0]["message"]["content"].strip()
                # strip markdown fences if present
                text = re.sub(r"```json|```", "", text).strip()
                result = json.loads(text)
                callback(result["rank"].upper(), result["reasoning"])

        except Exception as e:
            callback("ERROR", str(e))

    threading.Thread(target=run, daemon=True).start()


class App:
    def __init__(self, root):
        self.root = root
        root.title("Achievement Ranker")
        root.configure(bg=BG)
        root.geometry("620x700")
        root.resizable(False, False)

        try:
            self.font_title = tkfont.Font(family="VCR OSD Mono", size=22, weight="bold")
            self.font_label = tkfont.Font(family="VCR OSD Mono", size=11)
            self.font_rank  = tkfont.Font(family="VCR OSD Mono", size=80, weight="bold")
            self.font_small = tkfont.Font(family="VCR OSD Mono", size=9)
        except:
            self.font_title = tkfont.Font(family="Courier", size=22, weight="bold")
            self.font_label = tkfont.Font(family="Courier", size=11)
            self.font_rank  = tkfont.Font(family="Courier", size=80, weight="bold")
            self.font_small = tkfont.Font(family="Courier", size=9)

        # Title
        tk.Label(root, text="ACHIEVEMENT RANKER", font=self.font_title,
                 bg=BG, fg=FG).pack(pady=(28, 4))
        tk.Label(root, text="list your achievements. get judged.", font=self.font_small,
                 bg=BG, fg="#555555").pack(pady=(0, 18))

        # Input frame
        input_frame = tk.Frame(root, bg=BORDER, padx=1, pady=1)
        input_frame.pack(padx=30, fill="x")
        inner = tk.Frame(input_frame, bg=ACCENT)
        inner.pack(fill="x")

        self.text = tk.Text(inner, height=8, bg=ACCENT, fg=FG,
                            insertbackground=FG, relief="flat",
                            font=self.font_label, padx=12, pady=10,
                            wrap="word", bd=0)
        self.text.pack(fill="x")
        self.text.insert("1.0", "e.g.\n- won a local chess tournament\n- got a B in math\n- finished a game on hard mode")
        self.text.bind("<FocusIn>", self._clear_placeholder)
        self._placeholder_active = True

        # Button
        self.btn = tk.Button(root, text="[ RANK ME ]", font=self.font_label,
                             bg="#111111", fg=FG, activebackground="#222222",
                             activeforeground=FG, relief="flat", bd=0,
                             cursor="hand2", pady=10,
                             command=self.submit)
        self.btn.pack(padx=30, fill="x", pady=(2, 0))
        self.btn.bind("<Enter>", lambda e: self.btn.config(bg="#1a1a1a", fg="#ffffff"))
        self.btn.bind("<Leave>", lambda e: self.btn.config(bg="#111111", fg=FG))

        # Rank display
        self.rank_var = tk.StringVar(value="?")
        self.rank_label = tk.Label(root, textvariable=self.rank_var,
                                   font=self.font_rank, bg=BG, fg="#333333")
        self.rank_label.pack(pady=(24, 0))

        # Rank name
        self.rank_name_var = tk.StringVar(value="")
        tk.Label(root, textvariable=self.rank_name_var, font=self.font_label,
                 bg=BG, fg="#555555").pack()

        # Reasoning
        self.reason_var = tk.StringVar(value="")
        self.reason_label = tk.Label(root, textvariable=self.reason_var,
                                     font=self.font_small, bg=BG, fg="#777777",
                                     wraplength=540, justify="center")
        self.reason_label.pack(pady=(10, 0), padx=30)

        # Rank legend
        legend_frame = tk.Frame(root, bg=BG)
        legend_frame.pack(pady=(20, 0))
        for rank, color, desc in RANKS:
            col = tk.Frame(legend_frame, bg=BG)
            col.pack(side="left", padx=6)
            tk.Label(col, text=rank, font=self.font_label, bg=BG, fg=color).pack()

        # Status
        self.status_var = tk.StringVar(value="")
        tk.Label(root, textvariable=self.status_var, font=self.font_small,
                 bg=BG, fg="#444444").pack(pady=(8, 0))

    def _clear_placeholder(self, event):
        if self._placeholder_active:
            self.text.delete("1.0", "end")
            self._placeholder_active = False

    def submit(self):
        achievements = self.text.get("1.0", "end").strip()
        if not achievements or self._placeholder_active:
            self.status_var.set("type something first.")
            return

        self.btn.config(state="disabled", text="[ RANKING... ]")
        self.rank_var.set("...")
        self.rank_label.config(fg="#333333")
        self.rank_name_var.set("")
        self.reason_var.set("")
        self.status_var.set("contacting the judges...")

        call_api(achievements, self._on_result)

    def _on_result(self, rank, reasoning):
        self.root.after(0, lambda: self._display(rank, reasoning))

    def _display(self, rank, reasoning):
        self.btn.config(state="normal", text="[ RANK ME ]")

        if rank == "ERROR":
            self.status_var.set(f"error: {reasoning[:80]}")
            return

        color = RANK_COLORS.get(rank, "#888888")
        rank_info = next((r for r in RANKS if r[0] == rank), None)

        self.rank_var.set(rank)
        self.rank_label.config(fg=color)

        if rank_info:
            self.rank_name_var.set(rank_info[2])

        self.reason_var.set(f'"{reasoning}"')
        self.status_var.set("")

        # flash animation
        self._flash(color, 0)

    def _flash(self, color, n):
        if n >= 6:
            self.rank_label.config(fg=color)
            return
        c = color if n % 2 == 0 else BG
        self.rank_label.config(fg=c)
        self.root.after(80, lambda: self._flash(color, n + 1))


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()