import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from matplotlib import rcParams

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False

# 给定内角（顺时针方向）
internal_angles = [108, 108, 108, 108, 144, 144]
# 外角 = 180 - 内角
turn_angles = [180 - a for a in internal_angles]

# 计算每条边的方向（角度）
def compute_directions():
    angles = []
    current_angle = 0  # 初始朝右
    for turn in turn_angles:
        current_angle -= turn  # 顺时针
        angles.append(np.deg2rad(current_angle))
    return angles

# 给定边长，返回点坐标
def compute_points(edge_lengths):
    angles = compute_directions()
    points = [(0, 0)]
    for i in range(6):
        dx = edge_lengths[i] * np.cos(angles[i])
        dy = edge_lengths[i] * np.sin(angles[i])
        last = points[-1]
        points.append((last[0] + dx, last[1] + dy))
    return points

# 优化目标：让最后一个点尽量靠近起点，实现闭合
def closure_error(edge_lengths):
    points = compute_points(edge_lengths)
    end_x, end_y = points[-1]
    return (end_x)**2 + (end_y)**2  # 距离原点的平方

# 初始猜测：所有边长为1
initial_lengths = [1.0] * 6

# 约束：边长必须为正
bounds = [(0.1, 10)] * 6


# 最小化闭合误差
result = minimize(closure_error, initial_lengths, bounds=bounds)

# 获取闭合后的点
final_points = compute_points(result.x)

# 拆分x, y坐标用于绘图
x, y = zip(*final_points)

# 绘图
plt.figure(figsize=(6, 6))
plt.plot(x, y, marker='o')
plt.gca().set_aspect('equal')
plt.title('闭合六边形：4个108°，2个144°')
plt.show()
