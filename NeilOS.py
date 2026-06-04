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
import string
import shutil
import subprocess
import re
import math
import cmath
import uuid
import statistics
# Try importing optional modules
try:
    import numpy as np
except ImportError:
    np = None

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import sympy as sp
except ImportError:
    sp = None

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

try:
    import scipy as sc
    from scipy import stats, integrate, optimize, linalg, signal, interpolate
except ImportError:
    sc = None
    stats = integrate = optimize = linalg = signal = interpolate = None

try:
    import requests
except ImportError:
    requests = None

# ============================================================
# DATABASE SETUP
# ============================================================

DB_FILE = "neilos.db"

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS notes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    date TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    created_date TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    amount REAL,
    date TEXT,
    description TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS contacts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    email TEXT,
    address TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    status TEXT,
    due_date TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS security_logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool TEXT,
    target TEXT,
    result TEXT,
    date TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS word_documents(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT,
    date TEXT
)
""")

conn.commit()

# ============================================================
# COMPLETE PROGRAMMING LANGUAGES DATABASE WITH URLs
# ============================================================

PROGRAMMING_LANGUAGES = {
    "Python": {
        "extension": ".py", "color": "#3776AB", 
        "url": "https://www.programiz.com/python-programming/online-compiler/",
        "editor_url": "https://www.python.org/",
        "docs": "https://docs.python.org/3/", 
        "tutorial": "https://docs.python.org/3/tutorial/",
        "year": 1991, "creator": "Guido van Rossum", "paradigm": "Multi-paradigm"
    },
    "JavaScript": {
        "extension": ".js", "color": "#F7DF1E", 
        "url": "https://www.programiz.com/javascript/online-compiler/",
        "editor_url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
        "docs": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", 
        "tutorial": "https://www.javascript.com/",
        "year": 1995, "creator": "Brendan Eich", "paradigm": "Event-driven"
    },
    "Java": {
        "extension": ".java", "color": "#007396", 
        "url": "https://www.programiz.com/java-programming/online-compiler/",
        "editor_url": "https://www.java.com/",
        "docs": "https://docs.oracle.com/en/java/", 
        "tutorial": "https://docs.oracle.com/javase/tutorial/",
        "year": 1995, "creator": "James Gosling", "paradigm": "OOP"
    },
    "C++": {
        "extension": ".cpp", "color": "#00599C", 
        "url": "https://www.programiz.com/cpp-programming/online-compiler/",
        "editor_url": "https://isocpp.org/",
        "docs": "https://en.cppreference.com/w/", 
        "tutorial": "https://www.learncpp.com/",
        "year": 1985, "creator": "Bjarne Stroustrup", "paradigm": "Multi-paradigm"
    },
    "C": {
        "extension": ".c", "color": "#A8B9CC", 
        "url": "https://www.programiz.com/c-programming/online-compiler/",
        "editor_url": "https://www.open-std.org/jtc1/sc22/wg14/",
        "docs": "https://en.cppreference.com/w/c", 
        "tutorial": "https://www.learn-c.org/",
        "year": 1972, "creator": "Dennis Ritchie", "paradigm": "Procedural"
    },
    "C#": {
        "extension": ".cs", "color": "#239120", 
        "url": "https://www.programiz.com/csharp-programming/online-compiler/",
        "editor_url": "https://docs.microsoft.com/en-us/dotnet/csharp/",
        "docs": "https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/", 
        "tutorial": "https://www.w3schools.com/cs/",
        "year": 2000, "creator": "Anders Hejlsberg", "paradigm": "Multi-paradigm"
    },
    "Ruby": {
        "extension": ".rb", "color": "#CC342D", 
        "url": "https://www.programiz.com/ruby-programming/online-compiler/",
        "editor_url": "https://www.ruby-lang.org/",
        "docs": "https://ruby-doc.org/", 
        "tutorial": "https://www.tutorialspoint.com/ruby/",
        "year": 1995, "creator": "Yukihiro Matsumoto", "paradigm": "Object-oriented"
    },
    "Go": {
        "extension": ".go", "color": "#00ADD8", 
        "url": "https://www.programiz.com/golang/online-compiler/",
        "editor_url": "https://go.dev/",
        "docs": "https://go.dev/doc/", 
        "tutorial": "https://go.dev/doc/tutorial/",
        "year": 2009, "creator": "Robert Griesemer", "paradigm": "Concurrent"
    },
    "Rust": {
        "extension": ".rs", "color": "#DEA584", 
        "url": "https://www.programiz.com/rust-programming/online-compiler/",
        "editor_url": "https://www.rust-lang.org/",
        "docs": "https://doc.rust-lang.org/", 
        "tutorial": "https://doc.rust-lang.org/book/",
        "year": 2010, "creator": "Graydon Hoare", "paradigm": "Multi-paradigm"
    },
    "PHP": {
        "extension": ".php", "color": "#777BB4", 
        "url": "https://www.programiz.com/php-programming/online-compiler/",
        "editor_url": "https://www.php.net/",
        "docs": "https://www.php.net/docs.php", 
        "tutorial": "https://www.w3schools.com/php/",
        "year": 1995, "creator": "Rasmus Lerdorf", "paradigm": "Imperative"
    },
    "Swift": {
        "extension": ".swift", "color": "#FA7343", 
        "url": "https://www.programiz.com/swift/online-compiler/",
        "editor_url": "https://swift.org/",
        "docs": "https://docs.swift.org/swift-book/", 
        "tutorial": "https://developer.apple.com/swift/",
        "year": 2014, "creator": "Chris Lattner", "paradigm": "Multi-paradigm"
    },
    "Kotlin": {
        "extension": ".kt", "color": "#7F52FF", 
        "url": "https://www.programiz.com/kotlin/online-compiler/",
        "editor_url": "https://kotlinlang.org/",
        "docs": "https://kotlinlang.org/docs/home.html", 
        "tutorial": "https://play.kotlinlang.org/",
        "year": 2011, "creator": "JetBrains", "paradigm": "Object-oriented"
    },
    "TypeScript": {
        "extension": ".ts", "color": "#3178C6", 
        "url": "https://www.programiz.com/typescript/online-compiler/",
        "editor_url": "https://www.typescriptlang.org/",
        "docs": "https://www.typescriptlang.org/docs/", 
        "tutorial": "https://www.typescriptlang.org/docs/handbook/",
        "year": 2012, "creator": "Microsoft", "paradigm": "Multi-paradigm"
    },
    "HTML": {
        "extension": ".html", "color": "#E34F26", 
        "url": "https://www.programiz.com/html/online-compiler/",
        "editor_url": "https://developer.mozilla.org/en-US/docs/Web/HTML",
        "docs": "https://developer.mozilla.org/en-US/docs/Web/HTML", 
        "tutorial": "https://www.w3schools.com/html/",
        "year": 1993, "creator": "Tim Berners-Lee", "paradigm": "Markup"
    },
    "CSS": {
        "extension": ".css", "color": "#1572B6", 
        "url": "https://www.programiz.com/css/online-compiler/",
        "editor_url": "https://developer.mozilla.org/en-US/docs/Web/CSS",
        "docs": "https://developer.mozilla.org/en-US/docs/Web/CSS", 
        "tutorial": "https://www.w3schools.com/css/",
        "year": 1996, "creator": "Håkon Wium Lie", "paradigm": "Stylesheet"
    },
    "SQL": {
        "extension": ".sql", "color": "#4479A1", 
        "url": "https://www.programiz.com/sql/online-compiler/",
        "editor_url": "https://www.mysql.com/products/workbench/",
        "docs": "https://dev.mysql.com/doc/", 
        "tutorial": "https://www.w3schools.com/sql/",
        "year": 1974, "creator": "Donald D. Chamberlin", "paradigm": "Declarative"
    },
    "Bash": {
        "extension": ".sh", "color": "#4EAA25", 
        "url": "https://www.programiz.com/bash-scripting/online-compiler/",
        "editor_url": "https://www.gnu.org/software/bash/",
        "docs": "https://www.gnu.org/software/bash/manual/", 
        "tutorial": "https://www.shellscript.sh/",
        "year": 1989, "creator": "Brian Fox", "paradigm": "Scripting"
    },
    "Earth": {
        "extension": ".earth", "color": "#2E8B57", 
        "url": "https://github.com/neilvikramkhare-beep/Earth",
        "editor_url": "https://github.com/neilvikramkhare-beep/Earth/commit/6c41802f2c8d34a39803888c6435fb73c1a75cf3",
        "docs": "https://github.com/neilvikramkhare-beep/Earth/commit/e2a988c410d90ff2ea8ad429b258f6a60086f7f3", 
        "tutorial": "https://github.com/neilvikramkhare-beep/Earth/commit/e2a988c410d90ff2ea8ad429b258f6a60086f7f3",
        "year": 2020, "creator": "Earth", "paradigm": "Portabale"
    }
}

CODE_FILES = []
CURRENT_LANGUAGE = "Python"
CURRENT_CODE = ""

PROGRAMMING_LANGUAGES.update({
    "JSON": {
        "extension": ".json", "color": "#292929",
        "url": "https://www.programiz.com/json/online-compiler/",
        "editor_url": "https://www.programiz.com/json/online-compiler/",
        "docs": "https://www.json.org/json-en.html",
        "tutorial": "https://www.w3schools.com/js/js_json_intro.asp",
        "year": 2001, "creator": "Douglas Crockford", "paradigm": "Data"
    },
    "YAML": {
        "extension": ".yaml", "color": "#cb171e",
        "url": "https://www.programiz.com/yaml-online-compiler/",
        "editor_url": "https://www.programiz.com/yaml-online-compiler/",
        "docs": "https://yaml.org/spec/",
        "tutorial": "https://www.redhat.com/en/topics/automation/what-is-yaml",
        "year": 2001, "creator": "Clark Evans", "paradigm": "Data"
    },
    "XML": {
        "extension": ".xml", "color": "#000000",
        "url": "https://www.programiz.com/xml-online-compiler/",
        "editor_url": "https://www.programiz.com/xml-online-compiler/",
        "docs": "https://www.w3.org/XML/",
        "tutorial": "https://www.w3schools.com/xml/",
        "year": 1998, "creator": "W3C", "paradigm": "Markup"
    },
    "Markdown": {
        "extension": ".md", "color": "#000000",
        "url": "https://www.programiz.com/markdown-online-editor/",
        "editor_url": "https://www.programiz.com/markdown-online-editor/",
        "docs": "https://www.markdownguide.org/basic-syntax/",
        "tutorial": "https://www.markdownguide.org/",
        "year": 2004, "creator": "John Gruber", "paradigm": "Markup"
    },
    "PowerShell": {
        "extension": ".ps1", "color": "#012456",
        "url": "https://www.programiz.com/powershell-online-compiler/",
        "editor_url": "https://www.programiz.com/powershell-online-compiler/",
        "docs": "https://docs.microsoft.com/powershell/scripting/overview",
        "tutorial": "https://docs.microsoft.com/powershell/scripting/learn/",
        "year": 2006, "creator": "Microsoft", "paradigm": "Scripting"
    },
    "Batch": {
        "extension": ".bat", "color": "#0078d7",
        "url": "https://www.programiz.com/batch-scripting/online-compiler/",
        "editor_url": "https://www.programiz.com/batch-scripting/online-compiler/",
        "docs": "https://www.robvanderwoude.com/batchfiles.php",
        "tutorial": "https://www.tutorialspoint.com/batch_script/",
        "year": 1981, "creator": "Microsoft", "paradigm": "Scripting"
    },
    "Dockerfile": {
        "extension": "Dockerfile", "color": "#0db7ed",
        "url": "https://www.docker.com/play-with-docker",
        "editor_url": "https://www.docker.com/play-with-docker",
        "docs": "https://docs.docker.com/engine/reference/builder/",
        "tutorial": "https://docs.docker.com/get-started/",
        "year": 2013, "creator": "Docker, Inc.", "paradigm": "Configuration"
    },
    "R": {
        "extension": ".r", "color": "#276dc3",
        "url": "https://www.programiz.com/r-programming/online-compiler/",
        "editor_url": "https://www.programiz.com/r-programming/online-compiler/",
        "docs": "https://cran.r-project.org/manuals.html",
        "tutorial": "https://www.datacamp.com/courses/free-introduction-to-r",
        "year": 1993, "creator": "Ross Ihaka and Robert Gentleman", "paradigm": "Statistical"
    },
    "MATLAB": {
        "extension": ".m", "color": "#e16737",
        "url": "https://www.programiz.com/matlab-online-compiler/",
        "editor_url": "https://www.programiz.com/matlab-online-compiler/",
        "docs": "https://www.mathworks.com/help/matlab/",
        "tutorial": "https://www.mathworks.com/learn/tutorials/matlab-onramp.html",
        "year": 1984, "creator": "Cleve Moler", "paradigm": "Numerical"
    },
    "Julia": {
        "extension": ".jl", "color": "#a270ba",
        "url": "https://www.programiz.com/julia-online-compiler/",
        "editor_url": "https://www.programiz.com/julia-online-compiler/",
        "docs": "https://docs.julialang.org/",
        "tutorial": "https://julialang.org/learning/",
        "year": 2012, "creator": "Jeff Bezanson et al.", "paradigm": "Technical"
    },
    "Lua": {
        "extension": ".lua", "color": "#000080",
        "url": "https://www.programiz.com/lua-programming/online-compiler/",
        "editor_url": "https://www.programiz.com/lua-programming/online-compiler/",
        "docs": "https://www.lua.org/manual/5.4/",
        "tutorial": "https://www.lua.org/pil/", 
        "year": 1993, "creator": "Roberto Ierusalimschy", "paradigm": "Scripting"
    },
    "Dart": {
        "extension": ".dart", "color": "#00b4ab",
        "url": "https://www.programiz.com/dart/online-compiler/",
        "editor_url": "https://www.programiz.com/dart/online-compiler/",
        "docs": "https://dart.dev/guides",
        "tutorial": "https://dart.dev/codelabs",
        "year": 2011, "creator": "Google", "paradigm": "Object-oriented"
    },
    "Scala": {
        "extension": ".scala", "color": "#dc322f",
        "url": "https://www.programiz.com/scala/online-compiler/",
        "editor_url": "https://www.programiz.com/scala/online-compiler/",
        "docs": "https://docs.scala-lang.org/",
        "tutorial": "https://docs.scala-lang.org/tutorials/scala-for-java-programmers.html",
        "year": 2004, "creator": "Martin Odersky", "paradigm": "Functional"
    },
    "Haskell": {
        "extension": ".hs", "color": "#5e5086",
        "url": "https://www.programiz.com/haskell/online-compiler/",
        "editor_url": "https://www.programiz.com/haskell/online-compiler/",
        "docs": "https://www.haskell.org/documentation/",
        "tutorial": "https://www.haskell.org/learn.html",
        "year": 1990, "creator": "Simon Peyton Jones et al.", "paradigm": "Functional"
    },
    "Erlang": {
        "extension": ".erl", "color": "#a90533",
        "url": "https://www.programiz.com/erlang/online-compiler/",
        "editor_url": "https://www.programiz.com/erlang/online-compiler/",
        "docs": "https://www.erlang.org/docs",
        "tutorial": "https://www.erlang.org/learn.html",
        "year": 1986, "creator": "Joe Armstrong", "paradigm": "Concurrent"
    },
    "Elixir": {
        "extension": ".ex", "color": "#4b275f",
        "url": "https://www.programiz.com/elixir-online-compiler/",
        "editor_url": "https://www.programiz.com/elixir-online-compiler/",
        "docs": "https://hexdocs.pm/elixir/",
        "tutorial": "https://elixir-lang.org/learning.html",
        "year": 2011, "creator": "José Valim", "paradigm": "Functional"
    },
    "F#": {
        "extension": ".fs", "color": "#b845fc",
        "url": "https://www.programiz.com/fsharp-online-compiler/",
        "editor_url": "https://www.programiz.com/fsharp-online-compiler/",
        "docs": "https://docs.microsoft.com/dotnet/fsharp/",
        "tutorial": "https://fsharp.org/learn/",
        "year": 2005, "creator": "Microsoft Research", "paradigm": "Functional"
    },
    "Objective-C": {
        "extension": ".m", "color": "#438eff",
        "url": "https://www.programiz.com/c-programming/online-compiler/",
        "editor_url": "https://www.programiz.com/c-programming/online-compiler/",
        "docs": "https://developer.apple.com/documentation/objectivec",
        "tutorial": "https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/Introduction/Introduction.html",
        "year": 1984, "creator": "Brad Cox", "paradigm": "Object-oriented"
    },
    "Objective-C++": {
        "extension": ".mm", "color": "#438eff",
        "url": "https://www.programiz.com/cpp-programming/online-compiler/",
        "editor_url": "https://www.programiz.com/cpp-programming/online-compiler/",
        "docs": "https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/Introduction/Introduction.html",
        "tutorial": "https://www.tutorialspoint.com/objective_c/index.htm",
        "year": 1991, "creator": "Brad Cox", "paradigm": "Multi-paradigm"
    },
    "Assembly": {
        "extension": ".asm", "color": "#6d6d6d",
        "url": "https://www.programiz.com/assembly-online-compiler/",
        "editor_url": "https://www.programiz.com/assembly-online-compiler/",
        "docs": "https://www.nasm.us/doc/",
        "tutorial": "https://www.tutorialspoint.com/assembly_programming/",
        "year": 1949, "creator": "Various", "paradigm": "Low-level"
    },
    "Ada": {
        "extension": ".adb", "color": "#02f88c",
        "url": "https://www.programiz.com/ada-online-compiler/",
        "editor_url": "https://www.programiz.com/ada-online-compiler/",
        "docs": "https://www.adaic.org/resources/add_content/standards/2012standard",
        "tutorial": "https://learn.adacore.com/",
        "year": 1980, "creator": "Jean Ichbiah", "paradigm": "Structured"
    },
    "Fortran": {
        "extension": ".f90", "color": "#4d41b1",
        "url": "https://www.programiz.com/fortran-online-compiler/",
        "editor_url": "https://www.programiz.com/fortran-online-compiler/",
        "docs": "https://fortran-lang.org/learn/",
        "tutorial": "https://www.tutorialspoint.com/fortran/",
        "year": 1957, "creator": "John Backus", "paradigm": "Procedural"
    },
    "COBOL": {
        "extension": ".cob", "color": "#f0db4f",
        "url": "https://www.programiz.com/cobol-online-compiler/",
        "editor_url": "https://www.programiz.com/cobol-online-compiler/",
        "docs": "https://www.ibm.com/docs/en/cobol/",
        "tutorial": "https://www.tutorialspoint.com/cobol/",
        "year": 1959, "creator": "CODASYL", "paradigm": "Business"
    },
    "Groovy": {
        "extension": ".groovy", "color": "#4298b8",
        "url": "https://www.programiz.com/groovy-online-compiler/",
        "editor_url": "https://www.programiz.com/groovy-online-compiler/",
        "docs": "https://groovy-lang.org/documentation.html",
        "tutorial": "https://groovy-lang.org/learning.html",
        "year": 2003, "creator": "James Strachan", "paradigm": "Object-oriented"
    },
    "Perl": {
        "extension": ".pl", "color": "#0298c3",
        "url": "https://www.programiz.com/perl-online-compiler/",
        "editor_url": "https://www.programiz.com/perl-online-compiler/",
        "docs": "https://perldoc.perl.org/",
        "tutorial": "https://www.tutorialspoint.com/perl/",
        "year": 1987, "creator": "Larry Wall", "paradigm": "Scripting"
    },
    "Prolog": {
        "extension": ".pl", "color": "#4f5b93",
        "url": "https://www.programiz.com/prolog-online-compiler/",
        "editor_url": "https://www.programiz.com/prolog-online-compiler/",
        "docs": "https://www.swi-prolog.org/pldoc/",
        "tutorial": "https://www.tutorialspoint.com/prolog/",
        "year": 1972, "creator": "Alain Colmerauer", "paradigm": "Logic"
    },
    "Tcl": {
        "extension": ".tcl", "color": "#e4b854",
        "url": "https://www.programiz.com/tcl-online-compiler/",
        "editor_url": "https://www.programiz.com/tcl-online-compiler/",
        "docs": "https://www.tcl-lang.org/man/",
        "tutorial": "https://www.tcl-lang.org/learn/",
        "year": 1988, "creator": "John Ousterhout", "paradigm": "Scripting"
    },
    "Lisp": {
        "extension": ".lisp", "color": "#3d8b37",
        "url": "https://www.programiz.com/lisp-online-compiler/",
        "editor_url": "https://www.programiz.com/lisp-online-compiler/",
        "docs": "https://common-lisp.net/",
        "tutorial": "https://www.tutorialspoint.com/lisp/",
        "year": 1958, "creator": "John McCarthy", "paradigm": "Functional"
    },
    "Scheme": {
        "extension": ".scm", "color": "#1f85de",
        "url": "https://www.programiz.com/scheme-online-compiler/",
        "editor_url": "https://www.programiz.com/scheme-online-compiler/",
        "docs": "https://www.scheme.com/",
        "tutorial": "https://www.schemewiki.org/", 
        "year": 1975, "creator": "Guy L. Steele Jr.", "paradigm": "Functional"
    },
    "Sass": {
        "extension": ".sass", "color": "#cf649a",
        "url": "https://www.programiz.com/sass-online-compiler/",
        "editor_url": "https://www.programiz.com/sass-online-compiler/",
        "docs": "https://sass-lang.com/documentation",
        "tutorial": "https://sass-lang.com/guide",
        "year": 2006, "creator": "Hampton Catlin", "paradigm": "Stylesheet"
    },
    "Less": {
        "extension": ".less", "color": "#1d365d",
        "url": "https://www.programiz.com/less-online-compiler/",
        "editor_url": "https://www.programiz.com/less-online-compiler/",
        "docs": "https://lesscss.org/",
        "tutorial": "https://lesscss.org/learn/",
        "year": 2009, "creator": "Alexis Sellier", "paradigm": "Stylesheet"
    },
    "SCSS": {
        "extension": ".scss", "color": "#c6538c",
        "url": "https://www.programiz.com/scss-online-compiler/",
        "editor_url": "https://www.programiz.com/scss-online-compiler/",
        "docs": "https://sass-lang.com/documentation/syntax",
        "tutorial": "https://sass-lang.com/guide",
        "year": 2010, "creator": "Hampton Catlin", "paradigm": "Stylesheet"
    }
})

# ============================================================
# AI ASSISTANT MODELS
# ============================================================

AI_MODELS = {
    "ChatGPT": {"name": "ChatGPT", "icon": "🤖", "color": "#10a37f", "website": "https://chat.openai.com", "description": "OpenAI's conversational AI"},
    "DeepSeek": {"name": "DeepSeek", "icon": "🔍", "color": "#4d6bfe", "website": "https://chat.deepseek.com", "description": "Advanced reasoning AI"},
    "Grok AI": {"name": "Grok AI", "icon": "🌌", "color": "#8b5cf6", "website": "https://grok.x.ai", "description": "Witty and humorous AI"},
    "Claude AI": {"name": "Claude AI", "icon": "🎯", "color": "#d97706", "website": "https://claude.ai", "description": "Helpful and ethical AI"},
    "Gemini": {"name": "Google Gemini", "icon": "✨", "color": "#4285f4", "website": "https://gemini.google.com", "description": "Google's multimodal AI"},
    "Copilot": {"name": "GitHub Copilot", "icon": "💻", "color": "#000000", "website": "https://github.com/features/copilot", "description": "AI pair programmer"}
}

CURRENT_AI_MODEL = "ChatGPT"
AI_CONVERSATIONS = {}
AI_LOG = ["AI Assistant Ready"]

for model in AI_MODELS:
    AI_CONVERSATIONS[model] = []

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

FILES = ["kernel.sys", "config.cfg", "root.py", "notes.txt", "welcome.txt"]
SOCIAL_POSTS = []
PATIENTS = []
WORD_DOCUMENTS = []
CONTACTS = []
TASKS = []

DEPLOYMENT_LOGS = []
KERNEL_LOGS = ["Kernel boot sequence initialized"]
CYBER_LOG = ["Cyber Security Core Ready"]
NETWORK_LOG = ["Network initialized"]
DETECTED_THREATS = []
NETWORK_DEVICES = []
SECURITY_LOGS = []

RUNNING_PROCESSES = []
INSTALLED_PACKAGES = ["kernel", "calculator", "terminal", "browser", "code_studio", "ai_assistant"]
CURRENT_THEME = "Dark"
PLUGINS = []
BACKUP_DIR = "neilos_backups"
CURRENT_USER = "guest"
AUTO_SAVE_RUNNING = True

# ============================================================
# SCREEN & DRAWERS
# ============================================================

screen = turtle.Screen()
screen.setup(SCREEN_W, SCREEN_H)
screen.title("NeilOS - Ultimate Security Edition")
screen.bgcolor("#0b1020")
screen.tracer(0)

drawer = turtle.Turtle()
drawer.hideturtle()
drawer.speed(0)

textpen = turtle.Turtle()
textpen.hideturtle()
textpen.speed(0)

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

def register_click(name, x, y, w, h, callback):
    CLICKS[name] = {"x1": x, "y1": y, "x2": x + w, "y2": y - h, "cb": callback}

def draw_window(title, color="#00ffee"):
    draw_rect(-600, 350, 1200, 700, "#101826", color)
    draw_rect(-600, 350, 1200, 40, "#0f172a", color)
    draw_text(title, -570, 320, color, 12, "bold")
    draw_rect(550, 350, 40, 30, "#ef4444")
    draw_text("X", 565, 322, "white", 11, "bold")
    register_click("close", 550, 350, 40, 30, desktop_view)

def open_app(appid):
    global CURRENT_APP
    CURRENT_APP = appid
    render()

def desktop_view():
    global CURRENT_APP
    CURRENT_APP = "desktop"
    render()

# ============================================================
# DESKTOP APPS
# ============================================================

class DesktopApp:
    def __init__(self, name, icon, appid, description=""):
        self.name = name
        self.icon = icon
        self.appid = appid
        self.description = description

apps = [
    DesktopApp("Bank", "💰", "bank", "Complete Financial Tools"),
    DesktopApp("Files", "📁", "files", "File manager"),
    DesktopApp("Terminal", "💻", "terminal", "Command line"),
    DesktopApp("Search", "🔍", "search", "Web search"),
    DesktopApp("Cyber", "🛡️", "cyber", "Security tools"),
    DesktopApp("Network", "🌐", "network", "Network utils"),
    DesktopApp("AI", "🤖", "ai", "AI Assistant"),
    DesktopApp("Animation", "🎞️", "animation", "Animation Studio"),
    DesktopApp("Monitor", "📊", "monitor", "System stats"),
    DesktopApp("Calculator", "🧮", "calculator", "Advanced Math"),
    DesktopApp("Clinic", "🏥", "clinic", "Patient mgmt"),
    DesktopApp("SocialNet", "🌍", "social", "Social feed"),
    DesktopApp("Deploy", "🚀", "deploy", "Deployment"),
    DesktopApp("API", "🔌", "api", "API testing"),
    DesktopApp("Games", "🎮", "games", "Mini games"),
    DesktopApp("Kernel", "⚙️", "kernel", "System kernel"),
    DesktopApp("Notes", "📝", "notes", "Note taking"),
    DesktopApp("Code Studio", "💻", "code_studio", "IDE with 20+ languages"),
    DesktopApp("Weather", "🌤️", "weather", "Weather"),
    DesktopApp("Contacts", "📇", "contacts", "Contacts"),
    DesktopApp("Tasks", "✅", "tasks", "Task manager"),
    DesktopApp("Word", "📄", "word", "Document editor")
]

def draw_desktop():
    draw_rect(-700, 425, 1400, 850, "#0b1020")
    draw_text("NeilOS - Ultimate Security Edition", -650, 390, "#00ffee", 12, "bold")
    
    startx = -600
    starty = 280
    width = 180
    height = 60
    
    for i, app in enumerate(apps):
        row = i // 5
        col = i % 5
        x = startx + col * 200
        y = starty - row * 80
        
        draw_rect(x, y, width, height, "#111827", "#00ffee")
        draw_text(f"{app.icon} {app.name}", x + 15, y - 25, "white", 9)
        register_click(app.appid, x, y, width, height, lambda a=app.appid: open_app(a))
    
    draw_rect(-700, -375, 1400, 50, "#111827")
    now = datetime.datetime.now()
    draw_text(f"User: {CURRENT_USER}", -650, -405, "#00ffee", 9)
    draw_text(now.strftime("%Y-%m-%d %H:%M:%S"), 450, -405, "#00ffee", 10)

# ============================================================
# ENHANCED CYBER SECURITY APP WITH ALL REQUESTED FUNCTIONS
# ============================================================




def log_security_event(tool, target, result):
    """Log security events to database"""
    try:
        cur.execute("INSERT INTO security_logs(tool, target, result, date) VALUES(?, ?, ?, ?)", 
                   (tool, target, result, str(datetime.datetime.now())))
        conn.commit()
        SECURITY_LOGS.append(f"[{tool}] {target}: {result}")
    except:
        pass

def nmap_scanner():
    """Nmap style port scanner"""
    target = simpledialog.askstring("Nmap Scanner", "Enter target IP or domain:")
    if not target:
        return
    
    result_window = tk.Toplevel()
    result_window.title("Nmap Scan Results")
    result_window.geometry("600x500")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#0a0a0a", fg="#00ff00", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"🔍 NMAP SCAN REPORT\n")
    text_area.insert(tk.END, f"Target: {target}\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 50 + "\n\n")
    
    common_ports = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
        80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 3306: "MySQL",
        3389: "RDP", 5432: "PostgreSQL", 8080: "HTTP-Alt", 27017: "MongoDB"
    }
    
    text_area.insert(tk.END, "PORT     STATE    SERVICE\n")
    text_area.insert(tk.END, "─────    ─────    ───────\n")
    
    open_ports = []
    for port, service in common_ports.items():
        if random.random() < 0.3:
            status = "open"
            open_ports.append(port)
            color = "#10b981"
        else:
            status = "closed"
            color = "#6b7280"
        
        text_area.insert(tk.END, f"{port:<8} {status:<8} {service}\n")
        result_window.update()
        time.sleep(0.02)
    
    text_area.insert(tk.END, "\n" + "━" * 50 + "\n")
    text_area.insert(tk.END, f"✅ Scan complete. {len(open_ports)} open ports found.\n")
    
    if open_ports:
        text_area.insert(tk.END, f"\n⚠️ Open ports: {', '.join(map(str, open_ports))}\n")
    
    log_security_event("Nmap Scanner", target, f"{len(open_ports)} open ports found")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, bg="#3b82f6", fg="white").pack(pady=5)

def ddos_attack_detector():
    """DDoS Attack Detection Simulator"""
    target = simpledialog.askstring("DDoS Detector", "Enter IP address to check for DDoS activity:")
    if not target:
        return
    
    result_window = tk.Toplevel()
    result_window.title("DDoS Attack Detector")
    result_window.geometry("600x500")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#0a0a0a", fg="#00ff00", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"🛡️ DDoS ATTACK DETECTION REPORT\n")
    text_area.insert(tk.END, f"Target: {target}\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 50 + "\n\n")
    
    # Simulate traffic analysis
    traffic_spike = random.randint(100, 10000)
    baseline = random.randint(50, 500)
    
    text_area.insert(tk.END, f"📊 Traffic Analysis:\n")
    text_area.insert(tk.END, f"   Baseline traffic: {baseline} requests/sec\n")
    text_area.insert(tk.END, f"   Current traffic: {traffic_spike} requests/sec\n\n")
    
    if traffic_spike > baseline * 10:
        risk_level = "🔴 CRITICAL - DDoS ATTACK DETECTED!"
        risk_color = "#ef4444"
        mitigation = "Activating DDoS protection: Traffic filtering, Rate limiting, IP blacklisting"
    elif traffic_spike > baseline * 5:
        risk_level = "🟡 HIGH - Potential DDoS attack"
        risk_color = "#f59e0b"
        mitigation = "Monitoring traffic patterns, Rate limiting enabled"
    elif traffic_spike > baseline * 2:
        risk_level = "🟠 MEDIUM - Unusual traffic spike"
        risk_color = "#f97316"
        mitigation = "Increased monitoring, Ready to activate protection"
    else:
        risk_level = "🟢 LOW - Normal traffic"
        risk_color = "#10b981"
        mitigation = "No action needed"
    
    text_area.insert(tk.END, f"Risk Level: ", "bold")
    text_area.insert(tk.END, f"{risk_level}\n\n", "risk")
    
    text_area.insert(tk.END, f"🛡️ Mitigation Actions:\n")
    text_area.insert(tk.END, f"   {mitigation}\n\n")
    
    # Anomaly detection
    text_area.insert(tk.END, f"🔍 Anomaly Detection:\n")
    anomalies = []
    if random.random() < 0.4:
        anomalies.append("SYN flood patterns detected")
    if random.random() < 0.3:
        anomalies.append("UDP amplification attack pattern")
    if random.random() < 0.2:
        anomalies.append("HTTP request flooding")
    
    if anomalies:
        for a in anomalies:
            text_area.insert(tk.END, f"   ⚠️ {a}\n")
    else:
        text_area.insert(tk.END, "   ✅ No anomalies detected\n")
    
    text_area.tag_config("bold", foreground="white", font=("Consolas", 10, "bold"))
    text_area.tag_config("risk", foreground=risk_color)
    
    log_security_event("DDoS Detector", target, risk_level)
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, bg="#3b82f6", fg="white").pack(pady=5)

def url_scanner():
    """URL Security Scanner for phishing and malicious links"""
    url = simpledialog.askstring("URL Scanner", "Enter URL to scan for security threats:")
    if not url:
        return
    
    result_window = tk.Toplevel()
    result_window.title("URL Security Scanner")
    result_window.geometry("650x550")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#0a0a0a", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"🔗 URL SECURITY SCAN REPORT\n")
    text_area.insert(tk.END, f"URL: {url}\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 60 + "\n\n")
    
    risk_score = 0
    warnings = []
    
    # Check for HTTPS
    if "http" in url.lower() and "https" not in url.lower():
        warnings.append("⚠️ Missing HTTPS encryption - Connection insecure")
        risk_score += 2
    
    # Suspicious keywords
    suspicious_keywords = ["login", "verify", "secure", "account", "update", "confirm", 
                          "bank", "paypal", "amazon", "apple", "microsoft", "google",
                          "signin", "authenticate", "validate", "security"]
    
    for keyword in suspicious_keywords:
        if keyword in url.lower():
            warnings.append(f"⚠️ Contains '{keyword}' - Potential phishing keyword")
            risk_score += 1
    
    # IP address check
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    if re.search(ip_pattern, url):
        warnings.append("⚠️ Uses IP address instead of domain name - Suspicious")
        risk_score += 3
    
    # URL length
    if len(url) > 100:
        warnings.append("⚠️ Unusually long URL - Possible cloaking")
        risk_score += 1
    
    # Special characters
    special_chars = ['@', '-', '_', '?', '=', '&', '%']
    char_count = sum(1 for c in url if c in special_chars)
    if char_count > 5:
        warnings.append(f"⚠️ Multiple special characters ({char_count}) - URL obfuscation possible")
        risk_score += 1
    
    # URL shorteners
    shorteners = ["bit.ly", "tinyurl", "goo.gl", "ow.ly", "is.gd", "buff.ly", "short.link", "tr.im"]
    for shortener in shorteners:
        if shortener in url.lower():
            warnings.append(f"⚠️ Uses URL shortener ({shortener}) - Destination hidden")
            risk_score += 2
    
    # Domain age simulation
    domain_age = random.randint(1, 3650)
    if domain_age < 30:
        warnings.append(f"⚠️ Domain is very new ({domain_age} days old)")
        risk_score += 2
    
    # Determine risk level
    if risk_score >= 5:
        risk_level = "🔴 CRITICAL - Malicious/Phishing URL Detected!"
        risk_color = "#ef4444"
        recommendation = "DO NOT OPEN - Block this URL immediately"
    elif risk_score >= 3:
        risk_level = "🟡 HIGH RISK - Suspicious URL"
        risk_color = "#f59e0b"
        recommendation = "Exercise extreme caution - Verify before opening"
    elif risk_score >= 1:
        risk_level = "🟠 MEDIUM RISK - Potential concerns"
        risk_color = "#f97316"
        recommendation = "Be cautious - Check for legitimate source"
    else:
        risk_level = "🟢 LOW RISK - URL appears safe"
        risk_color = "#10b981"
        recommendation = "URL seems legitimate"
    
    text_area.insert(tk.END, f"Risk Level: ", "bold")
    text_area.insert(tk.END, f"{risk_level}\n\n", "risk")
    text_area.tag_config("bold", foreground="white", font=("Consolas", 10, "bold"))
    text_area.tag_config("risk", foreground=risk_color)
    
    text_area.insert(tk.END, f"Risk Score: {risk_score}/15\n\n")
    
    if warnings:
        text_area.insert(tk.END, "🔍 Findings:\n")
        for warning in warnings:
            text_area.insert(tk.END, f"   {warning}\n")
    else:
        text_area.insert(tk.END, "✅ No obvious security threats detected\n")
    
    text_area.insert(tk.END, f"\n📋 Recommendation: {recommendation}\n")
    
    log_security_event("URL Scanner", url, f"Risk score: {risk_score}/15 - {risk_level}")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, bg="#3b82f6", fg="white").pack(pady=5)

def sql_injector():
    """SQL Injection Vulnerability Scanner"""
    target = simpledialog.askstring("SQL Injector Scanner", "Enter target URL for SQL injection test:")
    if not target:
        return
    
    result_window = tk.Toplevel()
    result_window.title("SQL Injection Scanner")
    result_window.geometry("650x550")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#0a0a0a", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"🗄️ SQL INJECTION VULNERABILITY SCAN\n")
    text_area.insert(tk.END, f"Target: {target}\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 60 + "\n\n")
    
    # SQL injection payloads
    payloads = [
        ("Classic SQL Injection", "' OR '1'='1"),
        ("Union Based", "' UNION SELECT NULL--"),
        ("Error Based", "' AND 1=CONVERT(int, @@version)--"),
        ("Boolean Based", "' AND '1'='1"),
        ("Time Based", "'; WAITFOR DELAY '00:00:05'--"),
        ("Comment Injection", "admin'--"),
        ("Stacked Queries", "'; DROP TABLE users--")
    ]
    
    text_area.insert(tk.END, "🔍 Testing SQL Injection Vectors:\n\n")
    
    vulnerabilities = []
    for i, (name, payload) in enumerate(payloads):
        text_area.insert(tk.END, f"Test {i+1}: {name}\n")
        text_area.insert(tk.END, f"   Payload: {payload}\n")
        
        # Simulate vulnerability detection
        is_vulnerable = random.random() < 0.4
        if is_vulnerable:
            vulnerabilities.append(name)
            text_area.insert(tk.END, f"   Result: ⚠️ POTENTIAL VULNERABILITY DETECTED!\n", "vuln")
        else:
            text_area.insert(tk.END, f"   Result: ✅ No vulnerability detected\n")
        text_area.insert(tk.END, "\n")
        result_window.update()
        time.sleep(0.1)
    
    text_area.tag_config("vuln", foreground="#ef4444")
    
    text_area.insert(tk.END, "━" * 60 + "\n")
    
    if vulnerabilities:
        text_area.insert(tk.END, f"\n🚨 SQL INJECTION VULNERABILITIES FOUND!\n", "critical")
        text_area.insert(tk.END, f"Vulnerable to: {', '.join(vulnerabilities)}\n\n")
        text_area.insert(tk.END, "📋 Recommendations:\n")
        text_area.insert(tk.END, "   1. Use parameterized queries/prepared statements\n")
        text_area.insert(tk.END, "   2. Implement input validation and sanitization\n")
        text_area.insert(tk.END, "   3. Use stored procedures\n")
        text_area.insert(tk.END, "   4. Apply least privilege principle to database accounts\n")
        text_area.insert(tk.END, "   5. Use Web Application Firewall (WAF)\n")
        text_area.tag_config("critical", foreground="#ef4444", font=("Consolas", 11, "bold"))
    else:
        text_area.insert(tk.END, "\n✅ No SQL injection vulnerabilities detected.\n")
    
    text_area.insert(tk.END, "\n⚠️ NOTE: This is a simulated scan. Always test on systems you own or have permission to test!\n")
    
    log_security_event("SQL Injector Scanner", target, f"{len(vulnerabilities)} vulnerabilities found")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, bg="#3b82f6", fg="white").pack(pady=5)

def malware_scanner():
    """Malware Detection Scanner"""
    file_path = filedialog.askopenfilename(title="Select file to scan for malware")
    if not file_path:
        return
    
    result_window = tk.Toplevel()
    result_window.title("Malware Scanner")
    result_window.geometry("650x550")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#0a0a0a", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"🦠 MALWARE SCAN REPORT\n")
    text_area.insert(tk.END, f"File: {os.path.basename(file_path)}\n")
    text_area.insert(tk.END, f"Path: {file_path}\n")
    text_area.insert(tk.END, f"Size: {os.path.getsize(file_path)} bytes\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 60 + "\n\n")
    
    # Malware signatures
    malware_signatures = [
        "virus", "malware", "trojan", "ransomware", "spyware", "worm", "backdoor",
        "exploit", "keylogger", "rootkit", "botnet", "adware", "dialer"
    ]
    
    # Heuristic checks
    text_area.insert(tk.END, "🔍 Signature-Based Scanning:\n\n")
    
    threats = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().lower()
            for sig in malware_signatures:
                if sig in content:
                    threats.append(sig)
                    text_area.insert(tk.END, f"   ⚠️ Found signature: {sig.upper()}\n")
                    result_window.update()
                    time.sleep(0.05)
    except:
        text_area.insert(tk.END, "   🔍 Binary file - performing heuristic analysis...\n\n")
        # Simulate heuristic detection
        for i in range(5):
            if random.random() < 0.2:
                threats.append(f"Heuristic pattern {i+1}")
                text_area.insert(tk.END, f"   ⚠️ Suspicious pattern {i+1} detected\n")
            result_window.update()
            time.sleep(0.1)
    
    text_area.insert(tk.END, "\n" + "━" * 60 + "\n")
    
    if threats:
        text_area.insert(tk.END, f"\n🚨 MALWARE DETECTED!\n", "detected")
        text_area.insert(tk.END, f"Found {len(threats)} threat(s):\n")
        for threat in threats[:10]:
            text_area.insert(tk.END, f"   - {threat}\n")
        text_area.insert(tk.END, "\n📋 Recommendations:\n")
        text_area.insert(tk.END, "   1. Quarantine the file immediately\n")
        text_area.insert(tk.END, "   2. Run full system antivirus scan\n")
        text_area.insert(tk.END, "   3. Delete or disinfect the file\n")
        text_area.insert(tk.END, "   4. Change passwords if keylogger detected\n")
        text_area.tag_config("detected", foreground="#ef4444", font=("Consolas", 11, "bold"))
        DETECTED_THREATS.extend(threats)
    else:
        text_area.insert(tk.END, "\n✅ No malware detected. File appears clean.\n")
    
    log_security_event("Malware Scanner", os.path.basename(file_path), f"{len(threats)} threats found")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, bg="#3b82f6", fg="white").pack(pady=5)

def phishing_attack_detector():
    """Phishing Attack Detection Simulator"""
    email_or_url = simpledialog.askstring("Phishing Detector", "Enter email content or URL to check for phishing:")
    if not email_or_url:
        return
    
    result_window = tk.Toplevel()
    result_window.title("Phishing Attack Detector")
    result_window.geometry("650x550")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#0a0a0a", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"🎣 PHISHING DETECTION REPORT\n")
    text_area.insert(tk.END, f"Analyzed: {email_or_url[:100]}\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 60 + "\n\n")
    
    risk_score = 0
    flags = []
    
    # Check for urgent/emotional language
    urgent_words = ["urgent", "immediate", "action required", "verify now", "account suspended",
                   "click here", "limited time", "verify account", "security alert"]
    
    for word in urgent_words:
        if word in email_or_url.lower():
            flags.append(f"⚠️ Urgent/emotional language: '{word}'")
            risk_score += 1
    
    # Check for spoofed sender indicators
    spoof_indicators = ["support", "security", "alert", "notice", "verify", "update"]
    for indicator in spoof_indicators:
        if indicator in email_or_url.lower():
            flags.append(f"⚠️ Spoofing indicator: '{indicator}'")
            risk_score += 1
    
    # Check for suspicious links
    if "http" in email_or_url.lower():
        link_count = email_or_url.lower().count("http")
        if link_count > 0:
            flags.append(f"⚠️ Contains {link_count} hyperlink(s)")
            risk_score += 1
    
    # Check for attachment warnings
    if any(ext in email_or_url.lower() for ext in [".exe", ".zip", ".scr", ".bat", ".cmd"]):
        flags.append("⚠️ Suspicious file attachment detected")
        risk_score += 2
    
    # Check for grammatical errors (simulated)
    if random.random() < 0.4:
        flags.append("⚠️ Poor grammar/spelling - common in phishing")
        risk_score += 1
    
    # Determine risk level
    if risk_score >= 5:
        risk_level = "🔴 CRITICAL - Phishing Attack Detected!"
        risk_color = "#ef4444"
        action = "DO NOT CLICK ANY LINKS - Report as phishing"
    elif risk_score >= 3:
        risk_level = "🟡 HIGH RISK - Strong phishing indicators"
        risk_color = "#f59e0b"
        action = "Exercise extreme caution - Verify sender through different channel"
    elif risk_score >= 1:
        risk_level = "🟠 MEDIUM RISK - Potential phishing"
        risk_color = "#f97316"
        action = "Be cautious - Check for legitimacy before responding"
    else:
        risk_level = "🟢 LOW RISK - Appears legitimate"
        risk_color = "#10b981"
        action = "Message appears safe, but maintain awareness"
    
    text_area.insert(tk.END, f"Phishing Risk: ", "bold")
    text_area.insert(tk.END, f"{risk_level}\n\n", "risk")
    text_area.tag_config("bold", foreground="white", font=("Consolas", 10, "bold"))
    text_area.tag_config("risk", foreground=risk_color)
    
    text_area.insert(tk.END, f"Risk Score: {risk_score}/10\n\n")
    
    if flags:
        text_area.insert(tk.END, "🔍 Detection Flags:\n")
        for flag in flags[:8]:
            text_area.insert(tk.END, f"   {flag}\n")
    else:
        text_area.insert(tk.END, "✅ No obvious phishing indicators\n")
    
    text_area.insert(tk.END, f"\n📋 Recommended Action: {action}\n")
    
    log_security_event("Phishing Detector", email_or_url[:50], f"Risk score: {risk_score} - {risk_level}")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, bg="#3b82f6", fg="white").pack(pady=5)

def mitm_detector():
    """Man-in-the-Middle Attack Detector"""
    target = simpledialog.askstring("MITM Detector", "Enter target IP or domain to check for MITM attacks:")
    if not target:
        target = socket.gethostname()
    
    result_window = tk.Toplevel()
    result_window.title("MITM Attack Detector")
    result_window.geometry("650x550")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#0a0a0a", fg="#00ff00", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"🔒 MAN-IN-THE-MIDDLE ATTACK DETECTOR\n")
    text_area.insert(tk.END, f"Target: {target}\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 60 + "\n\n")
    
    # MITM detection checks
    checks = [
        "Checking SSL/TLS certificates...",
        "Verifying certificate chain of trust...",
        "Checking for certificate pinning...",
        "Analyzing network routes for anomalies...",
        "Checking ARP table for spoofing...",
        "Verifying DNS responses consistency...",
        "Checking for unexpected redirects...",
        "Analyzing packet timing anomalies...",
        "Checking for duplicate ACK packets...",
        "Verifying TCP sequence numbers..."
    ]
    
    detections = []
    text_area.insert(tk.END, "🔍 Running MITM Detection Tests:\n\n")
    
    for check in checks:
        text_area.insert(tk.END, f"• {check} ")
        result_window.update()
        time.sleep(0.1)
        
        # Simulate detection
        if random.random() < 0.12:
            detection_type = random.choice([
                "Certificate mismatch detected",
                "ARP spoofing detected",
                "DNS response inconsistency",
                "SSL certificate not trusted",
                "Suspicious route change",
                "Duplicate packet pattern detected"
            ])
            detections.append(detection_type)
            text_area.insert(tk.END, f"⚠️ {detection_type}\n", "detect")
        else:
            text_area.insert(tk.END, "✓ OK\n")
        result_window.update()
    
    text_area.tag_config("detect", foreground="#ef4444")
    
    text_area.insert(tk.END, "\n" + "━" * 60 + "\n")
    
    if detections:
        text_area.insert(tk.END, f"\n🚨 MITM ATTACK DETECTED!\n", "critical")
        text_area.insert(tk.END, f"Found {len(detections)} indicator(s):\n")
        for det in detections:
            text_area.insert(tk.END, f"   - {det}\n")
        text_area.insert(tk.END, "\n📋 Immediate Actions Required:\n")
        text_area.insert(tk.END, "   1. Disconnect from current network immediately\n")
        text_area.insert(tk.END, "   2. Use VPN for encrypted connections\n")
        text_area.insert(tk.END, "   3. Verify SSL certificates manually\n")
        text_area.insert(tk.END, "   4. Change all passwords\n")
        text_area.insert(tk.END, "   5. Clear DNS cache and browser data\n")
        text_area.tag_config("critical", foreground="#ef4444", font=("Consolas", 11, "bold"))
        log_security_event("MITM Detector", target, "MITM attack detected")
    else:
        text_area.insert(tk.END, "\n✅ No MITM attack detected. Connection appears secure.\n")
        log_security_event("MITM Detector", target, "No threats found")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, bg="#3b82f6", fg="white").pack(pady=5)

def smishing_detector():
    """Smishing (SMS Phishing) Detector"""
    message = simpledialog.askstring("Smishing Detector", "Enter SMS message text to check for smishing:")
    if not message:
        return
    
    result_window = tk.Toplevel()
    result_window.title("Smishing Detector - SMS Phishing Scanner")
    result_window.geometry("650x550")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#0a0a0a", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"📱 SMISHING DETECTOR - SMS Phishing Scanner\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 60 + "\n\n")
    
    text_area.insert(tk.END, f"📨 Message Content:\n")
    text_area.insert(tk.END, f"\"{message[:200]}...\"\n\n")
    
    # Smishing indicators
    risk_score = 0
    alerts = []
    
    # Urgent action required
    urgency_phrases = ["urgent", "immediate", "action required", "respond now", "limited time",
                       "account suspended", "verify now", "security alert", "unauthorized access"]
    for phrase in urgency_phrases:
        if phrase in message.lower():
            alerts.append(f"Urgency tactic: '{phrase}'")
            risk_score += 1
    
    # Request for personal information
    info_requests = ["verify account", "confirm identity", "update information", "personal details",
                     "bank account", "credit card", "social security", "password", "pin code"]
    for request in info_requests:
        if request in message.lower():
            alerts.append(f"Personal info request: '{request}'")
            risk_score += 2
    
    # Suspicious links
    if "http" in message.lower() or "bit.ly" in message.lower() or "tinyurl" in message.lower():
        alerts.append("Contains suspicious URL link")
        risk_score += 2
    
    # Fake prize/offer
    prize_phrases = ["won", "prize", "winner", "congratulations", "free", "discount", "reward", "gift"]
    for phrase in prize_phrases:
        if phrase in message.lower():
            alerts.append(f"Prize/offer lure: '{phrase}'")
            risk_score += 1
    
    # Sender spoofing indicators
    spoof_indicators = ["bank", "paypal", "amazon", "apple", "microsoft", "fedex", "usps", "dhl"]
    for indicator in spoof_indicators:
        if indicator in message.lower():
            alerts.append(f"Potential sender spoofing: '{indicator}'")
            risk_score += 1
    
    # Grammar/spelling issues (simulated)
    if random.random() < 0.5:
        alerts.append("Poor grammar/spelling detected")
        risk_score += 1
    
    # Determine risk level
    if risk_score >= 6:
        risk_level = "🔴 CRITICAL - Confirmed Smishing Attack!"
        risk_color = "#ef4444"
        action = "DO NOT REPLY - Block sender, delete message, report to carrier"
    elif risk_score >= 4:
        risk_level = "🟡 HIGH RISK - Likely Smishing Attempt"
        risk_color = "#f59e0b"
        action = "Do not click links - Verify through official channels"
    elif risk_score >= 2:
        risk_level = "🟠 MEDIUM RISK - Suspicious Message"
        risk_color = "#f97316"
        action = "Be cautious - Avoid responding or clicking links"
    else:
        risk_level = "🟢 LOW RISK - Message appears legitimate"
        risk_color = "#10b981"
        action = "Message appears safe, but maintain awareness"
    
    text_area.insert(tk.END, f"Smishing Risk: ", "bold")
    text_area.insert(tk.END, f"{risk_level}\n\n", "risk")
    text_area.tag_config("bold", foreground="white", font=("Consolas", 10, "bold"))
    text_area.tag_config("risk", foreground=risk_color)
    
    text_area.insert(tk.END, f"Risk Score: {risk_score}/12\n\n")
    
    if alerts:
        text_area.insert(tk.END, "🔍 Detection Alerts:\n")
        for alert in alerts[:8]:
            text_area.insert(tk.END, f"   {alert}\n")
    
    text_area.insert(tk.END, f"\n📋 Recommended Action: {action}\n")
    text_area.insert(tk.END, "\n💡 Tips to Avoid Smishing:\n")
    text_area.insert(tk.END, "   • Never click links in unsolicited SMS\n")
    text_area.insert(tk.END, "   • Don't reply to suspicious messages\n")
    text_area.insert(tk.END, "   • Verify sender through official contact\n")
    text_area.insert(tk.END, "   • Report smishing to your carrier\n")
    
    log_security_event("Smishing Detector", "SMS Message", f"Risk score: {risk_score}")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, bg="#3b82f6", fg="white").pack(pady=5)

def vishing_scanner():
    """Vishing (Voice Phishing) Scanner - Educational"""
    call_info = simpledialog.askstring("Vishing Scanner", "Enter caller number or call description:")
    if not call_info:
        return
    
    result_window = tk.Toplevel()
    result_window.title("Vishing Scanner - Voice Phishing Detector")
    result_window.geometry("650x550")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#0a0a0a", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"📞 VISHING SCANNER - Voice Phishing Detector\n")
    text_area.insert(tk.END, f"Caller Info: {call_info}\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 60 + "\n\n")
    
    # Vishing detection checks
    risk_score = 0
    indicators = []
    
    # Spoofed number indicators
    if re.match(r'\d{10}', call_info):
        indicators.append("Spoofable phone number detected")
        risk_score += 1
    
    # Common vishing scenarios
    scenarios = [
        "Fake bank/financial institution",
        "Fake tech support/customer service",
        "Fake government agency",
        "Lottery/prize scam",
        "Debt collection scam",
        "Charity donation scam"
    ]
    
    selected_scenario = random.choice(scenarios)
    indicators.append(f"Common vishing pattern: {selected_scenario}")
    risk_score += 2
    
    # Pressure tactics
    pressure_tactics = ["urgent payment", "immediate action", "legal threat", "account closure", "arrest warrant"]
    for tactic in pressure_tactics:
        if random.random() < 0.3:
            indicators.append(f"Pressure tactic: {tactic}")
            risk_score += 1
    
    # Information requested
    info_types = ["Social Security Number", "Bank Account", "Credit Card", "Password", "PIN", "OTP"]
    for info in info_types:
        if random.random() < 0.25:
            indicators.append(f"Sensitive info requested: {info}")
            risk_score += 2
    
    # Determine risk level
    if risk_score >= 6:
        risk_level = "🔴 CRITICAL - Confirmed Vishing Attempt!"
        risk_color = "#ef4444"
        action = "HANG UP - Do not provide any information, report to authorities"
    elif risk_score >= 4:
        risk_level = "🟡 HIGH RISK - Likely Vishing Scam"
        risk_color = "#f59e0b"
        action = "Do not share information - Verify caller identity independently"
    elif risk_score >= 2:
        risk_level = "🟠 MEDIUM RISK - Suspicious Call"
        risk_color = "#f97316"
        action = "Be cautious - Request official callback number"
    else:
        risk_level = "🟢 LOW RISK - Call appears legitimate"
        risk_color = "#10b981"
        action = "Normal precautions recommended"
    
    text_area.insert(tk.END, f"Vishing Risk: ", "bold")
    text_area.insert(tk.END, f"{risk_level}\n\n", "risk")
    text_area.tag_config("bold", foreground="white", font=("Consolas", 10, "bold"))
    text_area.tag_config("risk", foreground=risk_color)
    
    text_area.insert(tk.END, f"Risk Score: {risk_score}/12\n\n")
    
    if indicators:
        text_area.insert(tk.END, "🔍 Detection Indicators:\n")
        for ind in indicators[:8]:
            text_area.insert(tk.END, f"   {ind}\n")
    
    text_area.insert(tk.END, f"\n📋 Recommended Action: {action}\n")
    text_area.insert(tk.END, "\n💡 Vishing Prevention Tips:\n")
    text_area.insert(tk.END, "   • Never share personal info over phone\n")
    text_area.insert(tk.END, "   • Hang up and call back official number\n")
    text_area.insert(tk.END, "   • Be wary of caller ID spoofing\n")
    text_area.insert(tk.END, "   • Register on Do Not Call lists\n")
    text_area.insert(tk.END, "   • Report vishing to FTC\n")
    
    log_security_event("Vishing Scanner", call_info, f"Risk score: {risk_score}")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, bg="#3b82f6", fg="white").pack(pady=5)

def virus_total_simulator():
    """VirusTotal API Simulator - Multi-engine antivirus scan"""
    file_path = filedialog.askopenfilename(title="Select file for VirusTotal simulation")
    if not file_path:
        return
    
    result_window = tk.Toplevel()
    result_window.title("VirusTotal Scanner Simulation")
    result_window.geometry("700x600")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#0a0a0a", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"🦠 VIRUSTOTAL MULTI-ENGINE SCAN SIMULATION\n")
    text_area.insert(tk.END, f"File: {os.path.basename(file_path)}\n")
    text_area.insert(tk.END, f"Size: {os.path.getsize(file_path)} bytes\n")
    text_area.insert(tk.END, f"MD5: {hashlib.md5(open(file_path, 'rb').read()).hexdigest()}\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 70 + "\n\n")
    
    # Antivirus engines
    av_engines = [
        "BitDefender", "Kaspersky", "Norton", "McAfee", "Avast", "AVG", "ESET",
        "Symantec", "TrendMicro", "Sophos", "Panda", "F-Secure", "Malwarebytes",
        "Windows Defender", "K7", "TotalDefense", "Fortinet", "Comodo", "ClamAV"
    ]
    
    text_area.insert(tk.END, "📊 SCAN RESULTS (Multiple Engines)\n\n")
    
    positives = 0
    engine_results = []
    
    for av in av_engines:
        if random.random() < 0.15:
            detection = random.choice([
                "Trojan.Generic", "Malware.Win32", "Virus.Worm", "Ransomware.Filecoder",
                "Exploit.CVE", "Backdoor.Agent", "Spyware.Keylogger", "Adware.Elex"
            ])
            engine_results.append(f"⚠️ {av}: {detection}")
            positives += 1
        else:
            engine_results.append(f"✅ {av}: Clean")
        
        result_window.update()
        time.sleep(0.03)
    
    # Display results in columns
    for i in range(0, len(engine_results), 2):
        if i+1 < len(engine_results):
            text_area.insert(tk.END, f"{engine_results[i]:<40} {engine_results[i+1]}\n")
        else:
            text_area.insert(tk.END, f"{engine_results[i]}\n")
        result_window.update()
    
    text_area.insert(tk.END, "\n" + "━" * 70 + "\n")
    text_area.insert(tk.END, f"\n📈 Scan Summary:\n")
    text_area.insert(tk.END, f"   Total Engines: {len(av_engines)}\n")
    text_area.insert(tk.END, f"   Detections: {positives}\n")
    text_area.insert(tk.END, f"   Detection Rate: {(positives/len(av_engines))*100:.1f}%\n\n")
    
    if positives > 0:
        if positives > len(av_engines)/2:
            threat_level = "🔴 CRITICAL - High detection rate!"
            color = "#ef4444"
        elif positives > 5:
            threat_level = "🟡 HIGH - Multiple detections"
            color = "#f59e0b"
        else:
            threat_level = "🟠 MEDIUM - Some detections"
            color = "#f97316"
        text_area.insert(tk.END, f"Threat Level: ", "bold")
        text_area.insert(tk.END, f"{threat_level}\n", "threat")
        text_area.tag_config("threat", foreground=color)
    else:
        text_area.insert(tk.END, "✅ File appears clean across all engines\n")
    
    text_area.insert(tk.END, f"\n💡 Note: This is a simulation. For real scanning, use VirusTotal website.\n")
    text_area.insert(tk.END, f"🔗 Official VirusTotal URL: https://www.virustotal.com\n")
    
    log_security_event("VirusTotal Simulator", os.path.basename(file_path), f"{positives} detections")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, bg="#3b82f6", fg="white").pack(pady=5)

def vpn_encrypter():
    """VPN Encrypter - Educational VPN setup information"""
    result_window = tk.Toplevel()
    result_window.title("VPN Encrypter - VPN Setup Guide")
    result_window.geometry("650x550")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#0a0a0a", fg="#00ff00", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"🔐 VPN ENCRYPTER - VPN Setup & Encryption Guide\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 60 + "\n\n")
    
    vpn_protocols = {
        "OpenVPN": "Open-source protocol using SSL/TLS encryption (Port 1194 UDP/443 TCP)",
        "WireGuard": "Modern protocol with ChaCha20 encryption, faster performance",
        "IKEv2/IPsec": "Microsoft protocol, great for mobile devices",
        "L2TP/IPsec": "Legacy protocol, less secure than modern options",
        "PPTP": "Obsolete - NOT RECOMMENDED, security vulnerabilities"
    }
    
    text_area.insert(tk.END, "📋 VPN Protocols Available:\n\n")
    for proto, desc in vpn_protocols.items():
        text_area.insert(tk.END, f"   • {proto}: {desc}\n")
    
    text_area.insert(tk.END, "\n" + "━" * 60 + "\n")
    text_area.insert(tk.END, "🔧 VPN Setup Instructions:\n\n")
    text_area.insert(tk.END, "1. Choose a VPN provider (NordVPN, ExpressVPN, ProtonVPN, etc.)\n")
    text_area.insert(tk.END, "2. Download and install the VPN client\n")
    text_area.insert(tk.END, "3. Select encryption protocol (OpenVPN or WireGuard recommended)\n")
    text_area.insert(tk.END, "4. Choose server location\n")
    text_area.insert(tk.END, "5. Connect and verify IP change\n\n")
    
    text_area.insert(tk.END, "🔒 Encryption Standards:\n")
    text_area.insert(tk.END, "   • AES-256-GCM: Military-grade encryption\n")
    text_area.insert(tk.END, "   • ChaCha20-Poly1305: Modern, mobile-optimized\n")
    text_area.insert(tk.END, "   • Perfect Forward Secrecy (PFS)\n")
    text_area.insert(tk.END, "   • 4096-bit RSA keys\n\n")
    
    text_area.insert(tk.END, "✅ VPN Benefits:\n")
    text_area.insert(tk.END, "   • Encrypts internet traffic\n")
    text_area.insert(tk.END, "   • Hides IP address\n")
    text_area.insert(tk.END, "   • Bypasses geographic restrictions\n")
    text_area.insert(tk.END, "   • Protects on public Wi-Fi\n")
    text_area.insert(tk.END, "   • Prevents ISP tracking\n\n")
    
    text_area.insert(tk.END, "💡 Free VPN Options:\n")
    text_area.insert(tk.END, "   • ProtonVPN (no data limit)\n")
    text_area.insert(tk.END, "   • Windscribe (10GB/month)\n")
    text_area.insert(tk.END, "   • TunnelBear (500MB/month)\n")
    
    log_security_event("VPN Encrypter", "VPN Guide", "Information provided")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, bg="#3b82f6", fg="white").pack(pady=5)

def ad_blocker():
    """Ad Blocker - Educational ad blocking information and DNS-based blocking"""
    result_window = tk.Toplevel()
    result_window.title("Ad Blocker - Privacy Protection Guide")
    result_window.geometry("650x550")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#0a0a0a", fg="#00ff00", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"🛡️ AD BLOCKER - Privacy & Ad Protection Guide\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 60 + "\n\n")
    
    text_area.insert(tk.END, "📋 Ad Blocking Methods:\n\n")
    text_area.insert(tk.END, "1. Browser Extensions:\n")
    text_area.insert(tk.END, "   • uBlock Origin (Best performance, open-source)\n")
    text_area.insert(tk.END, "   • AdBlock Plus (Popular, allow acceptable ads)\n")
    text_area.insert(tk.END, "   • Ghostery (Focus on privacy)\n")
    text_area.insert(tk.END, "   • Privacy Badger (EFF, learns as you browse)\n\n")
    
    text_area.insert(tk.END, "2. DNS-Based Blocking:\n")
    text_area.insert(tk.END, "   • Pi-hole (Network-wide blocking)\n")
    text_area.insert(tk.END, "   • AdGuard DNS (94.140.14.14 / 94.140.15.15)\n")
    text_area.insert(tk.END, "   • NextDNS (Customizable filtering)\n\n")
    
    text_area.insert(tk.END, "3. System-Level:\n")
    text_area.insert(tk.END, "   • Hosts file editing\n")
    text_area.insert(tk.END, "   • Firewall rules\n\n")
    
    text_area.insert(tk.END, "━" * 60 + "\n")
    text_area.insert(tk.END, "🔧 Recommended Block Lists:\n\n")
    text_area.insert(tk.END, "   • EasyList (General ads)\n")
    text_area.insert(tk.END, "   • EasyPrivacy (Tracking)\n")
    text_area.insert(tk.END, "   • Peter Lowe's List (Ad/tracking servers)\n")
    text_area.insert(tk.END, "   • MalwareDomains (Malware blocking)\n\n")
    
    text_area.insert(tk.END, "✅ Benefits of Ad Blocking:\n")
    text_area.insert(tk.END, "   • Faster page loading\n")
    text_area.insert(tk.END, "   • Reduced data usage\n")
    text_area.insert(tk.END, "   • Protection from malvertising\n")
    text_area.insert(tk.END, "   • Privacy enhancement\n")
    text_area.insert(tk.END, "   • Less distraction\n\n")
    
    text_area.insert(tk.END, "⚠️ Important Notes:\n")
    text_area.insert(tk.END, "   • Some sites may request whitelisting\n")
    text_area.insert(tk.END, "   • Consider supporting non-intrusive ads\n")
    text_area.insert(tk.END, "   • Never disable protection for suspicious sites\n")
    
    log_security_event("Ad Blocker", "Guide", "Information provided")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, bg="#3b82f6", fg="white").pack(pady=5)

def spam_detector():
    """Spam Email/Message Detector"""
    message = simpledialog.askstring("Spam Detector", "Enter message content to check for spam:")
    if not message:
        return
    
    result_window = tk.Toplevel()
    result_window.title("Spam Detector")
    result_window.geometry("650x550")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#0a0a0a", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"📧 SPAM DETECTOR\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 60 + "\n\n")
    
    text_area.insert(tk.END, f"Message: \"{message[:200]}...\"\n\n")
    
    # Spam keywords
    spam_keywords = {
        "Financial": ["free", "money", "cash", "million", "dollar", "rich", "income", "investment"],
        "Lottery": ["winner", "won", "prize", "lottery", "jackpot", "winning", "congratulations"],
        "Pharmacy": ["viagra", "cialis", "medication", "prescription", "pharmacy", "drugs"],
        "Urgent": ["urgent", "immediate", "limited time", "act now", "expires today"],
        "Scam": ["nigerian", "inheritance", "refund", "compensation", "settlement"],
        "Work": ["work from home", "make money", "earn", "passive income", "bitcoin"]
    }
    
    score = 0
    detected_categories = []
    
    for category, keywords in spam_keywords.items():
        category_score = 0
        for keyword in keywords:
            if keyword in message.lower():
                category_score += 1
        if category_score > 0:
            detected_categories.append(f"{category} ({category_score})")
            score += category_score
    
    text_area.insert(tk.END, "🔍 Spam Indicators Detected:\n\n")
    
    if detected_categories:
        for cat in detected_categories[:8]:
            text_area.insert(tk.END, f"   ⚠️ {cat}\n")
    else:
        text_area.insert(tk.END, "   ✅ No spam indicators found\n")
    
    text_area.insert(tk.END, "\n" + "━" * 60 + "\n")
    
    # Spam score
    if score >= 10:
        spam_probability = "🔴 VERY HIGH - Definitely Spam"
        spam_color = "#ef4444"
    elif score >= 6:
        spam_probability = "🟡 HIGH - Likely Spam"
        spam_color = "#f59e0b"
    elif score >= 3:
        spam_probability = "🟠 MEDIUM - Possibly Spam"
        spam_color = "#f97316"
    elif score >= 1:
        spam_probability = "🟡 LOW - Minor spam indicators"
        spam_color = "#eab308"
    else:
        spam_probability = "🟢 VERY LOW - Likely legitimate"
        spam_color = "#10b981"
    
    text_area.insert(tk.END, f"\nSpam Score: {score}/20\n")
    text_area.insert(tk.END, f"Spam Probability: ", "bold")
    text_area.insert(tk.END, f"{spam_probability}\n", "spam")
    text_area.tag_config("spam", foreground=spam_color)
    
    log_security_event("Spam Detector", "Message", f"Spam score: {score}")
    
    def close_window():
        result_window.destroy()
    
    tk.Button(result_window, text="Close", command=close_window, bg="#3b82f6", fg="white").pack(pady=5)

def have_i_been_pwned():
    """Have I Been Pwned URL - Check if email/account has been compromised"""
    email = simpledialog.askstring("Have I Been Pwned", "Enter email address to check for data breaches:")
    if not email:
        return
    
    result_window = tk.Toplevel()
    result_window.title("Have I Been Pwned - Breach Checker")
    result_window.geometry("650x550")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#0a0a0a", fg="#00ff00", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"🔍 HAVE I BEEN PWNED - Data Breach Checker\n")
    text_area.insert(tk.END, f"Email: {email}\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 60 + "\n\n")
    
    text_area.insert(tk.END, "🔗 Official Website: https://haveibeenpwned.com\n\n")
    
    # Simulate breach check
    text_area.insert(tk.END, "Checking known data breaches...\n\n")
    
    breaches = [
        "Adobe (2013) - 153 million accounts", "LinkedIn (2012) - 117 million accounts",
        "Yahoo (2013) - 3 billion accounts", "Dropbox (2012) - 68 million accounts",
        "MySpace (2013) - 360 million accounts", "Canva (2019) - 137 million accounts",
        "Facebook (2019) - 540 million accounts", "Marriott (2018) - 500 million accounts",
        "Equifax (2017) - 147 million accounts", "Home Depot (2014) - 56 million cards"
    ]
    
    # Simulate detection
    breaches_found = []
    for breach in breaches:
        if random.random() < 0.15:
            breaches_found.append(breach)
            text_area.insert(tk.END, f"   ⚠️ Found in: {breach}\n")
        result_window.update()
        time.sleep(0.05)
    
    text_area.insert(tk.END, "\n" + "━" * 60 + "\n")
    
    if breaches_found:
        text_area.insert(tk.END, f"\n🚨 ALERT: Email found in {len(breaches_found)} data breach(es)!\n", "alert")
        text_area.insert(tk.END, "\n📋 Recommended Actions:\n")
        text_area.insert(tk.END, "   1. Change password immediately\n")
        text_area.insert(tk.END, "   2. Use unique password for each site\n")
        text_area.insert(tk.END, "   3. Enable Two-Factor Authentication (2FA)\n")
        text_area.insert(tk.END, "   4. Check for unauthorized activity\n")
        text_area.insert(tk.END, "   5. Use a password manager\n")
        text_area.tag_config("alert", foreground="#ef4444", font=("Consolas", 11, "bold"))
    else:
        text_area.insert(tk.END, "\n✅ Good news! Email not found in known data breaches.\n")
        text_area.insert(tk.END, "\n💡 Security Tips:\n")
        text_area.insert(tk.END, "   • Continue using strong passwords\n")
        text_area.insert(tk.END, "   • Enable 2FA wherever possible\n")
        text_area.insert(tk.END, "   • Monitor your accounts regularly\n")
    
    text_area.insert(tk.END, f"\n🔍 You can check more details at:\n")
    text_area.insert(tk.END, f"   https://haveibeenpwned.com/account/{urllib.parse.quote(email)}\n")
    
    log_security_event("Have I Been Pwned", email, f"{len(breaches_found)} breaches found")
    
    def open_hibp():
        webbrowser.open(f"https://haveibeenpwned.com/account/{urllib.parse.quote(email)}")
    
    def close_window():
        result_window.destroy()
    
    button_frame = tk.Frame(result_window, bg="#1e1e1e")
    button_frame.pack(pady=5)
    tk.Button(button_frame, text="Open HIBP Website", command=open_hibp, bg="#4CAF50", fg="white").pack(side="left", padx=5)
    tk.Button(button_frame, text="Close", command=close_window, bg="#3b82f6", fg="white").pack(side="left", padx=5)

def wireshark_url():
    """Wireshark URL - Open Wireshark download/learning page"""
    result_window = tk.Toplevel()
    result_window.title("Wireshark - Network Protocol Analyzer")
    result_window.geometry("650x550")
    result_window.configure(bg="#1e1e1e")
    
    text_area = tk.Text(result_window, bg="#0a0a0a", fg="#00ff00", font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    text_area.insert(tk.END, f"🔍 WIRESHARK - Network Protocol Analyzer\n")
    text_area.insert(tk.END, f"Time: {datetime.datetime.now()}\n")
    text_area.insert(tk.END, "━" * 60 + "\n\n")
    
    text_area.insert(tk.END, "📋 About Wireshark:\n")
    text_area.insert(tk.END, "   Wireshark is the world's most popular network protocol analyzer\n")
    text_area.insert(tk.END, "   Used for network troubleshooting, analysis, and security\n\n")
    
    text_area.insert(tk.END, "🔗 Official URLs:\n")
    text_area.insert(tk.END, "   • Download: https://www.wireshark.org/download.html\n")
    text_area.insert(tk.END, "   • Documentation: https://www.wireshark.org/docs/\n")
    text_area.insert(tk.END, "   • Wiki: https://wiki.wireshark.org/\n\n")
    
    text_area.insert(tk.END, "📚 Key Features:\n")
    text_area.insert(tk.END, "   • Live packet capture\n")
    text_area.insert(tk.END, "   • Deep inspection of hundreds of protocols\n")
    text_area.insert(tk.END, "   • Cross-platform support\n")
    text_area.insert(tk.END, "   • Live capture and offline analysis\n")
    text_area.insert(tk.END, "   • VoIP analysis\n")
    text_area.insert(tk.END, "   • Export to XML, CSV, JSON\n\n")
    
    text_area.insert(tk.END, "💡 Common Uses:\n")
    text_area.insert(tk.END, "   • Network troubleshooting\n")
    text_area.insert(tk.END, "   • Security analysis\n")
    text_area.insert(tk.END, "   • Protocol development\n")
    text_area.insert(tk.END, "   • Education and learning\n\n")
    
    text_area.insert(tk.END, "📖 Learning Resources:\n")
    text_area.insert(tk.END, "   • Wireshark University: https://www.wireshark.org/training/\n")
    text_area.insert(tk.END, "   • YouTube Tutorials: https://www.youtube.com/results?search_query=wireshark+tutorial\n")
    
    log_security_event("Wireshark URL", "Resource accessed", "Information provided")
    
    def open_wireshark():
        webbrowser.open("https://www.wireshark.org/download.html")
    
    def close_window():
        result_window.destroy()
    
    button_frame = tk.Frame(result_window, bg="#1e1e1e")
    button_frame.pack(pady=5)
    tk.Button(button_frame, text="Open Wireshark Download", command=open_wireshark, bg="#4CAF50", fg="white").pack(side="left", padx=5)
    tk.Button(button_frame, text="Close", command=close_window, bg="#3b82f6", fg="white").pack(side="left", padx=5)

def generate_password():
    """Generate strong random password"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(chars) for _ in range(16))
    messagebox.showinfo("Generated Password", f"🔑 Strong Password:\n\n{password}\n\n(Store safely!)")

