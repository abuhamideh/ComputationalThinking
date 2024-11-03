import pytest
from tkinter import Tk, Canvas
from project import Maze, levels, move_player

def test_reset_level():
    root = Tk()
    canvas = Canvas(root)
    level = levels[0]
    maze = Maze(canvas, level)

    maze.move_to((3,3))
    maze.reset()
    assert maze.pos == maze.start

    root.destroy()

def test_is_blocked():
    root = Tk()
    canvas = Canvas(root)
    level = levels[0]
    maze = Maze(canvas, level)

    wall = (1,4)
    assert maze.is_blocked(wall)
    maze.move_to((1,5))
    move_player(maze, "up")
    assert maze.pos == (1,5)
    clear = (2, 2)
    assert not maze.is_blocked(clear)

    root.destroy()

def test_move_player():
    root = Tk()
    canvas = Canvas(root)
    level = levels[1]
    maze = Maze(canvas, level)

    maze.move_to((0,0))
    move_player(maze, "down")
    assert maze.pos == (0,1)
    move_player(maze, "down")
    assert maze.pos == (0,2)
    move_player(maze, "up")
    assert maze.pos == (0,1)
    move_player(maze, "up")
    assert maze.pos == (0,0)

    maze.move_to((3,3))
    move_player(maze, "left")
    assert maze.pos == (2,3)
    move_player(maze, "right")
    assert maze.pos == (3,3)

    root.destroy()
