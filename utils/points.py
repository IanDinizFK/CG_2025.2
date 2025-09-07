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