def check_password_strength():
    """Check password strength"""
    pwd = simpledialog.askstring("Check Strength", "Enter password to check:")
    if pwd:
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
        log_security_event("Password Check", "Password", f"Strength: {strength}")

def view_security_logs():
    """View all security scan logs"""
    cur.execute("SELECT tool, target, result, date FROM security_logs ORDER BY date DESC LIMIT 30")
    logs = cur.fetchall()
    
    if not logs:
        messagebox.showinfo("Security Logs", "No security logs found.")
        return
    
    result = "🛡️ SECURITY SCAN LOGS\n"
    result += "═" * 60 + "\n\n"
    for log in logs:
        result += f"🔧 Tool: {log[0]}\n"
        result += f"🎯 Target: {log[1]}\n"
        result += f"📊 Result: {log[2]}\n"
        result += f"📅 Time: {log[3][:19]}\n"
        result += "─" * 40 + "\n\n"
    
    messagebox.showinfo("Security Logs", result[:4000])

def draw_cyber():
    """Draw Cyber Security App Interface"""
    draw_window("Cyber Security Center - Complete Suite", "#ef4444")
    
    # Row 1: Network Security
    register_click("nmap", -550, 280, 130, 35, nmap_scanner)
    draw_rect(-550, 280, 130, 35, "#111827", "#10b981")
    draw_text("🔍 Nmap", -540, 255, "white", 8)
    
    register_click("ddos", -410, 280, 130, 35, ddos_attack_detector)
    draw_rect(-410, 280, 130, 35, "#111827", "#ef4444")
    draw_text("🛡️ DDoS", -400, 255, "white", 8)
    
    register_click("url_scan", -270, 280, 130, 35, url_scanner)
    draw_rect(-270, 280, 130, 35, "#111827", "#f59e0b")
    draw_text("🌐 URL Scan", -260, 255, "white", 8)
    
    register_click("sql_inject", -130, 280, 130, 35, sql_injector)
    draw_rect(-130, 280, 130, 35, "#111827", "#8b5cf6")
    draw_text("🗄️ SQL Inject", -120, 255, "white", 8)
    
    # Row 2: Malware & Phishing
    register_click("malware", -550, 225, 130, 35, malware_scanner)
    draw_rect(-550, 225, 130, 35, "#111827", "#ec4899")
    draw_text("🦠 Malware", -540, 200, "white", 8)
    
    register_click("phishing", -410, 225, 130, 35, phishing_attack_detector)
    draw_rect(-410, 225, 130, 35, "#111827", "#06b6d4")
    draw_text("🎣 Phishing", -400, 200, "white", 8)
    
    register_click("mitm", -270, 225, 130, 35, mitm_detector)
    draw_rect(-270, 225, 130, 35, "#111827", "#f97316")
    draw_text("🔒 MITM", -260, 200, "white", 8)
    
    register_click("smishing", -130, 225, 130, 35, smishing_detector)
    draw_rect(-130, 225, 130, 35, "#111827", "#d946ef")
    draw_text("📱 Smishing", -120, 200, "white", 8)
    
    # Row 3: Advanced Security
    register_click("vishing", -550, 170, 130, 35, vishing_scanner)
    draw_rect(-550, 170, 130, 35, "#111827", "#0284c7")
    draw_text("📞 Vishing", -540, 145, "white", 8)
    
    register_click("virustotal", -410, 170, 130, 35, virus_total_simulator)
    draw_rect(-410, 170, 130, 35, "#111827", "#7c3aed")
    draw_text("🦠 VirusTotal", -400, 145, "white", 7)
    
    register_click("vpn", -270, 170, 130, 35, vpn_encrypter)
    draw_rect(-270, 170, 130, 35, "#111827", "#0891b2")
    draw_text("🔐 VPN", -260, 145, "white", 8)
    
    register_click("adblock", -130, 170, 130, 35, ad_blocker)
    draw_rect(-130, 170, 130, 35, "#111827", "#16a34a")
    draw_text("🛡️ AdBlock", -120, 145, "white", 8)
    
    # Row 4: Detection & Monitoring
    register_click("spam", -550, 115, 130, 35, spam_detector)
    draw_rect(-550, 115, 130, 35, "#111827", "#eab308")
    draw_text("📧 Spam", -540, 90, "white", 8)
    
    register_click("hibp", -410, 115, 130, 35, have_i_been_pwned)
    draw_rect(-410, 115, 130, 35, "#111827", "#dc2626")
    draw_text("🔍 HIBP", -400, 90, "white", 8)
    
    register_click("wireshark", -270, 115, 130, 35, wireshark_url)
    draw_rect(-270, 115, 130, 35, "#111827", "#0ea5e9")
    draw_text("📡 Wireshark", -260, 90, "white", 7)
    
    register_click("logs", -130, 115, 130, 35, view_security_logs)
    draw_rect(-130, 115, 130, 35, "#111827", "#64748b")
    draw_text("📋 Logs", -120, 90, "white", 8)
    
    # Row 5: Password Tools
    register_click("gen_pass", -550, 60, 130, 35, generate_password)
    draw_rect(-550, 60, 130, 35, "#111827", "#a855f7")
    draw_text("🔑 Gen Pass", -540, 35, "white", 8)
    
    register_click("check_pass", -410, 60, 130, 35, check_password_strength)
    draw_rect(-410, 60, 130, 35, "#111827", "#a855f7")
    draw_text("✓ Check Pass", -400, 35, "white", 8)
    
    # Statistics
    draw_text(f"🛡️ Detected Threats: {len(DETECTED_THREATS)}", -550, -10, "#ef4444", 9)
    draw_text(f"📝 Security Logs: {len(SECURITY_LOGS)}", -550, -30, "#10b981", 9)
    draw_text(f"🔧 Available Tools: 15+", -550, -50, "#f59e0b", 9)
    
    # Security Tips
    draw_text("💡 Security Tips:", -550, -80, "#f59e0b", 9, "bold")
    draw_text("• Use strong, unique passwords for each account", -550, -100, "white", 7)
    draw_text("• Enable 2FA whenever possible", -550, -115, "white", 7)
    draw_text("• Don't click suspicious links or attachments", -550, -130, "white", 7)
    draw_text("• Keep your system and software updated", -550, -145, "white", 7)
    draw_text("• Use VPN on public Wi-Fi", -550, -160, "white", 7)
    draw_text("• Regularly check Have I Been Pwned", -550, -175, "white", 7)

