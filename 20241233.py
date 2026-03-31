import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
from matplotlib.animation import FuncAnimation
from collections import deque
import sys

def set_korean_font():
    candidates = ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'NanumBarunGothic']
    available = {f.name for f in fm.fontManager.ttflist}
    for font in candidates:
        if font in available:
            plt.rcParams['font.family'] = font
            plt.rcParams['axes.unicode_minus'] = False
            return
    
    for f in fm.fontManager.ttflist:
        if any(k in f.name for k in ['Gothic', 'Nanum', 'Malgun']):
            plt.rcParams['font.family'] = f.name
            plt.rcParams['axes.unicode_minus'] = False
            return

set_korean_font()

team_data = [
    {'학번': '20241233', '이름': '원솔은',  '단어': ['매실티', '플레인 휘낭시에', '레몬에이드']},
    {'학번': '20241261', '이름': '이채민',  '단어': ['얼그레이라떼', '캐모마일티', '모히또에이드']},
    {'학번': '20240743', '이름': '안서영',  '단어': ['말차라떼(제로슈가)', '초코 스콘(제로슈가)', '바스크치즈케이크']},
    {'학번': '20240749', '이름': 'jueun wi',  '단어': ['cafe latte', 'lemon tea', 'camomile tea']},
    {'학번': '20251177', '이름': '구수진',  '단어': ['카푸치노', '초코스콘', '자몽티']},
    {'학번': '20251213', '이름': '이승주',  '단어': ['바닐라라떼', '말차라떼', '초코 휘낭시에']},
    {'학번': '20251255', '이름': '진가연',  '단어': ['아메리카노', '카페모카', '바스크치즈케이크']},
]

all_words = [w for m in team_data for w in m['단어']]


class Queue:
    def __init__(self, max_size=10):
        self.data = deque()
        self.max_size = max_size

    def enqueue(self, item):
        if len(self.data) >= self.max_size:
            print('Queue Overflow!')
            return False
        self.data.append(item)
        return True

    def dequeue(self):
        if not self.data:
            print('Queue Underflow!')
            return None
        return self.data.popleft()

    def front(self):
        if not self.data:
            print('Queue가 비어있습니다.')
            return None
        return self.data[0]
    
    def isEmpty(self):
        return len(self.data) == 0
        
    def clear(self):
        self.data.clear()

queue = Queue(max_size=10)
history = []


print('사용 가능한 단어:')
for m in team_data:
    print(f"  [{m['이름']}] {' / '.join(m['단어'])}")
print()
print('명령어: enq <단어> / deq / front / isEmpty / clear / done(종료)')
print('-' * 55)

while True:
    try:
        cmd = input('>>> ').strip()
    except EOFError:
        break
    if not cmd:
        continue
    if cmd.lower() == 'done':
        break

    parts = cmd.split(maxsplit=1)
    op = parts[0].lower()

    if op == 'enq':
        if len(parts) < 2:
            print('단어를 입력하세요. 예: enqueue 벚꽃')
            continue
        word = parts[1].strip()
        if word not in all_words:
            print(f'  "{word}"은(는) 없는 단어입니다.')
            continue
        if queue.enqueue(word):
            history.append(('enqueue', word, list(queue.data)))
            print(f'  enqueue("{word}") -> {list(queue.data)}')
            
    elif op == 'deq':
        item = queue.dequeue()
        if item is not None:
            history.append(('dequeue', item, list(queue.data)))
            print(f'  dequeue() = "{item}" -> {list(queue.data)}')
            
    elif op == 'front':
        item = queue.front()
        if item is not None:
            history.append(('front', item, list(queue.data)))
            print(f'  front() = "{item}"')
            
    elif op == 'isempty':
        result = queue.isEmpty()
        history.append(('isempty', result, list(queue.data)))
        print(f'  isEmpty() = {result}')
        
    elif op == 'clear':
        queue.clear()
        history.append(('clear', None, list(queue.data)))
        print(f'  clear() 실행 완료 -> {list(queue.data)}')
        
    else:
        print('알 수 없는 명령어. enq / deq / front / isEmpty / clear / done 을 사용하세요.')

if not history:
    print("기록된 데이터가 없어 종료합니다.")
    sys.exit()

print(f'\n총 {len(history)}개 스텝 기록 완료 → 애니메이션 시작!')

MAX_QUEUE = 10
BOX_W = 1.35
BOX_H = 0.8
Y_CENTER = 0.5


BG        = '#1e1e2e'
SURFACE   = '#313244'
EMPTY     = '#45475a'
FILLED    = '#585b70'
TEXT      = '#cdd6f4'
IDX       = '#6c7086'
ENQ_C     = '#89dceb' 
DEQ_C     = '#f38ba8' 
FRONT_C   = '#a6e3a1' 
EMPTY_C   = '#f9e2af' 
CLEAR_C   = '#eba0ac' 
DARK      = '#1e1e2e'

fig, (ax_t, ax_b) = plt.subplots(2, 1, figsize=(13, 8), 
                                 gridspec_kw={'height_ratios': [1, 1.2]})
fig.patch.set_facecolor(BG)
plt.tight_layout(pad=4.0)

