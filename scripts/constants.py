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
CITY_COLORS = list(COLORS.values())
CITY_LABELS = list(COLORS.keys())
DEFAULT_OBSTRUCTED_PERCENTAGE = 30.0
TOTAL_PERCENTAGE = 100
