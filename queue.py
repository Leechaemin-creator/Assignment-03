import csv
import time
import os
from collections import deque

MAX_SIZE = 10


def load_words(filepath="queue.csv"):
    words = []
    members = []

    with open(filepath, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        # 헤더에 공백이나 따옴표가 들어가 있어도 정리
        reader.fieldnames = [
            name.strip().strip("'").strip('"')
            for name in reader.fieldnames
        ]

        for row in reader:
            clean_row = {}
            for k, v in row.items():
                clean_key = k.strip().strip("'").strip('"')
                clean_value = v.strip() if v else ""
                clean_row[clean_key] = clean_value

            members.append({
                "이름": clean_row["이름"],
                "학번": clean_row["학번"]
            })

            for key in ["단어1", "단어2", "단어3"]:
                if clean_row.get(key):
                    words.append(clean_row[key])

    return words, members


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause(sec=1.3):
    time.sleep(sec)

def format_item(text, width):
    text = str(text)
    if len(text) > width:
        return text[:width - 1] + "…"
    return text


def format_item(text, width):
    text = str(text)
    if len(text) > width:
        return text[:width - 1] + "…"
    return text


def draw_queue(queue, message=""):
    items = list(queue)
    box_width = 22

    print("현재 큐 상태\n")
    print("        front")
    print("         ↓")

    for i in range(MAX_SIZE):
        if i < len(items):
            item = format_item(items[i], box_width)
        else:
            item = ""

        print("      ┌" + "─" * box_width + "┐")
        print("       " + f"{item:^{box_width}}")
        print("      └" + "─" * box_width + "┘")

        if i == 0:
            print("         ↑ front")
        if len(items) > 0 and i == len(items) - 1:
            print("         ↓ rear")

    print()

    if len(items) == 0:
        print("      front = rear = 없음")
    else:
        print(f'      front = "{items[0]}"')
        print(f'      rear  = "{items[-1]}"')

    print(f"      size = {len(items)} / {MAX_SIZE}")

    if message:
        print(f"\n▶ {message}")

    print()


def animate(queue, members, message):
    clear_screen()
    draw_queue(queue, message)
    pause()


def is_empty(queue):
    return len(queue) == 0


def front(queue):
    if is_empty(queue):
        return None
    return queue[0]


def enqueue(queue, value):
    if len(queue) < MAX_SIZE:
        queue.append(value)
        return True
    return False


def dequeue(queue):
    if is_empty(queue):
        return None
    return queue.popleft()


def clear_queue(queue):
    queue.clear()


def main():
    words, members = load_words("queue.csv")
    queue = deque()

    # 1. 큐 선언
    animate(queue, members, "큐를 선언합니다")

    # 2. isEmpty 사용
    animate(queue, members, f"isEmpty() -> {is_empty(queue)}")

    # 3. 모든 단어를 한 번 이상 사용
    for word in words:
        if len(queue) >= MAX_SIZE:
            removed = dequeue(queue)
            animate(queue, members, f'dequeue() -> "{removed}"')

        enqueue(queue, word)
        animate(queue, members, f'enqueue() -> "{word}"')

    # 4. front 사용
    current_front = front(queue)
    animate(queue, members, f'front() -> "{current_front}"')

    # 5. dequeue 사용
    if not is_empty(queue):
        removed = dequeue(queue)
        animate(queue, members, f'dequeue() -> "{removed}"')

    # 6. clear 사용
    animate(queue, members, "clear() 실행 전")
    clear_queue(queue)
    animate(queue, members, "clear() 실행 후")

    # 7. isEmpty 다시 확인
    animate(queue, members, f"isEmpty() -> {is_empty(queue)}")

    # 8. 종료 화면
    clear_screen()
    draw_queue(queue, "애니메이션 완료")


if __name__ == "__main__":
    main()