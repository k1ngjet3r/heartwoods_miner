import math
from utils.utils import Coordinate

C1 = Coordinate(1, 2)
C2 = Coordinate(-1, 0, _type='rock')

class TestGroup:
    def test_coordinate_addition(self):
        assert C1 + C2 == Coordinate(0, 2)

    def test_coordinate_substraction(self):
        assert C1 - C2 == Coordinate(2, 2)

    def test_negitave_coordinate(self):
        assert -C1 == Coordinate(-1, -2)
        assert -C2 == Coordinate(1, 0, _type='rock')

    def test_distance(self):
        C1.distance_to(C2) == math.sqrt(8)
