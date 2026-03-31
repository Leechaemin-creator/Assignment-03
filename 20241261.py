import tkinter as tk
from tkinter import messagebox
import collections

class QueueAnimation:
    def __init__(self, root):
        self.root = root
        self.root.title("Cafe Order Queue Animation")
        self.root.geometry("800x500")

        # 1. 큐 선언 (최대 크기 10 유지)
        self.queue = collections.deque(maxlen=10)
        
        # 팀원들의 단어 리스트
        self.menu_items = [
            "말차라떼", "초코스콘", "바스트치즈케이크", "카페라떼", "레몬티",
            "캐모마일 티", "매실티", "휘낭시에", "카푸치노", "자몽티",
            "바닐라라떼", "아메리카노", "카페모카"
        ]
        self.current_index = 0

        # UI 구성
        self.canvas = tk.Canvas(self.root, width=600, height=200, bg="white")
        self.canvas.pack(pady=50)
        
        self.log_text = tk.Text(self.root, height=10, width=70)
        self.log_text.pack(pady=10)

        self.status_label = tk.Label(self.root, text="애니메이션 시작 버튼을 눌러주세요.", font=("NanumGothic", 12))
        self.status_label.pack()

        self.start_btn = tk.Button(self.root, text="시작", command=self.run_animation)
        self.start_btn.pack(pady=5)

    def update_canvas(self):
        """큐의 현재 상태를 시각화합니다."""
        self.canvas.delete("all")
        x_start = 50
        for i, item in enumerate(self.queue):
            # 큐 박스 그리기
            self.canvas.create_rectangle(x_start + (i * 55), 70, x_start + (i * 55) + 50, 120, fill="skyblue")
            # 텍스트 그리기 (글자가 길 경우 일부 생략)
            display_text = item[:4] + ".." if len(item) > 4 else item
            self.canvas.create_text(x_start + (i * 55) + 25, 95, text=display_text, font=("NanumGothic", 8))
            
            # Front 표시
            if i == 0:
                self.canvas.create_text(x_start + 25, 60, text="Front", fill="red", font=("NanumGothic", 10, "bold"))

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def run_animation(self):
        self.start_btn.config(state=tk.DISABLED)
        self.step_1_enqueue_all()

    def step_1_enqueue_all(self):
        """ii, iii, iv: 큐 선언 후 enqueue 연산 및 크기 제한 확인"""
        if self.current_index < len(self.menu_items):
            item = self.menu_items[self.current_index]
            
            # 큐 크기를 10 이하로 유지하기 위한 조건 (iv 준수)
            if len(self.queue) >= 10:
                self.log(f"[Full] 큐가 가득 찼습니다. {item}을 넣기 위해 공간이 필요합니다.")
                self.root.after(1000, self.step_2_front_and_dequeue)
            else:
                self.queue.append(item) # enqueue 연산
                self.log(f"[Enqueue] {item} 추가됨 (현재 크기: {len(self.queue)})")
                self.update_canvas()
                self.current_index += 1
                self.root.after(800, self.step_1_enqueue_all)
        else:
            self.log("모든 메뉴 입력 완료. 마무리 연산을 시작합니다.")
            self.root.after(1000, self.step_3_check_empty_and_clear)

    def step_2_front_and_dequeue(self):
        """ii: front 및 dequeue 연산 수행"""
        if self.queue:
            # front 연산 확인
            front_item = self.queue[0] 
            self.log(f"[Front] 현재 맨 앞 메뉴: {front_item}")
            
            # dequeue 연산
            removed = self.queue.popleft()
            self.log(f"[Dequeue] {removed} 처리 완료 및 제거")
            self.update_canvas()
            
            # 다시 enqueue 단계로 복귀
            self.root.after(800, self.step_1_enqueue_all)

    def step_3_check_empty_and_clear(self):
        """ii: isEmpty 및 clear 연산 수행"""
        # isEmpty 확인
        is_empty_status = len(self.queue) == 0
        self.log(f"[isEmpty] 현재 큐가 비어있나요? : {is_empty_status}")
        
        # clear 연산
        self.log("[Clear] 큐를 초기화합니다.")
        self.queue.clear()
        self.update_canvas()
        
        self.log("[Finish] 모든 제약 조건을 만족하며 애니메이션이 종료되었습니다.")
        messagebox.showinfo("완료", "모든 단어 사용 및 큐 연산이 완료되었습니다.")

if __name__ == "__main__":
    root = tk.Tk()
    app = QueueAnimation(root)
    root.mainloop()