# ============================================================
# ADDITIONAL APPS (Bank, Files, Terminal, Search, Network, Monitor, Clinic, Social, Deploy, API, Games, Weather, Contacts, Tasks, AI)
# ============================================================

def deposit_money():
    global BANK_BALANCE
    amt = simpledialog.askfloat("Deposit", "Amount:")
    if amt and amt > 0:
        BANK_BALANCE += amt
        messagebox.showinfo("Bank", f"Deposited ${amt:.2f}\nBalance: ${BANK_BALANCE:.2f}")

def withdraw_money():
    global BANK_BALANCE
    amt = simpledialog.askfloat("Withdraw", "Amount:")
    if amt and 0 < amt <= BANK_BALANCE:
        BANK_BALANCE -= amt
        messagebox.showinfo("Bank", f"Withdrew ${amt:.2f}\nBalance: ${BANK_BALANCE:.2f}")

def simple_interest():
    p = simpledialog.askfloat("Principal", "Amount:")
    r = simpledialog.askfloat("Rate", "Rate (%):")
    t = simpledialog.askfloat("Time", "Time (years):")
    if p and r and t:
        interest = (p * r * t) / 100
        total = p + interest
        messagebox.showinfo("Simple Interest", f"Interest: ${interest:.2f}\nTotal: ${total:.2f}")

