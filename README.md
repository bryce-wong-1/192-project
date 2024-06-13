# Drive in the City

**Drive in the City** is a simulation game that utilizes Pygame to allow players to drive a virtual car around a city track. The game focuses on navigating a predefined path without colliding with the track borders, managing speed, and monitoring fuel efficiency improvements.

## Installation

To run **Drive in the City**, you need Python and Pygame installed on your computer. Here are the steps to get started:

1. **Install Python:**
   Ensure Python 3 is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2. **Install Pygame:**
   Pygame is required to run the game. Install it using pip:
   ```
   pip install pygame
   ```

3. **Download the Game:**
   Download the source code from the repository or clone it using git:
   ```
   git clone https://github.com/bryce-wong-1/192-project
   ```

4. **Run the Game:**
   Navigate to the main folder and run the main script:
   ```
   python main.py
   ```

## Game Controls

- **Arrow Keys:**
  - **Up Arrow:** Accelerate the car forward.
  - **Down Arrow:** Decelerate or reverse the car.
  - **Left Arrow:** Rotate the car left.
  - **Right Arrow:** Rotate the car right.

- **General Gameplay:**
  - Avoid colliding with the track borders. If a collision occurs, the car will bounce back.
  - Manage the car's speed to navigate through the track effectively.
  - Stops are counted each time the car stops (i.e., when acceleration or reverse is released).

## Game Features

- **Fuel Efficiency Simulation:**
  - The game simulates fuel consumption based on distance traveled and number of stops.
  - Displays real-time metrics for fuel spent without and with the system, fuel saved, and potential savings.

- **Dynamic Path Following:**
  - The car must follow a predefined path, marked by waypoints on the track. Navigate carefully to stay on the path.

## Graphics and Interface

- **Visual Elements:**
  - The game features a city plan as the track, with a visible border to guide or restrict the car's movement.
  - A terminal interface displays the car's statistics, including stops, distance traveled, and fuel metrics.

- **Interactive Text Display:**
  - Real-time updates on the game's statistics are shown on the screen, helping players to understand their performance regarding fuel efficiency and driving accuracy.

## Objective

The main objective of the game is to navigate the city track as efficiently as possible, minimizing fuel usage and avoiding collisions. Players are encouraged to improve their driving strategies to maximize fuel savings.

Enjoy your drive through the city!

