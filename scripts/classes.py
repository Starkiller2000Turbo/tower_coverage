from math import sqrt
from random import sample
from typing import List, Set

from matplotlib import colors, patches, pyplot

from constants import (
    CITY_COLORS,
    CITY_LABELS,
    DEFAULT_OBSTRUCTED_PERCENTAGE,
    GRID_VALUES,
)
from objects import Path, Position, Tower
from utils import (
    additionally_optimize_place_for_tower,
    change_grid_from_data,
    create_grid_from_data,
    find_place_for_tower,
    find_tower_by_path,
    get_covered_area,
    get_percentage,
    get_percentage_amount,
)


class CityGrid:
    """Class for city grid."""

    def __init__(self, n: int, m: int) -> None:
        """Initialize class CityGrid.

        Args:
            n: rows amount (height).
            m: columns amount (width).
        """
        self.n = n
        self.m = m
        self.towers: List[Tower] = []
        self.paths: List[Path] = []
        self.min_percentage = DEFAULT_OBSTRUCTED_PERCENTAGE
        self.obstructed_amount = get_percentage_amount(
            m * n,
            self.min_percentage,
        )
        self.percentage = get_percentage(m * n, self.obstructed_amount)
        self.clear_map = set(
            [Position(i, j) for i in range(n) for j in range(m)],
        )
        self.obstructed_blocks = set(
            sample(self.clear_map, self.obstructed_amount),
        )
        self.clear_blocks = self.clear_map - self.obstructed_blocks
        self.covered_blocks: Set[Position] = set()
        self.uncovered_blocks: Set[Position] = self.clear_blocks.copy()
        self.obstructed_covered_blocks: Set[Position] = set()
        self.over_covered_blocks: Set[Position] = set()
        self.grid = create_grid_from_data(
            n,
            m,
            {GRID_VALUES['obstructed']: self.obstructed_blocks},
        )

    def get_name(self) -> str:
        """Create the name of class CityGrid.

        Returns:
            String with the name.
        """
        return f'CityGrid {self.n}x{self.m}. {self.percentage}% obstructed'

    def __str__(self) -> str:
        """Print class in comand line.

        Returns:
            Name attribute.
        """
        return self.get_name()

    def vizualize(self) -> None:
        """Show grid using matplotlib."""
        cmap = colors.ListedColormap(CITY_COLORS)
        city_figure = pyplot.figure()
        city_plot = city_figure.add_subplot(111)
        city_plot.set_title(self.get_name())
        city_plot.pcolor(
            self.grid,
            cmap=cmap,
            edgecolors='k',
            vmin=min(GRID_VALUES.values()),
            vmax=max(GRID_VALUES.values()),
        )
        color_patches = [
            patches.Patch(
                facecolor=CITY_COLORS[option],
                label=CITY_LABELS[option],
            )
            for option in range(len(CITY_COLORS))
        ]
        city_plot.legend(
            handles=color_patches,
            bbox_to_anchor=[0.5, -0.05],
            loc='upper center',
            ncol=len(CITY_COLORS) // 2,
        )

    def change_obstructed(self, percentage: float) -> None:
        """Change obstructed blocks percentage.

        Args:
            percentage: new obstructed blocks percentage.
        """
        self.clear_city()
        if not 100 >= percentage >= 0:
            raise Exception('Percentage should be in the range from 0 to 100')
        self.min_percentage = percentage
        new_obstructed_amount = get_percentage_amount(
            self.m * self.n,
            percentage,
        )
        if new_obstructed_amount > self.obstructed_amount:
            self.percentage = get_percentage(
                self.m * self.n,
                new_obstructed_amount,
            )
            new_obstructed_blocks = set(
                sample(
                    self.clear_blocks,
                    new_obstructed_amount - self.obstructed_amount,
                ),
            )
            self.clear_blocks -= new_obstructed_blocks
            self.uncovered_blocks = self.clear_blocks.copy()
            self.obstructed_blocks |= new_obstructed_blocks
            self.obstructed_amount = new_obstructed_amount
            change_grid_from_data(self.grid, {1: new_obstructed_blocks})
        elif new_obstructed_amount < self.obstructed_amount:
            self.percentage = get_percentage(
                self.m * self.n,
                new_obstructed_amount,
            )
            new_clear_blocks = set(
                sample(
                    self.obstructed_blocks,
                    self.obstructed_amount - new_obstructed_amount,
                ),
            )
            self.clear_blocks |= new_clear_blocks
            self.uncovered_blocks = self.clear_blocks.copy()
            self.obstructed_blocks -= new_clear_blocks
            self.obstructed_amount = new_obstructed_amount
            change_grid_from_data(
                self.grid,
                {GRID_VALUES['clear']: new_clear_blocks},
            )

    def place_tower(self, position: Position, tower_range: int) -> None:
        """Place tower to provided place.

        Args:
            position: position of tower.
            tower_range: range of tower.

        Returns:
            Created tower object.
        """
        if self.grid[position] in (
            GRID_VALUES['obstructed'],
            GRID_VALUES['obstructed covered'],
            GRID_VALUES['tower'],
        ):
            raise Exception('Forbidden to place the tower')
        tower = Tower(
            position,
            tower_range,
            get_covered_area(self.n, self.m, position, tower_range),
            [],
        )
        self.towers.append(tower)
        self.clear_blocks -= {tower.position}
        self.uncovered_blocks -= {tower.position}
        self.covered_blocks -= {tower.position}
        self.over_covered_blocks -= {tower.position}
        new_covered_blocks = self.uncovered_blocks & tower.covered
        new_obstructed_covered_blocks = self.obstructed_blocks & tower.covered
        new_over_covered_blocks = self.covered_blocks & tower.covered - {
            tower.position,
        }
        self.obstructed_covered_blocks |= new_obstructed_covered_blocks
        self.over_covered_blocks |= new_over_covered_blocks
        self.covered_blocks |= new_covered_blocks
        self.covered_blocks -= new_over_covered_blocks
        self.uncovered_blocks -= new_covered_blocks
        change_grid_from_data(
            self.grid,
            {
                GRID_VALUES['covered']: new_covered_blocks,
                GRID_VALUES[
                    'obstructed covered'
                ]: new_obstructed_covered_blocks,
                GRID_VALUES['over covered']: new_over_covered_blocks,
                GRID_VALUES['tower']: set([tower.position]),
            },
        )

    def clear_city(self) -> None:
        """Clear city grid from all towers and paths."""
        tower_blocks = {tower.position for tower in self.towers}
        self.clear_blocks |= tower_blocks
        self.uncovered_blocks = self.clear_blocks.copy()
        change_grid_from_data(
            self.grid,
            {
                GRID_VALUES['clear']: self.covered_blocks
                | self.over_covered_blocks
                | tower_blocks,
                GRID_VALUES['obstructed']: self.obstructed_covered_blocks,
            },
        )
        self.covered_blocks = set()
        self.over_covered_blocks = set()
        self.obstructed_covered_blocks = set()
        self.towers = []
        self.paths = []

    def cover_with_towers(self, tower_range: int) -> None:
        """Cover the whole city with minimum amount of towers.

        Args:
            tower_range: range og towers.
        """
        self.clear_city()
        while self.uncovered_blocks:
            closest_position = min(
                self.uncovered_blocks,
                key=lambda position: position.x + position.y,
            )
            optimized_place = find_place_for_tower(
                tower_range,
                closest_position,
                self.clear_blocks,
                self.uncovered_blocks,
                self.covered_blocks,
                self.n,
                self.m,
            )
            additionally_optimized_place = (
                additionally_optimize_place_for_tower(
                    optimized_place,
                    self.uncovered_blocks,
                    self.clear_blocks,
                    tower_range,
                    self.n,
                    self.m,
                )
            )
            self.place_tower(
                additionally_optimized_place,
                tower_range,
            )

    def create_paths(self) -> None:
        """Create paths between all towers on pyplot."""
        for index1 in range(len(self.towers)):
            for index2 in range(index1 + 1, len(self.towers)):
                tower1 = self.towers[index1]
                tower2 = self.towers[index2]
                tower_range = tower1.range
                position1 = tower1.position
                position2 = tower2.position
                if (
                    abs(position1.x - position2.x) <= 2 * tower_range + 1
                    and abs(position1.y - position2.y) <= 2 * tower_range + 1
                ):
                    self.paths.append(Path(position1, position2))
                    tower1.connections.append(position2)
                    tower2.connections.append(position1)
        self.vizualize()
        for path in self.paths:
            pyplot.plot(*zip(path.start[::-1], path.end[::-1]), 'k--')

    def path_between_towers(
        self,
        position1: Position,
        position2: Position,
    ) -> None:
        """Create path between two towers on pyplot.

        Args:
            position1: position of the first tower.
            position2: position of the second tower.
        """
        find_tower_by_path(self.towers, position1)
        find_tower_by_path(self.towers, position1)
        positions = [position1]
        paths = []
        while positions[-1] != position2:
            positions.append(
                min(
                    find_tower_by_path(self.towers, positions[-1]).connections,
                    key=lambda position: sqrt(
                        (position.x - position2.x) ** 2
                        + (position.y - position2.y) ** 2,
                    ),
                ),
            )
            paths.append(Path(positions[-2], positions[-1]))
        self.vizualize()
        for path in paths:
            pyplot.plot(*zip(path.start[::-1], path.end[::-1]), 'g--')
