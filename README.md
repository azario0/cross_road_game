
# Cross Road Game (A Frogger Clone)

![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.x-green.svg)

A simple Frogger clone created with Python and the Pygame library. The goal is to help a frog cross a busy, multi-lane road without getting hit by cars. This project is completely self-contained and requires no external image or sound assets.


## Features

-   **Player Control:** Use the arrow keys to navigate the frog.
-   **Dynamic Obstacles:** Multiple lanes of traffic with cars moving at different speeds and in opposite directions.
-   **Collision Detection:** The game ends if the frog collides with a car.
-   **Win/Lose States:** Clear on-screen messages for winning a round or losing the game.
-   **Scoring:** Your score increases each time you successfully cross the road.
-   **No Dependencies:** The game uses only Pygame's built-in drawing functions, so no external image files are needed.

## Requirements

-   Python 3.x
-   Pygame 2.x

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/azario0/cross_road_game.git
    cd cross_road_game
    ```

2.  **Install Pygame:**
    It's recommended to use a virtual environment.
    ```bash
    # Create and activate a virtual environment (optional but good practice)
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

    # Install the required package
    pip install pygame
    ```

## How to Play

1.  **Run the game:**
    Execute the main Python script from your terminal.
    ```bash
    python frogger.py
    ```
    *(Assuming your file is named `frogger.py`)*

2.  **Controls:**
    -   **Up Arrow:** Move the frog forward.
    -   **Down Arrow:** Move the frog backward.
    -   **Left Arrow:** Move the frog left.
    -   **Right Arrow:** Move the frog right.
    -   **R Key:** Restart the game after a win or loss.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
Created by **azario0**.