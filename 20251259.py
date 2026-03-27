import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mp
from matplotlib.animation import FuncAnimation, FFMpegWriter
import matplotlib.font_manager as fm
import subprocess

# ── 한글 폰트 ──────────────────────────────────────────────────
r = subprocess.run(['fc-list', ':lang=ko'], capture_output=True, text=True)
fonts = [l.split(':')[0].strip() for l in r.stdout.splitlines() if l.strip()]
if fonts:
    fm.fontManager.addfont(fonts[0])
    prop = fm.FontProperties(fname=fonts[0])
    plt.rcParams['font.family'] = prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

# ── 색상 ───────────────────────────────────────────────────────
BG    = '#1a1a2e'
PANEL = '#16213e'
TW    = '#ffffff'
TG    = '#aaaacc'
CARD  = '#0f3460'
BORDER = '#4466aa'
EMPTY  = '#0a1628'

# ── 데이터 (이름·학번 제외, 메뉴만) ───────────────────────────
members = [
    ['카페라떼',     '카푸치노',       '말차라떼'],
    ['바닐라라떼',   '말차라떼',       '초코휘낭시에'],
    ['카푸치노',     '초코스콘',       '자몽티'],
    ['카페라떼',     '레몬티',         '캐모마일티'],
    ['말차라떼',     '초코스콘',       '바스크치즈케이크'],
    ['바닐라라떼',   '카페라떼',       '바스크치즈케이크'],
    ['아메리카노',   '카페모카',       '바스크치즈케이크'],
    ['매실티',       '플레인휘낭시에', '레몬에이드'],
]

MAX = 10

# ── 시나리오 빌드 ──────────────────────────────────────────────
# 각 스텝: (code_line, queue_snapshot, highlight_idx)
# highlight_idx: 강조할 슬롯 인덱스 (None이면 없음)
steps = []

# 1) 큐 선언
steps.append(('카페무솔트 = Queue(maxsize=10)', [], None))

# 2) isEmpty
steps.append(('카페무솔트.isEmpty()  →  True', [], None))

# 3) enqueue / 필요시 dequeue
q = []
for menus in members:
    for menu in menus:
        if len(q) >= MAX:
            old = q.pop(0)
            steps.append((f'카페무솔트.dequeue()  →  "{old}"', list(q), None))
        q.append(menu)
        steps.append((f'카페무솔트.enqueue("{menu}")', list(q), len(q) - 1))

# 4) front
if q:
    steps.append((f'카페무솔트.front()  →  "{q[0]}"', list(q), 0))

# 5) 나머지 dequeue
while len(q) > 1:
    old = q.pop(0)
    steps.append((f'카페무솔트.dequeue()  →  "{old}"', list(q), None))

# 6) front (마지막 1개)
if q:
    steps.append((f'카페무솔트.front()  →  "{q[0]}"', list(q), 0))

# 7) clear
steps.append(('카페무솔트.clear()', [], None))

# 8) isEmpty
steps.append(('카페무솔트.isEmpty()  →  True', [], None))

# ── 프레임 데이터 생성 ─────────────────────────────────────────
HOLD = 14   # 스텝당 유지 프레임 수
fdata = []
for code, qu, hl in steps:
    for _ in range(HOLD):
        fdata.append((code, list(qu), hl))
# 마지막 정지
for _ in range(20):
    fdata.append(fdata[-1])

# ── Figure 레이아웃 (메뉴판·로그 패널 제거) ────────────────────
fig = plt.figure(figsize=(11, 7), facecolor=BG)
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

# 제목 영역
ax_t = fig.add_axes([0.0, 0.88, 1.0, 0.12])
# 연산 코드 영역
ax_o = fig.add_axes([0.05, 0.60, 0.90, 0.27])
# 큐 시각화 영역
ax_q = fig.add_axes([0.05, 0.06, 0.90, 0.52])

for ax in [ax_t, ax_o, ax_q]:
    ax.set_facecolor(PANEL)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_edgecolor('#2a2a4a')

# ── 제목 (정적) ───────────────────────────────────────────────
ax_t.set_xlim(0, 1); ax_t.set_ylim(0, 1)
ax_t.set_facecolor('#0d0d1a')
ax_t.text(0.5, 0.68, '카페무솔트  Queue  애니메이션',
          ha='center', va='center', fontsize=17, fontweight='bold', color=TW)
