import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from libs.slopes.slopes import count_trees

import pytest

challenge_input = '''...#..............#.#....#..#..
...#..#..#..............#..#...
....#.#.......#............#...
..##.....##.........#........##
...#...........#...##.#...#.##.
..#.#...#....#.....#........#..
....##.###.....#..#.......#....
.#..##...#.....#......#..#.....
............##.#...#.#.....#.#.
..........#....#....#.#...#...#
..##....#.#.#......#.........#.
#.#.........#..............##..
....##.##......................
....##..#...........#..........
..#..#.#........##....#......#.
..............#..#....#.....#..
.............#...#.....#...#...
.#...........#..........#...#..
.#......#.......#......#.......
#..#.............#..#....##.###
........#.#...........##.#...#.
......#..#.....##......#.......
.....#.....#....#..............
#...##.#......#......#...#.....
...........................#...
...#....................#.....#
..#.....#...#.....##.....#.....
....................#......#..#
.......#.....##......##....#...
#........##...#.....##..#...#..
........#..#.#......#..###..#.#
##.....#.............#.#....#..
..#.................#....######
.#.#..#.....#.#..........#.#...
.........#....#...#............
........#..#.....#.............
............#.#.............##.
...#....#..#......#............
.##....#.....#...#.#...........
..#..............#...........##
.....#.#.##...#................
..........#..#.#..........##..#
..#....#...#...#.....######....
....#.#..#........#....#.###...
.......................#.......
..#.....#.##................#..
.....#......#..#.....#........#
.#...###.......#.#.........#..#
............#..................
..#.........##.........##......
#...........#.#.......###.#....
.#...#.....#.........###.....#.
.#............#........#..#....
...##.#......##................
........#...#...#...#..........
.......#.##......##.#..........
....##.......#..#....#....#....
......#.........###........#...
#....#....####....##......#....
......................#....#.#.
...#.#.#....#.#...#...#......#.
......#.....##.#...........###.
#........#.........##......#.#.
....##.....#.....#..#..........
......#...#...#.........#...##.
..#........#..................#
.........#..##.#..#..#...#.#..#
.....#.....#...#.....###.....##
.............#....#...#........
..........#.#.#...#..#...#....#
#...............##.......#.....
#...#.............#..#...#....#
..#...#...##...##...#..#.......
..#..#........#.#...........#..
.....#.....#..................#
....#....##....###..###...##...
..#......###.........##....#.##
.......#.##...#.......#..#.....
...#.#.#.#.....##..#..#........
................##....#.#......
..#...#...#...#.....##.#...#..#
..#..#.....#..##....#....#.....
.###...#......#........#.....##
##......#..#........#..........
....#...#..#....##..#......####
.#.....##....#..........#......
.#...#....#.........#...#....#.
.....#..#.#..#......#..##....#.
...#.##...#...#........#......#
.#..#...#.#..#.........#...#...
#....#......##.....#.......#...
..##............##..#.#.#...#..
##.......#.......##............
#......#.##........#...#...#...
.#.#.......##.........#..#.#...
.............##.#........#.....
.#..#...###...#..#.............
.....#...#..#....#.......#.....
#.#.........#.#.#...#...#.#....
.....#.......#.##.##...#....#..
.#.##..#.....#...#.#.#.#.#..#..
..........#...................#
.....#.#.#...##.........#..#..#
.#..#....##......#...#.........
.##......#......#...#........#.
.....##.#......#............#.#
.#.....##..#...........##......
.....#......#.......##....#....
..#..##..........#.#..........#
#.#.......##..#..##.#....#.....
.......#..#.#.......##......#.#
....#...##...#..............#..
.....#.........#......#...##...
#.........#........##..#.....#.
.#.#..#.....##.......#......#..
........#..#....#.....###..#...
#.#..#.#..........#............
..#......##..#....#.........#..
#..............................
.......#............#..#..#.#..
.#.....#.#....#..#.##.#........
.......#.###.#........##.#..#..
..............#....#.....##.#..
#..............#....#.###......
.#..#..#...###............#...#
.#.##...#....#..#...#...#......
......##..#..#......#..#....#..
.........#.......##............
...........##...#..#....####...
.#..................#..........
#...#..#..................#....
..............#.....##.....#...
..#.#..#...##..#.....#.....#..#
....#....#.#.........#.....#...
.#.......#...#....#...#.#..#..#
#.........##.....##.......#...#
#..#............#....#........#
..........##...#......#....#...
.......#..##...............#...
#............#.#.#.....#.......
.#........##...#...............
..##....#.....#..#.##.#......#.
.#...#.............#...#.....#.
...##....#.......#......#.#..#.
#......................#..#.##.
...#..........#..#.........#...
..#......#.......#.#....#......
....#............#...#......#..
.....#..#..##...#...#.........#
.....#......#....#....#........
.............#..#..........#...
....#..............#.....#.#...
....#.................#.#...#.#
.........#.#...........###.#.##
#...........#..##.#....#.##.#..
#.#.....#......................
##.#.........#....##.#.#..#.#..
#..........#.#.#.#.#..#..##..#.
..#...#..###.........#......#..
.....#......#..#.#............#
...........#...#.#.#.###....#..
#....#..#.......##.#.......##..
..............#.....##.#.......
.#.....#.#..#.........#.#.#..#.
..#..#..#..#................#..
...........#..#.#...#.........#
.#..#..#...#........#...#.#..#.
...#.#..#......#..#............
........#......##.....#....#...
#...#......##.#.#..............
.#........................#....
#.#.....#.##.....#..#.#........
#..........##.#.......#....#..#
#...#..#..#.....#....#....#....
#...........#..#.#....##.##....
##......#..#........#.......##.
#........#..#...#..........#...
...#...#......##....#.#........
...##..#..#.##....#...#........
#.#..#....#...#........#.......
..........#.......#..........#.
......##...#....###...#....#...
........#..#.....#......#......
....#.........##...#..##......#
....#...........#.#..#.#.#.#..#
..#......#..#......#........#.#
#..#....#.....#.............#..
............................#..
#...#.#.....#...#....#....#....
........#...#...#...#...#......
.###........#....#.##.....##.#.
.........#.....#..........#....
.#.........#....##.#.....#.....
#..#....................##.#...
..##.#.............#....#.#....
..#.#........#............##.#.
#........#...##.....#...#.....#
.........#.#..........#....#..#
...###.#..#.#......#.#.....#...
......#.....#..#...#........#..
.......#...#.....#....#....#..#
.#.#........#......##.......#..
#.................###..........
#........#.#..#....#..#........
..##....#.#...##...#...##....#.
...#.#......##...#.....#..#....
#..#........#...###....#.......
##.#....#..#.#..........#......
....#...###...#.....#........#.
..#.#........#....##.#.........
......##.##.................##.
.#....##...#.#..#.#............
.#...###........#......#.......
##..#.#......#..#..#...#.......
.......##..#....#........#....#
......#..........#.............
....##..##..#......#.#.........
.....#....................##...
...###.....#.....#...#.#.##.#..
....#.#..#.......#..#......##..
.......#.#..#.##.#...#......#..
...#.#....#.#...#..##...#...#..
#.##...#....#..#.............#.
...#...#...#.......#..........#
.#..#.............#..##.#......
....#.......#..............#.#.
..................#..#.....##.#
.#...#..#......#..........#...#
..#.#.....#..#....#....#####.#.
.......###.......#....#....#...
......#.#........#...#.........
......#..#.#.#....#.#.#....##..
.#...#.#...##.#......#.........
#....#..##....#.#.......#....#.
..##.#.....#.....#.........#...
......#......#....#....#.....#.
...##.....#....#......#......#.
......#......##............#.#.
.##.#.......#....#...#....#....
....#..#..#...##.......#..#....
....#....#...#.#........#..#...
....#.....#..........#..#......
....#....#...#.....#..##.....#.
##...#..##......#....##..#..#..
.....##.##..............##.....
#.#....#.##..#....#...##.......
..#.....##.....#.....######...#
...#.....#.#.#......#......##.#
...........##.............#....
...##......#..#......#...#.....
....#.##......#..#....#.#..#...
.#..#....#...#..#.....##.......
.....#..#.................#..#.
................#..#...#......#
...##....#.....#..#....##......
....##...............##...#....
......#..........#..##.........
.......###.......#.........#..#
......................#....#.#.
#.#.....#...##............#....
........#......##......#.....#.
...#....#....#.#..##.#..#.#.#..
..#.#....#.##...#..#.....#.#...
............#....#..#.......#..
#...#...#.#......#...##.....#.#
......#....#....#.......#......
....#.......#..........#....#..
........#####........#....#....
......#....##..............#.#.
....#....#.......#.......#.....
.##.#....##....#...............
#.....##........#..#.#...#.#...
...#......##....#..............
.#.....#.....#.......##....##..
#....#..........#.#..#.........
......##..........##.......#...
.##......##.....#.#....#......#
....#......................#...
.#...........###........#...#..
#.#..#..#..#...##.#....#.#..#..
...##...........#.#..........#.
......#.#..#....#....#.........
....#....#.#......#.........##.
.#..#...#...##....#...#......#.
#.#......#...#.#.#...........#.
##.....#..........##....##..##.
...#.#.....#..##........#......
..#........##........#..#......
.......#...............##..#...
.......#.#....#..###...........
.............#........#...#....
#.................#......#..#..
...#....#..#..............#...#
.............#....##....#..##..
#........#..........##...##...#
............#....#.....#.#....#
.....#..............##..#...#..
..#....#......###....#.#...##..
....##......#.....#....#.......
.....#...............#.....#...
.#.....#.....#..............#..
#................#..#..........
.##....#....#.....#............
#.####...#..#..#....#..........
..##........##.....##......#..#
......#.....#...##.........##..
....##..#.....#.#.........#...#
.....##..#....#....#.#...#..#..
...#............#...........#..
.......#.#..#.#.#..#........#.#
....#.#........#.#.#..#...#...#
..#....#....#..#......#........
.#...........................#.
.#..#....####........##......#.
.#.....#..#.#.................#
.#..#...........#...#....#...#.
......##..#........#..#....#...
..#.............#....#........#
#.#..........#.##.......#.#..#.
..#....#...#...............#...
..............#..........#..#..
..#.....#.#.....#...#...#..#...
.........#...###.#...#........#'''

tree_count_testcases = [
    {
        'description': "No treees",
        'input': '.',
        'expected': 0,
    },
    {
        'description': "One",
        'input': '#',
        'expected': 1,

    },
        {
        'description': "Two rows",
        'input': '#...\n...#',
        'expected': 2,

    },
    {
        'description': "challenge input",
        'input': challenge_input,
        'expected': 191,
    },
]


def test_tree_count():
    for tc in tree_count_testcases:
        output = count_trees(tc['input'], {'right': 3, 'down': 1})
        assert tc['expected'] == output

different_slopes_for_different_flopes = [
        {
        'description': "challenge input",
        'input': challenge_input,
        'slopes': [
            {'right': 1, "down": 1},
            {'right': 3, "down": 1},
            {'right': 5, "down": 1},
            {'right': 7, "down": 1},
            {'right': 1, "down": 2},
        ],
        'expected': 1478615040,
    },
]

def test_tree_count_with_slopes():
    for tc in different_slopes_for_different_flopes:
        running_total = 1
        for slope in tc['slopes']:
            running_total = running_total * count_trees(tc['input'], slope)
        assert tc['expected'] == running_total
