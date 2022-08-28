"""Implementation for the class representing City"""
import math

class City:
    """Class representing a single city with its position and demand"""
    def __init__(self, x, y, demand):
        self.x = x
        self.y = y
        self.demand = demand

    def __str__(self):
        return F"Pos = ({self.x},{self.y}), demand = {self.demand}"

    def distance(self, other):
        """Calculates distance to other city passed as other"""
        dx = self.x - other.x
        dy = self.y - other.y
        return math.hypot(dx, dy)
