from typing import List, Tuple

from utils.matrix import translation_matrix, scale_matrix, apply_matrix_point, shear_matrix


Point = Tuple[float, float]

def aplicar_translacao(pontos: List[Point], tx: float, ty: float) -> List[Point]:
    """Aplica translação (tx, ty) a uma lista de pontos."""
    mat = translation_matrix(tx, ty)
    return [apply_matrix_point(mat, x, y) for x, y in pontos]


def aplicar_escala(pontos: List[Point], sx: float, sy: float, cx: float = 0.0, cy: float = 0.0) -> List[Point]:
    """Aplica escala (sx, sy) em torno de (cx, cy) a uma lista de pontos."""
    mat = scale_matrix(sx, sy, cx, cy)
    return [apply_matrix_point(mat, x, y) for x, y in pontos]

# Placeholders para próximas operações
def aplicar_rotacao(pontos: List[Point], angulo_graus: float, cx: float = 0.0, cy: float = 0.0) -> List[Point]:
    raise NotImplementedError("Rotação será implementada futuramente.")

def aplicar_reflexao(pontos: List[Point], tipo: str) -> List[Point]:
    """tipo: 'x', 'y', 'origem', 'y=x'"""
    raise NotImplementedError("Reflexão será implementada futuramente.")


def aplicar_cisalhamento(pontos: List[Point], shx: float = 0.0, shy: float = 0.0, cx: float = 0.0, cy: float = 0.0) -> List[Point]:
    """Aplica cisalhamento nos eixos X e/ou Y usando matrizes homogêneas."""
    mat = shear_matrix(shx, shy, cx, cy)
    return [apply_matrix_point(mat, x, y) for x, y in pontos]


