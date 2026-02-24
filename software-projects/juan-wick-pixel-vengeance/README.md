<h1 align="center">🎮 Juan Wick: Pixel Vengeance</h1>

<p align="center">
A 2D pixel-style action game inspired by the John Wick universe, built in Java using object-oriented design and real-time game architecture.
</p>

<div align="center">
  <img src="Readme head.png" alt="Pixel Heads">
</div>

---

## 📘 Project Overview

**Juan Wick: Pixel Vengeance** is a 2D pixel-based action game developed in Java as part of a collaborative software engineering project.  

Players navigate through enemy-filled environments, survive increasingly challenging rounds, and engage in combat using responsive controls and real-time rendering.

This project demonstrates strong fundamentals in:

- Object-Oriented Programming (OOP)
- Game loop architecture
- Collision detection systems
- Event-driven input handling
- Modular software design
- Java desktop application development

---

## 🧠 Technical Architecture

The game was built using Java with a modular, object-oriented design approach to ensure scalability and maintainability.

### Core Components

- **Main Game Loop** – Manages rendering and updates at a fixed frame rate.
- **Player Class** – Handles movement, animations, combat logic, and state management.
- **Enemy Classes** – Controls AI behavior and spawning mechanics.
- **Collision System** – Detects interactions between player, enemies, and projectiles.
- **Rendering Engine** – Loads sprites and updates frames dynamically.
- **Input Handler** – Processes keyboard-based event listeners for player control.

The architecture separates:
- Game logic
- Rendering
- Input handling
- State management

This separation improves readability, debugging, and future feature expansion.

---

## ✨ Features

### ✅ Implemented Features
- Player movement and animation
- Enemy spawning and combat logic
- Health and damage system
- Score tracking
- Real-time rendering loop
- Keyboard control interface

### 🚧 Future Enhancements
- **Character Customization** – Multiple Juan Wick skins  
- **Unique Maps** – Distinct terrains, buildings, and environments  
- **Background Story Elements** – Narrative summaries between levels  
- **Multiplayer Mode** – Split-screen cooperative gameplay  
- **Weapon Customization System** – Gameplay-based weapon upgrades  

---

## 🛠️ Technologies Used

- **Java**
- Java Swing / AWT
- Object-Oriented Programming principles
- Event Listeners
- Game Loop design patterns
- Sprite rendering techniques

---

## 🚀 Getting Started

Follow these instructions to run **Juan Wick: Pixel Vengeance** locally.

### 📋 Prerequisites

- Java Development Kit (JDK 8 or higher)
- Computer with at least 5GB RAM
- Keyboard for gameplay controls

---

## 🔧 Installation

1. Clone the repository:

```bash
git clone https://github.com/cttres/Juan-Wick-Pixel-Vengeance.git
```

2. Navigate into the project directory:

```bash
cd Juan-Wick-Pixel-Vengeance
```

3. Compile the game:

```bash
javac -d bin -sourcepath src src/main/Main.java
```

4. Run the game:

### On Windows:
```bash
java -cp "bin;res" main.Main
```

### On Unix / Mac:
```bash
java -cp bin:res main.Main
```

---

## 🎮 Usage

- Use keyboard controls to move and attack.
- Survive enemy waves to progress through rounds.
- Track your score and health throughout gameplay.

---

## 👥 Collaboration

This project was developed collaboratively as part of a university software engineering course focused on applying object-oriented programming principles to real-time application development.

---

## ⭐ Show Your Support

If you enjoyed this project, consider giving it a ⭐️ on GitHub!

Happy coding!
