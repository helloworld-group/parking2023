import copt as cp
import numpy as np

# 正交多边形的外围坐标点
polygon_coordinates = [(0, 0), (5, 0), (5, 5), (2, 5), (2, 2), (0, 2)]
polygon_area = 14  # 替换为实际正交多边形的面积

# 创建线性规划问题
lp = cp.model.create()

# 创建变量
num_rectangles = len(polygon_coordinates)
w = lp.add_variable("w", shape=num_rectangles, kind="integer")
h = lp.add_variable("h", shape=num_rectangles, kind="integer")

# 添加目标函数
lp.set_objective("min", cp.dot([1] * num_rectangles, w * h))

# 添加约束条件
for j in range(len(polygon_coordinates)):
    constraint = np.zeros(num_rectangles)
    for i in range(num_rectangles):
        constraint[i] = (polygon_coordinates[j][0] >= 0 and polygon_coordinates[j][0] <= w[i] and
                         polygon_coordinates[j][1] >= 0 and polygon_coordinates[j][1] <= h[i])
    lp.add_constraint(constraint @ w == 1)

for i in range(num_rectangles):
    for j in range(i + 1, num_rectangles):
        lp.add_constraint(w[i] + w[j] <= 1)
        lp.add_constraint(h[i] + h[j] <= 1)

lp.add_constraint(cp.dot(w * h, [1] * num_rectangles) >= polygon_area)

# 求解问题
lp.solve(solver="cbc")

# 输出结果
print("Status:", lp.get_status())
print("Optimal Solution:")
for i in range(num_rectangles):
    print(f"Rectangle {i + 1}: Width={w.value[i]}, Height={h.value[i]}")