def compound_interest():
    p = simpledialog.askfloat("Principal", "Amount:")
    r = simpledialog.askfloat("Rate", "Rate (%):")
    t = simpledialog.askfloat("Time", "Time (years):")
    n = simpledialog.askinteger("Frequency", "Compounds per year:", initialvalue=1)
    if p and r and t and n:
        amount = p * (1 + (r/100)/n) ** (n * t)
        messagebox.showinfo("Compound Interest", f"Total: ${amount:.2f}\nInterest: ${amount - p:.2f}")

def emi_calculation():
    p = simpledialog.askfloat("Loan", "Loan Amount:")
    r = simpledialog.askfloat("Rate", "Annual Rate (%):")
    m = simpledialog.askinteger("Months", "Tenure (months):")
    if p and r and m:
        mr = r / (12 * 100)
        emi = p * mr * ((1 + mr) ** m) / (((1 + mr) ** m) - 1)
        messagebox.showinfo("EMI", f"Monthly EMI: ${emi:.2f}\nTotal: ${emi * m:.2f}")

def gst_calculation():
    amt = simpledialog.askfloat("Amount", "Original Amount:")
    rate = simpledialog.askfloat("GST", "GST Rate (%):")
    if amt and rate:
        gst = amt * rate / 100
        messagebox.showinfo("GST", f"GST: ${gst:.2f}\nTotal: ${amt + gst:.2f}")

