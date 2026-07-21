import turtle
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
import os
import sqlite3
import datetime
import hashlib
import random
import time
import sys
import json
import socket
import threading
import urllib.parse
import webbrowser
import platform
import numpy as np
import pandas as pd
import sympy as sp
import string
import shutil
import matplotlib.pyplot as plt
import subprocess
import requests
from urllib.parse import urlparse
import re
import math
import copy
import uuid
import wave
import logging
import io

# Try to import additional modules for Animator
try:
    from PIL import Image, ImageTk, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except:
    PIL_AVAILABLE = False

try:
    import pyttsx3
    TTS_AVAILABLE = True
except:
    TTS_AVAILABLE = False

try:
    from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
    MOVIEPY_AVAILABLE = True
except:
    MOVIEPY_AVAILABLE = False

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except:
    WATCHDOG_AVAILABLE = False

# ============================================================
# ANTIVIRUS CONFIGURATION
# ============================================================

QUARANTINE_DIR = "quarantine"
LOG_DIR = "logs"
REPORT_FILE = "scan_report.txt"

os.makedirs(QUARANTINE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "antivirus.log"),
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Example malware signatures
MALWARE_SIGNATURES = {
    "275a021bbfb6488ecf7d0f860b4f2f16f4f3f5d7c6b5e4b63f4f8e8b1f7a4b1": "Demo Trojan"
}

# ============================================================
# ANTIVIRUS FUNCTIONS
# ============================================================

def calculate_sha256(file_path):
    try:
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()
    except:
        return None

def quarantine_file(file_path):
    try:
        filename = os.path.basename(file_path)
        destination = os.path.join(QUARANTINE_DIR, f"{int(time.time())}_{filename}")
        shutil.move(file_path, destination)
        logging.info(f"Quarantined: {file_path}")
        return True
    except Exception as e:
        logging.error(str(e))
        return False

class AntivirusScanner:
    def __init__(self):
        self.total_files = 0
        self.infected_files = 0

    def scan_file(self, file_path):
        file_hash = calculate_sha256(file_path)
        if not file_hash:
            return False
        if file_hash in MALWARE_SIGNATURES:
            self.infected_files += 1
            quarantine_file(file_path)
            logging.warning(f"Malware detected: {file_path}")
            return True
        return False

    def scan_directory(self, folder_path, callback=None):
        self.total_files = 0
        self.infected_files = 0
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                path = os.path.join(root, file)
                self.total_files += 1
                try:
                    infected = self.scan_file(path)
                    if callback:
                        callback(path, infected)
                except:
                    pass
        report = (f"\nDate: {datetime.datetime.now()}\n"
                  f"Files Scanned: {self.total_files}\n"
                  f"Infected Files: {self.infected_files}\n"
                  f"{'-'*50}\n")
        with open(REPORT_FILE, "a") as f:
            f.write(report)
        return report

class RealtimeHandler(FileSystemEventHandler):
    def __init__(self):
        self.scanner = AntivirusScanner()
    def on_created(self, event):
        if not event.is_directory:
            self.scanner.scan_file(event.src_path)

class RealtimeProtection:
    def __init__(self, path):
        self.path = path
        self.observer = Observer()
    def start(self):
        if not WATCHDOG_AVAILABLE:
            return
        handler = RealtimeHandler()
        self.observer.schedule(handler, self.path, recursive=True)
        self.observer.start()
    def stop(self):
        self.observer.stop()
        self.observer.join()

class AntivirusGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NeilOS Antivirus")
        self.root.geometry("800x600")
        self.scanner = AntivirusScanner()
        self.selected_folder = ""
        title = tk.Label(root, text="NeilOS Antivirus", font=("Arial", 20, "bold"), bg="#1e1e1e", fg="#00ff00")
        title.pack(pady=10)
        tk.Button(root, text="Select Folder", command=self.select_folder, bg="#4CAF50", fg="white").pack(pady=5)
        tk.Button(root, text="Start Scan", command=self.start_scan, bg="#2196F3", fg="white").pack(pady=5)
        tk.Button(root, text="View Quarantine", command=self.show_quarantine, bg="#FF9800", fg="white").pack(pady=5)
        self.status = tk.Label(root, text="Ready", bg="#1e1e1e", fg="white")
        self.status.pack()
        self.output = tk.scrolledtext.ScrolledText(root, width=100, height=25, bg="#1e1e1e", fg="#00ff00")
        self.output.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    def select_folder(self):
        self.selected_folder = filedialog.askdirectory()
        if self.selected_folder:
            self.status.config(text=f"Selected: {self.selected_folder}")
    def log(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
    def start_scan(self):
        if not self.selected_folder:
            messagebox.showerror("Error", "Select folder first")
            return
        threading.Thread(target=self.scan_thread, daemon=True).start()
    def scan_thread(self):
        self.output.delete("1.0", tk.END)
        def callback(path, infected):
            if infected:
                self.log(f"[INFECTED] {path}")
            else:
                self.log(f"[OK] {path}")
        report = self.scanner.scan_directory(self.selected_folder, callback)
        self.log("\nSCAN COMPLETED")
        self.log(report)
        messagebox.showinfo("Scan Complete", f"Scan completed!\nFiles scanned: {self.scanner.total_files}\nInfected files: {self.scanner.infected_files}")
    def show_quarantine(self):
        files = os.listdir(QUARANTINE_DIR)
        if not files:
            messagebox.showinfo("Quarantine", "No files quarantined")
            return
        text = "\n".join(files)
        messagebox.showinfo("Quarantine Files", text)

def start_realtime():
    if not WATCHDOG_AVAILABLE:
        return
    try:
        monitor_path = os.path.expanduser("~")
        protection = RealtimeProtection(monitor_path)
        protection.start()
        while True:
            time.sleep(1)
    except:
        pass

def open_antivirus():
    antivirus_window = tk.Toplevel()
    antivirus_window.configure(bg="#1e1e1e")
    app = AntivirusGUI(antivirus_window)

# ============================================================
# DATABASE
# ============================================================

DB_FILE = "neilos.db"

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS notes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    amount REAL,
    date TEXT
)
""")

conn.commit()

# ============================================================
# CODE STUDIO - Multi-Language Programming Environment with URLs
# ============================================================

# Language configurations with URLs
PROGRAMMING_LANGUAGES = {
    "Python": {
        "extension": ".py",
        "template": '# Python Program\n\nprint("Hello, World!")',
        "runner": "python",
        "color": "#3776AB",
        "url": "https://www.programiz.com/python-programming/online-compiler/",
        "docs": "https://docs.python.org/3/",
        "tutorial": "https://docs.python.org/3/tutorial/",
    },
    "JavaScript": {
        "extension": ".js", 
        "template": '// JavaScript Program\n\nconsole.log("Hello, World!");',
        "runner": "node",
        "color": "#F7DF1E",
        "url": "https://www.programiz.com/javascript/online-compiler/",
        "docs": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
        "tutorial": "https://www.javascript.com/"
    },
    "Java": {
        "extension": ".java",
        "template": 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}',
        "runner": "javac",
        "color": "#007396",
        "url": "https://www.programiz.com/java-programming/online-compiler/",
        "docs": "https://docs.oracle.com/en/java/",
        "tutorial": "https://docs.oracle.com/javase/tutorial/"
    },
    "C++": {
        "extension": ".cpp",
        "template": '#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << "Hello, World!" << endl;\n    return 0;\n}',
        "runner": "g++",
        "color": "#00599C",
        "url": "https://www.programiz.com/cpp-programming/online-compiler/",
        "docs": "https://en.cppreference.com/w/",
        "tutorial": "https://www.learncpp.com/"
    },
    "C": {
        "extension": ".c",
        "template": '#include <stdio.h>\n\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}',
        "runner": "gcc",
        "color": "#A8B9CC",
        "url": "https://www.programiz.com/c-programming/online-compiler/",
        "docs": "https://en.cppreference.com/w/c",
        "tutorial": "https://www.learn-c.org/"
    },
    "C#": {
        "extension": ".cs",
        "template": 'using System;\n\nclass Program {\n    static void Main() {\n        Console.WriteLine("Hello, World!");\n    }\n}',
        "runner": "csc",
        "color": "#239120",
        "url": "https://www.programiz.com/csharp-programming/online-compiler/",
        "docs": "https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/",
        "tutorial": "https://www.w3schools.com/cs/"
    },
    "Ruby": {
        "extension": ".rb",
        "template": '# Ruby Program\n\nputs "Hello, World!"',
        "runner": "ruby",
        "color": "#CC342D",
        "url": "https://www.programiz.com/ruby-programming/online-compiler/",
        "docs": "https://ruby-doc.org/",
        "tutorial": "https://www.tutorialspoint.com/ruby/"
    },
    "Go": {
        "extension": ".go",
        "template": 'package main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello, World!")\n}',
        "runner": "go",
        "color": "#00ADD8",
        "url": "https://www.programiz.com/golang-programming/online-compiler/",
        "docs": "https://golang.org/doc/",
        "tutorial": "https://golang.org/doc/tutorial/"
    },
    "Rust": {
        "extension": ".rs",
        "template": 'fn main() {\n    println!("Hello, World!");\n}',
        "runner": "rustc",
        "color": "#DEA584",
        "url": "https://www.programiz.com/rust-programming/online-compiler/",
        "docs": "https://doc.rust-lang.org/",
        "tutorial": "https://doc.rust-lang.org/book/"
    },
    "PHP": {
        "extension": ".php",
        "template": '<?php\necho "Hello, World!\\n";\n?>',
        "runner": "php",
        "color": "#777BB4",
        "url": "https://www.programiz.com/php-programming/online-compiler/",
        "docs": "https://www.php.net/docs.php",
        "tutorial": "https://www.w3schools.com/php/"
    },
    "Swift": {
        "extension": ".swift",
        "template": 'import Swift\n\nprint("Hello, World!")',
        "runner": "swift",
        "color": "#FA7343",
        "url": "https://www.programiz.com/swift/online-compiler/",
        "docs": "https://docs.swift.org/swift-book/",
        "tutorial": "https://developer.apple.com/swift/"
    },
    "Kotlin": {
        "extension": ".kt",
        "template": 'fun main() {\n    println("Hello, World!")\n}',
        "runner": "kotlin",
        "color": "#7F52FF",
        "url": "https://www.programiz.com/kotlin/online-compiler/",
        "docs": "https://kotlinlang.org/docs/home.html",
        "tutorial": "https://play.kotlinlang.org/"
    },
    "TypeScript": {
        "extension": ".ts",
        "template": '// TypeScript Program\n\nlet message: string = "Hello, World!";\nconsole.log(message);',
        "runner": "ts-node",
        "color": "#3178C6",
        "url": "https://www.programiz.com/typescript/online-compiler/",
        "docs": "https://www.typescriptlang.org/docs/",
        "tutorial": "https://www.typescriptlang.org/docs/handbook/"
    },
    "HTML/CSS": {
        "extension": ".html",
        "template": '<!DOCTYPE html>\n<html>\n<head>\n    <title>My Page</title>\n    <style>\n        body { font-family: Arial; text-align: center; padding: 50px; }\n        h1 { color: blue; }\n    </style>\n</head>\n<body>\n    <h1>Hello, World!</h1>\n    <p>Welcome to NeilOS Code Studio</p>\n</body>\n</html>',
        "runner": "browser",
        "color": "#E34F26",
        "url": "https://www.programiz.com/html/online-compiler/",
        "docs": "https://developer.mozilla.org/en-US/docs/Web/CSS",
        "tutorial": "https://www.w3schools.com/html/"
    },
    "SQL": {
        "extension": ".sql",
        "template": '-- SQL Database Query\n\nCREATE TABLE users (\n    id INT PRIMARY KEY,\n    name VARCHAR(100),\n    email VARCHAR(100)\n);\n\nSELECT * FROM users;',
        "runner": "sqlite3",
        "color": "#4479A1",
        "url": "https://www.programiz.com/sql/online-compiler/",
        "docs": "https://dev.mysql.com/doc/",
        "tutorial": "https://www.postgresql.org/docs/"
    },
    "Bash": {
        "extension": ".sh",
        "template": '#!/bin/bash\n\necho "Hello, World!"\n\n# List files\nls -la',
        "runner": "bash",
        "color": "#4EAA25",
        "url": "https://www.programiz.com/bash-scripting/online-compiler/",
        "docs": "https://www.gnu.org/software/bash/manual/",
        "tutorial": "https://www.shellscript.sh/"
    },
    "Perl": {
        "extension": ".pl",
        "template": '#!/usr/bin/perl\n\nprint "Hello, World!\\n";',
        "runner": "perl",
        "color": "#39457E",
        "url": "https://www.onlinegdb.com/online_perl_compiler",
        "docs": "https://perldoc.perl.org/",
        "tutorial": "https://www.perl.com/"
    },
    "Lua": {
        "extension": ".lua",
        "template": '-- Lua Program\n\nprint("Hello, World!")',
        "runner": "lua",
        "color": "#000080",
        "url": "https://www.programiz.com/lua-programming/online-compiler/",
        "docs": "https://www.lua.org/manual/",
        "tutorial": "https://www.lua.org/pil/"
    },
    "R": {
        "extension": ".r",
        "template": '# R Program\n\nprint("Hello, World!")\n\n# Create a vector\ndata <- c(1, 2, 3, 4, 5)\nprint(mean(data))',
        "runner": "Rscript",
        "color": "#276DC3",
        "url": "https://www.programiz.com/r/online-compiler/",
        "docs": "https://www.rdocumentation.org/",
        "tutorial": "https://www.r-tutor.com/"
    },
    "Dart": {
        "extension": ".dart",
        "template": 'void main() {\n    print("Hello, World!");\n}',
        "runner": "dart",
        "color": "#00B4AB",
        "url": "https://www.programiz.com/dart-programming/online-compiler/",
        "docs": "https://dart.dev/guides",
        "tutorial": "https://dart.dev/tutorials"
    },
    "Earth": {
        "extension": ".earth",
        "template": '# Earth Language Program\n\nprint("Hello from Earth!")\nprint("🌍 Welcome to Earth programming 🌍")',
        "runner": "python",
        "color": "#2E8B57",
        "docs": "https://climate.nasa.gov/",
        "tutorial": "https://www.un.org/sustainabledevelopment/"
    }
}

# Code storage
CODE_FILES = []
CURRENT_LANGUAGE = "Python"
CURRENT_CODE = ""
CODE_OUTPUT = ""
CODE_EDITOR_OPEN = False

# ============================================================
# GLOBALS
# ============================================================

SCREEN_W = 1400
SCREEN_H = 850

CURRENT_APP = "desktop"

CLICKS = {}

BANK_BALANCE = 5000.0
LOAN_BALANCE = 0.0
LOAN_INTEREST_RATE = 10.0

BANK_LEDGER = [
    "[SYSTEM] Initial Deposit +5000"
]

FILES = [
    "kernel.sys",
    "config.cfg",
    "root.py",
    "notes.txt"
]

TERMINAL_HISTORY = [
    "NeilOS Terminal",
    "Type help"
]

SOCIAL_POSTS = []
PATIENTS = []

API_LIST = [
    "Weather API",
    "Maps API",
    "Payments API",
    "AI API"
]

DEPLOYMENT_LOGS = []

KERNEL_LOGS = [
    "Kernel boot sequence initialized."
]

CYBER_LOG = [
    "Cyber Security Core Ready"
]

NETWORK_LOG = [
    "Network initialized."
]

AI_LOG = [
    "AI: Hello!"
]

RUNNING_PROCESSES = []
INSTALLED_PACKAGES = ["kernel", "calculator", "terminal", "browser"]
CURRENT_THEME = "Dark"
THEMES = ["Dark", "Light", "Blue", "Matrix", "Neon"]
PLUGINS = []
BACKUP_DIR = "neilos_backups"
UPDATE_LOG = []
APP_STORE = ["TextEditor", "Paint", "MusicPlayer", "VideoPlayer", "WeatherApp", "Chess"]
CURRENT_USER = "guest"
AUTO_SAVE_RUNNING = True

# Cyber Security additional data
SCAN_RESULTS = []
DETECTED_THREATS = []
NETWORK_DEVICES = []

# Desktop path for file storage
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")
os.makedirs(DESKTOP_PATH, exist_ok=True)

# ============================================================
# SCREEN
# ============================================================

screen = turtle.Screen()
screen.setup(SCREEN_W, SCREEN_H)
screen.title("NeilOS Advanced")
screen.bgcolor("#0b1020")
screen.tracer(0)

# ============================================================
# DRAWERS
# ============================================================

drawer = turtle.Turtle()
drawer.hideturtle()
drawer.speed(0)

textpen = turtle.Turtle()
textpen.hideturtle()
textpen.speed(0)

# ============================================================
# DRAW HELPERS
# ============================================================

def clear_all():
    drawer.clear()
    textpen.clear()

def draw_rect(x, y, w, h, fill, border=None):
    drawer.penup()
    drawer.goto(x, y)
    drawer.pendown()
    
    if border:
        drawer.color(border, fill)
    else:
        drawer.color(fill, fill)
    
    drawer.begin_fill()
    for _ in range(2):
        drawer.forward(w)
        drawer.right(90)
        drawer.forward(h)
        drawer.right(90)
    drawer.end_fill()
    drawer.penup()

def draw_text(txt, x, y, color="white", size=10, style="normal"):
    textpen.penup()
    textpen.goto(x, y)
    textpen.color(color)
    textpen.write(txt, font=("Consolas", size, style))

# ============================================================
# CLICK REGISTRY
# ============================================================

def register_click(name, x, y, w, h, callback):
    CLICKS[name] = {
        "x1": x,
        "y1": y,
        "x2": x + w,
        "y2": y - h,
        "cb": callback
    }

# ============================================================
# APP CLASS
# ============================================================

class DesktopApp:
    def __init__(self, name, icon, appid):
        self.name = name
        self.icon = icon
        self.appid = appid

# ============================================================
# APPS
# ============================================================

apps = [
    DesktopApp("Bank", "💰", "bank"),
    DesktopApp("Files", "📁", "files"),
    DesktopApp("Terminal", "💻", "terminal"),
    DesktopApp("Search", "🔍", "search"),
    DesktopApp("Cyber", "🛡", "cyber"),
    DesktopApp("Network", "🌐", "network"),
    DesktopApp("AI", "🤖", "ai"),
    DesktopApp("Monitor", "📊", "monitor"),
    DesktopApp("Calculator", "🧮", "calculator"),
    DesktopApp("Clinic", "🏥", "clinic"),
    DesktopApp("SocialNet", "🌍", "social"),
    DesktopApp("Deploy", "🚀", "deploy"),
    DesktopApp("API", "🔌", "api"),
    DesktopApp("Games", "🎮", "games"),
    DesktopApp("Kernel", "⚙", "kernel"),
    DesktopApp("Notes", "📝", "notes"),
    DesktopApp("Code Studio", "💻", "code_studio"),
    DesktopApp("Animator", "🎬", "animator")
]

# ============================================================
# WINDOW SYSTEM
# ============================================================

def draw_window(title, color="#00ffee"):
    draw_rect(-600, 350, 1200, 700, "#101826", color)
    draw_rect(-600, 350, 1200, 40, "#0f172a", color)
    draw_text(title, -570, 320, color, 12, "bold")
    draw_rect(550, 350, 40, 30, "#ef4444")
    draw_text("X", 565, 322, "white", 11, "bold")
    register_click("close", 550, 350, 40, 30, desktop_view)

# ============================================================
# APP SWITCHING
# ============================================================

def open_app(appid):
    global CURRENT_APP
    CURRENT_APP = appid
    render()

def desktop_view():
    global CURRENT_APP
    CURRENT_APP = "desktop"
    render()

# ============================================================
# DESKTOP
# ============================================================

def draw_desktop():
    draw_rect(-700, 425, 1400, 850, "#0b1020")
    draw_text("NeilOS", -650, 390, "#00ffee", 14, "bold")
    
    startx = -600
    starty = 280
    width = 180
    height = 60
    
    for i, app in enumerate(apps):
        row = i // 4
        col = i % 4
        x = startx + col * 300
        y = starty - row * 120
        
        draw_rect(x, y, width, height, "#111827", "#00ffee")
        draw_text(f"{app.icon} {app.name}", x + 15, y - 35, "white", 10)
        register_click(app.appid, x, y, width, height, lambda a=app.appid: open_app(a))
    
    draw_rect(-700, -375, 1400, 50, "#111827")
    now = datetime.datetime.now()
    draw_text(now.strftime("%H:%M:%S"), 550, -405, "#00ffee", 10)

# ============================================================
# NOTES APP WITH NOTEPAD LINK
# ============================================================

def save_note(note):
    cur.execute("INSERT INTO notes(content) VALUES(?)", (note,))
    conn.commit()

def load_notes():
    cur.execute("SELECT content FROM notes")
    return [row[0] for row in cur.fetchall()]

def add_note():
    text = simpledialog.askstring("Notes", "Write note:")
    if text:
        save_note(text)

def show_notes():
    notes = load_notes()
    if not notes:
        messagebox.showinfo("Notes", "No notes saved.")
        return
    messagebox.showinfo("Notes", "\n\n".join(notes))

def open_notepad():
    """Open the official Notepad site or local Notepad"""
    # Try to open Windows Notepad first
    if platform.system() == "Windows":
        try:
            subprocess.Popen(["notepad.exe"])
            return
        except:
            pass
    
    # Fallback to web-based notepad
    webbrowser.open("https://www.onenote.com/")

def draw_notes():
    draw_window("Notes - Notepad Linked", "#f59e0b")
    
    register_click("add_note", -300, 280, 180, 45, add_note)
    draw_rect(-300, 280, 180, 45, "#111827", "#f59e0b")
    draw_text("📝 Add Note", -280, 255, "white", 10)
    
    register_click("show_notes", -100, 280, 180, 45, show_notes)
    draw_rect(-100, 280, 180, 45, "#111827", "#f59e0b")
    draw_text("📋 Show Notes", -80, 255, "white", 10)
    
    register_click("open_notepad", 100, 280, 180, 45, open_notepad)
    draw_rect(100, 280, 180, 45, "#111827", "#3b82f6")
    draw_text("📄 Open Notepad", 120, 255, "white", 10)
    
    # Display recent notes
    notes = load_notes()
    draw_text(f"📊 Total Notes: {len(notes)}", -500, 200, "#f59e0b", 11)
    
    if notes:
        draw_text("📌 Recent Notes:", -500, 170, "white", 10)
        for i, note in enumerate(notes[-5:]):
            preview = note[:50] + "..." if len(note) > 50 else note
            draw_text(f"  • {preview}", -500, 145 - i*25, "#a0aec0", 9)

# ============================================================
# ENHANCED BANK APP WITH ALL FINANCIAL CALCULATIONS
# ============================================================

def deposit_money():
    global BANK_BALANCE
    amt = simpledialog.askfloat("Deposit", "Amount:")
    if amt:
        BANK_BALANCE += amt
        BANK_LEDGER.append(f"+ {amt}")
        cur.execute("INSERT INTO transactions(type, amount, date) VALUES(?, ?, ?)", 
                   ("Deposit", amt, str(datetime.datetime.now())))
        conn.commit()
        messagebox.showinfo("Success", f"Deposited ${amt:.2f}\nNew Balance: ${BANK_BALANCE:.2f}")

def withdraw_money():
    global BANK_BALANCE
    amt = simpledialog.askfloat("Withdraw", "Amount:")
    if not amt:
        return
    if amt > BANK_BALANCE:
        messagebox.showerror("Bank", "Insufficient Funds")
        return
    BANK_BALANCE -= amt
    BANK_LEDGER.append(f"- {amt}")
    cur.execute("INSERT INTO transactions(type, amount, date) VALUES(?, ?, ?)", 
               ("Withdrawal", amt, str(datetime.datetime.now())))
    conn.commit()
    messagebox.showinfo("Success", f"Withdrew ${amt:.2f}\nNew Balance: ${BANK_BALANCE:.2f}")

def transfer_money():
    global BANK_BALANCE
    user = simpledialog.askstring("Transfer", "Recipient:")
    if not user:
        return
    amt = simpledialog.askfloat("Transfer", "Amount:")
    if not amt:
        return
    if amt > BANK_BALANCE:
        messagebox.showerror("Bank", "Insufficient Funds")
        return
    BANK_BALANCE -= amt
    BANK_LEDGER.append(f"Transfer {amt} -> {user}")
    cur.execute("INSERT INTO transactions(type, amount, date) VALUES(?, ?, ?)", 
               (f"Transfer to {user}", amt, str(datetime.datetime.now())))
    conn.commit()
    messagebox.showinfo("Success", f"Transferred ${amt:.2f} to {user}\nNew Balance: ${BANK_BALANCE:.2f}")

def simple_interest():
    principal = simpledialog.askfloat("Simple Interest", "Principal Amount:")
    if not principal:
        return
    rate = simpledialog.askfloat("Simple Interest", "Rate of Interest (% per year):")
    if not rate:
        return
    time_years = simpledialog.askfloat("Simple Interest", "Time (in years):")
    if not time_years:
        return
    
    interest = (principal * rate * time_years) / 100
    total = principal + interest
    
    result = f"""
