import math
import yaml
import logging
from pathlib import Path

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class Coordinate:
    def __init__(self, x, y, _type=None):
        self.x = x
        self.y = y
        self._type = _type

    def __str__(self):
        return f"({self.x}, {self.y} - {self._type})"

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

    def __neg__(self):
        return Coordinate(-self.x, -self.y, self._type)

    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def is_close_to(self, other, threshold=20.0):
        distance = self.distance_to(other)
        return distance <= threshold

    staticmethod
    def append_if_not_close(new_coordinate, coordinates_list, threshold=20):
        if len(coordinates_list) == 0:
            coordinates_list.append(new_coordinate)
        else:
            for coord in coordinates_list:
                if new_coordinate.is_close_to(coord, threshold):
                    break
            else:
                coordinates_list.append(new_coordinate)

    @staticmethod
    def find_closest_coordinate(coordinates_list, center):
        distances = [center.distance_to(coor) for coor in coordinates_list]
        return min(distances)

    @staticmethod
    def sort_coordinates_by_distance(coordinates_list, center):
        return sorted(coordinates_list, key=lambda coord: center.distance_to(coord))

    @staticmethod
    def valid_move(coordinates_list, position, center, absolute_boundary):
        sorted_coordinate_list = sorted(coordinates_list, \
                                key=lambda coord: position.distance_to(coord))
        LOGGER.debug(f'sorted list: {[str(c) for c in sorted_coordinate_list]}')
        for coord in sorted_coordinate_list:
            vector = coord - center
            absolute_coord = position + vector
            LOGGER.debug(f'Coordinate: {coord}, vector: {str(vector)}, absolute coor: {absolute_coord}')
            if absolute_boundary.is_within_boundary(absolute_coord):
                LOGGER.debug(f'{coord} is the closest and within boundary')
                vector._type = coord._type
                return vector
        else:
            LOGGER.debug('No valid move available')

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
    data = _load_yaml_file('params/dimensions.yaml')
    return {key: Coordinate(value[0], value[1]) for key, value in data.items()}

if __name__ == '__main__':
    # rlt = []
    # current = Coordinate(2, 2)
    # center = Coordinate(2, 2)
    # c1 = Coordinate(4, 0, _type='a')

    # absolute_boundary = Boundary(
    #     x_max=5,
    #     x_min=0,
    #     y_max=5,
    #     y_min=0
    # )
    # l = [c1]
    # v = Coordinate.valid_move(
    #     coordinates_list=l,
    #     position=current,
    #     center=center,
    #     absolute_boundary=absolute_boundary
    # )
    # print('valid move', str(v))

    # current += v
    # print('position after move', str(current))

    # c2 = Coordinate(3, 1)
    # l2 = [c2]
    # v2 = Coordinate.valid_move(
    #     coordinates_list=l,
    #     position=current,
    #     center=center,
    #     absolute_boundary=absolute_boundary
    # )
    # print('valid move', str(v2))

    # c4 = c2-c1
    # c4._type = 'd'
    # print(c4.x)
    # print(c4.y)
    # print(c4._type)

    print(load_dimension_params())
