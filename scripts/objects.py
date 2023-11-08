from collections import namedtuple

Position = namedtuple('Position', 'x y', defaults=(0, 0))
Tower = namedtuple(
    'Tower',
    'position range covered connections',
)
Path = namedtuple(
    'Path',
    'start end',
    defaults=(Position(0, 0), Position(0, 0)),
)
