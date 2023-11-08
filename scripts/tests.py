from unittest import TestCase, main

from classes import CityGrid
from constants import DEFAULT_OBSTRUCTED_PERCENTAGE

TEST_WIDTH = 100
TEST_HEIGHT = 100
TEST_PERCENTAGE = 73.5


class TestCityGridAttributes(TestCase):
    """Класс для тестирования аттрибутов класса CityGrid."""

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
            'Сетка неверного размера',
        )

    def test_city_str(self) -> None:
        """Test __str__ method."""
        city = TestCityGridAttributes.city  # type: ignore[attr-defined]
        self.assertEqual(city.get_name(), str(city), 'Displayed incorrectly')


class TestCityGridMethods(TestCase):
    """Класс для тестирования методов класса CityGrid."""

    def setUp(self) -> None:
        """Подготовка данных для тестирования."""
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
        """Проверка замены процента затруднения."""
        city = TestCityGridAttributes.city  # type: ignore[attr-defined]
        city.change_obstructed(
            TEST_PERCENTAGE,
        )
        self.assertEqual(
            TEST_PERCENTAGE,
            city.min_percentage,
            'Проценты сохранены неправильно',
        )
        self.assertGreaterEqual(
            city.percentage,  # type: ignore[attr-defined]
            TEST_PERCENTAGE,
            'Процент меньше заданного',
        )
        self.check_attributes(city)

    def test_clear_city(self) -> None:
        """Проверка замены процента затруднения."""
        city = TestCityGridAttributes.city  # type: ignore[attr-defined]
        for _ in range(10):
            clear_position = city.clear_blocks.pop()
            city.place_tower(clear_position, 10)
        city.clear_city()
        self.assertGreaterEqual(
            city.towers,
            [],
            'Some towers left',
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


if __name__ == '__main__':
    main()