ax_t.text(0.5, 0.22, 'enqueue  ·  dequeue  ·  front  ·  isEmpty  ·  clear',
          ha='center', va='center', fontsize=9, color=TG)

# 진행 바 핸들
prog = [None]

def draw_op(code):
    """연산 코드 패널 갱신"""
    ax_o.clear()
    ax_o.set_facecolor(PANEL)
    ax_o.set_xticks([]); ax_o.set_yticks([])
    for s in ax_o.spines.values(): s.set_edgecolor('#2a2a4a')
    ax_o.set_xlim(0, 1); ax_o.set_ylim(0, 1)

    # 코드 박스
    ax_o.add_patch(mp.FancyBboxPatch(
        (0.03, 0.25), 0.94, 0.50,
        boxstyle='round,pad=0.03',
        facecolor='#0a0a1e', edgecolor='#445577', linewidth=1.5))
    ax_o.text(0.5, 0.52, code,
              ha='center', va='center',
              fontsize=13, color=TW,
              fontfamily=plt.rcParams['font.family'])


def draw_queue(qu, hl):
    """큐 시각화 패널 갱신"""
    ax_q.clear()
    ax_q.set_facecolor(PANEL)
    ax_q.set_xticks([]); ax_q.set_yticks([])
    for s in ax_q.spines.values(): s.set_edgecolor('#2a2a4a')
    ax_q.set_xlim(-0.3, 10.3); ax_q.set_ylim(-0.15, 2.0)

    # Front / Rear 레이블
    ax_q.text(-0.15, 1.72, 'Front', ha='center', va='center',
              fontsize=9, color=TG, fontweight='bold')
    ax_q.text(9.15, 1.72, 'Rear', ha='center', va='center',
              fontsize=9, color=TG, fontweight='bold')
    # 화살표
    ax_q.annotate('', xy=(0.4, 1.55), xytext=(-0.1, 1.55),
                  arrowprops=dict(arrowstyle='->', color=TG, lw=1.2))
    ax_q.annotate('', xy=(8.6, 1.55), xytext=(9.1, 1.55),
                  arrowprops=dict(arrowstyle='->', color=TG, lw=1.2))

    # 슬롯 10개
    for i in range(MAX):
        filled = i < len(qu)
        face  = CARD  if filled else EMPTY
        edge  = BORDER if filled else '#223344'
        lw    = 2.0 if i == hl else 1.2

        ax_q.add_patch(mp.FancyBboxPatch(
            (i + 0.08, 0.45), 0.84, 0.95,
            boxstyle='round,pad=0.04',
            facecolor=face, edgecolor=edge, linewidth=lw))

        if filled:
            txt = qu[i]
            if len(txt) > 6:
                txt = txt[:5] + '…'
            ax_q.text(i + 0.5, 0.93, txt,
                      ha='center', va='center',
                      fontsize=7.5, color=TW, fontweight='bold')

        # 인덱스
        ax_q.text(i + 0.5, 0.22, str(i),
                  ha='center', va='center', fontsize=7, color=TG)

    # Size 표시
    ax_q.text(5.0, 0.0, f'size : {len(qu)} / {MAX}',
              ha='center', va='center', fontsize=9, color=TG)


def animate(fi):
    code, qu, hl = fdata[fi]
    draw_op(code)
    draw_queue(qu, hl)

    # 진행 바
    if prog[0]:
        try: prog[0].remove()
        except: pass
    p = mp.Rectangle((0, 0), fi / len(fdata), 0.08,
                     facecolor='#445577', edgecolor='none',
                     transform=ax_t.transAxes, clip_on=False)
    ax_t.add_patch(p)
    prog[0] = p
    return []


print(f'총 {len(fdata)} 프레임 렌더링 시작...')
anim = FuncAnimation(fig, animate, frames=len(fdata), interval=50, blit=False)
writer = FFMpegWriter(fps=20, bitrate=1400)
anim.save('/mnt/user-data/outputs/20251259.mp4', writer=writer, dpi=110)
print('저장 완료')
plt.close()
