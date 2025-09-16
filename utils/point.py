from typing import Self

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @staticmethod
    def input() -> Self:
        x = int(input("Digite o valor de x: "))
        y = int(input("Degite o valor de y: "))

        return Point(x, y)

        