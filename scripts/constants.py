from collections import OrderedDict

COLORS = OrderedDict(
    [
        ('clear', '#ffe4e1'),
        ('obstructed', '#741b47'),
        ('covered', '#ffff00'),
        ('obstructed covered', '#9f0000'),
        ('over covered', '#e69138'),
        ('tower', '#6fa8dc'),
    ],
)
GRID_VALUES = OrderedDict(
    [
        ('clear', 0),
        ('obstructed', 1),
        ('covered', 2),
        ('obstructed covered', 3),
        ('over covered', 4),
        ('tower', 5),
    ],
)
CITY_COLORS = list(COLORS.values())
CITY_LABELS = list(COLORS.keys())
DEFAULT_OBSTRUCTED_PERCENTAGE = 30.0
TOTAL_PERCENTAGE = 100
TEST_WIDTH = 100
TEST_HEIGHT = 100
TEST_PERCENTAGE = 73.5
TEST_RANGE = 10
TEST_TOWERS_AMOUNT = 10
