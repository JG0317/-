# 绘制六边形

要求：

- 六个顶点构成一个闭合多边形（六边形）
- 每个顶点的**内角分别为：36°, 108°, 144°, 144°, 144°, 144°**
- 不要求边长一致（可变），但图形必须闭合

------

## 🔧 使用方法：优化几何向量来闭合路径

------

## 🧩 一、导入库和设置中文支持

```
pythonCopyEditimport numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from matplotlib import rcParams

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False
```

> 我们用 `numpy` 做数学计算，`matplotlib` 来画图，`scipy.optimize.minimize` 来做闭合优化。

------

## 🧩 二、定义角度

```
pythonCopyEditinternal_angles = [36, 108, 144, 144, 144, 144]
turn_angles = [180 - a for a in internal_angles]
```

- **internal_angles**：你提供的六个内角
- **turn_angles**：因为我们在平面上画图是“一个边→转弯→下一边”，所以真正用的是“**外角**”，也就是每个顶点的转弯角 = 180° - 内角。

------

## 🧩 三、根据外角计算每条边的方向

```
pythonCopyEditdef compute_directions():
    angles = []
    current_angle = 0  # 初始方向（x轴正方向）
    for turn in turn_angles:
        current_angle -= turn  # 顺时针旋转（减）
        angles.append(np.deg2rad(current_angle))  # 转为弧度
    return angles
```

- 这是一个从起始方向出发，顺时针依次转弯的过程。
- 最后返回每条边对应的方向角（弧度制），用于生成坐标。

------

## 🧩 四、根据方向和边长，计算所有顶点坐标

```
pythonCopyEditdef compute_points(edge_lengths):
    angles = compute_directions()
    points = [(0, 0)]
    for i in range(6):
        dx = edge_lengths[i] * np.cos(angles[i])
        dy = edge_lengths[i] * np.sin(angles[i])
        last = points[-1]
        points.append((last[0] + dx, last[1] + dy))
    return points
```

- 从点 `(0, 0)` 出发，按方向和边长依次画出六条边
- 每条边是一个向量，用三角函数计算 `dx`, `dy`
- 累加这些点，构成多边形的顶点序列

------

## 🧩 五、定义优化目标：闭合误差

```
pythonCopyEditdef closure_error(edge_lengths):
    points = compute_points(edge_lengths)
    end_x, end_y = points[-1]
    return (end_x)**2 + (end_y)**2  # 终点离原点的距离平方
```

- 理想情况下，最后一个点要回到原点 `(0,0)`
- 所以我们要优化的目标是：**“让路径终点尽量接近起点”**

------

## 🧩 六、运行优化器，自动找出边长

```
pythonCopyEditinitial_lengths = [1.0] * 6
bounds = [(0.1, 10)] * 6  # 每条边长度允许范围

result = minimize(closure_error, initial_lengths, bounds=bounds)
```

- 初始猜测：六条边都是 1.0
- 允许优化器在边长范围内自由调节，寻找使路径闭合的解

------

## 🧩 七、获取结果并绘图

```
pythonCopyEditfinal_points = compute_points(result.x)
x, y = zip(*final_points)

plt.figure(figsize=(6, 6))
plt.plot(x, y, marker='o')
plt.gca().set_aspect('equal')
plt.title('闭合六边形：1个36°，1个108°，4个144°')
plt.grid(True)
plt.show()
```

- 用优化出的边长 `result.x` 重新计算顶点坐标
- 使用 matplotlib 画出闭合的六边形

------

## ✅ 最终效果：

- **六个点，六条边，图形闭合**
- **角度精确符合要求：[36°, 108°, 144°, 144°, 144°, 144°]**
- **边长自动调整，满足几何约束**

------

如你想查看优化后的边长（数值），可以加一行：

```
python


CopyEdit
print("优化后的边长：", result.x)
```