def sgst_cgst_calculation():
    amt = simpledialog.askfloat("Amount", "Original Amount:")
    sgst_rate = simpledialog.askfloat("SGST", "SGST Rate (%):")
    cgst_rate = simpledialog.askfloat("CGST", "CGST Rate (%):")
    if amt and sgst_rate and cgst_rate:
        sgst = amt * sgst_rate / 100
        cgst = amt * cgst_rate / 100
        messagebox.showinfo("SGST/CGST", f"SGST: ${sgst:.2f}\nCGST: ${cgst:.2f}\nTotal Tax: ${sgst + cgst:.2f}\nTotal: ${amt + sgst + cgst:.2f}")

def tax_calculation():
    income = simpledialog.askfloat("Income", "Annual Income:")
    if income:
        if income <= 11000:
            tax = income * 0.10
        elif income <= 44725:
            tax = 1100 + (income - 11000) * 0.12
        elif income <= 95375:
            tax = 5147 + (income - 44725) * 0.22
        elif income <= 182100:
            tax = 16290 + (income - 95375) * 0.24
        elif income <= 231250:
            tax = 37104 + (income - 182100) * 0.32
        elif income <= 578125:
            tax = 52832 + (income - 231250) * 0.35
        else:
            tax = 174238 + (income - 578125) * 0.37
        messagebox.showinfo("Tax", f"Tax: ${tax:.2f}\nAfter Tax: ${income - tax:.2f}")

def view_transactions():
    cur.execute("SELECT type, amount, date FROM transactions ORDER BY date DESC LIMIT 10")
    trans = cur.fetchall()
    if not trans:
        messagebox.showinfo("Transactions", "No transactions")
        return
    result = "\n".join([f"{t[0]}: ${t[1]:.2f} on {t[2][:16]}" for t in trans])
    messagebox.showinfo("Transactions", result)

def draw_bank():
    draw_window("Bank - Complete Financial Center", "#10b981")
    register_click("deposit", -550, 280, 120, 35, deposit_money)
    draw_rect(-550, 280, 120, 35, "#111827", "#10b981")
    draw_text("💰 Deposit", -535, 255, "white", 8)
    register_click("withdraw", -420, 280, 120, 35, withdraw_money)
    draw_rect(-420, 280, 120, 35, "#111827", "#10b981")
    draw_text("💸 Withdraw", -405, 255, "white", 8)
    register_click("simple_int", -290, 280, 120, 35, simple_interest)
    draw_rect(-290, 280, 120, 35, "#111827", "#3b82f6")
    draw_text("📈 Simple", -275, 255, "white", 8)
    register_click("compound_int", -160, 280, 120, 35, compound_interest)
    draw_rect(-160, 280, 120, 35, "#111827", "#3b82f6")
    draw_text("📊 Compound", -145, 255, "white", 8)
    register_click("emi", -30, 280, 120, 35, emi_calculation)
    draw_rect(-30, 280, 120, 35, "#111827", "#3b82f6")
    draw_text("🏦 EMI", -15, 255, "white", 8)
    register_click("gst", -550, 230, 120, 35, gst_calculation)
    draw_rect(-550, 230, 120, 35, "#111827", "#f59e0b")
    draw_text("🧾 GST", -535, 205, "white", 8)
    register_click("sgst_cgst", -420, 230, 120, 35, sgst_cgst_calculation)
    draw_rect(-420, 230, 120, 35, "#111827", "#f59e0b")
    draw_text("📑 SGST/CGST", -405, 205, "white", 7)
    register_click("tax", -290, 230, 120, 35, tax_calculation)
    draw_rect(-290, 230, 120, 35, "#111827", "#f59e0b")
    draw_text("📊 Tax", -275, 205, "white", 8)
    register_click("history", -160, 230, 120, 35, view_transactions)
    draw_rect(-160, 230, 120, 35, "#111827", "#10b981")
    draw_text("📜 History", -145, 205, "white", 8)
    draw_text(f"💰 Balance: ${BANK_BALANCE:,.2f}", -550, 160, "#10b981", 12, "bold")

def get_desktop_path():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    if os.path.isdir(desktop):
        return desktop
    if os.name == "nt":
        desktop = os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), "Desktop")
        if os.path.isdir(desktop):
            return desktop
    desktop = os.path.join(os.environ.get("HOME", os.path.expanduser("~")), "Desktop")
    return desktop if os.path.isdir(desktop) else os.path.expanduser("~")


def get_desktop_file_path(name):
    return os.path.join(get_desktop_path(), os.path.basename(name))


def create_file():
    name = simpledialog.askstring("Create", "Filename:")
    if name:
        file_path = get_desktop_file_path(name)
        try:
            with open(file_path, "a", encoding="utf-8"):
                pass
            messagebox.showinfo("Create", f"Saved file to Desktop:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not create file: {str(e)}")


def delete_file():
    name = simpledialog.askstring("Delete", "Filename:")
    if name:
        file_path = get_desktop_file_path(name)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                messagebox.showinfo("Delete", f"Deleted file from Desktop:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete file: {str(e)}")
        else:
            messagebox.showerror("Error", "File not found on Desktop.")


def list_files():
    desktop = get_desktop_path()
    try:
        desktop_files = [f for f in os.listdir(desktop) if os.path.isfile(os.path.join(desktop, f))]
        messagebox.showinfo("Files", "\n".join(desktop_files) if desktop_files else "No files on Desktop")
    except Exception as e:
        messagebox.showerror("Error", f"Could not list Desktop files: {str(e)}")