def draw(i):
    ax_t.cla(); ax_b.cla()
    op, item, state = history[i]

    ax_t.set_facecolor(BG)
    ax_t.set_xlim(0, 10); ax_t.set_ylim(0, 5)
    ax_t.axis('off')

    if op == 'enqueue':
        code, accent, badge = f'queue.enqueue("{item}")', ENQ_C, 'ENQUEUE'
    elif op == 'dequeue':
        code, accent, badge = f'queue.dequeue()\n-> "{item}"', DEQ_C, 'DEQUEUE'
    elif op == 'front':
        code, accent, badge = f'queue.front()\n-> "{item}"', FRONT_C, 'FRONT'
    elif op == 'isempty':
        code, accent, badge = f'queue.isEmpty()\n-> {item}', EMPTY_C, 'isEmpty'
    elif op == 'clear':
        code, accent, badge = f'queue.clear()', CLEAR_C, 'CLEAR'

    ax_t.text(5, 4.0, badge, fontsize=14, color=DARK, ha='center', va='center',
              fontweight='bold', bbox=dict(boxstyle='round,pad=0.5', facecolor=accent, edgecolor='none'))
    ax_t.text(5, 2.3, code, fontsize=20, color=accent, ha='center', va='center',
              bbox=dict(boxstyle='round,pad=0.8', facecolor=SURFACE, edgecolor=accent, linewidth=2.5))
    ax_t.text(5, 0.8, f'Step {i+1} / {len(history)}  |  Size: {len(state)} / {MAX_QUEUE}', 
              fontsize=12, color=TEXT, ha='center')

    
    ax_b.set_facecolor(BG)
    ax_b.set_xlim(-1, MAX_QUEUE * BOX_W + 1)
    ax_b.set_ylim(-0.5, 2.5)
    ax_b.axis('off')

    
    pipe_color = CLEAR_C if op == 'clear' else EMPTY
    ax_b.plot([-0.5, MAX_QUEUE * BOX_W - 0.2], [Y_CENTER - 0.1, Y_CENTER - 0.1], color=pipe_color, lw=2)
    ax_b.plot([-0.5, MAX_QUEUE * BOX_W - 0.2], [Y_CENTER + BOX_H + 0.1, Y_CENTER + BOX_H + 0.1], color=pipe_color, lw=2)
    
    ax_b.text(-0.8, Y_CENTER + BOX_H/2 + 0.1, '출구\n(Front)', color=DEQ_C, ha='center', va='center', fontsize=10, fontweight='bold')
    ax_b.text(MAX_QUEUE * BOX_W + 0.3, Y_CENTER + BOX_H/2 + 0.1, '입구\n(Rear)', color=ENQ_C, ha='center', va='center', fontsize=10, fontweight='bold')

    
    for j in range(MAX_QUEUE):
        x = j * BOX_W
        box_edge = EMPTY_C if op == 'isempty' else EMPTY
        ax_b.add_patch(mpatches.FancyBboxPatch((x, Y_CENTER), BOX_W - 0.1, BOX_H,
            boxstyle='round,pad=0.05', facecolor=SURFACE, edgecolor=box_edge, lw=1, alpha=0.3))
        ax_b.text(x + BOX_W/2 - 0.05, Y_CENTER - 0.4, f'[{j}]', fontsize=9, color=IDX, ha='center')

    
    for j, word in enumerate(state):
        x = j * BOX_W
        is_front = (j == 0)
        is_rear = (j == len(state) - 1)
        
        
        if op == 'front' and is_front: fc, ec, tc = FRONT_C, FRONT_C, DARK
        elif op == 'enqueue' and is_rear: fc, ec, tc = ENQ_C, ENQ_C, DARK
        else: fc, ec, tc = FILLED, '#7f849c', TEXT

        ax_b.add_patch(mpatches.FancyBboxPatch((x, Y_CENTER), BOX_W - 0.1, BOX_H,
            boxstyle='round,pad=0.05', facecolor=fc, edgecolor=ec, lw=2))
        ax_b.text(x + BOX_W/2 - 0.05, Y_CENTER + BOX_H/2, word, fontsize=11, color=tc,
                  ha='center', va='center', fontweight='bold')

    
    if op == 'dequeue':
        ghost_x = -1.2
        ax_b.add_patch(mpatches.FancyBboxPatch((ghost_x, Y_CENTER), BOX_W - 0.1, BOX_H,
            boxstyle='round,pad=0.05', facecolor=DEQ_C, edgecolor=DEQ_C, lw=2, alpha=0.5))
        ax_b.text(ghost_x + BOX_W/2 - 0.05, Y_CENTER + BOX_H/2, item, fontsize=10, color=DARK,
                  ha='center', va='center', fontweight='bold')
        ax_b.annotate('', xy=(-1.5, Y_CENTER + BOX_H/2), xytext=(-0.2, Y_CENTER + BOX_H/2),
                     arrowprops=dict(arrowstyle='->', color=DEQ_C, lw=2))

    fig.suptitle('Queue (FIFO) Animation', fontsize=16, color=TEXT, y=0.95)

anim = FuncAnimation(fig, draw, frames=len(history), interval=1800, repeat=True)
plt.show()