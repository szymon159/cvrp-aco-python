"""Implementation for the class representing City"""
import math

class City:
    """Class representing a single city with its position and demand"""
    def __init__(self, x_pos: float, y_pos: float, demand: float) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.demand = demand

    def __str__(self) -> str:
        return F"Pos = ({self.x_pos},{self.y_pos}), demand = {self.demand}"

    def distance(self, other: "City") -> float:
        """Calculates distance to other city passed as other"""
        d_x = self.x_pos - other.x_pos
        d_y = self.y_pos - other.y_pos
        return math.hypot(d_x, d_y)
