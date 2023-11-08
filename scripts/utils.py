from math import ceil
from typing import Any, Dict, List, Set, Union

from numpy import floating, inf, ndarray, zeros

from constants import TOTAL_PERCENTAGE
from objects import Position, Tower


def find_tower_by_path(towers: List[Tower], position: Position) -> Tower:
    """Find tower by its path.

    Args:
        towers: list of towers.
        position: specified position of tower.

    Returns:
        Founded tower.

    Raises:
        Exception if tower was not found.
    """
    for tower in towers:
        if tower.position == position:
            return tower
    raise Exception('Tower not found in this position')


def get_percentage_amount(total_amount: int, percentage: float) -> int:
    """Get a minimum share with a percentage greater than specified.

    Args:
        total_amount: total amount.
        percentage: specified percentage.

    Returns:
        Minimum share with a percentage greater than specified.
    """
    return ceil(total_amount / TOTAL_PERCENTAGE * percentage)


def get_percentage(total_amount: int, amount: int) -> float:
    """Calculate share percentage.

    Args:
        total_amount: total ampunt.
        amount: share.

    Returns:
        Calculated percentage.
    """
    return amount / total_amount * TOTAL_PERCENTAGE


def create_grid_from_data(
    n: int,
    m: int,
    data: Dict[Any, Set[Position]],
) -> ndarray:
    """Create grid from data.

    Args:
        n: rows amount (height).
        m: columns amount (width).
        data: values (except 0) with set of positions.

    Returns:
        Created grid.
    """
    grid = zeros((n, m))
    for value, positions in data.items():
        for position in positions:
            grid[position] = value
    return grid


def change_grid_from_data(
    grid: ndarray,
    data: Dict[Any, Set[Position]],
) -> None:
    """Change specified grid using data.

    Args:
        grid: grid to change.
        data: values (except 0) with set of positions.
    """
    for value, positions in data.items():
        for position in list(positions):
            grid[position] = value


def get_covered_area(
    n: int,
    m: int,
    position: Position,
    tower_range: int,
) -> Set[Position]:
    """Get whole covered area of tower.

    Args:
        n: rows amount (height).
        m: columns amount (width).
        position: tower position.
        tower_range: tower range.

    Returns:
        Set of covered positions.
    """
    left = max(0, position.y - tower_range)
    right = min(m, position.y + tower_range)
    up = min(n, position.x + tower_range)
    down = max(0, position.x - tower_range)
    return set(
        [
            Position(i, j)
            for i in range(down, up + 1)
            for j in range(left, right + 1)
            if i != position.x or j != position.y
        ],
    )


def get_total_covered_area(
    n: int,
    m: int,
    position: Position,
    tower_range: int,
) -> Set[Position]:
    """Get whole covered area of tower.

    Args:
        n: rows amount (height).
        m: columns amount (width).
        position: tower position.
        tower_range: tower range.

    Returns:
        Set of covered positions.
    """
    left = max(0, position.y - tower_range)
    right = min(m, position.y + tower_range)
    up = min(n, position.x + tower_range)
    down = max(0, position.x - tower_range)
    return set(
        [
            Position(i, j)
            for i in range(down, up + 1)
            for j in range(left, right + 1)
        ],
    )


def get_left_bottom_neighbors_in_range(
    position: Position,
    neighbors_range: int,
) -> List[Position]:
    """Get neighbors placed to the left below in specified range.

    Args:
        position: starting position.
        neighbors_range: range to neighbors.

    Returns:
        List of neighbors.
    """
    return [
        Position(i, position.y - neighbors_range)
        for i in range(position.x, position.x - neighbors_range - 1, -1)
    ] + [
        Position(position.x - neighbors_range, j)
        for j in range(position.y - neighbors_range + 1, position.y + 1)
    ]


