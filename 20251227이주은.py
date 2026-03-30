import os
import time

class CafeQueue:
    def __init__(self):
        self.queue = []
        self.max_size = 10
        self.current_code = ""

    def render(self):
     
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n" + "="*75)
        print(f"{'카페무솔트 자료구조(Queue) 연산 시뮬레이션':^75}")
        print("="*75 + "\n")
        
    
        header = f" {self.current_code:<38} |      [ 카페무솔트 ]"
        print(header)
        print("-" * 40 + "| --------------------------")
        

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
        time.sleep(1.2) 

    def enqueue(self, item):
      
        clean_item = item.replace("(제로슈가)", "").strip()
        self.current_code = f"카페무솔트.enqueue(\"{clean_item}\")"
        if len(self.queue) < self.max_size:
            self.queue.append(clean_item)
        self.render()

    def dequeue(self):
        self.current_code = "카페무솔트.dequeue()"
        if len(self.queue) > 0:
            self.queue.pop(0) 
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

  
    cafe.current_code = "Queue 카페무솔트 = new Queue();"
    cafe.render()

   
    for group in menu_data:
        cafe.is_empty() 
        
        for menu in group:
            cafe.enqueue(menu)
        
        cafe.front()
        cafe.dequeue()

        if len(cafe.queue) >= 8:
            cafe.clear()

 
    cafe.clear()
    cafe.is_empty()
    print("\n[ 시뮬레이션이 모두 완료되었습니다. ]")

if __name__ == "__main__":
    main()
