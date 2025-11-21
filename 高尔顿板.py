import numpy as np
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']   # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus'] = False     # 允许负号正常显示
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ========== 参数区域 ==========
n_rows = 12        # 钉子层数（对应二项分布的 n）
n_balls = 2000     # 总小球数
p_right = 0.7      # 向右的概率，你可以改 0.5, 0.6, 0.8 等
fps = 25           # 动画帧率
save_gif = True    # 是否保存为 gif

# ========== 模拟小球落点 ==========
# 每个小球的“向右次数” ~ Binomial(n_rows, p_right)
# 落点索引就可以直接用向右次数：0, 1, ..., n_rows
rng = np.random.default_rng(seed=42)
positions = rng.binomial(n_rows, p_right, size=n_balls)

# ========== 搭建图像 ==========
fig, ax = plt.subplots(figsize=(6, 4))

# 槽的编号 0,1,...,n_rows
bins_index = np.arange(n_rows + 1)

# 初始的柱状图，高度全为 0
bars = ax.bar(bins_index, np.zeros_like(bins_index), align='center')

ax.set_xlim(-0.5, n_rows + 0.5)
ax.set_ylim(0, n_balls * 0.25)  # 上界可以根据喜好调
ax.set_xlabel("落点位置（向右次数）")
ax.set_ylabel("小球数量")
title = ax.set_title(f"Galton Board (p_right = {p_right:.2f}) | balls = 0")

# ========== 动画更新函数 ==========
def update(frame):
    """
    frame 表示当前已经“落下”的小球数量
    """
    # 取前 frame 个小球的落点
    current_positions = positions[:frame]
    counts = np.bincount(current_positions, minlength=n_rows + 1)

    # 更新每根柱子的高度
    for bar, h in zip(bars, counts):
        bar.set_height(h)

    title.set_text(
        f"Galton Board (p_right = {p_right:.2f}) | balls = {frame}"
    )
    return (*bars, title)

# 帧数：可以设置为 n_balls，或者略少（比如每 5 个球更新一帧）
frames = np.linspace(1, n_balls, num=200, dtype=int)  # 200 帧，平滑一点

anim = FuncAnimation(
    fig,
    update,
    frames=frames,
    interval=1000 / fps,  # 每帧间隔（毫秒）
    blit=True
)

# ========== 保存或展示 ==========
if save_gif:
    # 需要提前安装 pillow：pip install pillow
    anim.save("galton_board.gif", writer="pillow", fps=fps)
    print("已保存为 galton_board.gif")

plt.show()