def find_place_for_tower(
    tower_range: int,
    closest_tower_position: Position,
    clear_blocks: Set[Position],
    uncovered_blocks: Set[Position],
    covered_blocks: Set[Position],
    n: int,
    m: int,
) -> Position:
    """Find place for tower.

    Args:
        tower_range: tower range.
        farthest_tower_position: farthest tower position.

    Returns:
        Founded clodest position to the start.
    """
    farthest_tower_position = Position(
        min(closest_tower_position.x + tower_range, n),
        min(closest_tower_position.y + tower_range, m),
    )
    optimal_position = closest_tower_position
    optimal_covered_area = get_covered_area(
        n,
        m,
        optimal_position,
        tower_range,
    )
    optimal_covered = len(uncovered_blocks & optimal_covered_area)
    optimal_over_covered = len(covered_blocks & optimal_covered_area)
    optimized = True
    distance = 0
    while optimized and distance <= tower_range:
        neighbors = get_left_bottom_neighbors_in_range(
            farthest_tower_position,
            distance,
        )
        clear_neighbors = list(
            filter(lambda neighbor: neighbor in clear_blocks, neighbors),
        )
        if len(clear_neighbors) != 0:
            optimized = False
            for neighbor in clear_neighbors:
                covered_area = get_total_covered_area(
                    n,
                    m,
                    neighbor,
                    tower_range,
                )
                covered = len(uncovered_blocks & covered_area)
                over_covered = len(covered_blocks & covered_area)
                if (
                    covered >= optimal_covered
                    and over_covered <= optimal_over_covered
                ) and not (
                    covered == optimal_covered
                    and over_covered == optimal_over_covered
                ):
                    optimal_position = neighbor
                    optimal_covered = covered
                    optimal_over_covered = over_covered
                    optimized = True
        distance += 1
    return optimal_position


def calculate_avg_y_distance(
    positions: Set[Position],
) -> Union[floating[Any], float]:
    """Calculate average distance from (0,0) to every position.

    Args:
        positions: positions to calculate average distance.

    Returns:
        Average distance to all positions.
    """
    if len(positions) == 0:
        return inf
    return sum([position.y for position in positions]) / len(positions)


def calculate_avg_x_distance(
    positions: Set[Position],
) -> Union[floating[Any], float]:
    """Calculate average distance from (0,0) to every position.

    Args:
        positions: positions to calculate average distance.

    Returns:
        Average distance to all positions.
    """
    if len(positions) == 0:
        return inf
    return sum([position.x for position in positions]) / len(positions)


def get_min_x_with_min_y(
    positions: Set[Position],
) -> Position:
    """Calculate average distance from (0,0) to every position.

    Args:
        positions: positions to calculate average distance.

    Returns:
        Average distance to all positions.
    """
    if len(positions) == 0:
        return Position(inf, inf)
    return min(positions)


def get_min_y_with_min_x(
    positions: Set[Position],
) -> Position:
    """Calculate average distance from (0,0) to every position.

    Args:
        positions: positions to calculate average distance.

    Returns:
        Average distance to all positions.
    """
    if len(positions) == 0:
        return Position(inf, inf)
    return min(positions, key=lambda position: (position.y, position.x))


