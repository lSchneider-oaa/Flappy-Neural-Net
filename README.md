# Headless Flappy AI: Neural Network From Scratch

This project implements a custom-built, feedforward Neural Network and a Genetic Algorithm from absolute scratch to solve a Flappy Bird-style physics simulation. 

Instead of relying on heavy machine learning libraries like TensorFlow or `neat-python`, the "brain" is built purely with matrix mathematics using `numpy`. The training environment runs "headlessly" (without GUI rendering) to simulate hundreds of generations in mere seconds, before finally rendering the evolved champion using `pygame`.

## 🚀 Features

* **Custom Neural Network:** A 3-layer Multi-Layer Perceptron (MLP) built from scratch using NumPy dot products and a Sigmoid activation function.
* **Headless Training:** The physics engine is built purely with math (no Pygame collision boxes during training), allowing for lightning-fast evolution.
* **Genetic Algorithm:** Custom logic for Population Generation, Truncation Selection (Elitism), Deep-Copy Cloning, and Matrix-Level Mutation.
* **Input Normalization:** Environment variables (distances, heights) are normalized to prevent math overflows and speed up network convergence.
* **Champion Replay:** Automatically transitions from the headless simulation to a Pygame visualizer to watch the winning AI perform in real-time.

## 📁 Project Structure

* `brain.py`: Contains the `NeuralNet` class. Handles weight/bias initialization, forward propagation (`predict`), deep cloning, and random mutation.
* `headless_jumper.py`: Contains the pure-math `Bird` and `Pipe` physics classes, the `run_headless_evolution()` loop, and the `play_champion()` Pygame visualizer.

## 🧠 The AI Architecture

* **Inputs (3):** Normalized Bird Y-Position, X-Distance to the next pipe, Y-Position of the pipe's gap.
* **Hidden Layer (4):** 4 nodes processing the inputs to form logical associations.
* **Output (1):** A single Sigmoid-activated float. If `> 0.5`, the bird jumps.

## 🛠️ Installation & Requirements

You will need Python 3.x and the following packages:

```bash
pip install numpy pygame
```

## 🎮 How to Run
Simply execute the main simulation file:

```bash
python headless_jumper.py
```
The terminal will print the progress of the genetic algorithm. Once a bird survives for 5,000 frames (or 100 generations pass), a Pygame window will automatically open to show the champion navigating the pipes!