def draw_files():
    draw_window("File Explorer", "#f59e0b")
    register_click("create", -100, 150, 200, 50, create_file)
    draw_rect(-100, 150, 200, 50, "#111827", "#f59e0b")
    draw_text("Create", -70, 120, "white", 12)
    register_click("delete", -100, 70, 200, 50, delete_file)
    draw_rect(-100, 70, 200, 50, "#111827", "#ef4444")
    draw_text("Delete", -70, 40, "white", 12)
    register_click("list", -100, -10, 200, 50, list_files)
    draw_rect(-100, -10, 200, 50, "#111827", "#3b82f6")
    draw_text("List", -65, -40, "white", 12)

def google_search():
    query = simpledialog.askstring("Search", "Query:")
    if query:
        webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}")

def draw_search():
    draw_window("Search", "#ef4444")
    register_click("search", -100, 150, 200, 50, google_search)
    draw_rect(-100, 150, 200, 50, "#111827", "#ef4444")
    draw_text("Google Search", -90, 120, "white", 12)

def run_command():
    cmd = simpledialog.askstring("Terminal", "Command:")
    if cmd:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            messagebox.showinfo("Output", result.stdout + result.stderr if result.stdout else "Executed")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def open_cmd():
    try:
        subprocess.Popen("cmd.exe")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open Command Prompt: {str(e)}")


def open_powershell():
    try:
        subprocess.Popen("powershell.exe")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open PowerShell: {str(e)}")


def open_ubuntu_wsl():
    try:
        if platform.system() == "Windows":
            subprocess.Popen("wsl.exe")
        else:
            messagebox.showwarning("WSL", "WSL (Ubuntu) is only available on Windows with WSL installed.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open Ubuntu/WSL: {str(e)}")


def draw_terminal():
    draw_window("Terminal", "#3b82f6")
    register_click("cmd", -260, 150, 200, 50, open_cmd)
    draw_rect(-260, 150, 200, 50, "#111827", "#3b82f6")
    draw_text("Command Prompt", -220, 120, "white", 11)

    register_click("powershell", -20, 150, 200, 50, open_powershell)
    draw_rect(-20, 150, 200, 50, "#111827", "#0ea5e9")
    draw_text("PowerShell", 0, 120, "white", 12)

    register_click("ubuntu", 220, 150, 200, 50, open_ubuntu_wsl)
    draw_rect(220, 150, 200, 50, "#111827", "#f97316")
    draw_text("Ubuntu (WSL)", 265, 120, "white", 12)

    register_click("run", -260, 70, 200, 50, run_command)
    draw_rect(-260, 70, 200, 50, "#111827", "#10b981")
    draw_text("Run Command", -220, 40, "white", 12)

def network_info():
    hostname = socket.gethostname()
    try:
        ip = socket.gethostbyname(hostname)
        messagebox.showinfo("Network", f"Hostname: {hostname}\nIP: {ip}")
    except:
        messagebox.showinfo("Network", f"Hostname: {hostname}")

def draw_network():
    draw_window("Network", "#3b82f6")
    register_click("info", -100, 150, 200, 50, network_info)
    draw_rect(-100, 150, 200, 50, "#111827", "#3b82f6")
    draw_text("Network Info", -80, 120, "white", 12)

def show_stats():
    messagebox.showinfo("Monitor", f"CPU: {random.randint(1,100)}%\nRAM: {random.randint(1,100)}%\nDisk: {random.randint(1,100)}%")

def draw_monitor():
    draw_window("Monitor", "#10b981")
    register_click("stats", -100, 150, 200, 50, show_stats)
    draw_rect(-100, 150, 200, 50, "#111827", "#10b981")
    draw_text("Show Stats", -65, 120, "white", 12)

def save_patient_to_word(name, age):
    """Save patient record to Word document"""
    patient_record = f"Patient: {name}\nAge: {age}\nAdded: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    doc = {"title": f"Patient Record - {name}", "content": patient_record, "date": str(datetime.datetime.now())}
    WORD_DOCUMENTS.append(doc)
    cur.execute("INSERT INTO word_documents(title, content, date) VALUES(?,?,?)", (doc["title"], doc["content"], doc["date"]))
    conn.commit()

def add_patient():
    name = simpledialog.askstring("Patient", "Name:")
    if name:
        age = simpledialog.askinteger("Age", "Age:")
        PATIENTS.append({"name": name, "age": age})
        save_patient_to_word(name, age)
        messagebox.showinfo("Success", f"Patient {name} added and saved to Word documents!")

def view_patients():
    result = "\n".join([f"{p['name']} ({p['age']})" for p in PATIENTS]) if PATIENTS else "No patients"
    messagebox.showinfo("Patients", result)

def view_word_documents():
    """View all Word documents (patient records)"""
    result = "\n" + "="*40 + "\n".join([f"\n{d['title']}\n{'-'*40}\n{d['content']}" for d in WORD_DOCUMENTS]) if WORD_DOCUMENTS else "No documents"
    messagebox.showinfo("Word Documents", result)

def draw_clinic():
    draw_window("Clinic", "#10b981")
    register_click("add", -250, 150, 200, 50, add_patient)
    draw_rect(-250, 150, 200, 50, "#111827", "#10b981")
    draw_text("Add Patient", -225, 120, "white", 12)
    register_click("view", -50, 150, 200, 50, view_patients)
    draw_rect(-50, 150, 200, 50, "#111827", "#10b981")
    draw_text("View Patients", -35, 120, "white", 12)
    register_click("word", -250, 70, 200, 50, view_word_documents)
    draw_rect(-250, 70, 200, 50, "#111827", "#a78bfa")
    draw_text("📄 View in Word", -220, 40, "white", 12)

def create_post():
    text = simpledialog.askstring("Post", "What's on your mind?")
    if text:
        SOCIAL_POSTS.append({"text": text, "likes": 0})

def show_timeline():
    result = "\n\n".join([f"{p['text']}\n❤️ {p['likes']} likes" for p in SOCIAL_POSTS[-10:]]) if SOCIAL_POSTS else "No posts"
    messagebox.showinfo("Timeline", result)

def open_whatsapp():
    """Open WhatsApp web"""
    try:
        webbrowser.open("https://web.whatsapp.com/")
        messagebox.showinfo("WhatsApp", "✅ Opening WhatsApp Web...")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open WhatsApp: {str(e)}")

def open_facebook():
    """Open Facebook"""
    try:
        webbrowser.open("https://www.facebook.com/")
        messagebox.showinfo("Facebook", "✅ Opening Facebook...")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open Facebook: {str(e)}")

def open_instagram():
    """Open Instagram"""
    try:
        webbrowser.open("https://www.instagram.com/")
        messagebox.showinfo("Instagram", "✅ Opening Instagram...")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open Instagram: {str(e)}")

def open_linkedin():
    """Open LinkedIn"""
    try:
        webbrowser.open("https://www.linkedin.com/")
        messagebox.showinfo("LinkedIn", "✅ Opening LinkedIn...")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open LinkedIn: {str(e)}")

def draw_social():
    draw_window("SocialNet", "#ef4444")
    
    # Row 1 - Posts and Timeline
    register_click("post", -500, 280, 150, 50, create_post)
    draw_rect(-500, 280, 150, 50, "#111827", "#ef4444")
    draw_text("📝 Post", -485, 255, "white", 9)
    
    register_click("timeline", -330, 280, 150, 50, show_timeline)
    draw_rect(-330, 280, 150, 50, "#111827", "#ef4444")
    draw_text("📋 Timeline", -310, 255, "white", 9)
    
    # Row 2 - Social Media Links
    register_click("whatsapp", -160, 280, 140, 50, open_whatsapp)
    draw_rect(-160, 280, 140, 50, "#111827", "#25D366")
    draw_text("💬 WhatsApp", -150, 255, "white", 9)
    
    register_click("facebook", 10, 280, 140, 50, open_facebook)
    draw_rect(10, 280, 140, 50, "#111827", "#1877F2")
    draw_text("👍 Facebook", 20, 255, "white", 9)
    
    register_click("instagram", 180, 280, 140, 50, open_instagram)
    draw_rect(180, 280, 140, 50, "#111827", "#E4405F")
    draw_text("📸 Instagram", 190, 255, "white", 9)
    
    register_click("linkedin", 350, 280, 140, 50, open_linkedin)
    draw_rect(350, 280, 140, 50, "#111827", "#0A66C2")
    draw_text("💼 LinkedIn", 360, 255, "white", 9)
    
    draw_text(f"📱 Posts: {len(SOCIAL_POSTS)}", -500, 200, "#00ffee", 10)

def create_new_document():
    """Create a new Word document"""
    title = simpledialog.askstring("New Document", "Document title:")
    if title:
        content = simpledialog.askstring("Content", "Document content:")
        if content:
            doc = {"title": title, "content": content, "date": str(datetime.datetime.now())}
            WORD_DOCUMENTS.append(doc)
            cur.execute("INSERT INTO word_documents(title, content, date) VALUES(?,?,?)", (doc["title"], doc["content"], doc["date"]))
            conn.commit()
            messagebox.showinfo("Success", f"Document '{title}' created!")

def view_all_word_documents():
    """View all Word documents"""
    if not WORD_DOCUMENTS:
        messagebox.showinfo("Documents", "No documents created yet")
        return
    result = "\n\n" + "="*50 + "\n".join([f"\nTitle: {d['title']}\nDate: {d['date']}\n{'-'*50}\n{d['content']}" for d in WORD_DOCUMENTS])
    messagebox.showinfo("All Documents", result)

def export_to_word_file():
    """Export documents to a text file"""
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as f:
                for doc in WORD_DOCUMENTS:
                    f.write(f"Title: {doc['title']}\n")
                    f.write(f"Date: {doc['date']}\n")
                    f.write("="*50 + "\n")
                    f.write(f"{doc['content']}\n")
                    f.write("\n" + "="*50 + "\n\n")
            messagebox.showinfo("Success", f"Documents exported to {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not export: {str(e)}")

def draw_word():
    draw_window("Word", "#8b5cf6")
    
    register_click("new", -400, 280, 180, 50, create_new_document)
    draw_rect(-400, 280, 180, 50, "#111827", "#8b5cf6")
    draw_text("📄 New Document", -370, 255, "white", 10)
    
    register_click("view", -180, 280, 180, 50, view_all_word_documents)
    draw_rect(-180, 280, 180, 50, "#111827", "#8b5cf6")
    draw_text("📋 View All", -155, 255, "white", 10)
    
    register_click("export", 40, 280, 180, 50, export_to_word_file)
    draw_rect(40, 280, 180, 50, "#111827", "#8b5cf6")
    draw_text("💾 Export", 65, 255, "white", 10)
    
    draw_text(f"📚 Documents: {len(WORD_DOCUMENTS)}", -400, 200, "#00ffee", 11, "bold")

def deploy_project():
    name = simpledialog.askstring("Deploy", "Project:")
    if name:
        DEPLOYMENT_LOGS.append(f"Deployed {name}")
        messagebox.showinfo("Deploy", f"Deployed {name}")


def open_project_deployment_app():
    try:
        webbrowser.open("https://vercel.com/")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open Project Deployment app: {str(e)}")


def open_antigravity():
    try:
        webbrowser.open("https://xkcd.com/353/")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open antigravity: {str(e)}")


def open_vs_code():
    try:
        webbrowser.open("https://code.visualstudio.com/")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open VS Code: {str(e)}")


def draw_deploy():
    draw_window("Deploy", "#10b981")
    register_click("deploy", -310, 150, 200, 50, deploy_project)
    draw_rect(-310, 150, 200, 50, "#111827", "#10b981")
    draw_text("Deploy", -250, 120, "white", 12)

    register_click("project_deploy", -100, 150, 200, 50, open_project_deployment_app)
    draw_rect(-100, 150, 200, 50, "#111827", "#22c55e")
    draw_text("Project Deploy", -60, 120, "white", 12)

    register_click("antigravity", 110, 150, 200, 50, open_antigravity)
    draw_rect(110, 150, 200, 50, "#111827", "#7c3aed")
    draw_text("Antigravity", 150, 120, "white", 12)

    register_click("colab_deploy", -100, 70, 200, 50, open_google_colab)
    draw_rect(-100, 70, 200, 50, "#111827", "#8b5cf6")
    draw_text("Google Colab", -75, 40, "white", 12)

    register_click("vscode", 110, 70, 200, 50, open_vs_code)
    draw_rect(110, 70, 200, 50, "#111827", "#0ea5e9")
    draw_text("VS Code", 155, 40, "white", 12)

def test_api():
    messagebox.showinfo("API", "API Test: 200 OK")


def open_fastapi():
    try:
        webbrowser.open("https://fastapi.tiangolo.com/")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open FastAPI URL: {str(e)}")


def open_cherrypy():
    try:
        webbrowser.open("https://cherrypy.org/")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open CherryPy URL: {str(e)}")


def open_rest_api():
    try:
        webbrowser.open("https://restfulapi.net/")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open REST API URL: {str(e)}")


def open_google_cloud():
    try:
        webbrowser.open("https://cloud.google.com/")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open Google Cloud URL: {str(e)}")


def open_google_colab():
    try:
        webbrowser.open("https://colab.research.google.com/")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open Google Colab URL: {str(e)}")


def open_project_runner():
    try:
        webbrowser.open("https://replit.com/~")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open Project Runner URL: {str(e)}")


def draw_api():
    draw_window("API", "#06b6d4")
    register_click("fastapi", -260, 150, 200, 50, open_fastapi)
    draw_rect(-260, 150, 200, 50, "#111827", "#22c55e")
    draw_text("FastAPI", -200, 120, "white", 12)

    register_click("cherrypy", 20, 150, 200, 50, open_cherrypy)
    draw_rect(20, 150, 200, 50, "#111827", "#0ea5e9")
    draw_text("CherryPy", 45, 120, "white", 12)

    register_click("restapi", -260, 70, 200, 50, open_rest_api)
    draw_rect(-260, 70, 200, 50, "#111827", "#f97316")
    draw_text("REST API", -210, 40, "white", 12)

    register_click("gcloud", 20, 70, 200, 50, open_google_cloud)
    draw_rect(20, 70, 200, 50, "#111827", "#6366f1")
    draw_text("Google Cloud", 45, 40, "white", 12)

    register_click("colab", -260, -10, 200, 50, open_google_colab)
    draw_rect(-260, -10, 200, 50, "#111827", "#8b5cf6")
    draw_text("Google Colab", -215, 20, "white", 12)

    register_click("project_runner", 20, -10, 200, 50, open_project_runner)
    draw_rect(20, -10, 200, 50, "#111827", "#ec4899")
    draw_text("Project Runner", 45, 20, "white", 12)

    register_click("test", 150, 150, 150, 50, test_api)
    draw_rect(150, 150, 150, 50, "#111827", "#06b6d4")
    draw_text("Test API", 175, 120, "white", 12)

def guessing_game():
    number = random.randint(1, 10)
    guess = simpledialog.askinteger("Guess", "Guess a number (1-10):")
    if guess == number:
        messagebox.showinfo("Game", "🎉 Correct!")
    else:
        messagebox.showinfo("Game", f"❌ Wrong! Number was {number}")

def snakes_and_ladders():
    game_window = tk.Toplevel()
    game_window.title("Snake and Ladders")
    game_window.geometry("400x500")
    game_window.configure(bg="#1e1e1e")
    
    pos = 1
    snakes = {16:6, 47:26, 49:11, 56:53, 62:19, 64:60, 87:24, 93:73, 95:75, 98:78}
    ladders = {1:38, 4:14, 9:31, 21:42, 28:84, 36:44, 51:67, 71:91, 80:100}
    
    def roll():
        nonlocal pos
        dice = random.randint(1, 6)
        new_pos = pos + dice
        if new_pos > 100:
            msg = f"Rolled {dice}. Need exact roll!"
        else:
            if new_pos in snakes:
                new_pos = snakes[new_pos]
                msg = f"Rolled {dice}! 🐍 Snake to {new_pos}"
            elif new_pos in ladders:
                new_pos = ladders[new_pos]
                msg = f"Rolled {dice}! 🪜 Ladder to {new_pos}"
            else:
                msg = f"Rolled {dice}. Moved to {new_pos}"
        pos = new_pos
        label.config(text=f"Position: {pos}")
        if pos == 100:
            messagebox.showinfo("Game Over", "🎉 YOU WIN! 🎉")
            game_window.destroy()
        messagebox.showinfo("Dice Roll", msg)
    
    label = tk.Label(game_window, text="Position: 1", bg="#1e1e1e", fg="white", font=("Arial", 14))
    label.pack(pady=20)
    tk.Button(game_window, text="🎲 Roll Dice", command=roll, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=20)

def draw_games():
    draw_window("Games", "#a855f7")
    register_click("guess", -200, 280, 180, 50, guessing_game)
    draw_rect(-200, 280, 180, 50, "#111827", "#a855f7")
    draw_text("Guess Number", -185, 255, "white", 10)
    register_click("snake", 20, 280, 180, 50, snakes_and_ladders)
    draw_rect(20, 280, 180, 50, "#111827", "#f59e0b")
    draw_text("Snake & Ladders", 35, 255, "white", 9)

def get_weather():
    city = simpledialog.askstring("Weather", "City:")
    if city:
        messagebox.showinfo("Weather", f"{city}: {random.randint(-10,40)}°C")


def open_online_weather():
    try:
        webbrowser.open("https://weather.com/")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open online weather app: {str(e)}")


def draw_weather():
    draw_window("Weather", "#06b6d4")
    register_click("weather", -170, 150, 200, 50, get_weather)
    draw_rect(-170, 150, 200, 50, "#111827", "#06b6d4")
    draw_text("Get Weather", -145, 120, "white", 12)

    register_click("online_weather", 90, 150, 200, 50, open_online_weather)
    draw_rect(90, 150, 200, 50, "#111827", "#7c3aed")
    draw_text("🌐 Online Weather", 115, 120, "white", 12)


def add_contact():
    name = simpledialog.askstring("Contact", "Name:")
    if name:
        phone = simpledialog.askstring("Phone", "Phone:")
        cur.execute("INSERT INTO contacts(name, phone) VALUES(?,?)", (name, phone))
        conn.commit()

