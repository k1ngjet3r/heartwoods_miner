import math
import yaml

from pathlib import Path

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(self.x + other.x, self.y + other.y)
        else:
            raise TypeError("Can only add another Coordinate object")

    def __sub__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(self.x - other.x, self.y - other.y)
        else:
            raise TypeError("Can only subtract another Coordinate object")

    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def is_close_to(self, other, threshold=1.0):
        distance = self.distance_to(other)
        return distance <= threshold

class Boundary(Coordinate):
    def __init__(self, x_min, y_min, x_max, y_max):
        super().__init__(x_max, y_max)
        self.x_min = x_min
        self.y_min = y_min

    def is_within_boundary(self, point:Coordinate):
        return self.x_min <= point.x <= self.x and self.y_min <= point.y <= self.y

def _load_yaml_file(yaml_filepath:str):
    path = Path(yaml_filepath)
    with open(path, 'r') as yml:
        data = yaml.safe_load(yml)
    return data

def load_mvmt_params() -> list[dict]:
    return _load_yaml_file('params/mvmt.yaml')

def load_dimension_params() -> list[tuple]:
    return _load_yaml_file('params/dimensions.yaml')

if __name__ == '__main__':
    print(load_dimension_params())