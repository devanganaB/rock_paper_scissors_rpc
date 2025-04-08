# 🪨📄✂️ Rock Paper Scissors – Distributed Multiplayer Game

A distributed Rock Paper Scissors game implemented using a client-server architecture with Remote Procedure Calls (RPC). Multiple clients can connect and play the game simultaneously, with state and score managed on the server side.

---

## 📦 Project Overview

This project demonstrates the use of RPC for communication between client and server, enabling multiple players to register, play, and track their scores in a classic Rock Paper Scissors game.

---

## 🚀 Getting Started

### 🔧 Requirements

- Python 3.x
- `xmlrpc` library (comes pre-installed with Python)

---

## 💻 How to Run

### 1️⃣ Start the Server

Open a terminal and run:

```bash
python rpc_server.py
```
### 2️⃣ Start the Client(s)

In a separate terminal, run:

```bash
python rpc_client.py
```
✅ You can open and run multiple clients simultaneously to simulate different players connecting to the same server.

---

## 🎯 Features
- 👤 Player Registration System

- 🧠 Game Logic for Rock, Paper, Scissors

- 🏅 Score Tracking per player

- 🕹️ Interactive Menu System in the client

- 📜 Game History Tracking

- 🔁 RPC Communication between client and server

---

## 🧠 Distributed Computing Concepts Demonstrated
- 🛰️ RPC (Remote Procedure Call)
The client invokes methods that are executed remotely on the server.

- 🏗️ Client-Server Architecture
Clear separation of concerns between client (UI + inputs) and server (game logic + state).

- 🧾 State Management
The server keeps track of player states, scores, and history across all sessions.

- ⚙️ Concurrency
Server handles requests from multiple clients concurrently.

---

## 🛠️ File Structure

```bash
project-folder/
│
├── server.py          # Main server script
├── client.py          # Client script to play the game
└── README.md          # You're here!
```
---

## 📬 Contact
For questions or suggestions, feel free to reach out! 😊

---

## 📄 License
This project is open-source and free to use under the MIT License.

---

Happy coding & may the best player win! 🎉

