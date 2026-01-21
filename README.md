# Adventure Explorer 🎮

A top-down adventure game developed in **Python** using the **Pygame Zero** library. This project serves as a technical assessment for programming tutors, demonstrating proficiency in Object-Oriented Programming (OOP), sprite animation, and game state management.

## 🚀 How to Run
1.  **Install Python**: Ensure you have Python 3.x installed on your system.
2.  **Install Pygame Zero**: Run the following command in your terminal:
    ```bash
    pip install pgzero
    ```
3.  **Launch the Game**: Open the terminal in the project folder and run:
    ```bash
    pgzrun main.py
    ```

## 🕹️ Controls & Mechanics
* **Movement**: Use the **Arrow Keys** to move the hero freely across the screen (Adventure style).
* **Pause/Resume**: Click the **PAUSE** button during gameplay to freeze the action.
* **Exit**: Use the **EXIT** button to return to the menu or close the game.
* **Objective**: Collect gold coins to reach 100 points while avoiding enemies.

## ✨ Technical Features
* **Rich Sprite Animation**: Both Hero and Enemies feature continuous 3-frame cyclic animations (using frames 0, 1, 2/3), meeting the "rich animation" requirement.
* **OOP Structure**: Organized into clear classes (`Hero` and `Enemy`) to demonstrate pedagogical best practices.
* **Game State Management**: Includes distinct states for Menu, Play, Pause, Game Over, and Victory.
* **Advanced Logic**: Features invincibility frames (blinking effect) and autonomous enemy movement with border bouncing.

## 🛠️ Compliance Checklist
- [x] **Genre**: Adventure (free movement).
- [x] **Libraries**: Strictly uses `pgzrun`, `math`, `random`, and `Rect`.
- [x] **Main Menu**: Functional buttons for Start, Sound Toggle, and Exit.
- [x] **PEP8**: Follows Python naming conventions with clear English variables.
- [x] **Originality**: 100% unique code written for this assessment.

---
*Developed for the Tutor Selection Process - 2026*