def additionally_optimize_place_for_tower(
    start_position: Position,
    uncovered_blocks: Set[Position],
    save_blocks: Set[Position],
    tower_range: int,
    n: int,
    m: int,
) -> Position:
    """Optimize place for tower by average distance.

    Args:
        start_position: specified position to start optimization.
        uncovered_blocks: uncovered bu towers blocks.
        save_blocks: blocks on which the tower can be located.
        tower_range: tower range.
        n: rows amount (height).
        m: columns amount (width).

    Returns:
        Set of covered positions.
    """
    optimal_position = start_position
    optimal_covered = get_total_covered_area(
        n,
        m,
        optimal_position,
        tower_range,
    )
    uncovered_in_x_range = {
        block
        for block in uncovered_blocks - optimal_covered
        if optimal_position.x - tower_range
        <= block.x
        <= optimal_position.x + tower_range
    }
    optimal_average_y_distance = calculate_avg_y_distance(
        uncovered_in_x_range,
    )
    optimal_min_y_element = get_min_y_with_min_x(
        uncovered_in_x_range,
    )
    uncovered_in_y_range = {
        block
        for block in uncovered_blocks - optimal_covered
        if optimal_position.y - tower_range
        <= block.y
        <= optimal_position.y + tower_range
    }
    optimal_average_x_distance = calculate_avg_x_distance(
        uncovered_in_y_range,
    )
    optimal_min_x_element = get_min_x_with_min_y(
        uncovered_in_y_range,
    )
    left_allowed = True
    bottom_allowed = True
    while left_allowed or bottom_allowed:
        closest_left = Position(optimal_position.x, optimal_position.y - 1)
        while closest_left not in save_blocks:
            closest_left = Position(closest_left.x, closest_left.y - 1)
            if closest_left.y < 0:
                left_allowed = False
                break
        closest_bottom = Position(optimal_position.x - 1, optimal_position.y)
        while closest_bottom not in save_blocks:
            closest_bottom = Position(closest_bottom.x - 1, closest_bottom.y)
            if closest_bottom.x < 0:
                bottom_allowed = False
                break
        if left_allowed and (
            not bottom_allowed
            or (
                optimal_position.y - closest_left.y
                <= optimal_position.x - closest_bottom.x
            )
        ):
            lefter_covered = get_total_covered_area(
                n,
                m,
                closest_left,
                tower_range,
            )
            uncovered_in_x_range = {
                block
                for block in uncovered_blocks - lefter_covered
                if optimal_position.x - tower_range
                <= block.x
                <= optimal_position.x + tower_range
            }
            lefter_average_y_distance = calculate_avg_y_distance(
                uncovered_in_x_range,
            )
            lefter_min_y_element = get_min_y_with_min_x(
                uncovered_in_x_range,
            )
            if (
                lefter_average_y_distance <= optimal_average_y_distance
                and lefter_min_y_element.y <= optimal_min_y_element.y
                and len(lefter_covered & uncovered_blocks)
                <= len(optimal_covered & uncovered_blocks)
            ):
                left_allowed = False
            else:
                optimal_average_y_distance = lefter_average_y_distance
                optimal_min_y_element = lefter_min_y_element
                optimal_covered = lefter_covered
                optimal_position = closest_left
                uncovered_in_y_range = {
                    block
                    for block in uncovered_blocks - optimal_covered
                    if optimal_position.y - tower_range
                    <= block.y
                    <= optimal_position.y + tower_range
                }
                optimal_average_x_distance = calculate_avg_x_distance(
                    uncovered_in_y_range,
                )
                optimal_min_x_element = get_min_x_with_min_y(
                    uncovered_in_y_range,
                )
        elif bottom_allowed:
            lower_covered = get_total_covered_area(
                n,
                m,
                closest_bottom,
                tower_range,
            )
            uncovered_in_y_range = {
                block
                for block in uncovered_blocks - lower_covered
                if optimal_position.y - tower_range
                <= block.y
                <= optimal_position.y + tower_range
            }
            lower_average_x_distance = calculate_avg_x_distance(
                uncovered_in_y_range,
            )
            lower_min_x_element = get_min_x_with_min_y(
                uncovered_in_y_range,
            )
            if (
                lower_average_x_distance <= optimal_average_x_distance
                and lower_min_x_element.x <= optimal_min_x_element.x
                and len(lower_covered & uncovered_blocks)
                <= len(optimal_covered & uncovered_blocks)
            ):
                bottom_allowed = False
            else:
                optimal_average_x_distance = lower_average_x_distance
                optimal_min_x_element = lower_min_x_element
                optimal_position = closest_bottom
                optimal_covered = lower_covered
                uncovered_in_x_range = {
                    block
                    for block in uncovered_blocks - optimal_covered
                    if optimal_position.x - tower_range
                    <= block.x
                    <= optimal_position.x + tower_range
                }
                optimal_average_y_distance = calculate_avg_y_distance(
                    uncovered_in_x_range,
                )
                optimal_min_y_element = get_min_y_with_min_x(
                    uncovered_in_x_range,
                )
    return optimal_position
