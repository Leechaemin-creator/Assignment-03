import csv
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle

# ffmpeg 경로 직접 지정
plt.rcParams["animation.ffmpeg_path"] = r"C:\Users\user\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe"

# 한글 설정
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

MAX_QUEUE_SIZE = 10


def wrap_text(text, max_len=8):
    lines = []
    while len(text) > max_len:
        lines.append(text[:max_len])
        text = text[max_len:]
    lines.append(text)
    return "\n".join(lines)


def load_menus_from_csv():
    base_dir = Path(__file__).resolve().parent
    csv_path = base_dir / "menus.csv"

    menus = []

    if not csv_path.exists():
        return [
            "카페라떼", "아메리카노", "초코맛 바스크치케이크",
            "카푸치노", "바닐라라떼", "디카페인 아메리카노",
            "카라멜마끼아또", "돌체라떼", "티라미수",
            "녹차라떼", "콜드브루", "마카롱"
        ]

    encodings = ["utf-8-sig", "cp949"]

    for enc in encodings:
        try:
            with open(csv_path, "r", encoding=enc, newline="") as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) >= 5:
                        menus.extend(row[2:5])
            return menus
        except UnicodeDecodeError:
            menus = []
            continue

    raise UnicodeDecodeError(
        "menus.csv", b"", 0, 1,
        "지원되지 않는 인코딩입니다. UTF-8 또는 CP949로 저장해 주세요."
    )


def generate_frames(menus):
    frames = []
    queue = []

    # 시작
    frames.append((queue.copy(), "초기 상태: queue = []"))

    # isEmpty
    frames.append((queue.copy(), f"isEmpty 확인: {len(queue) == 0}"))

    for i, menu in enumerate(menus):
        # enqueue 전
        frames.append((queue.copy(), f'enqueue 준비: "{menu}"'))

        # enqueue
        if len(queue) < MAX_QUEUE_SIZE:
            queue.append(menu)
            frames.append((queue.copy(), f'enqueue 실행: "{menu}"'))
        else:
            frames.append((queue.copy(), f'overflow: "{menu}" 추가 불가'))

        # front
        if queue and (i % 3 == 1):
            frames.append((queue.copy(), f'front 확인: "{queue[0]}"'))

        # 크기 10 이하 유지
        if len(queue) >= 8:
            removed = queue.pop(0)
            frames.append((queue.copy(), f'dequeue 실행: "{removed}"'))

    # 마지막 front
    if queue:
        frames.append((queue.copy(), f'마지막 front: "{queue[0]}"'))

    # isEmpty 다시 확인
    frames.append((queue.copy(), f"isEmpty 확인: {len(queue) == 0}"))

    # clear 전에 dequeue 한두 번 더 보여주기
    for _ in range(min(2, len(queue))):
        removed = queue.pop(0)
        frames.append((queue.copy(), f'dequeue 실행: "{removed}"'))

    # clear
    frames.append((queue.copy(), "clear 준비"))
    queue.clear()
    frames.append((queue.copy(), "clear 실행: queue 비움"))

    # 마지막 isEmpty
    frames.append((queue.copy(), f"isEmpty 확인: {len(queue) == 0}"))

    frames.append((queue.copy(), "종료"))

    return frames


def draw_frame(frame):
    queue, message = frame

    ax = plt.gca()
    ax.clear()

    ax.set_title("Queue Animation", fontsize=16, pad=16)

    # 왼쪽 설명 영역
    ax.text(-1.5, 9.2, f"현재 연산: {message}", fontsize=12)
    ax.text(-1.5, 8.4, "자료구조: Queue / FIFO (First In, First Out)", fontsize=10)

    code_lines = [
        "queue = []",
        "queue.append(x)   # enqueue",
        "queue.pop(0)      # dequeue",
        "queue[0]          # front",
        "len(queue) == 0   # isEmpty",
        "queue.clear()     # clear",
    ]
    y0 = 6.8
    for idx, line in enumerate(code_lines):
        ax.text(-1.5, y0 - idx * 0.6, line, fontsize=10, family="monospace")

    # 오른쪽 큐 영역
    start_x = 8.5
    box_width = 2.8
    box_height = 1.2
    y = 4.0

    for i, item in enumerate(queue):
        is_front = (i == 0)
        is_rear = (i == len(queue) - 1)

        color = "#BFDBFE"
        if is_front and is_rear:
            color = "#FDE68A"
        elif is_front:
            color = "#FDBA74"
        elif is_rear:
            color = "#C4B5FD"

        x = start_x + i * box_width
        box = Rectangle(
            (x, y), box_width, box_height,
            facecolor=color,
            edgecolor="black",
            linewidth=1.5
        )
        ax.add_patch(box)

        wrapped = wrap_text(item, 8)
        ax.text(
            x + box_width / 2,
            y + box_height / 2,
            wrapped,
            ha="center",
            va="center",
            fontsize=8,
            linespacing=1.1
        )

    if queue:
        front_x = start_x + box_width / 2
        rear_x = start_x + (len(queue) - 1) * box_width + box_width / 2
        ax.text(front_x, y - 0.5, "FRONT", ha="center", fontsize=11)
        ax.text(rear_x, y + 1.35, "REAR", ha="center", fontsize=11)

    ax.set_xlim(-2, 38)
    ax.set_ylim(0, 10)
    ax.axis("off")


def main():
    ffmpeg_path = Path(plt.rcParams["animation.ffmpeg_path"])
    if not ffmpeg_path.exists():
        raise FileNotFoundError(f"ffmpeg.exe 경로를 찾을 수 없음: {ffmpeg_path}")

    menus = load_menus_from_csv()
    frames = generate_frames(menus)

    fig = plt.figure(figsize=(14, 6))
    ani = animation.FuncAnimation(
        fig,
        draw_frame,
        frames=frames,
        interval=1000,
        repeat=False
    )

    base_dir = Path(__file__).resolve().parent
    output_path = base_dir / "queue_animation.mp4"

    writer = animation.FFMpegWriter(fps=1)
    ani.save(str(output_path), writer=writer)

    plt.close(fig)
    print(f"MP4 생성 완료: {output_path}")


if __name__ == "__main__":
    main()
    