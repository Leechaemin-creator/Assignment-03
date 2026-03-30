import os
import time

class CafeQueue:
    def __init__(self):
        self.queue = []
        self.max_size = 10
        self.current_code = ""

    def render(self):
        # CMD 화면 초기화 (윈도우: cls, 맥: clear)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n" + "="*75)
        print(f"{'카페무솔트 자료구조(Queue) 연산 시뮬레이션':^75}")
        print("="*75 + "\n")
        
        # 사진과 유사한 2분할 레이아웃 (왼쪽: 코드 | 오른쪽: 표)
        header = f" {self.current_code:<38} |      [ 카페무솔트 ]"
        print(header)
        print("-" * 40 + "| --------------------------")
        
        # 큐 데이터 출력 (10칸 고정)
        # 큐의 특성상 먼저 들어온게 아래(Front)에 있도록 출력
        for i in range(self.max_size):
            if i < len(self.queue):
                # 사진처럼 아래쪽부터 채워지는 느낌을 위해 역순 출력
                display_idx = len(self.queue) - 1 - i
                item = self.queue[display_idx]
                print(f"{' ':40}| {item:^24}")
            else:
                print(f"{' ':40}| {' ':^24}")
            print(" " * 40 + "| --------------------------")
        
        print(f"{' ':40}  (Front)            (Rear)")
        time.sleep(1.2) # 다음 동작까지 대기 시간

    def enqueue(self, item):
        # (제로슈가) 문구 제거 및 영어 메뉴 한글화 처리된 데이터 사용
        clean_item = item.replace("(제로슈가)", "").strip()
        self.current_code = f"카페무솔트.enqueue(\"{clean_item}\")"
        if len(self.queue) < self.max_size:
            self.queue.append(clean_item)
        self.render()

    def dequeue(self):
        self.current_code = "카페무솔트.dequeue()"
        if len(self.queue) > 0:
            self.queue.pop(0) # FIFO: 가장 먼저 들어온 0번 인덱스 제거
        self.render()

    def front(self):
        self.current_code = "카페무솔트.front()"
        self.render()

    def is_empty(self):
        self.current_code = "카페무솔트.isEmpty()"
        self.render()

    def clear(self):
        self.current_code = "카페무솔트.clear()"
        self.queue = []
        self.render()

def main():
    # 팀원들 메뉴 데이터 (수정 반영)
    menu_data = [
        ["말차라떼(제로슈가)", "초코스콘(제로슈가)", "바스크치즈케이크"],
        ["카페라떼", "레몬티", "캐모마일티"], # 영어 메뉴 한글화
        ["매실티", "플레인 휘낭시에", "레몬에이드"],
        ["얼그레이라떼", "캐모마일티", "모히또에이드"],
        ["카푸치노", "초코스콘", "자몽티"],
        ["바닐라라떼", "말차라떼", "초코 휘낭시에"],
        ["아메리카노", "카페모카", "바스크치즈케이크"],
        ["카페라떼", "카푸치노", "말차라떼"],
        ["초코스콘", "피넛라떼", "말차라떼"]
    ]

    cafe = CafeQueue()

    # 1. 큐 선언 (d-iii 조건)
    cafe.current_code = "Queue 카페무솔트 = new Queue();"
    cafe.render()

    # 2. 데이터 순회 및 연산 (d-ii, d-v 조건)
    for group in menu_data:
        cafe.is_empty() 
        
        for menu in group:
            cafe.enqueue(menu)
        
        cafe.front()
        cafe.dequeue()

        # 큐 크기 10 이하 유지 (d-iv 조건)
        if len(cafe.queue) >= 8:
            cafe.clear()

    # 3. 마지막 정리
    cafe.clear()
    cafe.is_empty()
    print("\n[ 시뮬레이션이 모두 완료되었습니다. ]")

if __name__ == "__main__":
    main()
