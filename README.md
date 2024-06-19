
# Tic-Tac-Toe Game

This repository contains a simple implementation of the classic Tic-Tac-Toe game using Python and Pygame.

## Features

- Two-player gameplay
- Graphical user interface using Pygame
- Basic AI for single-player mode (if applicable)
- Game state management and winner detection

## Requirements

- Python 3.x
- Pygame

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/merismbatyan/Tic-Tac-Toe.git
    cd tic-tac-toe
    ```

2. Install the required dependencies:

    ```bash
    pip install pygame
    ```

## Usage

Run the game using the following command:

```bash
python main.py
```

## Game Instructions

1. The game starts with an empty 3x3 grid.
2. Player 'X' makes the first move, followed by player 'O'.
3. Players take turns to place their mark (X or O) on the grid.
4. The first player to get three of their marks in a row (horizontally, vertically, or diagonally) wins the game.
5. If all nine squares are filled and neither player has three marks in a row, the game is a draw.

## File Overview

- `main.py`: Main script that contains the game logic and runs the game.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any bug fixes, improvements, or new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project uses [Pygame](https://www.pygame.org/) for the graphical interface and game loop.
