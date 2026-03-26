import tkinter as tk
from tkinter import font as tkfont

all_menu = [
    "카페라떼", "카푸치노", "말차라떼", "말차라떼(제로슈가)", 
    "초코 스콘(제로슈가)", "바스크치즈케이크", "cafe latte", "lemon tea", 
    "camomile tea", "매실티", "플레인 휘낭시에", "레몬에이드", 
    "초코스콘", "자몽티", "바닐라라떼", "초코 휘낭시에", "아메리카노", "카페모카"
]

class CafeMusealtQueue:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Queue Animation - Cafe Musealt")
        self.root.geometry("1100x750")
        self.root.configure(bg="#F8F9FA")

        self.queue = []
        self.step_index = 0
        self.scenario = []
        
        self.setup_ui()
        self.create_scenario()

        self.root.after(1500, self.next_step)

    def setup_ui(self):

        main_frame = tk.Frame(self.root, bg="#F8F9FA", padx=30, pady=30)
        main_frame.pack(fill="both", expand=True)
        self.display_box = tk.Frame(main_frame, bd=3, relief="solid", highlightbackground="#00AEEF", 
                                   highlightthickness=2, bg="white", padx=20, pady=20)
        self.display_box.pack(fill="both", expand=True)
        logo_label = tk.Label(self.display_box, text="카페무솔트", font=("Malgun Gothic", 16, "bold"), 
                             bg="white", relief="solid", bd=1, padx=15, pady=5)
        logo_label.pack(anchor="ne")
        self.code_label = tk.Label(self.display_box, text="Queue q = new Queue();", 
                                  font=("Consolas", 22, "bold", "italic"), bg="white", fg="#333", justify="left")
        self.code_label.place(relx=0.05, rely=0.5, anchor="w")

        right_panel = tk.Frame(self.display_box, bg="white")
        right_panel.pack(side="right", fill="y", padx=10)
        
        tk.Label(right_panel, text="[ Queue Status (Max 10) ]", font=("Malgun Gothic", 11), bg="white", fg="#666").pack(pady=5)
        
        self.queue_container = tk.Frame(right_panel, bd=2, relief="solid", bg="#444", width=400, height=550)
        self.queue_container.pack_propagate(False)
        self.queue_container.pack()
        self.slots = []
        for i in range(10):
            slot = tk.Frame(self.queue_container, bg="white", height=50, bd=1, relief="ridge")
            slot.pack(side="bottom", fill="x", padx=4, pady=2)
            slot.pack_propagate(False)
            
            txt = tk.Label(slot, text="", font=("Malgun Gothic", 12), bg="white")
            txt.pack(expand=True)
            self.slots.append((slot, txt))

    def create_scenario(self):
        """과제 제약 조건을 모두 충족하는 시나리오 생성"""
        self.scenario.append(("isEmpty", None, "isEmpty() -> True", "#2980b9"))
        self.scenario.append(("enqueue", all_menu[0], f'enqueue("{all_menu[0]}")', "#27ae60"))
        self.scenario.append(("front", None, f'front() -> "{all_menu[0]}" 확인', "#8e44ad"))
        self.scenario.append(("clear", None, "clear() 연산 실행", "#e67e22"))
        self.scenario.append(("isEmpty", None, "isEmpty() -> True", "#2980b9"))

        temp_q_size = 0
        for i, menu in enumerate(all_menu):
            if temp_q_size >= 10:
                self.scenario.append(("dequeue", None, "Queue Full! dequeue()", "#c0392b"))
                temp_q_size -= 1
            
            self.scenario.append(("enqueue", menu, f'enqueue("{menu}")', "#27ae60"))
            temp_q_size += 1

            if i == 10:
                self.scenario.append(("front", None, "front() -> 현재 대기열 1번 확인", "#8e44ad"))

        self.scenario.append(("info", None, "--- 모든 메뉴 투입 완료 (순차 비우기) ---", "#333"))
        for _ in range(temp_q_size):
            self.scenario.append(("dequeue", None, "dequeue()", "#c0392b"))
        
        self.scenario.append(("info", None, "애니메이션 종료 (과제 조건 충족)", "#000"))

    def next_step(self):
        if self.step_index >= len(self.scenario):
            return

        op, item, label, color = self.scenario[self.step_index]

        if op == "enqueue":
            self.queue.append(item)
        elif op == "dequeue" and self.queue:
            self.queue.pop(0)
        elif op == "clear":
            self.queue = []

        self.code_label.config(text=f"카페무솔트.{label}", fg=color)

        for i in range(10):
            slot_frame, slot_label = self.slots[i]
            if i < len(self.queue):
                slot_label.config(text=self.queue[i], fg="black")
                if op == "front" and i == 0:
                    slot_frame.config(bg="#E1BEE7") 
                    slot_label.config(bg="#E1BEE7")
                else:
                    slot_frame.config(bg="white")
                    slot_label.config(bg="white")
            else:
                slot_label.config(text="")
                slot_frame.config(bg="#F0F0F0")
                slot_label.config(bg="#F0F0F0")

        self.step_index += 1
        self.root.after(1000, self.next_step)

if __name__ == "__main__":
    root = tk.Tk()
    root.eval('tk::PlaceWindow . center')
    app = CafeMusealtQueue(root)
    root.mainloop()
