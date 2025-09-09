from typing import List, Tuple


Matrix3 = List[List[float]]


def multiply_matrices(a: Matrix3, b: Matrix3) -> Matrix3:
    """Multiplica duas matrizes 3x3 (lista de listas)."""
    res = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            res[i][j] = sum(a[i][k] * b[k][j] for k in range(3))
    return res


def apply_matrix_point(mat: Matrix3, x: float, y: float) -> Tuple[float, float]:
    """Aplica matriz 3x3 homogênea a um ponto (x, y)."""
    nx = mat[0][0] * x + mat[0][1] * y + mat[0][2]
    ny = mat[1][0] * x + mat[1][1] * y + mat[1][2]
    w = mat[2][0] * x + mat[2][1] * y + mat[2][2]
    if w != 0:
        nx /= w
        ny /= w
    return nx, ny


def translation_matrix(tx: float, ty: float) -> Matrix3:
    return [
        [1.0, 0.0, tx],
        [0.0, 1.0, ty],
        [0.0, 0.0, 1.0],
    ]


def scale_matrix(sx: float, sy: float, cx: float = 0.0, cy: float = 0.0) -> Matrix3:
    """Escala em torno do ponto (cx, cy)."""
    # T(cx,cy) * S(sx,sy) * T(-cx,-cy)
    t1 = translation_matrix(-cx, -cy)
    s = [
        [sx, 0.0, 0.0],
        [0.0, sy, 0.0],
        [0.0, 0.0, 1.0],
    ]
    t2 = translation_matrix(cx, cy)
    return multiply_matrices(t2, multiply_matrices(s, t1))

def shear_matrix(shx: float, shy: float, cx: float = 0.0, cy: float = 0.0) -> Matrix3:
    
    # Translada o centro para a origem
    t1 = translation_matrix(-cx, -cy)

    # Matriz de cisalhamento
    s = [
        [1.0, shx, 0.0],  # x' = x + shx*y
        [shy, 1.0, 0.0],  # y' = y + shy*x
        [0.0, 0.0, 1.0]
    ]

    # Translada de volta para o centro original
    t2 = translation_matrix(cx, cy)

    # Matriz final: T(cx,cy) * S(shx,shy) * T(-cx,-cy)
    return multiply_matrices(t2, multiply_matrices(s, t1))



