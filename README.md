### Задача покрытия города вышками

### Описание:

Проект Towers Coverage - проект, созданный в рамках знакомства с matplotlib. В данном проекте имеется класс для сетки города, содержащий свободные и затруднённые участки (где нельзя размещать вышки). В результате можно с помощью специального метода cover_with_towers покрыть город минимальным количеством вышек.

Также предусмотрено создание сети из ближайших вышек. И нахождение кратчайшего пути между двумя вышками.

### Как установить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Starkiller2000Turbo/tower_coverage.git
cd tower_coverage
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
make pip
make req
```

Отредактируйте файл scripts/main.py и запустите проект:

```
make run
```

### Стек технологий использованный в проекте:

- Python
- Matplotlib
- Collections
- NumPy
- Unittest

### Автор:

- :white_check_mark: [Starkiller2000Turbo](https://github.com/Starkiller2000Turbo)