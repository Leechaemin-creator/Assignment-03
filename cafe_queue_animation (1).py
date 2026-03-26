import tkinter as tk
import time

# ── 색상 팔레트 ──
COLORS = ["#6cbfee","#6db87a","#f4845f","#b97ce8","#e8a73c","#e87c9a","#5bc4c4","#8a8fe8"]

MENUS = [
    "말차라떼","초코스콘","바스크치즈케익","라떼","레몬티",
    "캐모마일","매실티","플레인 휘낭시에","레몬에이드","카푸치노",
    "자몽티","바닐라라떼","초코 휘낭시에","아메리카노","카페모카"
]

SCENARIO = [
    ("isEmpty",  None),
    ("enqueue",  "말차라떼"),
    ("enqueue",  "초코스콘"),
    ("enqueue",  "바스크치즈케익"),
    ("enqueue",  "라떼"),
    ("enqueue",  "레몬티"),
    ("enqueue",  "캐모마일"),
    ("enqueue",  "매실티"),
    ("enqueue",  "플레인 휘낭시에"),
    ("front",    None),
    ("dequeue",  None),
    ("dequeue",  None),
    ("dequeue",  None),
    ("isEmpty",  None),
    ("enqueue",  "레몬에이드"),
    ("enqueue",  "카푸치노"),
    ("enqueue",  "자몽티"),
    ("enqueue",  "바닐라라떼"),
    ("enqueue",  "초코 휘낭시에"),
    ("front",    None),
    ("dequeue",  None),
    ("dequeue",  None),
    ("enqueue",  "아메리카노"),
    ("enqueue",  "카페모카"),
    ("front",    None),
    ("isEmpty",  None),
    ("clear",    None),
    ("isEmpty",  None),
]

# ── Queue 클래스 ──
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.isEmpty():
            return None
        return self.items.pop(0)

    def front(self):
        if self.isEmpty():
            return None
        return self.items[0]

    def isEmpty(self):
        return len(self.items) == 0

    def clear(self):
        self.items = []

    def size(self):
        return len(self.items)


