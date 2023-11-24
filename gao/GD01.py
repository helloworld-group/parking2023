from matplotlib import pyplot as plt

plt.plot([0, 0, 100, 100, 0], [0, 50, 50, 0, 0], color='blue')

width = 2.5 # 车位宽度
length = 5.4 # 车位长度

x_limit = 100
x_count = 0
y_limit = 50
y_count = 0

for j in range(x_limit):
    x = j * width + length
    y1 = 0
    y2 = 50 - length
    x_count = x_count + 1
    if x + width >= x_limit - length:
        break
    else:
        plt.plot([x, x, x + width, x + width, x], [y1, y1 + length, y1 + length, y1, y1], color='orange')
        plt.plot([x, x, x + width, x + width, x], [y2, y2 + length, y2 + length, y2, y2], color='orange')

for j in range(y_limit):
    y = j*width+length
    x1 = 0
    x2 = 100 - length
    y_count = y_count + 1
    if y + width >= y_limit - length:
        break
    else:
        plt.plot([x1, x1, x1 + length, x1 + length, x1], [y, y + width, y + width, y, y], color='red')
        plt.plot([x2, x2, x2 + length, x2 + length, x2], [y, y + width, y + width, y, y], color='red')

print(f'y_count=', y_count)
print(f'total=',2 * x_count + 2*y_count)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()




