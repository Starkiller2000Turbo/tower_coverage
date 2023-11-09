from unittest import TestCase, main

from classes import CityGrid
from constants import (
    DEFAULT_OBSTRUCTED_PERCENTAGE,
    TEST_HEIGHT,
    TEST_PERCENTAGE,
    TEST_RANGE,
    TEST_TOWERS_AMOUNT,
    TEST_WIDTH,
)


class TestCityGridAttributes(TestCase):
    """Class for CityGrid attributes testing."""

    @classmethod
    def setUpClass(cls) -> None:
        """Create data for testing."""
        super().setUpClass()
        cls.city = CityGrid(  # type: ignore[attr-defined]
            TEST_WIDTH,
            TEST_HEIGHT,
        )

    def test_saved_data(self) -> None:
        """Test saving input data."""
        city = TestCityGridAttributes.city  # type: ignore[attr-defined]
        self.assertEqual(TEST_WIDTH, city.m, 'Width saved incorrectly')
        self.assertEqual(TEST_HEIGHT, city.n, 'Height saved incorrectly')
        self.assertEqual(
            DEFAULT_OBSTRUCTED_PERCENTAGE,
            city.min_percentage,
            'Percentage saved incorrectly',
        )

    def test_creating_attributes(self) -> None:
        """Test creating attributes."""
        city = TestCityGridAttributes.city  # type: ignore[attr-defined]
        self.assertGreaterEqual(
            city.percentage,
            DEFAULT_OBSTRUCTED_PERCENTAGE,
            'Percentage is less than specified',
        )
        self.assertEqual(
            city.clear_blocks & city.obstructed_blocks,
            set(),
            'Some blocks are clear and obstructed at the same time',
        )
        self.assertEqual(
            city.uncovered_blocks,
            city.clear_blocks,
            'Uncovered blocks are not equal clear blocks at initialization',
        )

    def test_creating_grid(self) -> None:
        """Test grid creation."""
        city = TestCityGridAttributes.city  # type: ignore[attr-defined]
        self.assertEqual(
            (TEST_HEIGHT, TEST_WIDTH),
            city.grid.shape,
            'Grid has wrong shape',
        )

    def test_city_str(self) -> None:
        """Test __str__ method."""
        city = TestCityGridAttributes.city  # type: ignore[attr-defined]
        self.assertEqual(city.get_name(), str(city), 'Displayed incorrectly')


class TestCityGridMethods(TestCase):
    """Class for CityGrid methods testing."""

    def setUp(self) -> None:
        """Create data for testing."""
        self.city = CityGrid(  # type: ignore[attr-defined]
            TEST_WIDTH,
            TEST_HEIGHT,
        )

    def check_attributes(self, city: CityGrid) -> None:
        """Check attributes of CityGrid class."""
        self.assertEqual(
            city.covered_blocks & city.uncovered_blocks,
            set(),
            'Some blocks are covered and uncovered at the same time',
        )
        self.assertEqual(
            (city.clear_blocks | {tower.position for tower in city.towers})
            & city.obstructed_blocks,
            set(),
            'Some blocks are clear and obstructed at the same time',
        )
        self.assertEqual(
            city.covered_blocks
            | city.uncovered_blocks
            | city.over_covered_blocks,
            city.clear_blocks,
            'Covered and uncovered blocks do not make up clear blocks',
        )

    def test_change_obstructed(self) -> None:
        """Test obstructed percentage changing."""
        city = TestCityGridAttributes.city  # type: ignore[attr-defined]
        city.change_obstructed(
            TEST_PERCENTAGE,
        )
        self.assertEqual(
            TEST_PERCENTAGE,
            city.min_percentage,
            'Min percentage saved incorrectly',
        )
        self.assertGreaterEqual(
            city.percentage,  # type: ignore[attr-defined]
            TEST_PERCENTAGE,
            'Real percentage is less than specified',
        )
        self.check_attributes(city)

    def change_place_tower(self) -> None:
        """Test placing tower."""
        city = TestCityGridAttributes.city  # type: ignore[attr-defined]
        clear_place = city.clear_blocks[-1]
        city.place_tower(clear_place, TEST_RANGE)
        towers = city.towers
        self.assertEqual(
            len(towers),
            1,
            'Tower not placed or placed more than one time',
        )
        tower = city.towers[0]
        self.assertEqual(
            tower.position,
            clear_place,
            'Tower placed at the wrong spot',
        )
        self.assertEqual(tower.range, TEST_RANGE, 'Tower has incorrect range')

    def test_clear_city(self) -> None:
        """Test cleat city."""
        city = TestCityGridAttributes.city  # type: ignore[attr-defined]
        for _ in range(TEST_TOWERS_AMOUNT):
            clear_position = city.clear_blocks.pop()
            city.place_tower(clear_position, TEST_RANGE)
        city.clear_city()
        self.assertGreaterEqual(
            city.towers,
            [],
            'Some towers left',
        )
        self.assertGreaterEqual(
            city.paths,
            [],
            'Some paths left',
        )
        self.assertEqual(city.covered_blocks, set(), 'Covered blocks left')
        self.assertEqual(
            city.over_covered_blocks,
            set(),
            'Over covered blocks left',
        )
        self.assertEqual(
            city.obstructed_covered_blocks,
            set(),
            'Obstructed covered blocks left',
        )
        self.check_attributes(city)

    def test_cover_with_towers(self) -> None:
        """Test method cover_with_towers."""
        city = TestCityGridAttributes.city  # type: ignore[attr-defined]
        city.cover_with_towers(TEST_RANGE)
        self.assertNotEqual(
            city.towers,
            [],
            'No towers created',
        )
        self.assertEqual(city.uncovered_blocks, set(), 'Uncovered blocks left')
        self.check_attributes(city)


if __name__ == '__main__':
    main()