# ── GUI ──
class QueueApp:
    CARD_W = 90
    CARD_H = 54
    CARD_GAP = 10
    CARD_Y = 55   # center Y in queue canvas
    ANIM_STEPS = 18
    ANIM_MS = 14

    def __init__(self, root):
        self.root = root
        self.root.title("큐(Queue) 애니메이션 — 카페무솔트")
        self.root.configure(bg="#f8f3ff")
        self.root.resizable(False, False)

        self.q = Queue()
        self.color_idx = 0
        self.ops_lit = set()
        self.step_idx = 0
        self.animating = False
        self.chip_colors = {}   # name → color

        self._build_ui()
        self.root.after(1200, self._run_next)

    # ── UI BUILD ──
    def _build_ui(self):
        W = 780

        # Title
        tk.Label(self.root, text="☕  큐(Queue) 애니메이션",
                 font=("맑은 고딕", 17, "bold"), bg="#f8f3ff", fg="#2d2d2d"
                 ).pack(pady=(18,2))
        tk.Label(self.root, text="카페무솔트 메뉴로 배우는 자료구조",
                 font=("맑은 고딕", 9), bg="#f8f3ff", fg="#999"
                 ).pack()

        # Op banner
        self.banner_var = tk.StringVar(value="Queue 카페무솔트 = new Queue()")
        banner_frame = tk.Frame(self.root, bg="#1e1e2e", padx=14, pady=8, bd=0)
        banner_frame.pack(fill="x", padx=20, pady=(14,0))
        tk.Label(banner_frame, text=">>>", font=("Consolas",11,"bold"),
                 bg="#1e1e2e", fg="#89b4fa").pack(side="left")
        tk.Label(banner_frame, textvariable=self.banner_var,
                 font=("Consolas",11,"bold"), bg="#1e1e2e", fg="#a6e3a1",
                 anchor="w").pack(side="left", padx=(8,0))

        # Main card
        card = tk.Frame(self.root, bg="#fff", bd=0,
                        highlightbackground="#e0d6f5", highlightthickness=2)
        card.pack(padx=20, pady=14, fill="both")

        # ── Queue canvas ──
        q_top = tk.Frame(card, bg="#fff")
        q_top.pack(fill="x", padx=16, pady=(14,4))
        tk.Label(q_top, text="🧾  QUEUE", font=("맑은 고딕",10,"bold"),
                 bg="#fff", fg="#555").pack(side="left")
        self.meta_var = tk.StringVar(value="FRONT: — | SIZE: 0/10 | REAR: —")
        tk.Label(q_top, textvariable=self.meta_var,
                 font=("Consolas",8), bg="#fff", fg="#aaa").pack(side="right")

        q_wrap = tk.Frame(card, bg="#faf8ff",
                          highlightbackground="#e0d6f5", highlightthickness=2)
        q_wrap.pack(fill="x", padx=16, pady=(0,4))

        self.q_canvas = tk.Canvas(q_wrap, bg="#faf8ff", height=110,
                                  width=W-40, highlightthickness=0)
        self.q_canvas.pack()

        # Direction labels inside canvas (drawn after)
        self.q_canvas.create_text(6, 104, anchor="sw",
            text="◀ FRONT (dequeue)", font=("Consolas",7,"bold"), fill="#e87c9a")
        self.q_canvas.create_text(W-46, 104, anchor="se",
            text="REAR (enqueue) ▶", font=("Consolas",7,"bold"), fill="#6db87a")

        self.card_items = []   # list of canvas item ids per queue slot

        # ── Badges ──
        badge_row = tk.Frame(card, bg="#fff")
        badge_row.pack(fill="x", padx=16, pady=(4,4))
        self.badges = {}
        ops = [("enqueue","#6db87a"),("dequeue","#e87c9a"),("front","#6cbfee"),
               ("isEmpty","#e8a73c"),("clear","#b97ce8")]
        for op, col in ops:
            lbl = tk.Label(badge_row, text=op, font=("Consolas",8,"bold"),
                           bg="#fff", fg=col, relief="solid", bd=1,
                           padx=8, pady=3)
            lbl.pack(side="left", padx=4)
            lbl.config(fg="#ccc", highlightbackground="#ccc")  # dim start
            self.badges[op] = (lbl, col)

        self.step_var = tk.StringVar(value="0 / 0")
        tk.Label(badge_row, textvariable=self.step_var,
                 font=("Consolas",8), bg="#fff", fg="#bbb").pack(side="right", padx=4)

        # ── Log box ──
        log_frame = tk.Frame(card, bg="#fff")
        log_frame.pack(fill="x", padx=16, pady=(2,10))
        tk.Label(log_frame, text="// 콘솔 출력", font=("맑은 고딕",8),
                 bg="#fff", fg="#999").pack(anchor="w")

        log_inner = tk.Frame(log_frame, bg="#1e1e2e")
        log_inner.pack(fill="x", pady=(4,0))
        self.log_text = tk.Text(log_inner, height=5, font=("Consolas",9),
                                bg="#1e1e2e", fg="#cdd6f4", bd=0,
                                state="disabled", wrap="word", padx=12, pady=8)
        self.log_text.pack(fill="x")
        self.log_text.tag_config("enqueue", foreground="#a6e3a1")
        self.log_text.tag_config("dequeue", foreground="#f38ba8")
        self.log_text.tag_config("front",   foreground="#89dceb")
        self.log_text.tag_config("isEmpty", foreground="#f9e2af")
        self.log_text.tag_config("clear",   foreground="#cba6f7")
        self.log_text.tag_config("info",    foreground="#6c7086")
        self._log("// Queue 선언 완료", "info")

        # ── Menu chips ──
        chip_frame = tk.Frame(card, bg="#fff")
        chip_frame.pack(fill="x", padx=16, pady=(0,14))
        tk.Label(chip_frame, text="사용할 단어 목록", font=("맑은 고딕",8),
                 bg="#fff", fg="#999").pack(anchor="w", pady=(0,6))

        self.chip_labels = {}
        wrap = tk.Frame(chip_frame, bg="#fff")
        wrap.pack(fill="x")
        for i, m in enumerate(MENUS):
            lbl = tk.Label(wrap, text=m, font=("맑은 고딕",8),
                           bg="#faf8ff", fg="#555", relief="solid", bd=1,
                           padx=8, pady=3)
            lbl.grid(row=i//5, column=i%5, padx=3, pady=3, sticky="ew")
            self.chip_labels[m] = lbl

    # ── LOG ──
    def _log(self, text, tag="info"):
        self.log_text.config(state="normal")
        self.log_text.insert("end", text + "\n", tag)
        lines = int(self.log_text.index("end-1c").split(".")[0])
        if lines > 9:
            self.log_text.delete("1.0", "2.0")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    # ── BADGE ──
    def _light_badge(self, op):
        if op not in self.ops_lit:
            self.ops_lit.add(op)
            lbl, col = self.badges[op]
            lbl.config(fg=col)

    # ── META ──
    def _update_meta(self):
        s = self.q.size()
        f = self.q.front() if not self.q.isEmpty() else "—"
        r = self.q.items[-1] if s else "—"
        self.meta_var.set(f"FRONT: {f}  |  SIZE: {s}/10  |  REAR: {r}")

    # ── CANVAS RENDER ──
    def _redraw_queue(self):
        self.q_canvas.delete("card")
        self.card_items = []
        for i, item in enumerate(self.q.items):
            self._draw_card(i, item, self.chip_colors.get(item, COLORS[0]),
                            is_front=(i == 0), tag="card")
        self._update_meta()

    def _draw_card(self, idx, name, color, is_front=False, tag="card", x_offset=0):
        x = 12 + idx * (self.CARD_W + self.CARD_GAP) + x_offset
        y = 14
        # shadow
        self.q_canvas.create_rectangle(x+3, y+3, x+self.CARD_W+3, y+self.CARD_H+3,
                                        fill="#ddd", outline="", tags=tag)
        # card body
        rect = self.q_canvas.create_rectangle(x, y, x+self.CARD_W, y+self.CARD_H,
                                               fill=color, outline="", tags=tag)
        # front highlight border
        if is_front:
            self.q_canvas.create_rectangle(x, y, x+self.CARD_W, y+self.CARD_H,
                                            fill="", outline="#fff", width=2, tags=tag)
            # FRONT arrow
            self.q_canvas.create_text(x + self.CARD_W//2, y - 6,
                                       text="▼ FRONT", font=("Consolas",7,"bold"),
                                       fill="#e87c9a", tags=tag)
        # index
        self.q_canvas.create_text(x+8, y+8, anchor="nw",
                                   text=f"[{idx}]", font=("Consolas",7),
                                   fill="#dddddd",
                                   tags=tag)
        self.q_canvas.create_text(x + self.CARD_W//2, y + self.CARD_H//2 + 4,
                                   text=name, font=("맑은 고딕",8,"bold"),
                                   fill="#ffffff", width=self.CARD_W-8, tags=tag)
        return rect

    # ── ANIMATE ENQUEUE (slide in from right) ──
    def _anim_enqueue(self, name, color, callback):
        idx = len(self.q.items) - 1
        start_x = idx * (self.CARD_W + self.CARD_GAP) + 50
        end_x = 0
        steps = self.ANIM_STEPS
        dx = (end_x - start_x) / steps

        def step(s, cur_x):
            self.q_canvas.delete("anim_new")
            self._draw_card_at_offset(idx, name, color, cur_x, tag="anim_new",
                                      is_front=(idx == 0))
            if s < steps:
                self.root.after(self.ANIM_MS, lambda: step(s+1, cur_x+dx))
            else:
                self.q_canvas.delete("anim_new")
                self._redraw_queue()
                self.animating = False
                callback()

        step(0, start_x)

    def _draw_card_at_offset(self, idx, name, color, x_off, tag="anim_new", is_front=False):
        base_x = 12 + idx * (self.CARD_W + self.CARD_GAP)
        x = base_x + x_off
        y = 14
        self.q_canvas.create_rectangle(x+3, y+3, x+self.CARD_W+3, y+self.CARD_H+3,
                                        fill="#ddd", outline="", tags=tag)
        self.q_canvas.create_rectangle(x, y, x+self.CARD_W, y+self.CARD_H,
                                        fill=color, outline="", tags=tag)
        if is_front:
            self.q_canvas.create_rectangle(x, y, x+self.CARD_W, y+self.CARD_H,
                                            fill="", outline="#fff", width=2, tags=tag)
            self.q_canvas.create_text(x + self.CARD_W//2, y-6,
                                       text="▼ FRONT", font=("Consolas",7,"bold"),
                                       fill="#e87c9a", tags=tag)
        self.q_canvas.create_text(x + self.CARD_W//2, y + self.CARD_H//2 + 4,
                                   text=name, font=("맑은 고딕",8,"bold"),
                                   fill="#ffffff", width=self.CARD_W-8, tags=tag)

    # ── ANIMATE DEQUEUE (slide out to left) ──
    def _anim_dequeue(self, name, color, callback):
        steps = self.ANIM_STEPS
        dx = -50 / steps

        def step(s, cur_x):
            self.q_canvas.delete("anim_leave")
            # Redraw rest without first card
            self.q_canvas.delete("card")
            for i, item in enumerate(self.q.items):
                self._draw_card(i, item, self.chip_colors.get(item, COLORS[0]),
                                is_front=(i == 0), tag="card")
            # Animate first card
            self._draw_card_at_offset(0, name, color, cur_x, tag="anim_leave")
            if s < steps:
                self.root.after(self.ANIM_MS, lambda: step(s+1, cur_x+dx))
            else:
                self.q_canvas.delete("anim_leave")
                self._redraw_queue()
                self.animating = False
                callback()

        step(0, 0)

    # ── ANIMATE CLEAR ──
    def _anim_clear(self, items_snapshot, colors_snapshot, callback):
        total = len(items_snapshot)
        if total == 0:
            self._redraw_queue()
            self.animating = False
            callback()
            return

        removed = [False] * total
        done_count = [0]

        def remove_one(i):
            removed[i] = True
            done_count[0] += 1
            self.q_canvas.delete("card")
            for j, item in enumerate(items_snapshot):
                if not removed[j]:
                    self._draw_card(j, item, colors_snapshot[j],
                                    is_front=(j == min(k for k,r in enumerate(removed) if not r)),
                                    tag="card")
            if done_count[0] == total:
                self._redraw_queue()
                self.animating = False
                callback()

        for i in range(total):
            self.root.after(i * 90, lambda idx=i: remove_one(idx))

    # ── ANIMATE FRONT PULSE ──
    def _anim_front_pulse(self, callback):
        colors_cycle = ["#fff", "#ffd700", "#fff", "#ffd700", "#fff"]
        def step(i):
            if i >= len(colors_cycle):
                self._redraw_queue()
                self.animating = False
                callback()
                return
            self.q_canvas.delete("card")
            for idx, item in enumerate(self.q.items):
                col = self.chip_colors.get(item, COLORS[0])
                self._draw_card(idx, item, col, is_front=(idx == 0), tag="card")
            if self.q.items:
                x = 12
                y = 14
                self.q_canvas.create_rectangle(x, y, x+self.CARD_W, y+self.CARD_H,
                                                fill="", outline=colors_cycle[i],
                                                width=3, tags="card")
            self.root.after(120, lambda: step(i+1))
        step(0)

    # ── CHIP COLORS ──
    def _chip_enqueue(self, name, color):
        if name in self.chip_labels:
            self.chip_labels[name].config(bg=color, fg="#fff",
                                           relief="solid", bd=0)

    def _chip_dequeue(self, name):
        if name in self.chip_labels:
            self.chip_labels[name].config(bg="#f0f0f0", fg="#bbb",
                                           relief="solid", bd=1,
                                           font=("맑은 고딕",8,"overstrike"))

    def _chip_reset(self):
        for m, lbl in self.chip_labels.items():
            lbl.config(bg="#faf8ff", fg="#555", relief="solid", bd=1,
                       font=("맑은 고딕",8))

    # ── OPERATIONS ──
    def do_enqueue(self, name, callback):
        color = COLORS[self.color_idx % len(COLORS)]
        self.color_idx += 1
        self.chip_colors[name] = color
        self.q.enqueue(name)
        self._chip_enqueue(name, color)
        self._light_badge("enqueue")
        self.banner_var.set(f'카페무솔트.enqueue("{name}")')
        self._log(f'enqueue("{name}")  →  큐에 추가됨', "enqueue")
        self._update_meta()
        self.animating = True
        self._anim_enqueue(name, color, callback)

    def do_dequeue(self, callback):
        if self.q.isEmpty():
            callback(); return
        name = self.q.front()
        color = self.chip_colors.get(name, COLORS[0])
        self.q.dequeue()
        self._chip_dequeue(name)
        self._light_badge("dequeue")
        self.banner_var.set(f'카페무솔트.dequeue()')
        self._log(f'dequeue()  →  "{name}" 제거됨', "dequeue")
        self._update_meta()
        self.animating = True
        self._anim_dequeue(name, color, callback)

    def do_front(self, callback):
        self._light_badge("front")
        val = self.q.front()
        self.banner_var.set(f'카페무솔트.front()  →  "{val}"')
        self._log(f'front()  →  "{val}"  (맨 앞 확인)', "front")
        self.animating = True
        self._anim_front_pulse(callback)

    def do_isEmpty(self, callback):
        self._light_badge("isEmpty")
        result = self.q.isEmpty()
        self.banner_var.set(f'카페무솔트.isEmpty()  →  {result}')
        self._log(f'isEmpty()  →  {result}', "isEmpty")
        self.root.after(700, callback)

    def do_clear(self, callback):
        self._light_badge("clear")
        snapshot_items = list(self.q.items)
        snapshot_colors = [self.chip_colors.get(n, COLORS[0]) for n in snapshot_items]
        for n in snapshot_items:
            self._chip_dequeue(n)
        self.q.clear()
        self.banner_var.set("카페무솔트.clear()")
        self._log("clear()  →  큐 전체 초기화", "clear")
        self._update_meta()
        self.animating = True
        self._anim_clear(snapshot_items, snapshot_colors, callback)

    # ── SCENARIO RUNNER ──
    def _run_next(self):
        if self.animating:
            self.root.after(50, self._run_next)
            return

        total = len(SCENARIO)
        if self.step_idx >= total:
            # End — reset after pause
            self._log("// ✓ 모든 연산 완료! 잠시 후 다시 시작...", "info")
            self.banner_var.set("// 완료 — 잠시 후 다시 시작합니다")
            self.root.after(4000, self._reset_and_restart)
            return

        self.step_var.set(f"{self.step_idx+1} / {total}")
        op, arg = SCENARIO[self.step_idx]
        self.step_idx += 1

        next_cb = lambda: self.root.after(200, self._run_next)

        if   op == "enqueue": self.do_enqueue(arg, next_cb)
        elif op == "dequeue": self.do_dequeue(next_cb)
        elif op == "front":   self.do_front(next_cb)
        elif op == "isEmpty": self.do_isEmpty(next_cb)
        elif op == "clear":   self.do_clear(next_cb)

    def _reset_and_restart(self):
        self.q = Queue()
        self.color_idx = 0
        self.ops_lit = set()
        self.step_idx = 0
        self.chip_colors = {}
        for op, (lbl, col) in self.badges.items():
            lbl.config(fg="#ccc")
        self._chip_reset()
        self._redraw_queue()
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")
        self._log("// Queue 선언 완료", "info")
        self.banner_var.set("Queue 카페무솔트 = new Queue()")
        self.step_var.set("0 / 0")
        self.root.after(1200, self._run_next)


# ── MAIN ──
if __name__ == "__main__":
    root = tk.Tk()
    app = QueueApp(root)
    root.mainloop()
