# 🌀 MAZE ESCAPE: A Computational Thinking Game

## DESCRIPTION:

Maze Escape is a computational thinking game developed in Python. It’s designed as an educational tool, especially for those with minimal programming experience. The game aims to introduce essential programming concepts like loops, logical thinking, and structured problem solving in an engaging way. By providing an interactive experience, Maze Escape allows players to think like a programmer without requiring them to write any code themselves.

## INTRODUCTION:

Maze Escape is intended for aspiring programmers, or young learners who want to understand how coding works without having to dive straight into complex syntax. The game builds on the fundamentals of computational thinking and helps players develop skills like sequencing, iteration, and problem decomposition. Each level becomes a stepping stone toward understanding how a series of commands can be organized to solve a problem.

The design of Maze Escape is influenced by classic puzzle games but focuses on helping players understand programming concepts through a simple and interactive interface. The goal is to make learning these abstract ideas tangible and enjoyable, ensuring players get the satisfaction of solving puzzles while absorbing foundational programming principles.

### GAMEPLAY:

Each level in Maze Escape is designed to either introduce or reinforce players to a concept in computational thinking, building from simple movement to more advanced thinking!

- **Level 0:** Basic Movement
- **Level 1:** Navigation with Obstacles
- **Level 2:** Loop Introduction
- **Level 3:** Complex Paths with Loops
- **Level 4:** Strategic Use of Loops and Commands
- **Level 5:** Problem Solving

### FEATURES:

- **Interactive Maze Navigation**: The game uses an intuitive interface where players can select movement commands. The character then navigates the maze according to the given instructions, providing a visual and interactive way to understand programming flow.
- **Command-Based Movements**: Players click buttons that look like lines of code to control the character. The available commands include `up()`, `down()`, `left()`, and `right()`. These commands make players think like a programmer, figuring out the sequence of steps needed to reach the goal.
- **Multiple Levels of Increasing Difficulty**: Maze Escape includes several levels that grow progressively more challenging. Players will encounter more obstacles and will need to use advanced strategies, like loops, to successfully reach the goal. Failing a level results in an automatic retry, encouraging players to rethink their approach and try again until they succeed.
- **Loop Functionality**: Some levels require players to use loops to complete repetitive movements efficiently. This feature helps introduce the concept of iteration, a fundamental building block in coding that allows for minimising repeated actions.
- **Real-Time Command Execution**: After setting up their commands, players click 'Execute' to watch the character carry out the steps. The commands are highlighted line-by-line in the terminal —yellow for commands in progress and green for completed ones— mirroring the way code is executed in real time.

### FILES:

- **`project.py`** – This is the main Python script that contains all the core components of the game. It includes the GUI setup using Tkinter, as well as the logic for player movement, handling loops, and collision detection. The script is designed to keep the gameplay simple and intuitive while focusing on educational value.
- **`test_project.py`** – This file contains basic unit tests built with pytest. These tests ensure that the core functionalities of the game, such as player movement, collision detection, work as intended.

## HOW TO RUN:

To play Maze Escape, clone the repository and install the required dependencies listed in `requirements.txt`. The game runs on Python and uses the Tkinter library for the GUI. Simply execute `python project.py` to start the game.

## INSTALLATION
If you're on Linux and Tkinter isn't installed you can run this command:
```bash
sudo apt-get install python3-tk
```