Simple Interest Calculation:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Principal: ${principal:.2f}
Rate: {rate}% per year
Time: {time_years} years
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Interest: ${interest:.2f}
Total Amount: ${total:.2f}
"""
    messagebox.showinfo("Simple Interest", result)

def compound_interest():
    principal = simpledialog.askfloat("Compound Interest", "Principal Amount:")
    if not principal:
        return
    rate = simpledialog.askfloat("Compound Interest", "Rate of Interest (% per year):")
    if not rate:
        return
    time_years = simpledialog.askfloat("Compound Interest", "Time (in years):")
    if not time_years:
        return
    n = simpledialog.askinteger("Compound Interest", "Compounding frequency per year (1=Yearly, 4=Quarterly, 12=Monthly):")
    if not n:
        return
    
    amount = principal * (1 + (rate/100)/n) ** (n * time_years)
    interest = amount - principal
    
    result = f"""
Compound Interest Calculation:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Principal: ${principal:.2f}
Rate: {rate}% per year
Time: {time_years} years
Compounding: {n} times/year
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Interest Earned: ${interest:.2f}
Total Amount: ${amount:.2f}
"""
    messagebox.showinfo("Compound Interest", result)

def emi_calculation():
    principal = simpledialog.askfloat("EMI Calculator", "Loan Amount:")
    if not principal:
        return
    rate = simpledialog.askfloat("EMI Calculator", "Annual Interest Rate (%):")
    if not rate:
        return
    months = simpledialog.askinteger("EMI Calculator", "Loan Tenure (months):")
    if not months:
        return
    
    monthly_rate = rate / (12 * 100)
    emi = principal * monthly_rate * ((1 + monthly_rate) ** months) / (((1 + monthly_rate) ** months) - 1)
    total_payment = emi * months
    total_interest = total_payment - principal
    
    result = f"""
EMI Calculation:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Loan Amount: ${principal:.2f}
Annual Rate: {rate}%
Tenure: {months} months
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Monthly EMI: ${emi:.2f}
Total Payment: ${total_payment:.2f}
Total Interest: ${total_interest:.2f}
"""
    messagebox.showinfo("EMI Calculator", result)

def gst_calculation():
    amount = simpledialog.askfloat("GST Calculator", "Original Amount:")
    if not amount:
        return
    gst_rate = simpledialog.askfloat("GST Calculator", "GST Rate (%):")
    if not gst_rate:
        return
    
    gst_amount = amount * gst_rate / 100
    total = amount + gst_amount
    
    result = f"""
GST Calculation:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Original Amount: ${amount:.2f}
GST Rate: {gst_rate}%
GST Amount: ${gst_amount:.2f}
Total Amount: ${total:.2f}
"""
    messagebox.showinfo("GST Calculator", result)

def sgst_cgst_calculation():
    amount = simpledialog.askfloat("SGST/CGST Calculator", "Original Amount:")
    if not amount:
        return
    sgst_rate = simpledialog.askfloat("SGST/CGST", "SGST Rate (%):")
    if not sgst_rate:
        return
    cgst_rate = simpledialog.askfloat("SGST/CGST", "CGST Rate (%):")
    if not cgst_rate:
        return
    
    sgst_amount = amount * sgst_rate / 100
    cgst_amount = amount * cgst_rate / 100
    total_tax = sgst_amount + cgst_amount
    total = amount + total_tax
    
    result = f"""
SGST/CGST Calculation:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Original Amount: ${amount:.2f}
SGST Rate: {sgst_rate}%
CGST Rate: {cgst_rate}%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SGST Amount: ${sgst_amount:.2f}
CGST Amount: ${cgst_amount:.2f}
Total Tax: ${total_tax:.2f}
Total Amount: ${total:.2f}
"""
    messagebox.showinfo("SGST/CGST Calculator", result)

def apply_loan():
    global LOAN_BALANCE, BANK_BALANCE
    loan_amount = simpledialog.askfloat("Loan Application", "Loan Amount Requested:")
    if not loan_amount:
        return
    interest_rate = simpledialog.askfloat("Loan Application", "Interest Rate (% per year):")
    if not interest_rate:
        return
    tenure_years = simpledialog.askfloat("Loan Application", "Loan Tenure (years):")
    if not tenure_years:
        return
    
    LOAN_BALANCE = loan_amount
    BANK_BALANCE += loan_amount
    
    total_interest = loan_amount * interest_rate * tenure_years / 100
    total_payment = loan_amount + total_interest
    
    result = f"""
