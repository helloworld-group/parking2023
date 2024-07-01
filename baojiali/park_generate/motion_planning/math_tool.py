import numpy as np

def distance2segment(P, A, B):
    """
    计算点 P 到线段 AB 的最短距离，并给出交点。
    P, A, B: 二维点，格式为 (x, y)
    返回值: 距离，交点（格式为 (x, y)）
    """
    # 将点转换为 numpy 数组
    P = np.array(P)
    A = np.array(A)
    B = np.array(B)
    
    # 计算向量
    AP = P - A
    AB = B - A
    
    # 计算向量 AB 的长度的平方
    AB_squared = np.dot(AB, AB)
    
    if AB_squared == 0:
        # 如果 A 和 B 是同一个点
        return np.linalg.norm(P - A), tuple(A)
    
    # 计算投影系数 t
    t = np.dot(AP, AB) / AB_squared
    
    if t < 0:
        # 投影点在 A 之外
        closest_point = A
    elif t > 1:
        # 投影点在 B 之外
        closest_point = B
    else:
        # 投影点在线段 AB 之间
        closest_point = A + t * AB
    
    # 计算最短距离
    distance = np.linalg.norm(P - closest_point)
    return distance, tuple(closest_point)


if __name__ == "__main__":
    # 示例使用
    P = (3, 4)
    A = (1, 2)
    B = (7, 8)

    distance, intersection_point = distance2segment(P, A, B)
    print(f"The shortest distance from point {P} to segment AB between {A} and {B} is {distance:.2f}")
    print(f"The closest point on the segment to {P} is {intersection_point}")