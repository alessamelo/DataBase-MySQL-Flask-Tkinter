# DataBase-MySQL-Flask-Tkinter
# 🎵 Music Streaming Platform – Full Stack Project

This project is a complete database-driven application simulating a music streaming service. It integrates a MySQL relational database, a RESTful API built with Flask, and a graphical user interface (GUI) developed in Tkinter.

## 📦 Features

- 🎧 **User Management**: Register and log in as a regular user or artist.
- 🎙️ **Artist Dashboard**: Add songs, publish collections (albums, EPs, singles), and assign music credits to collaborators.
- 🔎 **Search Functionality**: Search for songs by title or artist.
- 📊 **Streaming Tracking**: Each play is recorded and linked to the user.
- 🧾 **Credits System**: Users can be credited as vocalists, producers, composers, etc.
- 🎀 **Custom GUI**: Includes aesthetic enhancements like a pink background and styled fonts.
- 🐳 **Dockerized MySQL**: Database runs in a Docker container for easy deployment and isolation.

## ⚙️ Technologies Used

- **Python** (Flask, SQLAlchemy, Tkinter, Marshmallow)
- **MySQL** for relational data storage
- **Docker** for database containerization
- **JSON** for API communication

## 📁 Project Structure
├── main.py # Flask app entry point
├── gui.py # Tkinter-based GUI
├── include/ # Contains API Blueprints for each entity
│ ├── user.py
│ ├── artist.py
│ ├── song.py
│ └── ...
└── GUI_Images/ # Background images for the GUI