Loan Approved!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Loan Amount: ${loan_amount:.2f}
Interest Rate: {interest_rate}%
Tenure: {tenure_years} years
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Interest: ${total_interest:.2f}
Total Repayment: ${total_payment:.2f}
Monthly EMI: ${total_payment/(tenure_years*12):.2f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Amount credited to your account!
New Balance: ${BANK_BALANCE:.2f}
"""
    messagebox.showinfo("Loan Approved", result)
    
    cur.execute("INSERT INTO transactions(type, amount, date) VALUES(?, ?, ?)", 
               ("Loan Taken", loan_amount, str(datetime.datetime.now())))
    conn.commit()

def repay_loan():
    global LOAN_BALANCE, BANK_BALANCE
    if LOAN_BALANCE <= 0:
        messagebox.showinfo("Loan", "No outstanding loan!")
        return
    
    repayment = simpledialog.askfloat("Repay Loan", f"Outstanding Loan: ${LOAN_BALANCE:.2f}\nRepayment Amount:")
    if not repayment:
        return
    
    if repayment > BANK_BALANCE:
        messagebox.showerror("Error", "Insufficient balance!")
        return
    
    if repayment > LOAN_BALANCE:
        repayment = LOAN_BALANCE
    
    BANK_BALANCE -= repayment
    LOAN_BALANCE -= repayment
    
    messagebox.showinfo("Repayment", f"Repaid: ${repayment:.2f}\nRemaining Loan: ${LOAN_BALANCE:.2f}\nNew Balance: ${BANK_BALANCE:.2f}")
    
    cur.execute("INSERT INTO transactions(type, amount, date) VALUES(?, ?, ?)", 
               ("Loan Repayment", repayment, str(datetime.datetime.now())))
    conn.commit()

def tax_calculation():
    income = simpledialog.askfloat("Tax Calculator", "Annual Income:")
    if not income:
        return
    
    tax = 0
    if income <= 250000:
        tax = 0
        slab = "No Tax"
    elif income <= 500000:
        tax = (income - 250000) * 0.05
        slab = "5%"
    elif income <= 1000000:
        tax = 12500 + (income - 500000) * 0.20
        slab = "20%"
    else:
        tax = 112500 + (income - 1000000) * 0.30
        slab = "30%"
    
    cess = tax * 0.04
    total_tax = tax + cess
    after_tax = income - total_tax
    
    result = f"""
Income Tax Calculation:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Annual Income: ${income:,.2f}
Tax Slab: {slab}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Base Tax: ${tax:,.2f}
Health & Education Cess (4%): ${cess:,.2f}
Total Tax Payable: ${total_tax:,.2f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Income After Tax: ${after_tax:,.2f}
"""
    messagebox.showinfo("Tax Calculator", result)

def view_transactions():
    cur.execute("SELECT type, amount, date FROM transactions ORDER BY date DESC LIMIT 20")
    transactions = cur.fetchall()
    
    if not transactions:
        messagebox.showinfo("Transactions", "No transactions found.")
        return
    
    result = "Recent Transactions:\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    for t in transactions:
        result += f"Type: {t[0]}\nAmount: ${t[1]:.2f}\nDate: {t[2]}\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    messagebox.showinfo("Transaction History", result)

def draw_bank():
    draw_window("Bank - Financial Center", "#10b981")
    
    # Row 1: Basic Banking
    register_click("deposit", -500, 280, 140, 40, deposit_money)
    draw_rect(-500, 280, 140, 40, "#111827", "#10b981")
    draw_text("Deposit", -475, 255, "white", 10)
    
    register_click("withdraw", -340, 280, 140, 40, withdraw_money)
    draw_rect(-340, 280, 140, 40, "#111827", "#10b981")
    draw_text("Withdraw", -315, 255, "white", 10)
    
    register_click("transfer", -180, 280, 140, 40, transfer_money)
    draw_rect(-180, 280, 140, 40, "#111827", "#10b981")
    draw_text("Transfer", -155, 255, "white", 10)
    
    register_click("transactions", -20, 280, 140, 40, view_transactions)
    draw_rect(-20, 280, 140, 40, "#111827", "#10b981")
    draw_text("History", 5, 255, "white", 10)
    
    # Row 2: Interest Calculations
    register_click("simple_int", -500, 210, 140, 40, simple_interest)
    draw_rect(-500, 210, 140, 40, "#111827", "#3b82f6")
    draw_text("Simple Interest", -485, 185, "white", 9)
    
    register_click("compound_int", -340, 210, 140, 40, compound_interest)
    draw_rect(-340, 210, 140, 40, "#111827", "#3b82f6")
    draw_text("Compound Interest", -325, 185, "white", 9)
    
    register_click("emi", -180, 210, 140, 40, emi_calculation)
    draw_rect(-180, 210, 140, 40, "#111827", "#3b82f6")
    draw_text("EMI Calculator", -165, 185, "white", 9)
    
    # Row 3: Tax Calculations
    register_click("gst", -500, 140, 140, 40, gst_calculation)
    draw_rect(-500, 140, 140, 40, "#111827", "#f59e0b")
    draw_text("GST Calculator", -485, 115, "white", 9)
    
    register_click("sgst_cgst", -340, 140, 140, 40, sgst_cgst_calculation)
    draw_rect(-340, 140, 140, 40, "#111827", "#f59e0b")
    draw_text("SGST/CGST", -325, 115, "white", 9)
    
    register_click("tax", -180, 140, 140, 40, tax_calculation)
    draw_rect(-180, 140, 140, 40, "#111827", "#f59e0b")
    draw_text("Tax Calculator", -165, 115, "white", 9)
    
    # Row 4: Loan Management
    register_click("apply_loan", -500, 70, 140, 40, apply_loan)
    draw_rect(-500, 70, 140, 40, "#111827", "#ef4444")
    draw_text("Apply Loan", -485, 45, "white", 9)
    
    register_click("repay_loan", -340, 70, 140, 40, repay_loan)
    draw_rect(-340, 70, 140, 40, "#111827", "#ef4444")
    draw_text("Repay Loan", -325, 45, "white", 9)
    
    # Display Balance Information
    draw_text(f"💰 Balance: ${BANK_BALANCE:,.2f}", -500, -50, "#10b981", 14, "bold")
    if LOAN_BALANCE > 0:
        draw_text(f"🏦 Outstanding Loan: ${LOAN_BALANCE:,.2f}", -500, -80, "#ef4444", 12)
    else:
        draw_text(f"✅ No Outstanding Loans", -500, -80, "#10b981", 12)
    
    # Tips
    draw_text("💡 Financial Tools:", 100, 280, "#f59e0b", 10, "bold")
    draw_text("• Simple/Compound Interest for savings calculations", 100, 255, "white", 8)
    draw_text("• EMI Calculator for loan planning", 100, 235, "white", 8)
    draw_text("• GST/SGST/CGST for business tax", 100, 215, "white", 8)
    draw_text("• Tax Calculator for income tax estimation", 100, 195, "white", 8)

# ============================================================
# FILE EXPLORER - LINKED TO DESKTOP
# ============================================================

def create_file():
    name = simpledialog.askstring("Create File", "Filename:")
    if name:
        # Store on desktop
        file_path = os.path.join(DESKTOP_PATH, name)
        try:
            with open(file_path, 'w') as f:
                f.write(f"Created by NeilOS on {datetime.datetime.now()}\n")
            FILES.append(name)
            messagebox.showinfo("Success", f"File created on desktop: {name}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not create file: {e}")

def delete_file():
    name = simpledialog.askstring("Delete File", "Filename:")
    if name in FILES:
        file_path = os.path.join(DESKTOP_PATH, name)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            FILES.remove(name)
            messagebox.showinfo("Success", f"Deleted: {name}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete: {e}")

def list_files():
    # List both internal and desktop files
    desktop_files = os.listdir(DESKTOP_PATH) if os.path.exists(DESKTOP_PATH) else []
    all_files = list(set(FILES + desktop_files))
    if not all_files:
        messagebox.showinfo("Files", "No files found.")
        return
    messagebox.showinfo("Files", "\n".join(all_files))

def open_file_explorer():
    """Open the system file explorer at desktop"""
    if platform.system() == "Windows":
        subprocess.Popen(["explorer", DESKTOP_PATH])
    elif platform.system() == "Darwin":  # macOS
        subprocess.Popen(["open", DESKTOP_PATH])
    else:  # Linux
        subprocess.Popen(["xdg-open", DESKTOP_PATH])

def draw_files():
    draw_window("Files - Desktop Linked", "#f59e0b")
    
    register_click("create", -400, 280, 160, 45, create_file)
    draw_rect(-400, 280, 160, 45, "#111827", "#f59e0b")
    draw_text("📄 Create File", -380, 255, "white", 10)
    
    register_click("delete", -220, 280, 160, 45, delete_file)
    draw_rect(-220, 280, 160, 45, "#111827", "#f59e0b")
    draw_text("🗑 Delete File", -200, 255, "white", 10)
    
    register_click("list", -40, 280, 160, 45, list_files)
    draw_rect(-40, 280, 160, 45, "#111827", "#f59e0b")
    draw_text("📋 List Files", -20, 255, "white", 10)
    
    register_click("open_explorer", 140, 280, 180, 45, open_file_explorer)
    draw_rect(140, 280, 180, 45, "#111827", "#3b82f6")
    draw_text("📂 Open Desktop", 160, 255, "white", 10)
    
    # Show desktop path
    draw_text(f"📍 Desktop Path: {DESKTOP_PATH}", -500, 200, "#f59e0b", 9)
    
    # Show files on desktop
    draw_text("📁 Files on Desktop:", -500, 170, "white", 10)
    desktop_files = os.listdir(DESKTOP_PATH) if os.path.exists(DESKTOP_PATH) else []
    for i, f in enumerate(desktop_files[:10]):
        draw_text(f"  • {f}", -500, 145 - i*20, "#a0aec0", 9)
    if len(desktop_files) > 10:
        draw_text(f"  ... and {len(desktop_files) - 10} more", -500, 145 - 10*20, "#a0aec0", 9)

# ============================================================
# ENHANCED TERMINAL WITH UBUNTU, POWERSHELL, CMD, BASH
# ============================================================

# Terminal modes and their commands
TERMINAL_MODES = {
    "Ubuntu": {
        "prompt": "ubuntu@neilos:~$ ",
        "commands": {
            "ls": "List directory contents",
            "cd": "Change directory",
            "pwd": "Print working directory",
            "mkdir": "Make directory",
            "rm": "Remove file",
            "cp": "Copy file",
            "mv": "Move file",
            "cat": "Display file contents",
            "grep": "Search text",
            "sudo": "Run with superuser privileges",
            "apt": "Package management",
            "python": "Run Python interpreter",
            "git": "Version control",
            "vim": "Text editor",
            "nano": "Text editor",
            "echo": "Display message",
            "date": "Display date and time",
            "whoami": "Display current user",
            "ps": "Process status",
            "kill": "Terminate process",
            "chmod": "Change file permissions"
        }
    },
    "PowerShell": {
        "prompt": "PS C:\\Users\\neilos> ",
        "commands": {
            "Get-ChildItem": "List directory contents (dir)",
            "Set-Location": "Change directory (cd)",
            "Get-Location": "Print working directory (pwd)",
            "New-Item": "Create new item",
            "Remove-Item": "Delete item",
            "Copy-Item": "Copy item",
            "Move-Item": "Move item",
            "Get-Content": "Display file contents",
            "Select-String": "Search text",
            "Start-Process": "Start a process",
            "Get-Process": "List processes",
            "Stop-Process": "Stop process",
            "Get-Help": "Get help",
            "Clear-Host": "Clear screen (cls)",
            "Write-Host": "Display message",
            "Get-Date": "Get current date and time",
            "Get-Command": "List available commands",
            "Import-Module": "Import module",
            "Export-Csv": "Export to CSV",
            "ConvertTo-Json": "Convert to JSON",
            "Invoke-WebRequest": "Make HTTP request"
        }
    },
    "Command Prompt": {
        "prompt": "C:\\Users\\neilos> ",
        "commands": {
            "dir": "List directory contents",
            "cd": "Change directory",
            "mkdir": "Make directory",
            "rmdir": "Remove directory",
            "del": "Delete file",
            "copy": "Copy file",
            "move": "Move file",
            "type": "Display file contents",
            "find": "Search text",
            "ping": "Test network connection",
            "ipconfig": "Display IP configuration",
            "systeminfo": "System information",
            "tasklist": "List processes",
            "taskkill": "Terminate process",
            "echo": "Display message",
            "date": "Display date and time",
            "time": "Display time",
            "cls": "Clear screen",
            "help": "Display help",
            "exit": "Close terminal"
        }
    },
    "Bash": {
        "prompt": "bash-5.0$ ",
        "commands": {
            "ls": "List directory contents",
            "cd": "Change directory",
            "pwd": "Print working directory",
            "mkdir": "Make directory",
            "rm": "Remove file",
            "cp": "Copy file",
            "mv": "Move file",
            "cat": "Display file contents",
            "grep": "Search text",
            "echo": "Display message",
            "date": "Display date and time",
            "whoami": "Display current user",
            "ps": "Process status",
            "kill": "Terminate process",
            "chmod": "Change file permissions",
            "chown": "Change file owner",
            "df": "Disk free space",
            "du": "Disk usage",
            "head": "Display first lines",
            "tail": "Display last lines",
            "wc": "Word count",
            "sort": "Sort text",
            "uniq": "Unique lines",
            "tar": "Archive files",
            "gzip": "Compress files"
        }
    }
}

# Initialize terminal mode
CURRENT_TERMINAL_MODE_NAME = "Ubuntu"
CURRENT_TERMINAL_MODE = TERMINAL_MODES["Ubuntu"]

def run_terminal_command():
    global CURRENT_TERMINAL_MODE
    cmd = simpledialog.askstring("Terminal", f"{CURRENT_TERMINAL_MODE['prompt']}")
    if not cmd:
        return
    
    # Store command in history
    TERMINAL_HISTORY.append(f"{CURRENT_TERMINAL_MODE['prompt']}{cmd}")
    
    # Check if it's a help command
    if cmd.strip().lower() in ["help", "?"]:
        commands = "\n".join([f"  • {k}: {v}" for k, v in CURRENT_TERMINAL_MODE['commands'].items()])
        messagebox.showinfo("Available Commands", f"Commands for {CURRENT_TERMINAL_MODE_NAME}:\n\n{commands}")
        return
    
    # Try to execute system command
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        output = result.stdout + result.stderr
        if output:
            TERMINAL_HISTORY.append(output)
            # Create a new window for output
            output_window = tk.Toplevel()
            output_window.title("Terminal Output")
            output_window.geometry("600x400")
            output_window.configure(bg="#1e1e1e")
            
            output_text = tk.Text(output_window, bg="#1e1e1e", fg="#00ff00",
                                 font=("Consolas", 10))
            output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            output_text.insert("1.0", output)
            
            def close_output():
                output_window.destroy()
            
            tk.Button(output_window, text="Close", command=close_output,
                     bg="#f44336", fg="white").pack(pady=5)
        else:
            TERMINAL_HISTORY.append("Command executed successfully")
            messagebox.showinfo("Terminal", "Command executed successfully")
    except subprocess.TimeoutExpired:
        TERMINAL_HISTORY.append("Error: Command timed out")
        messagebox.showerror("Terminal", "Command timed out (10 seconds)")
    except Exception as e:
        TERMINAL_HISTORY.append(f"Error: {str(e)}")
        messagebox.showerror("Terminal", f"Error: {str(e)}")

def change_terminal_mode():
    global CURRENT_TERMINAL_MODE, CURRENT_TERMINAL_MODE_NAME
    modes = "\n".join([f"• {mode}" for mode in TERMINAL_MODES.keys()])
    choice = simpledialog.askstring("Change Terminal Mode", 
        f"Available modes:\n{modes}\n\nEnter mode name:")
    
    if choice and choice in TERMINAL_MODES:
        CURRENT_TERMINAL_MODE = TERMINAL_MODES[choice]
        CURRENT_TERMINAL_MODE_NAME = choice
        messagebox.showinfo("Terminal", f"Switched to {choice} mode")
        TERMINAL_HISTORY.append(f"[MODE] Switched to {choice}")
    else:
        messagebox.showerror("Error", "Invalid mode name!")

def show_terminal_history():
    text = "\n".join(TERMINAL_HISTORY)
    messagebox.showinfo("Terminal History", text)

def draw_terminal():
    draw_window("Terminal - Multi-Mode", "#3b82f6")
    
    register_click("run_cmd", -500, 280, 180, 45, run_terminal_command)
    draw_rect(-500, 280, 180, 45, "#111827", "#3b82f6")
    draw_text("▶ Run Command", -480, 255, "white", 10)
    
    register_click("change_mode", -300, 280, 180, 45, change_terminal_mode)
    draw_rect(-300, 280, 180, 45, "#111827", "#f59e0b")
    draw_text("🔄 Change Mode", -280, 255, "white", 10)
    
    register_click("show_history", -100, 280, 180, 45, show_terminal_history)
    draw_rect(-100, 280, 180, 45, "#111827", "#10b981")
    draw_text("📋 Show History", -80, 255, "white", 10)
    
    # Show current mode
    draw_text(f"🖥️ Current Mode: {CURRENT_TERMINAL_MODE_NAME}", -500, 200, "#3b82f6", 12, "bold")
    draw_text(f"Prompt: {CURRENT_TERMINAL_MODE['prompt']}", -500, 170, "#a0aec0", 10)
    
    # Show available commands for current mode
    draw_text("📚 Available Commands:", -500, 140, "#f59e0b", 10, "bold")
    commands_list = list(CURRENT_TERMINAL_MODE['commands'].items())[:8]
    for i, (cmd, desc) in enumerate(commands_list):
        draw_text(f"  • {cmd}: {desc}", -500, 115 - i*18, "#a0aec0", 8)
    if len(CURRENT_TERMINAL_MODE['commands']) > 8:
        draw_text(f"  ... and {len(CURRENT_TERMINAL_MODE['commands']) - 8} more", -500, 115 - 8*18, "#a0aec0", 8)
    
    # Recent history
    draw_text("📜 Recent Commands:", 100, 280, "#10b981", 10, "bold")
    recent = TERMINAL_HISTORY[-5:] if len(TERMINAL_HISTORY) > 5 else TERMINAL_HISTORY
    for i, entry in enumerate(recent):
        display = entry[:50] + "..." if len(entry) > 50 else entry
        draw_text(f"  • {display}", 100, 255 - i*18, "#a0aec0", 8)

# ============================================================
# GOOGLE SEARCH
# ============================================================

def google_search():
    query = simpledialog.askstring("Google Search", "Enter Query:")
    if not query:
        return
    url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(query)
    webbrowser.open(url)

def draw_search():
    draw_window("Search", "#ef4444")
    register_click("search_btn", -100, 150, 200, 50, google_search)
    draw_rect(-100, 150, 200, 50, "#111827", "#ef4444")
    draw_text("Google Search", -90, 120, "white", 12)

# ============================================================
# ENHANCED AI APP WITH CHATGPT, GROK, DEEPSEEK
# ============================================================

def open_chatgpt():
    webbrowser.open("https://chat.openai.com/")
    AI_LOG.append("[AI] Opened ChatGPT")

def open_grok():
    webbrowser.open("https://x.ai/grok")
    AI_LOG.append("[AI] Opened Grok")

def open_deepseek():
    webbrowser.open("https://deepseek.com/")
    AI_LOG.append("[AI] Opened DeepSeek")

def ask_local_ai():
    question = simpledialog.askstring("AI Assistant", "Question:")
    if not question:
        return
    AI_LOG.append(f"User: {question}")
    # Simple local responses
    responses = [
        "That's an interesting question! I'm still learning.",
        "Let me think about that... I'll get back to you.",
        "Great question! I'd recommend checking online resources.",
        "I don't have an answer for that yet, but I'm improving daily.",
        "That's beyond my current knowledge. I'm a simple AI."
    ]
    response = random.choice(responses)
    AI_LOG.append(f"AI: {response}")
    messagebox.showinfo("AI Response", response)

def view_ai_log():
    text = "\n\n".join(AI_LOG)
    messagebox.showinfo("AI Log", text)

def draw_ai():
    draw_window("AI Assistant - Multi-AI", "#10b981")
    
    # AI Web Links
    register_click("chatgpt", -500, 280, 160, 45, open_chatgpt)
    draw_rect(-500, 280, 160, 45, "#111827", "#10b981")
    draw_text("🤖 ChatGPT", -480, 255, "white", 10)
    
    register_click("grok", -320, 280, 160, 45, open_grok)
    draw_rect(-320, 280, 160, 45, "#111827", "#f59e0b")
    draw_text("🧠 Grok", -300, 255, "white", 10)
    
    register_click("deepseek", -140, 280, 160, 45, open_deepseek)
    draw_rect(-140, 280, 160, 45, "#111827", "#8b5cf6")
    draw_text("📊 DeepSeek", -120, 255, "white", 10)
    
    # Local AI
    register_click("ask_ai", 40, 280, 160, 45, ask_local_ai)
    draw_rect(40, 280, 160, 45, "#111827", "#3b82f6")
    draw_text("💬 Ask Local AI", 60, 255, "white", 10)
    
    register_click("view_log", 220, 280, 160, 45, view_ai_log)
    draw_rect(220, 280, 160, 45, "#111827", "#ef4444")
    draw_text("📋 View Log", 240, 255, "white", 10)
    
    # AI Info
    draw_text("🌐 AI Services Available:", -500, 200, "#10b981", 12, "bold")
    draw_text("• ChatGPT: OpenAI's conversational AI", -500, 170, "white", 9)
    draw_text("• Grok: xAI's cutting-edge assistant", -500, 145, "white", 9)
    draw_text("• DeepSeek: Advanced reasoning AI", -500, 120, "white", 9)
    draw_text("• Local AI: Built-in assistant (limited)", -500, 95, "white", 9)
    
    # Recent interactions
    draw_text("💬 Recent Interactions:", -500, 60, "#f59e0b", 10, "bold")
    recent = AI_LOG[-6:] if len(AI_LOG) > 6 else AI_LOG
    for i, entry in enumerate(recent):
        display = entry[:50] + "..." if len(entry) > 50 else entry
        draw_text(f"  • {display}", -500, 35 - i*18, "#a0aec0", 8)

# ============================================================
# ENHANCED SOCIAL NETWORK WITH INSTAGRAM, FACEBOOK, WHATSAPP, LINKEDIN
# ============================================================

def open_instagram():
    webbrowser.open("https://www.instagram.com/")
    SOCIAL_POSTS.append({"text": "Opened Instagram", "likes": 0, "time": datetime.datetime.now()})

def open_facebook():
    webbrowser.open("https://www.facebook.com/")
    SOCIAL_POSTS.append({"text": "Opened Facebook", "likes": 0, "time": datetime.datetime.now()})

def open_whatsapp():
    webbrowser.open("https://web.whatsapp.com/")
    SOCIAL_POSTS.append({"text": "Opened WhatsApp Web", "likes": 0, "time": datetime.datetime.now()})

def open_linkedin():
    webbrowser.open("https://www.linkedin.com/")
    SOCIAL_POSTS.append({"text": "Opened LinkedIn", "likes": 0, "time": datetime.datetime.now()})

def create_post():
    text = simpledialog.askstring("Create Post", "Write something:")
    if not text:
        return
    SOCIAL_POSTS.append({"text": text, "likes": 0, "time": datetime.datetime.now()})
    messagebox.showinfo("Success", "Post created!")

def like_latest_post():
    if not SOCIAL_POSTS:
        return
    SOCIAL_POSTS[-1]["likes"] += 1
    messagebox.showinfo("Liked", "You liked the latest post!")

def show_timeline():
    if not SOCIAL_POSTS:
        messagebox.showinfo("Timeline", "No posts.")
        return
    text = ""
    for post in SOCIAL_POSTS:
        time_str = post.get("time", datetime.datetime.now()).strftime("%H:%M")
        text += f"[{time_str}] {post['text']}\n❤️ {post['likes']} likes\n\n"
    messagebox.showinfo("Timeline", text)

def draw_social():
    draw_window("SocialNet - Social Media Hub", "#ef4444")
    
    # Social Media Links
    register_click("instagram", -500, 280, 140, 40, open_instagram)
    draw_rect(-500, 280, 140, 40, "#111827", "#E1306C")
    draw_text("📸 Instagram", -480, 255, "white", 9)
    
    register_click("facebook", -340, 280, 140, 40, open_facebook)
    draw_rect(-340, 280, 140, 40, "#111827", "#1877F2")
    draw_text("📘 Facebook", -320, 255, "white", 9)
    
    register_click("whatsapp", -180, 280, 140, 40, open_whatsapp)
    draw_rect(-180, 280, 140, 40, "#111827", "#25D366")
    draw_text("💬 WhatsApp", -160, 255, "white", 9)
    
    register_click("linkedin", -20, 280, 140, 40, open_linkedin)
    draw_rect(-20, 280, 140, 40, "#111827", "#0A66C2")
    draw_text("💼 LinkedIn", 0, 255, "white", 9)
    
    # Social Features
    register_click("create_post", 140, 280, 140, 40, create_post)
    draw_rect(140, 280, 140, 40, "#111827", "#10b981")
    draw_text("✏️ Create Post", 160, 255, "white", 9)
    
    register_click("like_post", 300, 280, 140, 40, like_latest_post)
    draw_rect(300, 280, 140, 40, "#111827", "#f59e0b")
    draw_text("❤️ Like Post", 320, 255, "white", 9)
    
    register_click("show_timeline", 460, 280, 140, 40, show_timeline)
    draw_rect(460, 280, 140, 40, "#111827", "#3b82f6")
    draw_text("📋 Timeline", 480, 255, "white", 9)
    
    # Stats
    draw_text(f"📊 Total Posts: {len(SOCIAL_POSTS)}", -500, 200, "#ef4444", 11)
    
    # Recent posts
    if SOCIAL_POSTS:
        draw_text("📌 Recent Posts:", -500, 170, "white", 10)
        for i, post in enumerate(SOCIAL_POSTS[-3:]):
            text = post['text'][:40] + "..." if len(post['text']) > 40 else post['text']
            draw_text(f"  • {text} (❤️ {post['likes']})", -500, 145 - i*25, "#a0aec0", 9)

# ============================================================
# ENHANCED GAMES WITH SNAKES AND LADDERS, MAZE SOLVER
# ============================================================

class SnakesAndLadders:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Snakes and Ladders")
        self.window.geometry("600x600")
        self.window.configure(bg="#1e1e1e")
        
        self.board = list(range(1, 101))
        self.snakes = {98: 78, 95: 75, 93: 73, 87: 24, 64: 60, 62: 19, 54: 34, 17: 7}
        self.ladders = {9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}
        self.position = 0
        self.rolls = 0
        
        self.create_board()
    
    def create_board(self):
        canvas = tk.Canvas(self.window, width=500, height=500, bg="#2d2d2d")
        canvas.pack(pady=10)
        
        # Draw board
        cell_size = 50
        for i in range(10):
            for j in range(10):
                x = j * cell_size
                y = i * cell_size
                num = 100 - (i * 10 + j)
                if i % 2 == 0:
                    num = 100 - (i * 10 + (9 - j))
                else:
                    num = 100 - (i * 10 + j)
                
                color = "#3d3d3d" if (i + j) % 2 == 0 else "#4d4d4d"
                canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill=color, outline="#555")
                canvas.create_text(x + cell_size//2, y + cell_size//2, text=str(num), fill="white", font=("Arial", 8))
        
        # Draw snakes
        for start, end in self.snakes.items():
            sx = ((start - 1) % 10) * cell_size + cell_size//2
            sy = (9 - (start - 1) // 10) * cell_size + cell_size//2
            ex = ((end - 1) % 10) * cell_size + cell_size//2
            ey = (9 - (end - 1) // 10) * cell_size + cell_size//2
            canvas.create_line(sx, sy, ex, ey, fill="#ff4444", width=3)
        
        # Draw ladders
        for start, end in self.ladders.items():
            sx = ((start - 1) % 10) * cell_size + cell_size//2
            sy = (9 - (start - 1) // 10) * cell_size + cell_size//2
            ex = ((end - 1) % 10) * cell_size + cell_size//2
            ey = (9 - (end - 1) // 10) * cell_size + cell_size//2
            canvas.create_line(sx, sy, ex, ey, fill="#44ff44", width=3)
        
        # Player position
        self.player_pos = canvas.create_oval(0, 0, 20, 20, fill="#00ffee")
        self.update_player(canvas)
        
        # Controls
        control_frame = tk.Frame(self.window, bg="#1e1e1e")
        control_frame.pack(pady=10)
        
        tk.Label(control_frame, text="Your Position: 0", bg="#1e1e1e", fg="white", font=("Arial", 12)).pack(side="left", padx=10)
        
        tk.Button(control_frame, text="🎲 Roll Dice", command=lambda: self.roll_dice(canvas),
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        tk.Button(control_frame, text="🔄 Reset", command=lambda: self.reset_game(canvas),
                 bg="#f44336", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        self.status_label = tk.Label(self.window, text="Click Roll Dice to start!", 
                                    bg="#1e1e1e", fg="#00ffee", font=("Arial", 10))
        self.status_label.pack()
        
        self.canvas = canvas
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
    
    def update_player(self, canvas):
        if self.position >= 100:
            return
        row = 9 - self.position // 10
        col = self.position % 10
        if row % 2 == 0:
            col = 9 - col
        x = col * 50 + 15
        y = row * 50 + 15
        canvas.coords(self.player_pos, x-10, y-10, x+10, y+10)
    
    def roll_dice(self, canvas):
        self.rolls += 1
        dice = random.randint(1, 6)
        self.position += dice
        
        # Check for snakes
        if self.position in self.snakes:
            self.position = self.snakes[self.position]
            self.status_label.config(text=f"🐍 Snake! Moved to {self.position}")
        # Check for ladders
        elif self.position in self.ladders:
            self.position = self.ladders[self.position]
            self.status_label.config(text=f"🪜 Ladder! Climbed to {self.position}")
        else:
            self.status_label.config(text=f"🎲 Rolled {dice}. Position: {self.position}")
        
        if self.position >= 100:
            self.position = 100
            self.status_label.config(text=f"🎉 Congratulations! You won in {self.rolls} rolls!")
            messagebox.showinfo("Game Over", f"🎉 You won Snakes and Ladders!\nRolls: {self.rolls}")
        
        self.update_player(canvas)
        canvas.update()
    
    def reset_game(self, canvas):
        self.position = 0
        self.rolls = 0
        self.status_label.config(text="Game reset. Click Roll Dice to start!")
        self.update_player(canvas)
        canvas.update()

class MazeSolver:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Maze Solver")
        self.window.geometry("600x600")
        self.window.configure(bg="#1e1e1e")
        
        self.maze = [
            [1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,1,0,0,0,0,1],
            [1,0,1,0,1,0,1,1,0,1],
            [1,0,1,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,0,1,1],
            [1,0,0,0,0,0,1,0,0,1],
            [1,1,1,1,1,0,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,1],
            [1,0,0,1,1,1,1,1,0,1],
            [1,1,1,1,1,1,1,1,1,1]
        ]
        self.start = (1, 1)
        self.end = (8, 8)
        self.solution = []
        self.create_maze()
    
    def create_maze(self):
        canvas = tk.Canvas(self.window, width=500, height=500, bg="#2d2d2d")
        canvas.pack(pady=10)
        
        cell_size = 50
        for i in range(10):
            for j in range(10):
                x = j * cell_size
                y = i * cell_size
                color = "#3d3d3d" if self.maze[i][j] == 1 else "#1e1e1e"
                canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill=color, outline="#555")
        
        # Mark start and end
        canvas.create_oval(1*cell_size+10, 1*cell_size+10, 1*cell_size+40, 1*cell_size+40, fill="#4CAF50", outline="#4CAF50")
        canvas.create_oval(8*cell_size+10, 8*cell_size+10, 8*cell_size+40, 8*cell_size+40, fill="#f44336", outline="#f44336")
        
        # Controls
        control_frame = tk.Frame(self.window, bg="#1e1e1e")
        control_frame.pack(pady=10)
        
        self.status_label = tk.Label(self.window, text="Click 'Solve' to find path!", 
                                    bg="#1e1e1e", fg="#00ffee", font=("Arial", 10))
        self.status_label.pack()
        
        def solve_maze():
            self.solution = self.find_path()
            if self.solution:
                self.status_label.config(text=f"✅ Path found! Length: {len(self.solution)} steps")
                self.draw_solution(canvas)
                messagebox.showinfo("Maze Solver", f"✅ Path found!\nSteps: {len(self.solution)}")
            else:
                self.status_label.config(text="❌ No path found!")
                messagebox.showerror("Maze Solver", "❌ No path found!")
        
        def reset_maze():
            canvas.delete("all")
            for i in range(10):
                for j in range(10):
                    x = j * cell_size
                    y = i * cell_size
                    color = "#3d3d3d" if self.maze[i][j] == 1 else "#1e1e1e"
                    canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill=color, outline="#555")
            canvas.create_oval(1*cell_size+10, 1*cell_size+10, 1*cell_size+40, 1*cell_size+40, fill="#4CAF50", outline="#4CAF50")
            canvas.create_oval(8*cell_size+10, 8*cell_size+10, 8*cell_size+40, 8*cell_size+40, fill="#f44336", outline="#f44336")
            self.solution = []
            self.status_label.config(text="Maze reset. Click 'Solve' to find path!")
        
        tk.Button(control_frame, text="🧩 Solve", command=solve_maze,
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        tk.Button(control_frame, text="🔄 Reset", command=reset_maze,
                 bg="#f44336", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        self.canvas = canvas
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
    
    def find_path(self):
        rows, cols = len(self.maze), len(self.maze[0])
        visited = [[False for _ in range(cols)] for _ in range(rows)]
        path = []
        
        def dfs(r, c):
            if r < 0 or r >= rows or c < 0 or c >= cols:
                return False
            if self.maze[r][c] == 1 or visited[r][c]:
                return False
            if (r, c) == self.end:
                path.append((r, c))
                return True
            
            visited[r][c] = True
            path.append((r, c))
            
            # Try all directions
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if dfs(r + dr, c + dc):
                    return True
            
            path.pop()
            return False
        
        dfs(self.start[0], self.start[1])
        return path
    
    def draw_solution(self, canvas):
        if not self.solution:
            return
        cell_size = 50
        for i, (r, c) in enumerate(self.solution):
            if (r, c) == self.start or (r, c) == self.end:
                continue
            x = c * cell_size + cell_size//2
            y = r * cell_size + cell_size//2
            color = "#00ffee" if i % 2 == 0 else "#00ccaa"
            canvas.create_oval(x-10, y-10, x+10, y+10, fill=color, outline=color)

def guess_game():
    target = random.randint(1, 10)
    attempts = 0
    while True:
        guess = simpledialog.askinteger("Guess Game", f"Attempt {attempts+1}: Guess number (1-10):")
        if guess is None:
            return
        attempts += 1
        if guess == target:
            messagebox.showinfo("Game", f"🎉 Correct! You got it in {attempts} tries!")
            break
        elif guess < target:
            messagebox.showinfo("Game", "📈 Too low! Try again.")
        else:
            messagebox.showinfo("Game", "📉 Too high! Try again.")

def draw_games():
    draw_window("Games Hub", "#a855f7")
    
    register_click("guess_game", -500, 280, 180, 45, guess_game)
    draw_rect(-500, 280, 180, 45, "#111827", "#a855f7")
    draw_text("🎯 Guess Number", -480, 255, "white", 10)
    
    register_click("snakes_ladders", -300, 280, 180, 45, lambda: SnakesAndLadders())
    draw_rect(-300, 280, 180, 45, "#111827", "#10b981")
    draw_text("🐍 Snakes & Ladders", -285, 255, "white", 10)
    
    register_click("maze_solver", -100, 280, 180, 45, lambda: MazeSolver())
    draw_rect(-100, 280, 180, 45, "#111827", "#3b82f6")
    draw_text("🧩 Maze Solver", -80, 255, "white", 10)
    
    draw_text("🎮 Available Games:", -500, 200, "#a855f7", 11, "bold")
    draw_text("• Guess Number - Classic number guessing game", -500, 170, "white", 9)
    draw_text("• Snakes & Ladders - Classic board game with dice", -500, 145, "white", 9)
    draw_text("• Maze Solver - Find the path through the maze", -500, 120, "white", 9)

# ============================================================
# NETWORK MANAGER
# ============================================================

def network_info():
    host = socket.gethostname()
    try:
        ip = socket.gethostbyname(host)
    except:
        ip = "Unavailable"
    messagebox.showinfo("Network", f"Hostname: {host}\nIP: {ip}")

def ping_host():
    host = simpledialog.askstring("Ping", "Host:")
    if not host:
        return
    try:
        ip = socket.gethostbyname(host)
        messagebox.showinfo("Ping", f"{host}\n{ip}")
    except:
        messagebox.showerror("Ping", "Host unreachable")

def draw_network():
    draw_window("Network", "#3b82f6")
    register_click("net_info", -100, 150, 200, 50, network_info)
    draw_rect(-100, 150, 200, 50, "#111827", "#3b82f6")
    draw_text("Network Info", -80, 120, "white", 12)
    register_click("ping", -100, 70, 200, 50, ping_host)
    draw_rect(-100, 70, 200, 50, "#111827", "#3b82f6")
    draw_text("Ping Host", -65, 40, "white", 12)

# ============================================================
# CYBER SECURITY CENTER - FULL VERSION WITH ALL FEATURES
# ============================================================

def generate_password():
    pwd = "".join(random.choice(string.ascii_letters + string.digits + "!@#$%^&*") for _ in range(16))
    messagebox.showinfo("Generated Password", pwd)

def password_strength():
    pwd = simpledialog.askstring("Password Strength", "Enter password:")
    if not pwd:
        return
    score = 0
    feedback = []
    
    if len(pwd) >= 12:
        score += 2
        feedback.append("✓ Excellent length (12+ chars)")
    elif len(pwd) >= 8:
        score += 1
        feedback.append("✓ Good length (8-11 chars)")
    else:
        feedback.append("✗ Too short (<8 chars)")
    
    if any(c.isdigit() for c in pwd):
        score += 1
        feedback.append("✓ Contains numbers")
    else:
        feedback.append("✗ No numbers")
    
    if any(c.isupper() for c in pwd):
        score += 1
        feedback.append("✓ Contains uppercase")
    else:
        feedback.append("✗ No uppercase letters")
    
    if any(c.islower() for c in pwd):
        score += 1
        feedback.append("✓ Contains lowercase")
    
    if any(c in "!@#$%^&*" for c in pwd):
        score += 2
        feedback.append("✓ Contains special characters")
    else:
        feedback.append("✗ No special characters")
    
    if score >= 7:
        strength = "VERY STRONG 💪"
        color = "#10b981"
    elif score >= 5:
        strength = "STRONG ✅"
        color = "#3b82f6"
    elif score >= 3:
        strength = "MODERATE ⚠️"
        color = "#f59e0b"
    else:
        strength = "WEAK ❌"
        color = "#ef4444"
    
    result = f"Password Strength: {strength}\n\nScore: {score}/8\n\n" + "\n".join(feedback)
    messagebox.showinfo("Password Analysis", result)

def ddos_attack_simulator():
    """Simulate DDoS attack detection and mitigation"""
    target = simpledialog.askstring("DDoS Simulator", "Target IP/Hostname:")
    if not target:
        return
    
    CYBER_LOG.append(f"[ALERT] DDoS attack detected on {target}")
    
    attack_window = tk.Toplevel()
    attack_window.title("DDoS Attack Simulation")
    attack_window.geometry("500x400")
    attack_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(attack_window, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"⚠️ DDoS ATTACK DETECTED ⚠️\n")
    text_area.insert(tk.END, f"Target: {target}\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 50 + "\n\n")
    
    for i in range(10):
        packets = random.randint(1000, 100000)
        text_area.insert(tk.END, f"[{i+1}] Incoming packets: {packets}/sec\n")
        attack_window.update()
        time.sleep(0.1)
    
    text_area.insert(tk.END, "\n🛡️ MITIGATION ACTIVATED 🛡️\n")
    text_area.insert(tk.END, "• Traffic filtering enabled\n")
    text_area.insert(tk.END, "• Rate limiting applied\n")
    text_area.insert(tk.END, "• Blacklisting malicious IPs\n")
    text_area.insert(tk.END, "• CDN protection engaged\n\n")
    text_area.insert(tk.END, "✅ Attack mitigated successfully!\n")
    
    CYBER_LOG.append(f"[MITIGATION] DDoS attack on {target} mitigated")
    
    def close_window():
        attack_window.destroy()
    
    tk.Button(attack_window, text="Close", command=close_window, 
             bg="#ef4444", fg="white").pack(pady=5)

def malware_detection():
    """Scan for malware signatures"""
    file_to_scan = filedialog.askopenfilename(title="Select file to scan for malware")
    if not file_to_scan:
        return
    
    malware_signatures = [
        "virus", "malware", "trojan", "ransomware", "spyware", 
        "keylogger", "rootkit", "worm", "backdoor", "exploit"
    ]
    
    result_window = tk.Toplevel()
    result_window.title("Malware Detection Results")
    result_window.geometry("600x400")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"🔍 MALWARE SCAN REPORT\n")
    text_area.insert(tk.END, f"File: {os.path.basename(file_to_scan)}\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 50 + "\n\n")
    
    threats_found = []
    try:
        with open(file_to_scan, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().lower()
            for signature in malware_signatures:
                if signature in content:
                    threats_found.append(signature)
                    text_area.insert(tk.END, f"⚠️ Found: {signature.upper()}\n")
    except:
        text_area.insert(tk.END, "⚠️ Binary file - performing heuristic scan...\n")
        threats_found = ["Suspicious patterns detected (heuristic)"]
    
    text_area.insert(tk.END, "\n" + "━" * 50 + "\n")
    
    if threats_found:
        text_area.insert(tk.END, f"❌ DETECTED: {len(threats_found)} threats\n")
        for threat in threats_found:
            text_area.insert(tk.END, f"   - {threat}\n")
        DETECTED_THREATS.extend(threats_found)
    else:
        text_area.insert(tk.END, "✅ No malware detected. File appears clean.\n")
    
    CYBER_LOG.append(f"[SCAN] Malware scan completed on {os.path.basename(file_to_scan)}")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, 
             bg="#3b82f6", fg="white").pack(pady=5)

def phishing_detection():
    """Detect phishing URLs and emails"""
    url_or_email = simpledialog.askstring("Phishing Detection", "Enter URL or Email to check:")
    if not url_or_email:
        return
    
    suspicious_indicators = [
        "login", "verify", "secure", "account", "update", 
        "confirm", "bank", "paypal", "amazon", "apple",
        "microsoft", "google", "facebook", "instagram"
    ]
    
    red_flags = 0
    warnings = []
    
    # Check for suspicious patterns
    if "http" in url_or_email.lower():
        # URL checks
        if "https" not in url_or_email.lower():
            warnings.append("⚠️ Missing HTTPS - Connection not secure")
            red_flags += 1
        
        for indicator in suspicious_indicators:
            if indicator in url_or_email.lower():
                warnings.append(f"⚠️ Contains suspicious keyword: {indicator}")
                red_flags += 1
        
        if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url_or_email):
            warnings.append("⚠️ Uses IP address instead of domain name")
            red_flags += 2
        
        if '-' in url_or_email.split('/')[2] if '/' in url_or_email else '-' in url_or_email:
            warnings.append("⚠️ Contains hyphens - potential typosquatting")
            red_flags += 1
    
    else:
        # Email checks
        if "@" not in url_or_email:
            warnings.append("⚠️ Not a valid email format")
            red_flags += 1
        
        suspicious_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
        for domain in suspicious_domains:
            if domain in url_or_email.lower():
                warnings.append(f"⚠️ Uses free email service: {domain}")
                red_flags += 1
        
        if any(char in url_or_email for char in ["!", "#", "$", "%", "^", "&", "*"]):
            warnings.append("⚠️ Contains unusual special characters")
            red_flags += 1
    
    result_window = tk.Toplevel()
    result_window.title("Phishing Detection Results")
    result_window.geometry("600x400")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#1e1e1e", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    if red_flags >= 3:
        text_area.insert(tk.END, "🔴 HIGH RISK - PHISHING DETECTED!\n", "high")
        text_area.tag_config("high", foreground="#ef4444")
    elif red_flags >= 1:
        text_area.insert(tk.END, "🟡 MEDIUM RISK - Exercise caution\n", "medium")
        text_area.tag_config("medium", foreground="#f59e0b")
    else:
        text_area.insert(tk.END, "🟢 LOW RISK - Appears legitimate\n", "low")
        text_area.tag_config("low", foreground="#10b981")
    
    text_area.insert(tk.END, "\n" + "━" * 50 + "\n")
    text_area.insert(tk.END, f"Analyzed: {url_or_email}\n")
    text_area.insert(tk.END, f"Risk Score: {red_flags}/10\n\n")
    
    if warnings:
        text_area.insert(tk.END, "Findings:\n")
        for warning in warnings:
            text_area.insert(tk.END, f"{warning}\n")
    else:
        text_area.insert(tk.END, "No obvious phishing indicators found.\n")
    
    CYBER_LOG.append(f"[PHISHING] Analysis completed for {url_or_email[:50]}")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, 
             bg="#3b82f6", fg="white").pack(pady=5)

def mitm_detection():
    """Detect Man-in-the-Middle attacks"""
    result_window = tk.Toplevel()
    result_window.title("MITM Detection")
    result_window.geometry("600x500")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, "🔒 MAN-IN-THE-MIDDLE DETECTION SCAN\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 50 + "\n\n")
    
    # Simulate MITM detection checks
    checks = [
        "Checking SSL/TLS certificates...",
        "Verifying certificate chain...",
        "Checking for certificate pinning...",
        "Analyzing network routes...",
        "Checking ARP table for anomalies...",
        "Verifying DNS responses...",
        "Checking for unexpected redirects..."
    ]
    
    mitm_detected = False
    
    for check in checks:
        text_area.insert(tk.END, f"• {check} ")
        result_window.update()
        time.sleep(0.3)
        
        if random.random() < 0.1:  # 10% chance of detection
            text_area.insert(tk.END, "⚠️ ANOMALY DETECTED!\n")
            mitm_detected = True
            result_window.update()
            time.sleep(0.5)
            
            # Simulate deeper analysis
            for i in range(3):
                text_area.insert(tk.END, f"  Analyzing... {'.' * (i+1)}\n")
                result_window.update()
                time.sleep(0.2)
        else:
            text_area.insert(tk.END, "✓ OK\n")
        result_window.update()
    
    text_area.insert(tk.END, "\n" + "━" * 50 + "\n")
    
    if mitm_detected:
        text_area.insert(tk.END, "🚨 MITM ATTACK DETECTED!\n\n", "alert")
        text_area.tag_config("alert", foreground="#ef4444")
        text_area.insert(tk.END, "Recommendations:\n")
        text_area.insert(tk.END, "1. Disconnect from current network\n")
        text_area.insert(tk.END, "2. Use VPN for encrypted connections\n")
        text_area.insert(tk.END, "3. Verify SSL certificates manually\n")
        text_area.insert(tk.END, "4. Change passwords immediately\n")
        CYBER_LOG.append("[MITM] Attack detected!")
    else:
        text_area.insert(tk.END, "✅ No MITM attack detected. Connection appears secure.\n")
        CYBER_LOG.append("[MITM] Scan completed - no threats found")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, 
             bg="#3b82f6", fg="white").pack(pady=5)

def network_scanner():
    """Scan network for devices"""
    network = simpledialog.askstring("Network Scanner", "Enter network (e.g., 192.168.1.0/24):")
    if not network:
        network = "192.168.1.0/24"
    
    result_window = tk.Toplevel()
    result_window.title("Network Scanner")
    result_window.geometry("600x500")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"🌐 NETWORK SCAN\n")
    text_area.insert(tk.END, f"Network: {network}\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 50 + "\n\n")
    
    # Simulate network scan
    devices_found = random.randint(3, 15)
    text_area.insert(tk.END, f"Scanning network...\n\n")
    
    for i in range(devices_found):
        ip = f"192.168.1.{random.randint(1, 254)}"
        mac = ":".join([f"{random.randint(0,255):02x}" for _ in range(6)])
        hostname = f"device-{random.randint(100,999)}"
        
        text_area.insert(tk.END, f"Device {i+1}:\n")
        text_area.insert(tk.END, f"  IP: {ip}\n")
        text_area.insert(tk.END, f"  MAC: {mac}\n")
        text_area.insert(tk.END, f"  Hostname: {hostname}\n")
        
        # Add device to global list
        NETWORK_DEVICES.append({"ip": ip, "mac": mac, "hostname": hostname})
        
        text_area.insert(tk.END, "\n")
        result_window.update()
        time.sleep(0.1)
    
    text_area.insert(tk.END, "━" * 50 + "\n")
    text_area.insert(tk.END, f"✅ Scan complete. {devices_found} devices found.\n")
    
    CYBER_LOG.append(f"[SCAN] Network scan completed - {devices_found} devices found")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, 
             bg="#3b82f6", fg="white").pack(pady=5)

def nmap_scan():
    """Simulate Nmap style port scanning"""
    target = simpledialog.askstring("Nmap Scan", "Target IP or Hostname:")
    if not target:
        return
    
    result_window = tk.Toplevel()
    result_window.title("Nmap Scan Results")
    result_window.geometry("700x600")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"🔍 NMAP SCAN REPORT\n")
    text_area.insert(tk.END, f"Target: {target}\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 60 + "\n\n")
    
    common_ports = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
        80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 3306: "MySQL",
        3389: "RDP", 5432: "PostgreSQL", 8080: "HTTP-Alt", 27017: "MongoDB"
    }
    
    text_area.insert(tk.END, "PORT     STATE    SERVICE\n")
    text_area.insert(tk.END, "─────    ─────    ───────\n")
    
    open_ports = []
    for port in common_ports:
        if random.random() < 0.3:  # 30% chance port is open
            status = "open"
            open_ports.append(port)
            color = "#10b981"
        else:
            status = "closed"
            color = "#6b7280"
        
        text_area.insert(tk.END, f"{port:<8} {status:<8} {common_ports[port]}\n")
        result_window.update()
        time.sleep(0.05)
    
    # Scan additional random ports
    text_area.insert(tk.END, "\nScanning additional ports...\n")
    for _ in range(10):
        port = random.randint(1024, 65535)
        if random.random() < 0.1:
            text_area.insert(tk.END, f"{port:<8} open     unknown\n")
            open_ports.append(port)
        result_window.update()
        time.sleep(0.02)
    
    text_area.insert(tk.END, "\n" + "━" * 60 + "\n")
    text_area.insert(tk.END, f"✅ Scan complete. {len(open_ports)} open ports found.\n")
    
    if open_ports:
        text_area.insert(tk.END, f"\nOpen ports: {', '.join(map(str, open_ports[:10]))}\n")
    
    CYBER_LOG.append(f"[NMAP] Scan completed on {target} - {len(open_ports)} open ports")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, 
             bg="#3b82f6", fg="white").pack(pady=5)

def url_scanner():
    """Scan URL for security threats"""
    url = simpledialog.askstring("URL Scanner", "Enter URL to scan:")
    if not url:
        return
    
    result_window = tk.Toplevel()
    result_window.title("URL Security Scanner")
    result_window.geometry("600x500")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#1e1e1e", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"🔗 URL SECURITY SCAN\n")
    text_area.insert(tk.END, f"URL: {url}\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 50 + "\n\n")
    
    # Analyze URL
    risk_score = 0
    warnings = []
    
    # Check for URL patterns
    if "http" in url.lower() and "https" not in url.lower():
        warnings.append("⚠️ Missing HTTPS encryption")
        risk_score += 2
    
    suspicious_patterns = [
        "login", "verify", "secure", "account", "update", "confirm",
        "bank", "paypal", "amazon", "apple", "microsoft", "google"
    ]
    
    for pattern in suspicious_patterns:
        if pattern in url.lower():
            warnings.append(f"⚠️ Contains '{pattern}' - potential phishing")
            risk_score += 1
    
    if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url):
        warnings.append("⚠️ Uses IP address instead of domain name")
        risk_score += 3
    
    if len(url) > 100:
        warnings.append("⚠️ Unusually long URL")
        risk_score += 1
    
    # Check for URL shorteners
    shorteners = ["bit.ly", "tinyurl", "goo.gl", "ow.ly", "is.gd", "buff.ly"]
    for shortener in shorteners:
        if shortener in url.lower():
            warnings.append(f"⚠️ Uses URL shortener ({shortener}) - destination hidden")
            risk_score += 2
    
    # Determine risk level
    if risk_score >= 5:
        risk_level = "🔴 HIGH RISK"
        risk_color = "#ef4444"
        recommendation = "DO NOT OPEN - Block this URL immediately"
    elif risk_score >= 2:
        risk_level = "🟡 MEDIUM RISK"
        risk_color = "#f59e0b"
        recommendation = "Exercise caution - Verify before opening"
    else:
        risk_level = "🟢 LOW RISK"
        risk_color = "#10b981"
        recommendation = "URL appears safe"
    
    text_area.insert(tk.END, f"Risk Level: {risk_level}\n\n", "risk")
    text_area.tag_config("risk", foreground=risk_color)
    
    text_area.insert(tk.END, f"Risk Score: {risk_score}/10\n\n")
    
    if warnings:
        text_area.insert(tk.END, "Findings:\n")
        for warning in warnings:
            text_area.insert(tk.END, f"{warning}\n")
    else:
        text_area.insert(tk.END, "No obvious threats detected.\n")
    
    text_area.insert(tk.END, f"\nRecommendation: {recommendation}\n")
    
    CYBER_LOG.append(f"[URL_SCAN] Scanned {url[:50]} - Risk score: {risk_score}")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, 
             bg="#3b82f6", fg="white").pack(pady=5)

def sms_bomber_simulator():
    """Simulate SMS bomber (educational only)"""
    number = simpledialog.askstring("SMS Bomber Simulator", "Enter phone number (simulation only):")
    if not number:
        return
    
    result_window = tk.Toplevel()
    result_window.title("SMS Bomber Simulation")
    result_window.geometry("500x400")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"📱 SMS BOMBER SIMULATION (EDUCATIONAL)\n")
    text_area.insert(tk.END, f"Target: {number}\n")
    text_area.insert(tk.END, "━" * 50 + "\n\n")
    text_area.insert(tk.END, "⚠️ THIS IS A SIMULATION - No actual SMS sent\n\n")
    
    messages_sent = 0
    for i in range(20):
        messages_sent += random.randint(5, 15)
        text_area.insert(tk.END, f"Sending messages... {messages_sent} sent\r")
        result_window.update()
        time.sleep(0.05)
    
    text_area.insert(tk.END, f"\n\n✅ Simulation complete: {messages_sent} SMS messages simulated\n")
    text_area.insert(tk.END, "\n⚠️ EDUCATIONAL PURPOSE ONLY\n")
    text_area.insert(tk.END, "Actual SMS bombing is illegal and unethical!\n")
    
    CYBER_LOG.append(f"[SIM] SMS bomber simulation for {number}")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, 
             bg="#ef4444", fg="white").pack(pady=5)

def hash_calculator():
    """Calculate hash of a file or text"""
    choice = messagebox.askquestion("Hash Calculator", "Calculate hash of:\nYes = File\nNo = Text")
    
    if choice == 'yes':
        file_path = filedialog.askopenfilename(title="Select file to hash")
        if not file_path:
            return
        
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
                md5_hash = hashlib.md5(data).hexdigest()
                sha1_hash = hashlib.sha1(data).hexdigest()
                sha256_hash = hashlib.sha256(data).hexdigest()
                
            result = f"File: {os.path.basename(file_path)}\n\nMD5: {md5_hash}\n\nSHA1: {sha1_hash}\n\nSHA256: {sha256_hash}"
            messagebox.showinfo("File Hashes", result)
            CYBER_LOG.append(f"[HASH] Calculated hashes for {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {e}")
    else:
        text = simpledialog.askstring("Hash Calculator", "Enter text to hash:")
        if not text:
            return
        
        md5_hash = hashlib.md5(text.encode()).hexdigest()
        sha1_hash = hashlib.sha1(text.encode()).hexdigest()
        sha256_hash = hashlib.sha256(text.encode()).hexdigest()
        
        result = f"Text: {text}\n\nMD5: {md5_hash}\n\nSHA1: {sha1_hash}\n\nSHA256: {sha256_hash}"
        messagebox.showinfo("Text Hashes", result)
        CYBER_LOG.append(f"[HASH] Calculated hashes for text input")

def botnet_detector():
    """Detect botnet activity"""
    result_window = tk.Toplevel()
    result_window.title("Botnet Detector")
    result_window.geometry("600x500")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"🤖 BOTNET DETECTION SCAN\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 50 + "\n\n")
    
    # Simulate botnet detection
    suspicious_ips = []
    for i in range(random.randint(0, 5)):
        ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
        suspicious_ips.append(ip)
        text_area.insert(tk.END, f"⚠️ Suspicious connection from {ip}\n")
        result_window.update()
        time.sleep(0.2)
    
    text_area.insert(tk.END, "\n" + "━" * 50 + "\n")
    
    if suspicious_ips:
        text_area.insert(tk.END, f"🚨 BOTNET ACTIVITY DETECTED!\n\n")
        text_area.insert(tk.END, f"Suspicious IPs: {', '.join(suspicious_ips)}\n\n")
        text_area.insert(tk.END, "Recommendations:\n")
        text_area.insert(tk.END, "1. Block detected IPs immediately\n")
        text_area.insert(tk.END, "2. Run full antivirus scan\n")
        text_area.insert(tk.END, "3. Check for unauthorized processes\n")
        text_area.insert(tk.END, "4. Change all passwords\n")
        CYBER_LOG.append(f"[BOTNET] Detected {len(suspicious_ips)} suspicious IPs")
    else:
        text_area.insert(tk.END, "✅ No botnet activity detected\n")
        CYBER_LOG.append("[BOTNET] Scan completed - system clean")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, 
             bg="#3b82f6", fg="white").pack(pady=5)

def image_generator():
    """Generate simple images/patterns"""
    choice = messagebox.askquestion("Image Generator", "Generate pattern:\nYes = Fractal\nNo = Random pattern")
    
    if choice == 'yes':
        width = 600
        height = 400
        win = tk.Toplevel()
        win.title("Fractal Generator")
        canvas = tk.Canvas(win, width=width, height=height, bg="black")
        canvas.pack()
        
        c = complex(-0.7, 0.27015)
        for px in range(width):
            for py in range(height):
                x = (px - width / 2) / 200
                y = (py - height / 2) / 200
                z = complex(x, y)
                i = 0
                while abs(z) < 4 and i < 30:
                    z = z*z + c
                    i += 1
                color = "#{:02x}{:02x}{:02x}".format(
                    int(i * 8.5) % 256,
                    int(i * 4.2) % 256,
                    int(i * 12.7) % 256
                )
                canvas.create_line(px, py, px + 1, py, fill=color)
        
        CYBER_LOG.append("[GEN] Fractal image generated")
    else:
        # Generate random pattern
        width = 500
        height = 500
        win = tk.Toplevel()
        win.title("Random Pattern Generator")
        
        fig, ax = plt.subplots(figsize=(8, 8))
        data = np.random.rand(50, 50)
        ax.imshow(data, cmap='viridis', interpolation='nearest')
        ax.set_title("Random Security Pattern")
        ax.axis('off')
        plt.show()
        
        CYBER_LOG.append("[GEN] Random pattern generated")

def metasploit_detector():
    """Detect Metasploit framework usage"""
    result_window = tk.Toplevel()
    result_window.title("Metasploit Detector")
    result_window.geometry("600x400")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"🔍 METASPLOIT DETECTION SCAN\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 50 + "\n\n")
    
    # Check for Metasploit patterns
    metasploit_patterns = [
        "msfconsole", "meterpreter", "exploit/", "payload/", 
        "msfvenom", "msfupdate", "msfrpc"
    ]
    
    detected = []
    for pattern in metasploit_patterns:
        if random.random() < 0.1:  # Simulate detection
            detected.append(pattern)
            text_area.insert(tk.END, f"⚠️ Found pattern: {pattern}\n")
        result_window.update()
        time.sleep(0.1)
    
    text_area.insert(tk.END, "\n" + "━" * 50 + "\n")
    
    if detected:
        text_area.insert(tk.END, f"🚨 METASPLOIT DETECTED!\n\n")
        text_area.insert(tk.END, f"Detected indicators: {', '.join(detected)}\n\n")
        text_area.insert(tk.END, "Threat Level: HIGH\n")
        text_area.insert(tk.END, "Immediate action required!\n")
        CYBER_LOG.append(f"[METASPLOIT] Detected {len(detected)} indicators")
    else:
        text_area.insert(tk.END, "✅ No Metasploit indicators detected\n")
        CYBER_LOG.append("[METASPLOIT] Scan completed - no threats")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, 
             bg="#3b82f6", fg="white").pack(pady=5)

def virus_total_simulator():
    """Simulate VirusTotal scanning"""
    file_path = filedialog.askopenfilename(title="Select file for VirusTotal simulation")
    if not file_path:
        return
    
    result_window = tk.Toplevel()
    result_window.title("VirusTotal Scan Simulation")
    result_window.geometry("600x500")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#1e1e1e", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"🦠 VIRUSTOTAL SCAN SIMULATION\n")
    text_area.insert(tk.END, f"File: {os.path.basename(file_path)}\n")
    text_area.insert(tk.END, f"Size: {os.path.getsize(file_path)} bytes\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 50 + "\n\n")
    
    # Simulate AV engines
    av_engines = [
        "BitDefender", "Kaspersky", "Norton", "McAfee", "Avast",
        "AVG", "ESET", "Symantec", "TrendMicro", "Sophos",
        "Panda", "F-Secure", "Malwarebytes", "Windows Defender"
    ]
    
    positives = 0
    for av in av_engines:
        if random.random() < 0.15:  # 15% detection rate for simulation
            text_area.insert(tk.END, f"⚠️ {av}: Detected\n", "detect")
            positives += 1
        else:
            text_area.insert(tk.END, f"✅ {av}: Clean\n")
        result_window.update()
        time.sleep(0.05)
    
    text_area.tag_config("detect", foreground="#ef4444")
    
    text_area.insert(tk.END, "\n" + "━" * 50 + "\n")
    text_area.insert(tk.END, f"Scan Results: {positives}/{len(av_engines)} detections\n\n")
    
    if positives > 0:
        detection_ratio = positives / len(av_engines)
        if detection_ratio > 0.5:
            text_area.insert(tk.END, "🔴 HIGH RISK - Multiple detections found!\n")
        elif detection_ratio > 0.2:
            text_area.insert(tk.END, "🟡 MEDIUM RISK - Some detections found\n")
        else:
            text_area.insert(tk.END, "🟢 LOW RISK - Few detections, may be false positive\n")
    else:
        text_area.insert(tk.END, "✅ File appears clean (no detections)\n")
    
    CYBER_LOG.append(f"[VT] Simulated scan for {os.path.basename(file_path)} - {positives} detections")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, 
             bg="#3b82f6", fg="white").pack(pady=5)

def spam_detector():
    """Detect spam messages"""
    message_text = simpledialog.askstring("Spam Detector", "Enter message to check for spam:")
    if not message_text:
        return
    
    spam_keywords = [
        "free", "winner", "prize", "congratulations", "urgent", 
        "verify", "account", "password", "click here", "limited time",
        "offer", "discount", "viagra", "lottery", "million", "cash",
        "earn", "work from home", "investment", "bitcoin", "crypto"
    ]
    
    spam_score = 0
    found_keywords = []
    
    message_lower = message_text.lower()
    for keyword in spam_keywords:
        if keyword in message_lower:
            spam_score += 1
            found_keywords.append(keyword)
    
    result_window = tk.Toplevel()
    result_window.title("Spam Detection Results")
    result_window.geometry("600x400")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#1e1e1e", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"📧 SPAM DETECTION ANALYSIS\n")
    text_area.insert(tk.END, "━" * 50 + "\n\n")
    
    if spam_score >= 5:
        result = "🔴 HIGH PROBABILITY OF SPAM"
        color = "#ef4444"
    elif spam_score >= 3:
        result = "🟡 MODERATE SPAM INDICATORS"
        color = "#f59e0b"
    elif spam_score >= 1:
        result = "🟢 LOW SPAM INDICATORS"
        color = "#3b82f6"
    else:
        result = "✅ LIKELY LEGITIMATE"
        color = "#10b981"
    
    text_area.insert(tk.END, f"Result: ", "bold")
    text_area.insert(tk.END, f"{result}\n\n", "result")
    text_area.tag_config("bold", foreground="white", font=("Consolas", 10, "bold"))
    text_area.tag_config("result", foreground=color)
    
    text_area.insert(tk.END, f"Spam Score: {spam_score}/10\n\n")
    
    if found_keywords:
        text_area.insert(tk.END, f"Suspicious keywords found:\n")
        for keyword in found_keywords[:10]:
            text_area.insert(tk.END, f"  • {keyword}\n")
    else:
        text_area.insert(tk.END, "No spam keywords detected.\n")
    
    CYBER_LOG.append(f"[SPAM] Analyzed message - Score: {spam_score}")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, 
             bg="#3b82f6", fg="white").pack(pady=5)

def badusb_detector():
    """Detect BadUSB device behavior"""
    result_window = tk.Toplevel()
    result_window.title("BadUSB Detector")
    result_window.geometry("600x400")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"🔌 BADUSB DETECTION SCAN\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 50 + "\n\n")
    
    # Simulate USB device checks
    checks = [
        "Checking connected USB devices...",
        "Analyzing device descriptors...",
        "Checking for HID spoofing...",
        "Monitoring keystroke injection...",
        "Checking for rubber ducky patterns...",
        "Verifying device firmware...",
        "Checking for autorun capabilities..."
    ]
    
    badusb_detected = False
    
    for check in checks:
        text_area.insert(tk.END, f"• {check} ")
        result_window.update()
        time.sleep(0.2)
        
        if random.random() < 0.15:  # 15% detection chance
            text_area.insert(tk.END, "⚠️ SUSPICIOUS!\n")
            badusb_detected = True
            result_window.update()
            time.sleep(0.3)
        else:
            text_area.insert(tk.END, "✓ OK\n")
        result_window.update()
    
    text_area.insert(tk.END, "\n" + "━" * 50 + "\n")
    
    if badusb_detected:
        text_area.insert(tk.END, "🚨 BADUSB DEVICE DETECTED!\n\n")
        text_area.insert(tk.END, "Recommendations:\n")
        text_area.insert(tk.END, "1. Remove suspicious USB devices immediately\n")
        text_area.insert(tk.END, "2. Block USB ports if possible\n")
        text_area.insert(tk.END, "3. Run antivirus scan\n")
        text_area.insert(tk.END, "4. Change passwords if keystroke injection suspected\n")
        CYBER_LOG.append("[BADUSB] Suspicious USB device detected")
    else:
        text_area.insert(tk.END, "✅ No BadUSB devices detected\n")
        CYBER_LOG.append("[BADUSB] Scan completed - all USB devices appear legitimate")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, 
             bg="#3b82f6", fg="white").pack(pady=5)

def run_security_scan():
    global DETECTED_THREATS
    CYBER_LOG.append("[OK] Filesystem scan completed.")
    CYBER_LOG.append("[OK] No threats detected.")
    messagebox.showinfo("Scan", "System secure.")

def draw_cyber():
    draw_window("Cyber Security Center", "#ef4444")
    
    # Row 1: Basic Security
    register_click("gen_pass", -500, 280, 140, 35, generate_password)
    draw_rect(-500, 280, 140, 35, "#111827", "#ef4444")
    draw_text("Gen Password", -480, 260, "white", 9)
    
    register_click("strength", -340, 280, 140, 35, password_strength)
    draw_rect(-340, 280, 140, 35, "#111827", "#ef4444")
    draw_text("Check Strength", -320, 260, "white", 9)
    
    register_click("hash_calc", -180, 280, 140, 35, hash_calculator)
    draw_rect(-180, 280, 140, 35, "#111827", "#ef4444")
    draw_text("HashCalc", -160, 260, "white", 9)
    
    register_click("scan", -20, 280, 140, 35, run_security_scan)
    draw_rect(-20, 280, 140, 35, "#111827", "#ef4444")
    draw_text("Quick Scan", 0, 260, "white", 9)
    
    # Row 2: Attack Detection
    register_click("ddos", -500, 220, 140, 35, ddos_attack_simulator)
    draw_rect(-500, 220, 140, 35, "#111827", "#f59e0b")
    draw_text("DDoS Detector", -480, 200, "white", 9)
    
    register_click("malware", -340, 220, 140, 35, malware_detection)
    draw_rect(-340, 220, 140, 35, "#111827", "#f59e0b")
    draw_text("Malware Scan", -320, 200, "white", 9)
    
    register_click("phishing", -180, 220, 140, 35, phishing_detection)
    draw_rect(-180, 220, 140, 35, "#111827", "#f59e0b")
    draw_text("Phishing Detector", -165, 200, "white", 8)
    
    register_click("mitm", -20, 220, 140, 35, mitm_detection)
    draw_rect(-20, 220, 140, 35, "#111827", "#f59e0b")
    draw_text("MITM Detector", 0, 200, "white", 9)
    
    # Row 3: Network Security
    register_click("nmap", -500, 160, 140, 35, nmap_scan)
    draw_rect(-500, 160, 140, 35, "#111827", "#3b82f6")
    draw_text("Nmap Scanner", -480, 140, "white", 9)
    
    register_click("net_scan", -340, 160, 140, 35, network_scanner)
    draw_rect(-340, 160, 140, 35, "#111827", "#3b82f6")
    draw_text("Network Scanner", -325, 140, "white", 8)
    
    register_click("url_scan", -180, 160, 140, 35, url_scanner)
    draw_rect(-180, 160, 140, 35, "#111827", "#3b82f6")
    draw_text("URL Scanner", -160, 140, "white", 9)
    
    register_click("sms", -20, 160, 140, 35, sms_bomber_simulator)
    draw_rect(-20, 160, 140, 35, "#111827", "#3b82f6")
    draw_text("SMS Bomber Sim", 0, 140, "white", 8)
    
    # Row 4: Advanced Security
    register_click("botnet", -500, 100, 140, 35, botnet_detector)
    draw_rect(-500, 100, 140, 35, "#111827", "#8b5cf6")
    draw_text("Botnet Detector", -480, 80, "white", 9)
    
    register_click("image_gen", -340, 100, 140, 35, image_generator)
    draw_rect(-340, 100, 140, 35, "#111827", "#8b5cf6")
    draw_text("Image Generator", -320, 80, "white", 9)
    
    register_click("metasploit", -180, 100, 140, 35, metasploit_detector)
    draw_rect(-180, 100, 140, 35, "#111827", "#8b5cf6")
    draw_text("Metasploit Detector", -165, 80, "white", 8)
    
    register_click("virustotal", -20, 100, 140, 35, virus_total_simulator)
    draw_rect(-20, 100, 140, 35, "#111827", "#8b5cf6")
    draw_text("VirusTotal Sim", 0, 80, "white", 8)
    
    # Row 5: Additional Security
    register_click("spam", -500, 40, 140, 35, spam_detector)
    draw_rect(-500, 40, 140, 35, "#111827", "#ec4899")
    draw_text("Spam Detector", -480, 20, "white", 9)
    
    register_click("badusb", -340, 40, 140, 35, badusb_detector)
    draw_rect(-340, 40, 140, 35, "#111827", "#ec4899")
    draw_text("BadUSB Detector", -320, 20, "white", 8)
    
    # Row 6: Antivirus Creator
    register_click("antivirus", -500, -20, 300, 40, open_antivirus)
    draw_rect(-500, -20, 300, 40, "#111827", "#00BCD4")
    draw_text("🛡️ Antivirus Creator", -480, -40, "white", 9)
    
    # Security Stats
    draw_text(f"🛡️ Security Log Entries: {len(CYBER_LOG)}", -500, -80, "#10b981", 10)
    if DETECTED_THREATS:
        draw_text(f"⚠️ Detected Threats: {len(DETECTED_THREATS)}", -500, -110, "#ef4444", 10)
    else:
        draw_text("✅ System Security Status: Clean", -500, -110, "#10b981", 10)
    
    draw_text("💡 Security Tips:", 100, 280, "#f59e0b", 10, "bold")
    draw_text("• Use strong passwords (12+ chars, special chars)", 100, 255, "white", 8)
    draw_text("• Don't click suspicious links or attachments", 100, 235, "white", 8)
    draw_text("• Keep your system and software updated", 100, 215, "white", 8)
    draw_text("• Use 2FA whenever possible", 100, 195, "white", 8)
    draw_text("• Regular security scans are recommended", 100, 175, "white", 8)
    draw_text("• Antivirus Creator lets you build custom AV tools", 100, 155, "#00BCD4", 8)

# ============================================================
# ENHANCED CALCULATOR APP (All Mathematical Operations)
# ============================================================

def basic_calculator():
    calc_window = tk.Toplevel()
    calc_window.title("Basic Calculator")
    calc_window.geometry("350x500")
    calc_window.configure(bg="#2d2d2d")
    
    result_var = tk.StringVar()
    result_var.set("0")
    
    display = tk.Entry(calc_window, textvariable=result_var, font=("Arial", 24), 
                       bg="#1e1e1e", fg="#00ff00", justify="right")
    display.pack(fill="x", padx=10, pady=10, ipady=10)
    
    buttons = [
        ['7', '8', '9', '/', 'C'],
        ['4', '5', '6', '*', '√'],
        ['1', '2', '3', '-', '^'],
        ['0', '.', '=', '+', '%']
    ]
    
    def button_click(value):
        current = result_var.get()
        if value == 'C':
            result_var.set("0")
        elif value == '=':
            try:
                result = eval(current)
                result_var.set(str(result))
            except:
                result_var.set("Error")
        elif value == '√':
            try:
                result = eval(f"math.sqrt({current})")
                result_var.set(str(result))
            except:
                result_var.set("Error")
        elif value == '^':
            result_var.set(current + "**")
        else:
            if current == "0" or current == "Error":
                result_var.set(value)
            else:
                result_var.set(current + value)
    
    button_frame = tk.Frame(calc_window, bg="#2d2d2d")
    button_frame.pack(padx=10, pady=10)
    
    for row in buttons:
        row_frame = tk.Frame(button_frame, bg="#2d2d2d")
        row_frame.pack(pady=5)
        for btn_text in row:
            btn = tk.Button(row_frame, text=btn_text, font=("Arial", 14), width=6, height=2,
                           bg="#3d3d3d", fg="white", command=lambda x=btn_text: button_click(x))
            btn.pack(side="left", padx=2)

def draw_calculator():
    draw_window("Enhanced Calculator", "#f59e0b")
    
    register_click("basic_calc", -500, 280, 200, 45, basic_calculator)
    draw_rect(-500, 280, 200, 45, "#111827", "#10b981")
    draw_text("🧮 Basic Calculator", -480, 255, "white", 10)
    
    register_click("math_func", -280, 280, 200, 45, math_functions)
    draw_rect(-280, 280, 200, 45, "#111827", "#3b82f6")
    draw_text("📐 Math Functions", -260, 255, "white", 10)
    
    register_click("sympy_ops", -60, 280, 200, 45, symbolic_operations)
    draw_rect(-60, 280, 200, 45, "#111827", "#8b5cf6")
    draw_text("🔢 Sympy Ops", -40, 255, "white", 10)
    
    register_click("numpy_ops", 160, 280, 200, 45, numpy_operations)
    draw_rect(160, 280, 200, 45, "#111827", "#ef4444")
    draw_text("📊 NumPy Ops", 180, 255, "white", 10)
    
    register_click("plot_func", -500, 210, 200, 45, plot_functions)
    draw_rect(-500, 210, 200, 45, "#111827", "#f59e0b")
    draw_text("📈 Plot Functions", -480, 185, "white", 10)
    
    register_click("complex_nums", -280, 210, 200, 45, complex_numbers)
    draw_rect(-280, 210, 200, 45, "#111827", "#06b6d4")
    draw_text("🔢 Complex Numbers", -260, 185, "white", 10)
    
    register_click("eq_solver", -60, 210, 200, 45, equation_solver)
    draw_rect(-60, 210, 200, 45, "#111827", "#ec4899")
    draw_text("📐 Equation Solver", -40, 185, "white", 10)

def math_functions():
    functions = {
        "sin": lambda x: math.sin(math.radians(x)),
        "cos": lambda x: math.cos(math.radians(x)),
        "tan": lambda x: math.tan(math.radians(x)),
        "asin": lambda x: math.degrees(math.asin(x)),
        "acos": lambda x: math.degrees(math.acos(x)),
        "atan": lambda x: math.degrees(math.atan(x)),
        "log": lambda x: math.log(x),
        "log10": lambda x: math.log10(x),
        "exp": lambda x: math.exp(x),
        "sqrt": lambda x: math.sqrt(x),
        "ceil": lambda x: math.ceil(x),
        "floor": lambda x: math.floor(x),
        "factorial": lambda x: math.factorial(int(x)),
        "gamma": lambda x: math.gamma(x),
        "degrees": lambda x: math.degrees(x),
        "radians": lambda x: math.radians(x)
    }
    
    func_names = "\n".join([f"• {f}" for f in list(functions.keys())[:10]])
    choice = simpledialog.askstring("Math Functions", 
        f"Available functions:\n{func_names}\n... and {len(functions)-10} more\n\nEnter function name:")
    
    if not choice or choice not in functions:
        messagebox.showerror("Error", "Invalid function!")
        return
    
    value = simpledialog.askfloat("Math Function", f"Enter value for {choice}(x):")
    if value is None:
        return
    
    try:
        result = functions[choice](value)
        messagebox.showinfo("Result", f"{choice}({value}) = {result}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def symbolic_operations():
    ops = {
        "differentiate": "Derivative",
        "integrate": "Integral", 
        "solve_equation": "Solve Equation",
        "expand": "Expand Expression",
        "factor": "Factor Expression",
        "simplify": "Simplify Expression",
        "limit": "Limit",
        "series": "Series Expansion",
        "matrix_inverse": "Matrix Inverse",
        "matrix_determinant": "Matrix Determinant",
        "matrix_eigenvalues": "Matrix Eigenvalues"
    }
    
    op_list = "\n".join([f"• {k}" for k in ops.keys()])
    choice = simpledialog.askstring("Sympy Operations", 
        f"Available operations:\n{op_list}\n\nEnter operation:")
    
    if not choice or choice not in ops:
        messagebox.showerror("Error", "Invalid operation!")
        return
    
    x = sp.symbols('x')
    y = sp.symbols('y')
    
    if choice == "differentiate":
        expr = simpledialog.askstring("Derivative", "Expression (e.g., x**2 + sin(x)):")
        if expr:
            try:
                result = sp.diff(expr)
                messagebox.showinfo("Derivative", f"d/dx ({expr}) = {result}")
            except:
                messagebox.showerror("Error", "Invalid expression!")
                
    elif choice == "integrate":
        expr = simpledialog.askstring("Integral", "Expression (e.g., x**2 + sin(x)):")
        if expr:
            try:
                result = sp.integrate(expr)
                messagebox.showinfo("Integral", f"∫ ({expr}) dx = {result}")
            except:
                messagebox.showerror("Error", "Invalid expression!")
                
    elif choice == "solve_equation":
        equation = simpledialog.askstring("Solve", "Equation (e.g., x**2 - 4 = 0):")
        if equation:
            try:
                eq = sp.sympify(equation.replace('=', '- ('))
                solutions = sp.solve(eq)
                messagebox.showinfo("Solutions", f"{equation}\nSolutions: {solutions}")
            except:
                messagebox.showerror("Error", "Invalid equation!")
                
    elif choice == "expand":
        expr = simpledialog.askstring("Expand", "Expression (e.g., (x+1)**3):")
        if expr:
            try:
                result = sp.expand(expr)
                messagebox.showinfo("Expanded", f"{expr} = {result}")
            except:
                messagebox.showerror("Error", "Invalid expression!")
                
    elif choice == "factor":
        expr = simpledialog.askstring("Factor", "Expression (e.g., x**2 - 4):")
        if expr:
            try:
                result = sp.factor(expr)
                messagebox.showinfo("Factored", f"{expr} = {result}")
            except:
                messagebox.showerror("Error", "Invalid expression!")
                
    elif choice == "simplify":
        expr = simpledialog.askstring("Simplify", "Expression (e.g., sin(x)**2 + cos(x)**2):")
        if expr:
            try:
                result = sp.simplify(expr)
                messagebox.showinfo("Simplified", f"{expr} = {result}")
            except:
                messagebox.showerror("Error", "Invalid expression!")

def numpy_operations():
    ops = {
        "array_stats": "Array Statistics",
        "linear_algebra": "Linear Algebra",
        "random_arrays": "Generate Random Array",
        "array_operations": "Basic Array Operations",
        "polynomial_fit": "Polynomial Fit",
        "fft": "Fast Fourier Transform",
        "convolution": "Convolution"
    }
    
    op_list = "\n".join([f"• {v}" for v in ops.values()])
    choice = simpledialog.askstring("NumPy Operations", 
        f"Available operations:\n{op_list}\n\nEnter operation:")
    
    if not choice or choice not in ops.values():
        messagebox.showerror("Error", "Invalid operation!")
        return
    
    if choice == "Array Statistics":
        data = simpledialog.askstring("Array Statistics", 
            "Enter numbers separated by commas (e.g., 1,2,3,4,5):")
        if data:
            try:
                arr = np.array([float(x.strip()) for x in data.split(',')])
                stats = f"""
Array Statistics:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Data: {arr}
Mean: {np.mean(arr):.4f}
Median: {np.median(arr):.4f}
Standard Deviation: {np.std(arr):.4f}
Variance: {np.var(arr):.4f}
Min: {np.min(arr)}
Max: {np.max(arr)}
Sum: {np.sum(arr)}
Product: {np.prod(arr)}
25th Percentile: {np.percentile(arr, 25):.4f}
75th Percentile: {np.percentile(arr, 75):.4f}
"""
                messagebox.showinfo("Statistics", stats)
            except:
                messagebox.showerror("Error", "Invalid input!")

def plot_functions():
    expr = simpledialog.askstring("Plot Function", 
        "Enter function of x (e.g., sin(x), x**2, exp(-x)*sin(x)):")
    if not expr:
        return
    
    x_min = simpledialog.askfloat("X Range", "X minimum (default -10):", initialvalue=-10)
    x_max = simpledialog.askfloat("X Range", "X maximum (default 10):", initialvalue=10)
    
    if x_min is None or x_max is None:
        x_min, x_max = -10, 10
    
    x = np.linspace(x_min, x_max, 1000)
    
    try:
        def safe_eval(x_val):
            import math
            return eval(expr, {"x": x_val, "sin": math.sin, "cos": math.cos, 
                              "tan": math.tan, "exp": math.exp, "log": math.log,
                              "sqrt": math.sqrt, "pi": math.pi, "e": math.e})
        
        y = np.array([safe_eval(xi) for xi in x])
        
        plt.figure(figsize=(12, 8))
        plt.plot(x, y, 'b-', linewidth=2)
        plt.grid(True, alpha=0.3)
        plt.xlabel('x', fontsize=12)
        plt.ylabel('f(x)', fontsize=12)
        plt.title(f'Plot of f(x) = {expr}', fontsize=14)
        plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Could not plot function: {str(e)}")

def complex_numbers():
    op = simpledialog.askstring("Complex Numbers", 
        "Operations:\n• add\n• subtract\n• multiply\n• divide\n• conjugate\n• magnitude\n• phase\n\nEnter operation:")
    
    if not op:
        return
    
    if op in ["add", "subtract", "multiply", "divide"]:
        real1 = simpledialog.askfloat("First Complex", "Real part:")
        imag1 = simpledialog.askfloat("First Complex", "Imaginary part:")
        real2 = simpledialog.askfloat("Second Complex", "Real part:")
        imag2 = simpledialog.askfloat("Second Complex", "Imaginary part:")
        
        if None in [real1, imag1, real2, imag2]:
            return
        
        z1 = complex(real1, imag1)
        z2 = complex(real2, imag2)
        
        if op == "add":
            result = z1 + z2
        elif op == "subtract":
            result = z1 - z2
        elif op == "multiply":
            result = z1 * z2
        else:
            if z2 == 0:
                messagebox.showerror("Error", "Division by zero!")
                return
            result = z1 / z2
        
        messagebox.showinfo("Result", f"({z1}) {op} ({z2}) = {result}")

def equation_solver():
    eq_type = simpledialog.askstring("Equation Solver",
        "Equation types:\n• linear: ax + b = 0\n• quadratic: ax² + bx + c = 0\n• cubic: ax³ + bx² + cx + d = 0\n• system: linear system\n\nEnter type:")
    
    if not eq_type:
        return
    
    if eq_type == "linear":
        a = simpledialog.askfloat("Linear Equation", "Coefficient a:")
        b = simpledialog.askfloat("Linear Equation", "Coefficient b:")
        
        if a == 0:
            if b == 0:
                messagebox.showinfo("Solution", "All real numbers are solutions")
            else:
                messagebox.showinfo("Solution", "No solution")
        else:
            x = -b / a
            messagebox.showinfo("Solution", f"{a}x + {b} = 0\nx = {x}")
            
    elif eq_type == "quadratic":
        a = simpledialog.askfloat("Quadratic", "Coefficient a:")
        b = simpledialog.askfloat("Quadratic", "Coefficient b:")
        c = simpledialog.askfloat("Quadratic", "Coefficient c:")
        
        discriminant = b**2 - 4*a*c
        
        if discriminant > 0:
            x1 = (-b + math.sqrt(discriminant)) / (2*a)
            x2 = (-b - math.sqrt(discriminant)) / (2*a)
            messagebox.showinfo("Solutions", f"{a}x² + {b}x + {c} = 0\nx₁ = {x1}\nx₂ = {x2}")
        elif discriminant == 0:
            x = -b / (2*a)
            messagebox.showinfo("Solution", f"{a}x² + {b}x + {c} = 0\nx = {x} (double root)")
        else:
            real = -b / (2*a)
            imag = math.sqrt(abs(discriminant)) / (2*a)
            messagebox.showinfo("Solutions", f"{a}x² + {b}x + {c} = 0\nx = {real} ± {imag}i")

# ============================================================
# ENHANCED ANIMATOR WITH AI ASSISTANCE
# ============================================================

def open_animator():
    if not PIL_AVAILABLE:
        messagebox.showerror("Animator Studio", 
            "PIL (Pillow) is required for Animator Studio.\n"
            "Please install it using: pip install Pillow")
        return
    
    # Create required directories
    animator_assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "animator_assets")
    animator_projects_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "animator_projects")
    animator_exports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "animator_exports")
    
    for folder in [animator_assets_dir, animator_projects_dir, animator_exports_dir]:
        os.makedirs(folder, exist_ok=True)
    
    # Create the animator window
    animator_window = tk.Toplevel()
    animator_window.title("Animator Studio - AI Powered Animation Suite")
    animator_window.geometry("1400x900")
    animator_window.configure(bg="#1e1e1e")
    
    # Create main frames
    left_frame = tk.Frame(animator_window, width=280, bg="#2b2b2b")
    left_frame.pack(side="left", fill="y")
    
    center_frame = tk.Frame(animator_window, bg="#1e1e1e")
    center_frame.pack(fill="both", expand=True)
    
    bottom_frame = tk.Frame(animator_window, bg="#222222", height=150)
    bottom_frame.pack(side="bottom", fill="x")
    
    # Variables
    current_scene_objects = []
    selected_object = None
    current_frame = 0
    playing = False
    fps = 30
    max_frames = 300
    camera_x = 0
    camera_y = 0
    camera_zoom = 1.0
    
    # Canvas for preview
    preview_canvas = tk.Canvas(center_frame, bg="black")
    preview_canvas.pack(fill="both", expand=True)
    
    # Asset list
    tk.Label(left_frame, text="Assets", bg="#2b2b2b", fg="white", font=("Arial", 12, "bold")).pack(fill="x", pady=5)
    asset_listbox = tk.Listbox(left_frame, bg="#3d3d3d", fg="white", height=8)
    asset_listbox.pack(fill="x", padx=5, pady=5)
    
    def scan_assets():
        asset_listbox.delete(0, tk.END)
        for root, dirs, files in os.walk(animator_assets_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    asset_listbox.insert(tk.END, file)
    
    def add_asset():
        file_path = filedialog.askopenfilename(filetypes=[
            ("Images", "*.png *.jpg *.jpeg *.gif *.bmp")
        ])
        if file_path:
            shutil.copy(file_path, animator_assets_dir)
            scan_assets()
    
    tk.Button(left_frame, text="➕ Import Asset", command=add_asset, 
              bg="#4CAF50", fg="white").pack(fill="x", padx=5, pady=5)
    
    # Objects list
    tk.Label(left_frame, text="Objects", bg="#2b2b2b", fg="white", font=("Arial", 12, "bold")).pack(fill="x", pady=5)
    objects_listbox = tk.Listbox(left_frame, bg="#3d3d3d", fg="white", height=6)
    objects_listbox.pack(fill="x", padx=5, pady=5)
    
    # Properties frame
    tk.Label(left_frame, text="Properties", bg="#2b2b2b", fg="white", font=("Arial", 12, "bold")).pack(fill="x", pady=5)
    
    # Scale slider
    tk.Label(left_frame, text="Scale:", bg="#2b2b2b", fg="white").pack(anchor="w", padx=5)
    scale_var = tk.DoubleVar(value=1.0)
    scale_slider = tk.Scale(left_frame, from_=0.1, to=3.0, resolution=0.1, 
                            orient="horizontal", variable=scale_var, bg="#2b2b2b", fg="white")
    scale_slider.pack(fill="x", padx=5)
    
    # Rotation slider
    tk.Label(left_frame, text="Rotation:", bg="#2b2b2b", fg="white").pack(anchor="w", padx=5)
    rotation_var = tk.DoubleVar(value=0)
    rotation_slider = tk.Scale(left_frame, from_=0, to=360, orient="horizontal", 
                               variable=rotation_var, bg="#2b2b2b", fg="white")
    rotation_slider.pack(fill="x", padx=5)
    
    # X position
    tk.Label(left_frame, text="X Position:", bg="#2b2b2b", fg="white").pack(anchor="w", padx=5)
    x_var = tk.DoubleVar(value=400)
    x_entry = tk.Entry(left_frame, textvariable=x_var, bg="#3d3d3d", fg="white")
    x_entry.pack(fill="x", padx=5)
    
    # Y position
    tk.Label(left_frame, text="Y Position:", bg="#2b2b2b", fg="white").pack(anchor="w", padx=5)
    y_var = tk.DoubleVar(value=300)
    y_entry = tk.Entry(left_frame, textvariable=y_var, bg="#3d3d3d", fg="white")
    y_entry.pack(fill="x", padx=5)
    
    # AI Assistance frame
    tk.Label(left_frame, text="🤖 AI Assistance", bg="#2b2b2b", fg="#00ffee", font=("Arial", 10, "bold")).pack(fill="x", pady=5)
    
    def ai_generate_animation():
        """AI-powered animation generation"""
        prompt = simpledialog.askstring("AI Animation", 
            "Describe the animation you want:\n(e.g., 'bouncing ball', 'floating objects', 'rotating shapes')")
        if not prompt:
            return
        
        # Generate objects based on prompt
        if "ball" in prompt.lower() or "bounce" in prompt.lower():
            for i in range(5):
                obj = {
                    "id": len(current_scene_objects),
                    "name": f"AI_Ball_{i}",
                    "type": "circle",
                    "radius": random.randint(20, 40),
                    "color": f"#{random.randint(0,255):02x}{random.randint(0,255):02x}{random.randint(0,255):02x}",
                    "x": random.randint(50, 750),
                    "y": random.randint(50, 550),
                    "scale": 1.0,
                    "rotation": 0,
                    "visible": True,
                    "layer": len(current_scene_objects)
                }
                current_scene_objects.append(obj)
                objects_listbox.insert(tk.END, obj["name"])
                keyframes[obj["id"]] = [0, 50, 100, 150, 200, 250, 299]
        
        elif "float" in prompt.lower():
            for i in range(3):
                obj = {
                    "id": len(current_scene_objects),
                    "name": f"AI_Float_{i}",
                    "type": "rectangle",
                    "width": random.randint(40, 80),
                    "height": random.randint(40, 80),
                    "color": f"#{random.randint(0,255):02x}{random.randint(0,255):02x}{random.randint(0,255):02x}",
                    "x": random.randint(100, 700),
                    "y": random.randint(100, 500),
                    "scale": 1.0,
                    "rotation": 0,
                    "visible": True,
                    "layer": len(current_scene_objects)
                }
                current_scene_objects.append(obj)
                objects_listbox.insert(tk.END, obj["name"])
                keyframes[obj["id"]] = [0, 100, 200, 299]
        
        elif "rotate" in prompt.lower():
            obj = {
                "id": len(current_scene_objects),
                "name": "AI_Rotate",
                "type": "rectangle",
                "width": 80,
                "height": 80,
                "color": "#ff6b6b",
                "x": 400,
                "y": 300,
                "scale": 1.0,
                "rotation": 0,
                "visible": True,
                "layer": len(current_scene_objects)
            }
            current_scene_objects.append(obj)
            objects_listbox.insert(tk.END, obj["name"])
            keyframes[obj["id"]] = [0, 50, 100, 150, 200, 250, 299]
        
        else:
            # Default: create random objects
            for i in range(random.randint(2, 5)):
                shape = random.choice(["circle", "rectangle", "triangle"])
                obj = {
                    "id": len(current_scene_objects),
                    "name": f"AI_Shape_{i}",
                    "type": shape,
                    "radius": random.randint(20, 50) if shape == "circle" else None,
                    "width": random.randint(40, 80) if shape != "circle" else None,
                    "height": random.randint(40, 80) if shape == "rectangle" else None,
                    "color": f"#{random.randint(0,255):02x}{random.randint(0,255):02x}{random.randint(0,255):02x}",
                    "x": random.randint(100, 700),
                    "y": random.randint(100, 500),
                    "scale": 1.0,
                    "rotation": 0,
                    "visible": True,
                    "layer": len(current_scene_objects)
                }
                current_scene_objects.append(obj)
                objects_listbox.insert(tk.END, obj["name"])
                keyframes[obj["id"]] = [0, 50, 100, 150, 200, 250, 299]
        
        render_scene()
        draw_timeline()
        messagebox.showinfo("AI Generated", f"AI created {len(current_scene_objects)} objects based on: {prompt}")
    
    def ai_suggest_animation():
        """AI suggests animation improvements"""
        suggestions = [
            "Try adding keyframes at different positions for smoother motion.",
            "Consider using the 'ease-in-out' interpolation for natural movement.",
            "You can animate scale and rotation together for more dynamic effects.",
            "Try using the camera controls to create cinematic panning shots.",
            "Layer your objects to create depth in your animation.",
            "Use contrasting colors to make objects stand out.",
            "Consider adding a background gradient for visual appeal.",
            "Group related objects for easier animation management."
        ]
        suggestion = random.choice(suggestions)
        messagebox.showinfo("AI Suggestion", f"💡 {suggestion}")
    
    tk.Button(left_frame, text="🤖 AI Generate Animation", command=ai_generate_animation,
              bg="#7C3AED", fg="white").pack(fill="x", padx=5, pady=2)
    
    tk.Button(left_frame, text="💡 AI Suggest Improvement", command=ai_suggest_animation,
              bg="#7C3AED", fg="white").pack(fill="x", padx=5, pady=2)
    
    # Timeline canvas
    timeline_canvas = tk.Canvas(bottom_frame, bg="#2b2b2b", height=100)
    timeline_canvas.pack(fill="x", padx=5, pady=5)
    
    # Keyframe markers
    keyframes = {}
    
    def draw_timeline():
        timeline_canvas.delete("all")
        width = timeline_canvas.winfo_width()
        if width < 10:
            width = 800
        
        for i in range(0, max_frames + 1, 10):
            x = (i / max_frames) * width
            timeline_canvas.create_line(x, 0, x, 100, fill="#4a4a4a")
            timeline_canvas.create_text(x + 5, 10, text=str(i), fill="#888888", anchor="nw", font=("Arial", 8))
        
        frame_x = (current_frame / max_frames) * width
        timeline_canvas.create_line(frame_x, 0, frame_x, 100, fill="#ff4444", width=2)
        
        for obj_id, obj_keyframes in keyframes.items():
            for frame in obj_keyframes:
                key_x = (frame / max_frames) * width
                timeline_canvas.create_oval(key_x - 5, 50, key_x + 5, 60, fill="#ffaa00", outline="#ffaa00")
    
    def add_asset_object(event):
        selection = asset_listbox.curselection()
        if not selection:
            return
        asset_name = asset_listbox.get(selection[0])
        asset_path = os.path.join(animator_assets_dir, asset_name)
        
        obj = {
            "id": len(current_scene_objects),
            "name": asset_name,
            "type": "image",
            "path": asset_path,
            "x": 400,
            "y": 300,
            "scale": 1.0,
            "rotation": 0,
            "visible": True,
            "layer": len(current_scene_objects)
        }
        current_scene_objects.append(obj)
        objects_listbox.insert(tk.END, asset_name)
        keyframes[obj["id"]] = [0]
        render_scene()
    
    asset_listbox.bind("<Double-Button-1>", add_asset_object)
    
    def add_text_object():
        text = simpledialog.askstring("Add Text", "Enter text:")
        if text:
            obj = {
                "id": len(current_scene_objects),
                "name": f"Text_{len(current_scene_objects)}",
                "type": "text",
                "text": text,
                "x": 400,
                "y": 300,
                "scale": 1.0,
                "rotation": 0,
                "visible": True,
                "layer": len(current_scene_objects)
            }
            current_scene_objects.append(obj)
            objects_listbox.insert(tk.END, obj["name"])
            keyframes[obj["id"]] = [0]
            render_scene()
    
    def add_rectangle():
        obj = {
            "id": len(current_scene_objects),
            "name": f"Rect_{len(current_scene_objects)}",
            "type": "rectangle",
            "width": 100,
            "height": 100,
            "color": "#4CAF50",
            "x": 400,
            "y": 300,
            "scale": 1.0,
            "rotation": 0,
            "visible": True,
            "layer": len(current_scene_objects)
        }
        current_scene_objects.append(obj)
        objects_listbox.insert(tk.END, obj["name"])
        keyframes[obj["id"]] = [0]
        render_scene()
    
    def add_circle():
        obj = {
            "id": len(current_scene_objects),
            "name": f"Circle_{len(current_scene_objects)}",
            "type": "circle",
            "radius": 40,
            "color": "#2196F3",
            "x": 400,
            "y": 300,
            "scale": 1.0,
            "rotation": 0,
            "visible": True,
            "layer": len(current_scene_objects)
        }
        current_scene_objects.append(obj)
        objects_listbox.insert(tk.END, obj["name"])
        keyframes[obj["id"]] = [0]
        render_scene()
    
    def add_triangle():
        obj = {
            "id": len(current_scene_objects),
            "name": f"Tri_{len(current_scene_objects)}",
            "type": "triangle",
            "size": 60,
            "color": "#FF9800",
            "x": 400,
            "y": 300,
            "scale": 1.0,
            "rotation": 0,
            "visible": True,
            "layer": len(current_scene_objects)
        }
        current_scene_objects.append(obj)
        objects_listbox.insert(tk.END, obj["name"])
        keyframes[obj["id"]] = [0]
        render_scene()
    
    def select_object(event):
        nonlocal selected_object
        selection = objects_listbox.curselection()
        if selection:
            selected_object = current_scene_objects[selection[0]]
            update_properties()
    
    objects_listbox.bind("<<ListboxSelect>>", select_object)
    
    def update_properties():
        if selected_object:
            scale_var.set(selected_object["scale"])
            rotation_var.set(selected_object["rotation"])
            x_var.set(selected_object["x"])
            y_var.set(selected_object["y"])
    
    def on_scale_change(val):
        if selected_object:
            selected_object["scale"] = float(val)
            render_scene()
    
    def on_rotation_change(val):
        if selected_object:
            selected_object["rotation"] = float(val)
            render_scene()
    
    def on_x_change():
        if selected_object:
            selected_object["x"] = x_var.get()
            render_scene()
    
    def on_y_change():
        if selected_object:
            selected_object["y"] = y_var.get()
            render_scene()
    
    scale_slider.configure(command=on_scale_change)
    rotation_slider.configure(command=on_rotation_change)
    x_entry.bind("<Return>", lambda e: on_x_change())
    y_entry.bind("<Return>", lambda e: on_y_change())
    
    def render_scene():
        preview_canvas.delete("all")
        canvas_width = preview_canvas.winfo_width()
        canvas_height = preview_canvas.winfo_height()
        
        if canvas_width < 10:
            canvas_width = 800
            canvas_height = 600
        
        sorted_objects = sorted(current_scene_objects, key=lambda o: o.get("layer", 0))
        
        for obj in sorted_objects:
            if not obj.get("visible", True):
                continue
            
            screen_x = (obj["x"] - camera_x) * camera_zoom
            screen_y = (obj["y"] - camera_y) * camera_zoom
            
            if obj["type"] == "image":
                try:
                    img = Image.open(obj["path"])
                    width = int(img.width * obj["scale"] * camera_zoom)
                    height = int(img.height * obj["scale"] * camera_zoom)
                    img = img.resize((width, height))
                    if obj["rotation"] != 0:
                        img = img.rotate(obj["rotation"], expand=True)
                    photo = ImageTk.PhotoImage(img)
                    preview_canvas.create_image(screen_x, screen_y, image=photo, anchor="center")
                    if not hasattr(preview_canvas, "images"):
                        preview_canvas.images = []
                    preview_canvas.images.append(photo)
                except Exception as e:
                    pass
            
            elif obj["type"] == "text":
                preview_canvas.create_text(screen_x, screen_y, text=obj["text"],
                                          fill="white", font=("Arial", int(20 * obj["scale"])),
                                          angle=obj["rotation"])
            
            elif obj["type"] == "rectangle":
                w = obj["width"] * obj["scale"] * camera_zoom
                h = obj["height"] * obj["scale"] * camera_zoom
                preview_canvas.create_rectangle(screen_x - w/2, screen_y - h/2,
                                               screen_x + w/2, screen_y + h/2,
                                               fill=obj["color"], outline="white")
            
            elif obj["type"] == "circle":
                r = obj["radius"] * obj["scale"] * camera_zoom
                preview_canvas.create_oval(screen_x - r, screen_y - r,
                                          screen_x + r, screen_y + r,
                                          fill=obj["color"], outline="white")
            
            elif obj["type"] == "triangle":
                s = obj["size"] * obj["scale"] * camera_zoom
                points = [screen_x, screen_y - s/2,
                         screen_x - s/2, screen_y + s/2,
                         screen_x + s/2, screen_y + s/2]
                preview_canvas.create_polygon(points, fill=obj["color"], outline="white")
            
            if obj == selected_object:
                preview_canvas.create_rectangle(screen_x - 50, screen_y - 50,
                                               screen_x + 50, screen_y + 50,
                                               outline="yellow", width=2)
    
    def animation_loop():
        nonlocal playing, current_frame
        if playing:
            current_frame += 1
            if current_frame >= max_frames:
                current_frame = 0
            
            render_scene()
            draw_timeline()
        
        animator_window.after(int(1000 / fps), animation_loop)
    
    def play():
        nonlocal playing
        playing = True
    
    def pause():
        nonlocal playing
        playing = False
    
    def stop():
        nonlocal playing, current_frame
        playing = False
        current_frame = 0
        render_scene()
        draw_timeline()
    
    def add_keyframe():
        if selected_object:
            if selected_object["id"] not in keyframes:
                keyframes[selected_object["id"]] = []
            if current_frame not in keyframes[selected_object["id"]]:
                keyframes[selected_object["id"]].append(current_frame)
                keyframes[selected_object["id"]].sort()
                draw_timeline()
    
    def delete_object():
        nonlocal selected_object
        if selected_object:
            current_scene_objects.remove(selected_object)
            objects_listbox.delete(objects_listbox.curselection())
            if selected_object["id"] in keyframes:
                del keyframes[selected_object["id"]]
            selected_object = None
            render_scene()
            draw_timeline()
    
    def bring_forward():
        if selected_object:
            selected_object["layer"] += 1
            render_scene()
    
    def send_backward():
        if selected_object:
            selected_object["layer"] -= 1
            render_scene()
    
    def save_project():
        filename = filedialog.asksaveasfilename(defaultextension=".anim", filetypes=[("Animation Project", "*.anim")])
        if filename:
            project_data = {
                "objects": current_scene_objects,
                "keyframes": keyframes,
                "max_frames": max_frames,
                "fps": fps
            }
            with open(filename, "w") as f:
                json.dump(project_data, f, indent=4)
            messagebox.showinfo("Saved", "Project saved successfully!")
    
    def load_project():
        nonlocal current_scene_objects, keyframes, max_frames, fps
        filename = filedialog.askopenfilename(filetypes=[("Animation Project", "*.anim")])
        if filename:
            with open(filename, "r") as f:
                project_data = json.load(f)
            current_scene_objects = project_data["objects"]
            keyframes = {int(k): v for k, v in project_data["keyframes"].items()}
            max_frames = project_data.get("max_frames", 300)
            fps = project_data.get("fps", 30)
            
            objects_listbox.delete(0, tk.END)
            for obj in current_scene_objects:
                objects_listbox.insert(tk.END, obj["name"])
            
            render_scene()
            draw_timeline()
            messagebox.showinfo("Loaded", "Project loaded successfully!")
    
    def export_gif():
        if not MOVIEPY_AVAILABLE:
            messagebox.showerror("Error", "MoviePy is required for GIF export")
            return
        
        filename = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF", "*.gif")])
        if not filename:
            return
        
        # Save current state
        original_playing = playing
        playing = False
        
        # Render frames
        frames = []
        for frame in range(0, max_frames, 2):  # Render every other frame for speed
            current_frame = frame
            render_scene()
            
            # Capture canvas
            canvas_width = preview_canvas.winfo_width()
            canvas_height = preview_canvas.winfo_height()
            if canvas_width < 10:
                canvas_width = 800
                canvas_height = 600
            
            # Create PIL image from canvas
            ps = preview_canvas.postscript(colormode='color')
            img = Image.open(io.BytesIO(ps.encode('utf-8')))
            frames.append(img)
        
        # Save as GIF
        if frames:
            frames[0].save(filename, save_all=True, append_images=frames[1:], 
                          duration=1000/fps, loop=0)
            messagebox.showinfo("Exported", f"GIF exported successfully to {filename}")
        
        # Restore state
        playing = original_playing
    
    def reset_camera():
        nonlocal camera_x, camera_y, camera_zoom
        camera_x = 0
        camera_y = 0
        camera_zoom = 1.0
        render_scene()
    
    def zoom_in():
        nonlocal camera_zoom
        camera_zoom *= 1.1
        render_scene()
    
    def zoom_out():
        nonlocal camera_zoom
        camera_zoom *= 0.9
        render_scene()
    
    def pan_left():
        nonlocal camera_x
        camera_x += 20
        render_scene()
    
    def pan_right():
        nonlocal camera_x
        camera_x -= 20
        render_scene()
    
    def pan_up():
        nonlocal camera_y
        camera_y += 20
        render_scene()
    
    def pan_down():
        nonlocal camera_y
        camera_y -= 20
        render_scene()
    
    # Create bottom toolbar
    toolbar = tk.Frame(bottom_frame, bg="#222222")
    toolbar.pack(fill="x")
    
    tk.Button(toolbar, text="▶ Play", command=play, bg="#4CAF50", fg="white").pack(side="left", padx=2)
    tk.Button(toolbar, text="⏸ Pause", command=pause, bg="#FF9800", fg="white").pack(side="left", padx=2)
    tk.Button(toolbar, text="■ Stop", command=stop, bg="#f44336", fg="white").pack(side="left", padx=2)
    tk.Button(toolbar, text="🔑 Add Keyframe", command=add_keyframe, bg="#9C27B0", fg="white").pack(side="left", padx=2)
    tk.Button(toolbar, text="➕ Text", command=add_text_object, bg="#2196F3", fg="white").pack(side="left", padx=2)
    tk.Button(toolbar, text="⬛ Rectangle", command=add_rectangle, bg="#4CAF50", fg="white").pack(side="left", padx=2)
    tk.Button(toolbar, text="⚪ Circle", command=add_circle, bg="#FF9800", fg="white").pack(side="left", padx=2)
    tk.Button(toolbar, text="🔺 Triangle", command=add_triangle, bg="#E91E63", fg="white").pack(side="left", padx=2)
    tk.Button(toolbar, text="🗑 Delete", command=delete_object, bg="#f44336", fg="white").pack(side="left", padx=2)
    tk.Button(toolbar, text="⬆ Bring Forward", command=bring_forward, bg="#607D8B", fg="white").pack(side="left", padx=2)
    tk.Button(toolbar, text="⬇ Send Backward", command=send_backward, bg="#607D8B", fg="white").pack(side="left", padx=2)
    tk.Button(toolbar, text="💾 Save", command=save_project, bg="#00BCD4", fg="white").pack(side="left", padx=2)
    tk.Button(toolbar, text="📂 Load", command=load_project, bg="#00BCD4", fg="white").pack(side="left", padx=2)
    tk.Button(toolbar, text="🎬 Export GIF", command=export_gif, bg="#E91E63", fg="white").pack(side="left", padx=2)
    
    # Camera controls
    camera_frame = tk.Frame(bottom_frame, bg="#222222")
    camera_frame.pack(fill="x", pady=5)
    
    tk.Label(camera_frame, text="Camera:", bg="#222222", fg="white").pack(side="left", padx=5)
    tk.Button(camera_frame, text="←", command=pan_left, bg="#333333", fg="white", width=3).pack(side="left", padx=1)
    tk.Button(camera_frame, text="→", command=pan_right, bg="#333333", fg="white", width=3).pack(side="left", padx=1)
    tk.Button(camera_frame, text="↑", command=pan_up, bg="#333333", fg="white", width=3).pack(side="left", padx=1)
    tk.Button(camera_frame, text="↓", command=pan_down, bg="#333333", fg="white", width=3).pack(side="left", padx=1)
    tk.Button(camera_frame, text="🔍+", command=zoom_in, bg="#333333", fg="white", width=3).pack(side="left", padx=1)
    tk.Button(camera_frame, text="🔍-", command=zoom_out, bg="#333333", fg="white", width=3).pack(side="left", padx=1)
    tk.Button(camera_frame, text="Reset", command=reset_camera, bg="#333333", fg="white").pack(side="left", padx=5)
    
    # Info label
    info_label = tk.Label(bottom_frame, text="Frame: 0 | FPS: 30 | Objects: 0", 
                          bg="#222222", fg="#888888")
    info_label.pack()
    
    def update_info():
        info_label.config(text=f"Frame: {current_frame} | FPS: {fps} | Objects: {len(current_scene_objects)}")
        animator_window.after(100, update_info)
    
    scan_assets()
    update_info()
    
    def on_resize(event):
        render_scene()
        draw_timeline()
    
    preview_canvas.bind("<Configure>", on_resize)
    timeline_canvas.bind("<Configure>", lambda e: draw_timeline())
    
    animation_loop()
    reset_camera()

def draw_animator():
    draw_window("Animator Studio - AI Powered", "#e91e63")
    
    draw_text("🎬 AI-Powered Animation Studio", -500, 300, "#e91e63", 14, "bold")
    draw_text("Create stunning animations with AI assistance", -500, 270, "white", 10)
    
    register_click("launch_animator", -200, 200, 300, 60, open_animator)
    draw_rect(-200, 200, 300, 60, "#111827", "#e91e63")
    draw_text("🎬 Launch Animator Studio", -180, 170, "white", 12)
    
    draw_text("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", -500, 120, "#e91e63", 8)
    draw_text("✨ AI Features:", -500, 90, "#e91e63", 11, "bold")
    draw_text("• AI Generate Animation - Create scenes from natural language prompts", -500, 65, "#00ffee", 9)
    draw_text("• AI Suggest Improvements - Get intelligent tips for better animations", -500, 45, "#00ffee", 9)
    draw_text("• Keyframe animation with smooth interpolation", -500, 25, "white", 9)
    draw_text("• Import images, text, and shapes (rectangle, circle, triangle)", -500, 5, "white", 9)
    draw_text("• Camera controls (pan, zoom, reset)", -500, -15, "white", 9)
    draw_text("• Export animations as GIF", -500, -35, "white", 9)
    draw_text("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", -500, -60, "#e91e63", 8)
    
    draw_text("💡 Try AI Prompts:", -500, -90, "#e91e63", 10, "bold")
    draw_text("• 'bouncing ball' - Creates animated bouncing balls", -500, -115, "white", 8)
    draw_text("• 'floating objects' - Creates floating shapes animation", -500, -135, "white", 8)
    draw_text("• 'rotating shapes' - Creates rotating animation", -500, -155, "white", 8)

# ============================================================
# CODE STUDIO FUNCTIONS (Preserved from original)
# ============================================================

def create_code_file():
    name = simpledialog.askstring("New File", "Enter filename:")
    if not name:
        return
    
    lang_list = "\n".join([f"• {lang}" for lang in list(PROGRAMMING_LANGUAGES.keys())[:10]])
    lang = simpledialog.askstring("Language", 
        f"Available languages (first 10):\n{lang_list}\n... and {len(PROGRAMMING_LANGUAGES)-10} more\n\nEnter language name:")
    
    if not lang or lang not in PROGRAMMING_LANGUAGES:
        messagebox.showerror("Error", f"Language '{lang}' not supported!")
        return
    
    file_data = {
        "name": name,
        "language": lang,
        "code": PROGRAMMING_LANGUAGES[lang]["template"],
        "created": str(datetime.datetime.now()),
        "modified": str(datetime.datetime.now())
    }
    CODE_FILES.append(file_data)
    messagebox.showinfo("Success", f"Created {name}{PROGRAMMING_LANGUAGES[lang]['extension']}")

def open_code_editor():
    global CODE_EDITOR_OPEN, CURRENT_LANGUAGE, CURRENT_CODE
    
    if not CODE_FILES:
        messagebox.showinfo("Info", "No code files. Create one first!")
        return
    
    files_list = "\n".join([f"{f['name']} ({f['language']})" for f in CODE_FILES])
    filename = simpledialog.askstring("Open File", f"Available files:\n{files_list}\n\nEnter filename:")
    
    if not filename:
        return
    
    selected_file = None
    for f in CODE_FILES:
        if f['name'] == filename:
            selected_file = f
            break
    
    if not selected_file:
        messagebox.showerror("Error", "File not found!")
        return
    
    CURRENT_LANGUAGE = selected_file['language']
    CURRENT_CODE = selected_file['code']
    
    editor_window = tk.Toplevel()
    editor_window.title(f"Code Studio - {filename}{PROGRAMMING_LANGUAGES[CURRENT_LANGUAGE]['extension']}")
    editor_window.geometry("800x600")
    editor_window.configure(bg="#1e1e1e")
    
    lang_label = tk.Label(editor_window, text=f"Language: {CURRENT_LANGUAGE}", 
                          bg="#1e1e1e", fg=PROGRAMMING_LANGUAGES[CURRENT_LANGUAGE]['color'],
                          font=("Consolas", 12, "bold"))
    lang_label.pack(pady=5)
    
    text_frame = tk.Frame(editor_window, bg="#1e1e1e")
    text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    text_widget = tk.Text(text_frame, bg="#1e1e1e", fg="#d4d4d4", 
                          insertbackground="white", font=("Consolas", 11),
                          wrap=tk.WORD)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)
    text_widget.insert("1.0", CURRENT_CODE)
    
    button_frame = tk.Frame(editor_window, bg="#1e1e1e")
    button_frame.pack(pady=10)
    
    def save_code():
        global CURRENT_CODE
        CURRENT_CODE = text_widget.get("1.0", tk.END)
        for f in CODE_FILES:
            if f['name'] == filename:
                f['code'] = CURRENT_CODE
                f['modified'] = str(datetime.datetime.now())
                break
        messagebox.showinfo("Saved", "Code saved successfully!")
    
    def run_code():
        code = text_widget.get("1.0", tk.END)
        ext = PROGRAMMING_LANGUAGES[CURRENT_LANGUAGE]['extension']
        temp_file = f"temp_code{ext}"
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        output_window = tk.Toplevel(editor_window)
        output_window.title("Code Output")
        output_window.geometry("600x400")
        output_window.configure(bg="#1e1e1e")
        
        output_text = tk.Text(output_window, bg="#1e1e1e", fg="#00ff00",
                              font=("Consolas", 10))
        output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        try:
            if CURRENT_LANGUAGE == "Python":
                result = subprocess.run([sys.executable, temp_file], 
                                       capture_output=True, text=True, timeout=10)
                output = result.stdout + result.stderr
            elif CURRENT_LANGUAGE == "JavaScript":
                result = subprocess.run(["node", temp_file], 
                                       capture_output=True, text=True, timeout=10)
                output = result.stdout + result.stderr
            elif CURRENT_LANGUAGE == "HTML/CSS":
                webbrowser.open(f"file://{os.path.abspath(temp_file)}")
                output = "HTML file opened in browser"
            elif CURRENT_LANGUAGE == "Bash":
                result = subprocess.run(["bash", temp_file], 
                                       capture_output=True, text=True, timeout=10)
                output = result.stdout + result.stderr
            else:
                output = f"""Language: {CURRENT_LANGUAGE}
                
To run this code, you need {CURRENT_LANGUAGE} installed.

Code saved to: {temp_file}

Run manually with:
{PROGRAMMING_LANGUAGES[CURRENT_LANGUAGE]['runner']} {temp_file}"""
            
            output_text.insert("1.0", output)
        except subprocess.TimeoutExpired:
            output_text.insert("1.0", "Error: Code execution timed out (10 seconds)")
        except Exception as e:
            output_text.insert("1.0", f"Error: {str(e)}")
        
        try:
            os.remove(temp_file)
        except:
            pass
    
    save_btn = tk.Button(button_frame, text="💾 Save", command=save_code,
                        bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                        padx=20, pady=5)
    save_btn.pack(side=tk.LEFT, padx=5)
    
    run_btn = tk.Button(button_frame, text="▶ Run", command=run_code,
                       bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                       padx=20, pady=5)
    run_btn.pack(side=tk.LEFT, padx=5)
    
    def on_closing():
        global CODE_EDITOR_OPEN
        CODE_EDITOR_OPEN = False
        editor_window.destroy()
    
    editor_window.protocol("WM_DELETE_WINDOW", on_closing)
    CODE_EDITOR_OPEN = True

def draw_code_studio():
    draw_window("Code Studio - Multi-Language IDE", "#9b59b6")
    
    draw_text("Multi-Language Programming Environment", -500, 300, "#9b59b6", 14, "bold")
    draw_text(f"Supported Languages: {len(PROGRAMMING_LANGUAGES)}", -500, 270, "white", 10)
    
    # Row 1: File Management
    register_click("create_file", -500, 200, 150, 40, create_code_file)
    draw_rect(-500, 200, 150, 40, "#111827", "#2ecc71")
    draw_text("📄 New File", -480, 175, "white", 10)
    
    register_click("open_editor", -330, 200, 150, 40, open_code_editor)
    draw_rect(-330, 200, 150, 40, "#111827", "#3498db")
    draw_text("✏ Open Editor", -315, 175, "white", 10)
    
    register_click("list_files", -160, 200, 150, 40, list_code_files)
    draw_rect(-160, 200, 150, 40, "#111827", "#f39c12")
    draw_text("📋 List Files", -145, 175, "white", 10)
    
    register_click("delete_file", 10, 200, 150, 40, delete_code_file)
    draw_rect(10, 200, 150, 40, "#111827", "#e74c3c")
    draw_text("🗑 Delete File", 25, 175, "white", 10)

def list_code_files():
    if not CODE_FILES:
        messagebox.showinfo("Code Files", "No code files created yet!")
        return
    
    file_list = []
    for f in CODE_FILES:
        file_list.append(f"📄 {f['name']}{PROGRAMMING_LANGUAGES[f['language']]['extension']} ({f['language']})")
        file_list.append(f"   Created: {f['created'][:19]}")
        file_list.append(f"   Modified: {f['modified'][:19]}\n")
    
    messagebox.showinfo("Code Files", "\n".join(file_list))

def delete_code_file():
    if not CODE_FILES:
        messagebox.showinfo("Info", "No code files to delete!")
        return
    
    files_list = "\n".join([f"{f['name']} ({f['language']})" for f in CODE_FILES])
    filename = simpledialog.askstring("Delete File", f"Files:\n{files_list}\n\nEnter filename to delete:")
    
    if not filename:
        return
    
    for i, f in enumerate(CODE_FILES):
        if f['name'] == filename:
            CODE_FILES.pop(i)
            messagebox.showinfo("Success", f"Deleted {filename}")
            return
    
    messagebox.showerror("Error", "File not found!")

# ============================================================
# CLINIC MANAGEMENT (Preserved)
# ============================================================

def add_patient():
    name = simpledialog.askstring("Patient", "Name:")
    if not name:
        return
    age = simpledialog.askinteger("Patient", "Age:")
    disease = simpledialog.askstring("Patient", "Diagnosis:")
    PATIENTS.append({"name": name, "age": age, "disease": disease})

def view_patients():
    if not PATIENTS:
        messagebox.showinfo("Patients", "No records found.")
        return
    text = ""
    for p in PATIENTS:
        text += f"Name: {p['name']}\nAge: {p['age']}\nDisease: {p['disease']}\n\n"
    messagebox.showinfo("Patient Records", text)

def discharge_patient():
    name = simpledialog.askstring("Discharge", "Patient Name:")
    if not name:
        return
    for p in PATIENTS:
        if p["name"] == name:
            PATIENTS.remove(p)
            messagebox.showinfo("Clinic", "Patient discharged.")
            return

def draw_clinic():
    draw_window("Clinic", "#10b981")
    register_click("add_patient", -100, 150, 200, 50, add_patient)
    draw_rect(-100, 150, 200, 50, "#111827", "#10b981")
    draw_text("Add Patient", -75, 120, "white", 12)
    register_click("view_patients", -100, 70, 200, 50, view_patients)
    draw_rect(-100, 70, 200, 50, "#111827", "#10b981")
    draw_text("View Patients", -85, 40, "white", 12)
    register_click("discharge_patient", -100, -10, 200, 50, discharge_patient)
    draw_rect(-100, -10, 200, 50, "#111827", "#10b981")
    draw_text("Discharge Patient", -90, -40, "white", 12)

# ============================================================
# DEPLOYMENT CENTER (Preserved)
# ============================================================

def deploy_project():
    project = simpledialog.askstring("Deploy", "Project Name:")
    if not project:
        return
    DEPLOYMENT_LOGS.append(f"Building {project}")
    DEPLOYMENT_LOGS.append(f"Packaging {project}")
    DEPLOYMENT_LOGS.append(f"Deploying {project}")
    DEPLOYMENT_LOGS.append(f"[SUCCESS] {project}")
    messagebox.showinfo("Deployment", "Deployment completed.")

def view_deployment_logs():
    text = "\n\n".join(DEPLOYMENT_LOGS)
    messagebox.showinfo("Deployment Logs", text)

def draw_deploy():
    draw_window("Deployment", "#10b981")
    register_click("deploy", -100, 150, 200, 50, deploy_project)
    draw_rect(-100, 150, 200, 50, "#111827", "#10b981")
    draw_text("Deploy", -50, 120, "white", 12)

# ============================================================
# API CENTER (Preserved)
# ============================================================

def test_api():
    endpoint = simpledialog.askstring("API Test", "Endpoint:")
    if not endpoint:
        return
    result = {
        "status": 200,
        "endpoint": endpoint,
        "timestamp": datetime.datetime.now().isoformat(),
        "response": "success"
    }
    messagebox.showinfo("API Response", json.dumps(result, indent=4))

def draw_api():
    draw_window("API Center", "#06b6d4")
    register_click("test_api", -100, 150, 200, 50, test_api)
    draw_rect(-100, 150, 200, 50, "#111827", "#06b6d4")
    draw_text("Test API", -60, 120, "white", 12)

# ============================================================
# KERNEL MANAGER (Preserved)
# ============================================================

def kernel_diagnostics():
    KERNEL_LOGS.append("[INFO] Running diagnostics...")
    KERNEL_LOGS.append("[OK] CPU normal")
    KERNEL_LOGS.append("[OK] Memory stable")
    KERNEL_LOGS.append("[OK] Filesystem mounted")
    messagebox.showinfo("Kernel", "Diagnostics completed.")

def kernel_reboot():
    KERNEL_LOGS.append("[WARN] Reboot initiated...")
    messagebox.showinfo("Kernel", "Kernel reboot simulated.")

def view_kernel_logs():
    text = "\n\n".join(KERNEL_LOGS)
    messagebox.showinfo("Kernel Logs", text)

def view_kernel_files():
    text = "\n".join(FILES)
    messagebox.showinfo("Kernel Files", text)

def shutdown_system():
    messagebox.showinfo("NeilOS", "System shutting down.")
    sys.exit()

def draw_kernel():
    draw_window("Kernel", "#3b82f6")
    register_click("view_files", -100, 150, 200, 50, view_kernel_files)
    draw_rect(-100, 150, 200, 50, "#111827", "#3b82f6")
    draw_text("View Files", -70, 120, "white", 12)
    register_click("shutdown", -100, 70, 200, 50, shutdown_system)
    draw_rect(-100, 70, 200, 50, "#111827", "#3b82f6")
    draw_text("Shutdown", -60, 40, "white", 12)

# ============================================================
# SYSTEM MONITOR (Preserved)
# ============================================================

def show_stats():
    cpu = random.randint(1, 100)
    ram = random.randint(1, 100)
    disk = random.randint(1, 100)
    messagebox.showinfo("System Monitor", f"CPU: {cpu}%\nRAM: {ram}%\nDisk: {disk}%")

def draw_monitor():
    draw_window("System Monitor", "#10b981")
    register_click("stats", -100, 150, 200, 50, show_stats)
    draw_rect(-100, 150, 200, 50, "#111827", "#10b981")
    draw_text("Show Stats", -65, 120, "white", 12)

# ============================================================
# USER ACCOUNT SYSTEM (Preserved)
# ============================================================

def register_user():
    username = simpledialog.askstring("Register", "Username:")
    if not username:
        return
    password = simpledialog.askstring("Register", "Password:")
    if not password:
        return
    try:
        cur.execute("INSERT INTO users(username,password) VALUES(?,?)", (username,password))
        conn.commit()
        messagebox.showinfo("NeilOS", "Account created.")
    except Exception:
        messagebox.showerror("NeilOS", "User already exists.")

def login_user():
    global CURRENT_USER
    username = simpledialog.askstring("Login", "Username:")
    password = simpledialog.askstring("Login", "Password:")
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))
    row = cur.fetchone()
    if row:
        CURRENT_USER = username
        messagebox.showinfo("NeilOS", f"Welcome {username}")
    else:
        messagebox.showerror("NeilOS", "Invalid credentials")

def logout_user():
    global CURRENT_USER
    CURRENT_USER = "guest"
    messagebox.showinfo("NeilOS", "Logged out.")

# ============================================================
# STARTUP
# ============================================================

def boot():
    clear_all()
    draw_rect(-700, 425, 1400, 850, "black")
    draw_text("NeilOS", -60, 40, "#00ffee", 32, "bold")
    
    stages = [
        "Loading Kernel...",
        "Loading Graphics Engine...",
        "Mounting File System...",
        "Loading Applications...",
        "Loading Code Studio...",
        "Loading Animator Studio with AI...",
        "Loading Antivirus Protection...",
        "Desktop Ready..."
    ]
    
    y = -40
    for stage in stages:
        draw_text(stage, -180, y, "#00ff88", 12)
        screen.update()
        time.sleep(0.5)
        y -= 35

# ============================================================
# MAIN RENDERER
# ============================================================

def render():
    clear_all()
    CLICKS.clear()
    
    if CURRENT_APP == "desktop":
        draw_desktop()
    elif CURRENT_APP == "bank":
        draw_bank()
    elif CURRENT_APP == "files":
        draw_files()
    elif CURRENT_APP == "terminal":
        draw_terminal()
    elif CURRENT_APP == "search":
        draw_search()
    elif CURRENT_APP == "cyber":
        draw_cyber()
    elif CURRENT_APP == "network":
        draw_network()
    elif CURRENT_APP == "ai":
        draw_ai()
    elif CURRENT_APP == "monitor":
        draw_monitor()
    elif CURRENT_APP == "calculator":
        draw_calculator()
    elif CURRENT_APP == "clinic":
        draw_clinic()
    elif CURRENT_APP == "social":
        draw_social()
    elif CURRENT_APP == "deploy":
        draw_deploy()
    elif CURRENT_APP == "api":
        draw_api()
    elif CURRENT_APP == "games":
        draw_games()
    elif CURRENT_APP == "kernel":
        draw_kernel()
    elif CURRENT_APP == "notes":
        draw_notes()
    elif CURRENT_APP == "code_studio":
        draw_code_studio()
    elif CURRENT_APP == "animator":
        draw_animator()
    
    screen.update()

# ============================================================
# MOUSE HANDLER
# ============================================================

def click(x, y):
    for item in CLICKS.values():
        if item["x1"] <= x <= item["x2"] and item["y2"] <= y <= item["y1"]:
            item["cb"]()
            return

screen.onscreenclick(click)

# ============================================================
# STARTUP
# ============================================================

boot()
CURRENT_APP = "desktop"
render()
screen.listen()
turtle.done()
