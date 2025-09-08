from typing import List, Tuple

Point = Tuple[float, float]


def parse_points(text: str) -> List[Point]:
    """Parse points from a multiline string.

    Supported formats per line:
      - (x, y)
      - x, y
      - x y

    Ignores empty lines. Raises ValueError if no valid points
    are found or if a line cannot be parsed into two floats.
    """
    points: List[Point] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue

        for ch in "()[]{}":
            line = line.replace(ch, "")
        line = line.replace(";", ",")

        parts = [p for p in (line.split(",") if "," in line else line.split()) if p != ""]
        if len(parts) != 2:
            raise ValueError(f"Linha inválida: '{raw}'")
        try:
            x = float(parts[0])
            y = float(parts[1])
        except Exception as exc:
            raise ValueError(f"Não foi possível converter para float: '{raw}'") from exc
        points.append((x, y))

    if not points:
        raise ValueError("Nenhum ponto informado.")
    return points


def normalize_points(points: List[Point]) -> List[Point]:
    """Normaliza os pontos para caberem dentro da viewport [-1, 1] x [-1, 1]."""
    if not points:
        return []

    xs = [x for x, y in points]
    ys = [y for x, y in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # Evita divisão por zero
    width_x = max_x - min_x if max_x > min_x else 1.0
    width_y = max_y - min_y if max_y > min_y else 1.0

    # Escala para caber em [-1, 1]
    normalized = []
    for x, y in points:
        nx = -1.0 + 2.0 * (x - min_x) / width_x
        ny = -1.0 + 2.0 * (y - min_y) / width_y
        normalized.append((nx, ny))

    return normalized