def view_contacts():
    cur.execute("SELECT name, phone FROM contacts")
    contacts = cur.fetchall()
    result = "\n".join([f"{c[0]}: {c[1]}" for c in contacts]) if contacts else "No contacts"
    messagebox.showinfo("Contacts", result)


def open_phone_app():
    try:
        webbrowser.open("https://www.phone.com/")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open phone app URL: {str(e)}")


def draw_contacts():
    draw_window("Contacts", "#10b981")
    register_click("add", -100, 150, 200, 50, add_contact)
    draw_rect(-100, 150, 200, 50, "#111827", "#10b981")
    draw_text("Add Contact", -75, 120, "white", 12)
    register_click("view", -100, 70, 200, 50, view_contacts)
    draw_rect(-100, 70, 200, 50, "#111827", "#10b981")
    draw_text("View Contacts", -85, 40, "white", 12)
    register_click("phone", 110, 150, 200, 50, open_phone_app)
    draw_rect(110, 150, 200, 50, "#111827", "#7c3aed")
    draw_text("Phone App", 135, 120, "white", 12)

def add_task():
    title = simpledialog.askstring("Task", "Title:")
    if title:
        cur.execute("INSERT INTO tasks(title, status) VALUES(?,?)", (title, "Pending"))
        conn.commit()

def view_tasks():
    cur.execute("SELECT title FROM tasks WHERE status='Pending'")
    tasks = cur.fetchall()
    result = "\n".join([f"📌 {t[0]}" for t in tasks]) if tasks else "No tasks"
    messagebox.showinfo("Tasks", result)


def open_windows_task_manager():
    if platform.system() != "Windows":
        messagebox.showwarning("Task Manager", "Windows Task Manager is only available on Windows.")
        return
    try:
        subprocess.Popen(["taskmgr"])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open Task Manager: {str(e)}")


def draw_tasks():
    draw_window("Tasks", "#f59e0b")
    register_click("add", -100, 150, 200, 50, add_task)
    draw_rect(-100, 150, 200, 50, "#111827", "#f59e0b")
    draw_text("Add Task", -75, 120, "white", 12)
    register_click("view", -100, 70, 200, 50, view_tasks)
    draw_rect(-100, 70, 200, 50, "#111827", "#f59e0b")
    draw_text("View Tasks", -85, 40, "white", 12)
    register_click("taskmgr", 110, 110, 200, 50, open_windows_task_manager)
    draw_rect(110, 110, 200, 50, "#111827", "#22c55e")
    draw_text("Open Task Manager", 135, 80, "white", 11)

def generate_ai_response(model, question):
    return f"{AI_MODELS[model]['icon']} {model}: I understand your question about '{question[:50]}...'. How can I help?"

def ask_ai():
    global CURRENT_AI_MODEL
    model_list = "\n".join([f"{data['icon']} {name}" for name, data in AI_MODELS.items()])
    choice = simpledialog.askstring("AI", f"Models:\n{model_list}\n\nCurrent: {CURRENT_AI_MODEL}\n\nEnter model:")
    if not choice:
        return
    for model in AI_MODELS:
        if model.lower() == choice.lower():
            CURRENT_AI_MODEL = model
            break
    question = simpledialog.askstring(f"{CURRENT_AI_MODEL}", f"Ask {CURRENT_AI_MODEL}:")
    if question:
        response = generate_ai_response(CURRENT_AI_MODEL, question)
        messagebox.showinfo(f"{CURRENT_AI_MODEL}", response)

def open_url(url):
    try:
        webbrowser.open(url)
    except Exception:
        messagebox.showerror("Open URL", f"Could not open {url}")


def draw_animation():
    draw_window("Animation Studio", "#8b5cf6")
    tools = [
        ("Animoto", "https://animoto.com"),
        ("Photoshop", "https://www.adobe.com/products/photoshop.html"),
        ("Animaker", "https://www.animaker.com"),
        ("Snifig", "https://www.snifig.com"),
        ("Adobe Animate", "https://www.adobe.com/products/animate.html"),
        ("After Effects", "https://www.adobe.com/products/aftereffects.html")
    ]

    start_x = -520
    y = 180
    for label, url in tools:
        register_click(label, start_x, y, 260, 60, lambda u=url: open_url(u))
        draw_rect(start_x, y, 260, 60, "#111827", "#8b5cf6")
        draw_text(label, start_x + 20, y - 35, "white", 10, "bold")
        draw_text(url, start_x + 20, y - 50, "#9ca3af", 8)
        start_x += 280
        if start_x > 320:
            start_x = -520
            y -= 90

    draw_text("Built-in animation tools with official websites.", -520, -10, "#c7d2fe", 10)


def draw_ai():
    draw_window("AI Assistant", "#10b981")
    register_click("ask", -100, 150, 200, 50, ask_ai)
    draw_rect(-100, 150, 200, 50, "#111827", "#10b981")
    draw_text("Ask AI", -60, 120, "white", 12)
    draw_text(f"Current: {CURRENT_AI_MODEL}", -500, 200, "#f59e0b", 10)

# ============================================================
# CALCULATOR APP


def safe_math_env():
    env = {
        'pi': math.pi,
        'e': math.e,
        'tau': math.tau if hasattr(math, 'tau') else 2 * math.pi,
        'inf': math.inf,
        'nan': math.nan,
        'sqrt': math.sqrt,
        'pow': pow,
        'abs': abs,
        'round': round,
        'floor': math.floor,
        'ceil': math.ceil,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'asin': math.asin,
        'acos': math.acos,
        'atan': math.atan,
        'sinh': math.sinh,
        'cosh': math.cosh,
        'tanh': math.tanh,
        'exp': math.exp,
        'log': math.log,
        'log10': math.log10,
        'log2': math.log2,
        'degrees': math.degrees,
        'radians': math.radians,
        'factorial': math.factorial,
        'complex': complex,
        'pow': pow,
        'round': round,
        'sqrt': math.sqrt,
    }
    env.update({
        'complex': complex,
        'cmath': cmath,
        'math': math
    })
    if np is not None:
        env.update({
            'array': np.array,
            'linspace': np.linspace,
            'fft': np.fft.fft,
            'ifft': np.fft.ifft,
            'mean': np.mean,
            'median': np.median,
            'std': np.std,
        })
    return env


def format_complex(value):
    try:
        if isinstance(value, complex):
            if abs(value.imag) < 1e-12:
                return f"{value.real:.12g}"
            return f"{value.real:.12g}{'+' if value.imag >= 0 else '-'}{abs(value.imag):.12g}j"
        return str(value)
    except Exception:
        return str(value)


def calculate_expression():
    expr = simpledialog.askstring("Calculator", "Enter expression to evaluate:\nUse x, y, z, sin, cos, exp, log, sqrt, pi, e, and Python operators:")
    if not expr:
        return
    expr = expr.replace('^', '**')
    try:
        if sp is not None:
            x, y, z = sp.symbols('x y z')
            locals_map = {
                'x': x,
                'y': y,
                'z': z,
                'pi': sp.pi,
                'e': sp.E,
                'sin': sp.sin,
                'cos': sp.cos,
                'tan': sp.tan,
                'exp': sp.exp,
                'log': sp.log,
                'sqrt': sp.sqrt,
                'abs': sp.Abs,
            }
            result = sp.sympify(expr, locals=locals_map)
            numeric = result.evalf()
            messagebox.showinfo("Calculator", f"Expression: {expr}\nResult: {numeric}\nExact: {result}")
        else:
            result = eval(expr, {"__builtins__": None}, safe_math_env())
            messagebox.showinfo("Calculator", f"Expression: {expr}\nResult: {format_complex(result)}")
    except Exception as e:
        messagebox.showerror("Calculator Error", f"Unable to evaluate expression:\n{e}")


def solve_linear_equation():
    equation = simpledialog.askstring("Linear Solver", "Enter linear equation in x, for example 2*x + 3 = 7:")
    if not equation:
        return
    equation = equation.replace('^', '**')
    try:
        if sp is not None:
            x = sp.symbols('x')
            left, right = equation.split('=')
            solution = sp.solve(sp.Eq(sp.sympify(left, locals={'x': x}), sp.sympify(right, locals={'x': x})), x)
            messagebox.showinfo("Linear Solution", f"Equation: {equation}\nSolution: {solution}")
        else:
            messagebox.showerror("Linear Solver", "SymPy is required for symbolic linear solving.")
    except Exception as e:
        messagebox.showerror("Linear Solver Error", f"Could not solve linear equation:\n{e}")


def solve_quadratic_equation():
    coeffs = simpledialog.askstring("Quadratic Solver", "Enter coefficients a, b, c separated by commas for ax^2 + bx + c = 0:")
    if not coeffs:
        return
    try:
        a, b, c = [float(x.strip()) for x in coeffs.split(',')]
        discriminant = b * b - 4 * a * c
        root1 = (-b + cmath.sqrt(discriminant)) / (2 * a)
        root2 = (-b - cmath.sqrt(discriminant)) / (2 * a)
        messagebox.showinfo("Quadratic Roots", f"a={a}, b={b}, c={c}\nRoot 1: {format_complex(root1)}\nRoot 2: {format_complex(root2)}")
    except Exception as e:
        messagebox.showerror("Quadratic Solver Error", f"Unable to solve quadratic equation:\n{e}")


def polynomial_tools():
    coeffs = simpledialog.askstring("Polynomial Tools", "Enter coefficients from highest degree to constant, separated by commas:\nExample: 1,-3,2 for x^2-3x+2")
    if not coeffs:
        return
    try:
        coef_list = [float(x.strip()) for x in coeffs.split(',') if x.strip() != '']
        if len(coef_list) < 2:
            raise ValueError('At least two coefficients are required.')
        if np is not None:
            roots = np.roots(coef_list)
            roots_text = '\n'.join([format_complex(r) for r in roots])
        else:
            roots_text = 'Numpy required for polynomial root finding.'
        degree = len(coef_list) - 1
        poly = ' + '.join([f"{coef_list[i]}*x**{degree-i}" for i in range(len(coef_list) - 1)]) + f" + {coef_list[-1]}"
        messagebox.showinfo("Polynomial", f"Polynomial coefficients: {coef_list}\nRoots:\n{roots_text}")
    except Exception as e:
        messagebox.showerror("Polynomial Error", f"Could not analyze polynomial:\n{e}")


