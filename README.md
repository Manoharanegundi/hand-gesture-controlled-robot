# Gesture-Controlled Robot 🤖

A real-time hand gesture-controlled mobile robot using **Python, OpenCV, MediaPipe, and Arduino Uno**.

## 🚀 Project Overview

This project enables wireless-style robot control through hand gestures captured by a laptop webcam.

MediaPipe detects hand landmarks, Python recognizes predefined gestures, and serial communication sends commands to Arduino Uno, which controls the motors through an L9110S motor driver.

## 🖐️ Gesture Controls

| Command | Robot Movement |
|---|---|
| F | Forward |
| B | Backward |
| L | Left |
| R | Right |
| S | Stop |

## 🧰 Technologies Used

- Python
- OpenCV
- MediaPipe
- Arduino Uno
- L9110S Motor Driver
- Serial Communication (PySerial)

## ⚙️ System Architecture

```text
Webcam
  ↓
OpenCV + MediaPipe
  ↓
Gesture Recognition
  ↓
Python Serial Communication
  ↓
Arduino Uno
  ↓
L9110S Motor Driver
  ↓
Robot Movement
```

## 🔧 Hardware

- Arduino Uno
- L9110S Motor Driver
- 2 DC Geared Motors
- Robot Chassis
- Battery Pack
- Laptop Webcam


[GitHub Profile](https://github.com/Manoharanegundi)

⭐ Feedback and suggestions are welcome!
