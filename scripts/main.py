from matplotlib import pyplot

from classes import CityGrid


def main() -> None:
    """Create CityGrid and cover it with towers."""
    city = CityGrid(100, 50)
    city.change_obstructed(45)
    city.cover_with_towers(5)
    city.create_paths()
    pyplot.show()
    city.path_between_towers(
        city.towers[0].position,
        city.towers[-1].position,
    )
    pyplot.show()


if __name__ == '__main__':
    main()