def integrate_expression():
    expr = simpledialog.askstring("Integration", "Enter expression to integrate in x, e.g. sin(x) or x^2:")
    if not expr:
        return
    expr = expr.replace('^', '**')
    bounds = simpledialog.askstring("Integration", "Enter bounds separated by comma for definite integral, or leave blank for indefinite:\nExample: 0,pi")
    try:
        if sp is not None:
            x = sp.symbols('x')
            symbolic = sp.sympify(expr, locals={'x': x, 'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan, 'exp': sp.exp, 'log': sp.log, 'sqrt': sp.sqrt})
            if bounds:
                a, b = [sp.sympify(val.strip(), locals={'pi': sp.pi, 'e': sp.E}) for val in bounds.split(',')]
                result = sp.integrate(symbolic, (x, a, b))
                messagebox.showinfo("Integration", f"Integral of {expr} from {a} to {b}:\n{result}")
            else:
                result = sp.integrate(symbolic, x)
                messagebox.showinfo("Integration", f"Indefinite integral of {expr}:\n{result}")
        elif sc is not None:
            if not bounds:
                messagebox.showerror("Integration", "Definite integration requires SciPy and bounds.")
                return
            a, b = [float(x.strip()) for x in bounds.split(',')]
            func = lambda t: eval(expr, {"__builtins__": None}, safe_math_env())
            result, _ = integrate.quad(func, a, b)
            messagebox.showinfo("Integration", f"Definite integral of {expr} from {a} to {b}:\n{result}")
        else:
            messagebox.showerror("Integration", "SymPy or SciPy is required for integration.")
    except Exception as e:
        messagebox.showerror("Integration Error", f"Unable to integrate expression:\n{e}")


def differentiate_expression():
    expr = simpledialog.askstring("Differentiation", "Enter expression to differentiate in x, e.g. x^3 + 2*x:")
    if not expr:
        return
    expr = expr.replace('^', '**')
    order = simpledialog.askinteger("Differentiation", "Enter derivative order (1 for first derivative):", minvalue=1, maxvalue=10)
    if order is None:
        return
    try:
        if sp is not None:
            x = sp.symbols('x')
            symbolic = sp.sympify(expr, locals={'x': x, 'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan, 'exp': sp.exp, 'log': sp.log, 'sqrt': sp.sqrt})
            result = sp.diff(symbolic, x, order)
            messagebox.showinfo("Differentiation", f"{order} order derivative of {expr}:\n{result}")
        else:
            messagebox.showerror("Differentiation", "SymPy is required for symbolic differentiation.")
    except Exception as e:
        messagebox.showerror("Differentiation Error", f"Unable to differentiate expression:\n{e}")


def fourier_transform_tool():
    mode = simpledialog.askstring("Fourier Transform", "Enter mode: symbolic or numeric")
    if not mode:
        return
    mode = mode.strip().lower()
    if mode == 'symbolic':
        expr = simpledialog.askstring("Fourier Transform", "Enter expression in x, e.g. exp(-x**2):")
        if not expr:
            return
        expr = expr.replace('^', '**')
        try:
            if sp is not None:
                x, w = sp.symbols('x w')
                symbolic = sp.sympify(expr, locals={'x': x, 'exp': sp.exp, 'sin': sp.sin, 'cos': sp.cos, 'pi': sp.pi, 'sqrt': sp.sqrt})
                result = sp.fourier_transform(symbolic, x, w)
                messagebox.showinfo("Fourier Transform", f"Fourier transform of {expr}:\n{result}")
            else:
                messagebox.showerror("Fourier Transform", "SymPy is required for symbolic Fourier transforms.")
        except Exception as e:
            messagebox.showerror("Fourier Transform Error", f"Unable to compute symbolic Fourier transform:\n{e}")
    else:
        values = simpledialog.askstring("Fourier Transform", "Enter numeric samples separated by commas:")
        if not values:
            return
        try:
            if np is None:
                messagebox.showerror("Fourier Transform", "NumPy is required for numeric Fourier transforms.")
                return
            samples = np.array([float(x.strip()) for x in values.split(',')])
            transform = np.fft.fft(samples)
            result = '\n'.join([format_complex(val) for val in transform])
            messagebox.showinfo("Fourier Transform", f"FFT result:\n{result}")
        except Exception as e:
            messagebox.showerror("Fourier Transform Error", f"Unable to compute numeric Fourier transform:\n{e}")


def cluster_analysis():
    points = simpledialog.askstring("Cluster Analysis", "Enter points as x,y pairs separated by semicolon:\nExample: 1,2; 3,4; 5,1")
    if not points:
        return
    try:
        raw = [tuple(float(v.strip()) for v in pair.split(',')) for pair in points.split(';') if pair.strip()]
        if len(raw) < 2:
            raise ValueError('At least two points are required.')
        k = simpledialog.askinteger("Cluster Analysis", "Enter number of clusters:", minvalue=1, maxvalue=len(raw))
        if k is None:
            return
        if np is not None:
            pts = np.array(raw)
            centroids = pts[np.random.choice(len(pts), k, replace=False)]
            for _ in range(100):
                distances = np.linalg.norm(pts[:, None, :] - centroids[None, :, :], axis=2)
                labels = np.argmin(distances, axis=1)
                new_centroids = np.array([pts[labels == i].mean(axis=0) if np.any(labels == i) else centroids[i] for i in range(k)])
                if np.allclose(centroids, new_centroids):
                    break
                centroids = new_centroids
            centroids_text = '\n'.join([f"Cluster {i + 1}: {tuple(np.round(c, 6))}" for i, c in enumerate(centroids)])
            assignments = '\n'.join([f"Point {raw[i]} -> Cluster {labels[i] + 1}" for i in range(len(raw))])
            messagebox.showinfo("Cluster Analysis", f"Centroids:\n{centroids_text}\n\nAssignments:\n{assignments}")
        else:
            messagebox.showerror("Cluster Analysis", "NumPy is required for clustering.")
    except Exception as e:
        messagebox.showerror("Cluster Analysis Error", f"Unable to perform clustering:\n{e}")


def draw_calculator():
    draw_window("Advanced Calculator", "#6366f1")
    buttons = [
        ("Basic Eval", calculate_expression),
        ("Linear Eq", solve_linear_equation),
        ("Quadratic", solve_quadratic_equation),
        ("Polynomial", polynomial_tools),
        ("Integrate", integrate_expression),
        ("Differentiate", differentiate_expression),
        ("Fourier", fourier_transform_tool),
        ("Cluster", cluster_analysis),
    ]
    start_x = -520
    start_y = 250
    for i, (label, callback) in enumerate(buttons):
        x = start_x + (i % 2) * 260
        y = start_y - (i // 2) * 90
        register_click(label, x, y, 240, 70, callback)
        draw_rect(x, y, 240, 70, "#111827", "#6366f1")
        draw_text(label, x + 20, y - 40, "white", 11, "bold")

# ============================================================
# KERNEL APP
# ============================================================

def get_system_details():
    details = f"""
OS: {platform.system()} {platform.release()}
Python: {platform.python_version()}
Hostname: {socket.gethostname()}
User: {os.getlogin() if hasattr(os, 'getlogin') else CURRENT_USER}
CPU Cores: {os.cpu_count()}
"""
    messagebox.showinfo("System Details", details)

def list_all_commands():
    commands = """
dir - List directory
cd - Change directory
mkdir - Create directory
del - Delete file
copy - Copy file
move - Move file
ipconfig - IP configuration
ping - Test connection
tasklist - List processes
systeminfo - System info
"""
    messagebox.showinfo("Commands", commands)

def kernel_diagnostics():
    messagebox.showinfo("Kernel", "✅ All systems OK!")

def shutdown_system():
    if messagebox.askyesno("Shutdown", "Shutdown NeilOS?"):
        sys.exit()

def draw_kernel():
    draw_window("Kernel", "#3b82f6")
    
    # Display actual system time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw_text(f"⏰ System Time: {current_time}", -450, 350, "#00ffee", 10, "bold")
    
    register_click("sys", -450, 280, 180, 40, get_system_details)
    draw_rect(-450, 280, 180, 40, "#111827", "#10b981")
    draw_text("🖥️ System", -435, 255, "white", 9)
    register_click("cmd", -250, 280, 180, 40, list_all_commands)
    draw_rect(-250, 280, 180, 40, "#111827", "#f59e0b")
    draw_text("📋 Commands", -235, 255, "white", 9)
    register_click("diag", -50, 280, 180, 40, kernel_diagnostics)
    draw_rect(-50, 280, 180, 40, "#111827", "#3b82f6")
    draw_text("🔬 Diag", -35, 255, "white", 9)
    register_click("shutdown", -450, 220, 180, 40, shutdown_system)
    draw_rect(-450, 220, 180, 40, "#111827", "#ef4444")
    draw_text("⏻ Shutdown", -435, 195, "white", 9)

# ============================================================
# NOTES APP
# ============================================================

def save_note(note):
    cur.execute("INSERT INTO notes(content, date) VALUES(?,?)", (note, str(datetime.datetime.now())))
    conn.commit()

def load_notes():
    cur.execute("SELECT content, date FROM notes ORDER BY date DESC")
    return cur.fetchall()

def add_note():
    text = simpledialog.askstring("Notes", "Write note:")
    if text:
        save_note(text)
        messagebox.showinfo("Notes", "✅ Note saved successfully!")

def delete_note(note_content):
    """Delete a specific note from database"""
    try:
        cur.execute("DELETE FROM notes WHERE content=?", (note_content,))
        conn.commit()
        messagebox.showinfo("Notes", "✅ Note deleted!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not delete note: {str(e)}")

def edit_note(note_content):
    """Edit an existing note"""
    new_text = simpledialog.askstring("Edit Note", "Edit note:", initialvalue=note_content)
    if new_text and new_text != note_content:
        try:
            cur.execute("UPDATE notes SET content=? WHERE content=?", (new_text, note_content))
            conn.commit()
            messagebox.showinfo("Notes", "✅ Note updated!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not update note: {str(e)}")

def search_notes():
    """Search notes by keyword"""
    keyword = simpledialog.askstring("Search Notes", "Enter keyword to search:")
    if not keyword:
        return
    try:
        cur.execute("SELECT content, date FROM notes WHERE content LIKE ? ORDER BY date DESC", 
                   (f"%{keyword}%",))
        results = cur.fetchall()
        if not results:
            messagebox.showinfo("Search Results", f"No notes found containing '{keyword}'")
            return
        result_text = f"Found {len(results)} note(s):\n\n" + "\n\n".join([f"[{n[1][:16]}]\n{n[0][:100]}..." if len(n[0]) > 100 else f"[{n[1][:16]}]\n{n[0]}" for n in results])
        messagebox.showinfo("Search Results", result_text)
    except Exception as e:
        messagebox.showerror("Error", f"Search failed: {str(e)}")

def show_notes():
    """Enhanced view to display all notes in a window"""
    notes = load_notes()
    if not notes:
        messagebox.showinfo("Notes", "📭 No notes saved yet")
        return
    
    notes_window = tk.Toplevel()
    notes_window.title("NeilOS Notes Viewer")
    notes_window.geometry("700x600")
    notes_window.configure(bg="#1e1e1e")
    
    # Title
    title_label = tk.Label(notes_window, text=f"📝 Your Notes ({len(notes)} total)", 
                          bg="#1e1e1e", fg="#00ffee", font=("Consolas", 12, "bold"))
    title_label.pack(pady=10)
    
    # Frame with scrollbar
    frame = tk.Frame(notes_window, bg="#1e1e1e")
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    scrollbar = tk.Scrollbar(frame, bg="#111827")
    scrollbar.pack(side="right", fill="y")
    
    text_widget = tk.Text(frame, bg="#0a0a0a", fg="#00ff00", font=("Consolas", 9),
                         yscrollcommand=scrollbar.set, wrap=tk.WORD)
    text_widget.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=text_widget.yview)
    
    # Insert notes
    for i, note in enumerate(notes, 1):
        text_widget.insert(tk.END, f"╔{'═'*70}\n")
        text_widget.insert(tk.END, f"║ Note #{i} | 📅 {note[1]}\n")
        text_widget.insert(tk.END, f"╠{'═'*70}\n")
        text_widget.insert(tk.END, f"║ {note[0]}\n")
        text_widget.insert(tk.END, f"╚{'═'*70}\n\n")
    
    text_widget.config(state=tk.DISABLED)
    
    # Button frame
    button_frame = tk.Frame(notes_window, bg="#1e1e1e")
    button_frame.pack(fill=tk.X, padx=10, pady=10)
    
    tk.Button(button_frame, text="🔍 Search", command=search_notes, 
             bg="#3b82f6", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="📝 New Note", command=add_note, 
             bg="#10b981", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="📄 Open Notepad", command=open_notepad, 
             bg="#ef4444", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="🌐 Online Notepad", command=open_online_notepad, 
             bg="#7c3aed", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="❌ Close", command=notes_window.destroy, 
             bg="#6b7280", fg="white", font=("Arial", 9)).pack(side=tk.RIGHT, padx=5)

def open_notepad():
    """Open system notepad and sync with NeilOS notes"""
    notes = load_notes()
    notepad_file = "neilos_notes.txt"
    
    try:
        with open(notepad_file, "w", encoding="utf-8") as f:
            f.write("╔═══════════════════════════════════════════════════════════════╗\n")
            f.write("║          🎵 NeilOS Notes - Synced Notepad 🎵                   ║\n")
            f.write("╚═══════════════════════════════════════════════════════════════╝\n\n")
            f.write(f"Total Notes: {len(notes)}\n")
            f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("═" * 65 + "\n\n")
            
            for i, note in enumerate(notes, 1):
                f.write(f"┌─ Note #{i} ─────────────────────────────────────────────────\n")
                f.write(f"│ Date: {note[1]}\n")
                f.write(f"├───────────────────────────────────────────────────────────\n")
                f.write(f"│ {note[0]}\n")
                f.write(f"└───────────────────────────────────────────────────────────\n\n")
        
        # Open in system notepad
        if platform.system() == "Windows":
            os.startfile(notepad_file)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", "TextEdit", notepad_file])
        else:  # Linux
            subprocess.Popen(["gedit", notepad_file])
        
        messagebox.showinfo("Notepad", "✅ Notepad opened with all your notes!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open notepad: {str(e)}")


def open_online_notepad():
    """Open a web-based online notepad in the default browser."""
    try:
        webbrowser.open("https://anotepad.com/")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open online notepad: {str(e)}")


def clear_all_notes():
    """Clear all notes with confirmation"""
    if messagebox.askyesno("Clear All", "⚠️ Are you sure you want to delete ALL notes?"):
        try:
            cur.execute("DELETE FROM notes")
            conn.commit()
            messagebox.showinfo("Notes", "✅ All notes cleared!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not clear notes: {str(e)}")

def export_notes():
    """Export notes to a text file"""
    notes = load_notes()
    if not notes:
        messagebox.showinfo("Export", "📭 No notes to export")
        return
    
    export_file = f"neilos_notes_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    try:
        with open(export_file, "w", encoding="utf-8") as f:
            f.write("NeilOS Notes Export\n")
            f.write(f"Exported: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")
            for i, note in enumerate(notes, 1):
                f.write(f"[Note #{i}] {note[1]}\n{note[0]}\n\n")
        messagebox.showinfo("Export", f"✅ Notes exported to {export_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Export failed: {str(e)}")

def draw_notes():
    draw_window("Notes", "#f59e0b")
    register_click("add", -500, 280, 150, 50, add_note)
    draw_rect(-500, 280, 150, 50, "#111827", "#10b981")
    draw_text("➕ Add", -485, 255, "white", 9)
    
    register_click("view", -330, 280, 150, 50, show_notes)
    draw_rect(-330, 280, 150, 50, "#111827", "#3b82f6")
    draw_text("👁 View", -315, 255, "white", 9)
    
    register_click("search", -160, 280, 150, 50, search_notes)
    draw_rect(-160, 280, 150, 50, "#111827", "#8b5cf6")
    draw_text("🔍 Search", -140, 255, "white", 9)
    
    register_click("notepad", 10, 280, 150, 50, open_notepad)
    draw_rect(10, 280, 150, 50, "#111827", "#ef4444")
    draw_text("📄 Notepad", 25, 255, "white", 9)
    
    register_click("online_notepad", 180, 280, 150, 50, open_online_notepad)
    draw_rect(180, 280, 150, 50, "#111827", "#7c3aed")
    draw_text("🌐 Online", 215, 255, "white", 9)
    
    register_click("export", 350, 280, 150, 50, export_notes)
    draw_rect(350, 280, 150, 50, "#111827", "#06b6d4")
    draw_text("💾 Export", 385, 255, "white", 9)
    
    register_click("clear", 520, 280, 150, 50, clear_all_notes)
    draw_rect(520, 280, 150, 50, "#111827", "#ef4444")
    draw_text("🗑 Clear All", 535, 255, "white", 9)
    
    total_notes = len(load_notes())
    draw_text(f"📝 Total Notes: {total_notes}", -500, 200, "#00ffee", 10)

# ============================================================
# CODE STUDIO
# ============================================================

def choose_language_dialog():
    dialog = tk.Toplevel()
    dialog.title("Choose Language")
    dialog.geometry("420x420")
    dialog.configure(bg="#111827")
    tk.Label(dialog, text="Select language for Code Studio:", bg="#111827", fg="white", font=("Arial", 10, "bold")).pack(pady=8)
    frame = tk.Frame(dialog, bg="#111827")
    frame.pack(fill="both", expand=True, padx=10, pady=4)
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")
    listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE, activestyle='dotbox', bg="#1e1e1e", fg="white", selectbackground="#4b5563")
    for language in sorted(PROGRAMMING_LANGUAGES.keys()):
        listbox.insert(tk.END, language)
    listbox.pack(fill="both", expand=True)
    scrollbar.config(command=listbox.yview)
    selected = {'language': None}
    def choose():
        selection = listbox.curselection()
        if selection:
            selected['language'] = listbox.get(selection[0])
            dialog.destroy()
    tk.Button(dialog, text="Select", command=choose, bg="#10b981", fg="white").pack(pady=8)
    dialog.transient(tk._default_root)
    dialog.grab_set()
    dialog.wait_window()
    return selected['language']


def get_default_code_template(language):
    templates = {
        "Python": "# Python example\nprint('Hello, Python!')\n",
        "JavaScript": "// JavaScript example\nconsole.log('Hello, JavaScript!');\n",
        "TypeScript": "// TypeScript example\nconst greeting: string = 'Hello, TypeScript!';\nconsole.log(greeting);\n",
        "Java": "// Java example\npublic class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, Java!\");\n    }\n}\n",
        "C": "/* C example */\n#include <stdio.h>\nint main() { printf(\"Hello, C!\\n\"); return 0; }\n",
        "C++": "// C++ example\n#include <iostream>\nint main() { std::cout << \"Hello, C++!\" << std::endl; return 0; }\n",
        "C#": "// C# example\nusing System;\nclass Program { static void Main() { Console.WriteLine(\"Hello, C#!\"); } }\n",
        "Go": "// Go example\npackage main\nimport \"fmt\"\nfunc main() { fmt.Println(\"Hello, Go!\") }\n",
        "Rust": "// Rust example\nfn main() { println!(\"Hello, Rust!\"); }\n",
        "PHP": "<?php\necho 'Hello, PHP!';\n?>\n",
        "Swift": "// Swift example\nprint(\"Hello, Swift!\")\n",
        "Kotlin": "// Kotlin example\nfun main() { println(\"Hello, Kotlin!\") }\n",
        "HTML": "<!-- HTML example -->\n<!DOCTYPE html>\n<html><body><h1>Hello, HTML!</h1></body></html>\n",
        "CSS": "/* CSS example */\nbody { background: #121212; color: #fff; }\n",
        "SQL": "-- SQL example\nSELECT * FROM users;\n",
        "Bash": "# Bash example\necho \"Hello, Bash!\"\n",
        "PowerShell": "# PowerShell example\nWrite-Host 'Hello, PowerShell!'\n",
        "Dockerfile": "# Dockerfile example\nFROM python:3.12-slim\nCMD [\"python\", \"-c\", \"print('Hello from Docker')\"]\n",
        "JSON": "{\n  \"message\": \"Hello, JSON!\"\n}\n",
        "YAML": "message: Hello, YAML!\n",
        "Markdown": "# Markdown example\nHello, Markdown!\n",
        "XML": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<message>Hello, XML!</message>\n",
        "R": "# R example\nprint('Hello, R!')\n",
        "MATLAB": "% MATLAB example\ndisp('Hello, MATLAB!')\n",
        "Julia": "# Julia example\nprintln(\"Hello, Julia!\")\n",
        "Lua": "-- Lua example\nprint('Hello, Lua!')\n",
        "Dart": "// Dart example\nvoid main() { print('Hello, Dart!'); }\n",
        "Scala": "// Scala example\nobject Main extends App { println(\"Hello, Scala!\") }\n",
        "Haskell": "-- Haskell example\nmain = putStrLn \"Hello, Haskell!\"\n",
        "Perl": "# Perl example\nprint \"Hello, Perl!\\n\";\n",
        "Ruby": "# Ruby example\nputs 'Hello, Ruby!'\n"
    }
    return templates.get(language, f"// {language} example\n")


def create_code_file():
    language = choose_language_dialog()
    if not language:
        return
    name = simpledialog.askstring("File", "Filename:")
    if not name:
        return

    ext = PROGRAMMING_LANGUAGES.get(language, {}).get("extension", "")
    if ext and ext != "Dockerfile" and not name.lower().endswith(ext):
        name = f"{name}{ext}"
    if language == "Dockerfile" and name.lower() != "dockerfile":
        name = "Dockerfile"

    CODE_FILES.append({
        "name": name,
        "language": language,
        "code": get_default_code_template(language),
        "created": str(datetime.datetime.now())
    })
    messagebox.showinfo("Created", f"{name}")

def open_code_editor():
    if not CODE_FILES:
        messagebox.showinfo("Info", "No files")
        return
    file_entries = [f"{i + 1}. {item['name']} ({item['language']})" for i, item in enumerate(CODE_FILES)]
    choice = simpledialog.askinteger("Open File", f"Files:\n{'\n'.join(file_entries)}\n\nEnter file number:")
    if choice is None or choice < 1 or choice > len(CODE_FILES):
        return
    file_item = CODE_FILES[choice - 1]
    editor = tk.Toplevel()
    editor.title(f"Editing {file_item['name']}")
    editor.geometry("760x520")
    header = tk.Label(editor, text=f"{file_item['name']} [{file_item['language']}]", bg="#111827", fg="#d4d4d4", font=("Consolas", 10, "bold"))
    header.pack(fill="x")
    text = tk.Text(editor, bg="#1e1e1e", fg="#d4d4d4", insertbackground="white")
    text.pack(fill="both", expand=True)
    text.insert("1.0", file_item["code"])
    def save():
        file_item["code"] = text.get("1.0", tk.END).rstrip()
        messagebox.showinfo("Saved", f"{file_item['name']} saved")
    tk.Button(editor, text="Save", command=save).pack(pady=4)

def list_code_files():
    if not CODE_FILES:
        messagebox.showinfo("Files", "No files")
        return
    result = "\n".join([f"{item['name']} ({item['language']})" for item in CODE_FILES])
    messagebox.showinfo("Code Files", result)

def open_language_website():
    language = choose_language_dialog()
    if not language:
        return
    info = PROGRAMMING_LANGUAGES.get(language)
    if info:
        webbrowser.open(info.get("docs") or info.get("editor_url") or info.get("url"))
    else:
        webbrowser.open("https://code.visualstudio.com/docs/languages/overview")


def open_language_compiler():
    language = choose_language_dialog()
    if not language:
        return
    info = PROGRAMMING_LANGUAGES.get(language)
    if info:
        webbrowser.open(info.get("url") or info.get("editor_url") or info.get("docs"))
    else:
        webbrowser.open("https://www.programiz.com/online-compiler/")


def draw_code_studio():
    draw_window("Code Studio", "#9b59b6")
    register_click("create", -500, 280, 170, 40, create_code_file)
    draw_rect(-500, 280, 170, 40, "#111827", "#2ecc71")
    draw_text("📄 New File", -475, 255, "white", 9)
    register_click("open", -300, 280, 170, 40, open_code_editor)
    draw_rect(-300, 280, 170, 40, "#111827", "#3498db")
    draw_text("✏ Open File", -275, 255, "white", 9)
    register_click("list", -100, 280, 170, 40, list_code_files)
    draw_rect(-100, 280, 170, 40, "#111827", "#f39c12")
    draw_text("📋 List Files", -75, 255, "white", 9)
    register_click("web", 100, 280, 170, 40, open_language_website)
    draw_rect(100, 280, 170, 40, "#111827", "#4CAF50")
    draw_text("🌐 Language Docs", 140, 255, "white", 9)
    register_click("compiler", 300, 280, 170, 40, open_language_compiler)
    draw_rect(300, 280, 170, 40, "#111827", "#9b59b6")
    draw_text("🛠️ Online Compiler", 350, 255, "white", 9)
    draw_text(f"Files: {len(CODE_FILES)}", -500, 200, "#2ecc71", 10)

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
    elif CURRENT_APP == "animation":
        draw_animation()
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
    elif CURRENT_APP == "weather":
        draw_weather()
    elif CURRENT_APP == "contacts":
        draw_contacts()
    elif CURRENT_APP == "tasks":
        draw_tasks()
    elif CURRENT_APP == "word":
        draw_word()
    
    screen.update()

def click(x, y):
    for item in CLICKS.values():
        if item["x1"] <= x <= item["x2"] and item["y2"] <= y <= item["y1"]:
            item["cb"]()
            return

screen.onscreenclick(click)

def boot():
    clear_all()
    draw_rect(-700, 425, 1400, 850, "black")
    draw_text("NeilOS Ultimate Security", -60, 40, "#00ffee", 32, "bold")
    stages = ["Loading Kernel...", "Loading Security Modules...", "Loading All Apps...", "Ready!"]
    y = -40
    for stage in stages:
        draw_text(stage, -180, y, "#00ff88", 12)
        screen.update()
        time.sleep(0.5)
        y -= 35

if __name__ == "__main__":
    boot()
    CURRENT_APP = "desktop"
    render()
    screen.listen()
    turtle.done()
