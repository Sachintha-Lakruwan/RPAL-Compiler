# RPAL Interpreter 🦾

Welcome to the **RPAL Interpreter** project! This repository contains a full implementation of an interpreter for the Right-reference Pedagogic Algorithmic Language (RPAL), built from scratch in Python. Whether you're a student, educator, or language enthusiast, this project is designed to help you explore language processing, parsing, and functional programming concepts in a hands-on way. 🚀

---

## 📋 Table of Contents

- [RPAL Interpreter 🦾](#rpal-interpreter-)
  - [📋 Table of Contents](#-table-of-contents)
  - [Overview](#overview)
  - [Features ✨](#features-)
  - [Project Structure 🗂️](#project-structure-️)
  - [Getting Started 🚦](#getting-started-)
  - [Usage 🛠️](#usage-️)
    - [Using Python](#using-python)
    - [Using Makefile](#using-makefile)
  - [Contributing 🤝](#contributing-)

---

## Overview

RPAL Interpreter is a modular Python application that reads, parses, standardizes, and executes RPAL source code. The project is split into several key components:

- **Lexical Analyzer**: Breaks input into tokens.
- **Parser**: Builds an Abstract Syntax Tree (AST) from tokens.
- **Standardizer**: Converts AST to a simplified Standardized Tree (ST).
- **CSE Machine**: Evaluates the standardized tree and executes the program logic.

No third-party dependencies are required—just plain Python! 🐍[^1]

---

## Features ✨

- **Pure Python**: No external libraries needed.
- **Custom Lexer \& Parser**: Built from scratch for educational clarity.
- **AST \& Standardized Tree Generation**: See your code's structure at every stage.
- **CSE Machine**: Fully interprets RPAL programs, supporting functional constructs.
- **Makefile \& CLI Support**: Easy to run, test, and explore.

---

## Project Structure 🗂️

- `myrpal.py` — Main entry point for the interpreter.
- `lexer.py` — Lexical analysis logic.
- `parser.py` — AST construction.
- `standardizer.py` — AST to ST transformation.
- `cse_machine.py` — Program execution engine.
- `Makefile` — Convenient build and run commands.

---

## Getting Started 🚦

1. **Clone the repository:**

```bash
git clone https://github.com/Sachintha-Lakruwan/RPAL-Compiler.git
cd RPAL-Compiler
```

2. **Prepare your RPAL source file:**
   Write your RPAL code in a file, e.g., `input.txt`.
3. **Run the interpreter:**
   Use either Python directly or the provided Makefile.

---

## Usage 🛠️

### Using Python

```bash
python3 myrpal.py input.txt           # Execute the program
python3 myrpal.py input.txt -tokens   # Print tokens
python3 myrpal.py input.txt -ast      # Print the Abstract Syntax Tree
python3 myrpal.py input.txt -sast     # Print the Standardized AST
python3 myrpal.py input.txt -cs       # Print control structures
```

### Using Makefile

```bash
make run file=input.txt     # Execute the program
make tokens file=input.txt  # Print tokens
make ast file=input.txt     # Print the Abstract Syntax Tree
make sast file=input.txt    # Print the Standardized AST
make cs file=input.txt      # Print control structures
```

_Replace `input.txt` with your own RPAL source file name!_[^1]

---

## Contributing 🤝

Contributions, bug reports, and suggestions are welcome! Please fork the repo and submit a pull request. For major changes, open an issue first to discuss what you would like to change.

---

> _"Happy interpreting! If you find this project helpful or want to learn more about programming languages, give it a ⭐ on GitHub!"_ 📝

---

<!-- Emojis used: 🦾 🚀 📋 ✨ 🗂️ 🚦 🛠️ 🤝 📄 📝 -->

[^1]

<div style="text-align: center">⁂</div>

[^1]: Document-6-3.pdf
[^2]: https://www.hatica.io/blog/best-practices-for-github-readme/
[^3]: https://www.codecademy.com/article/markdown-and-readme-md-files
[^4]: https://markdown-all-in-one.github.io/docs/contributing/emoji.html
[^5]: https://github.com/mhucka/readmine
[^6]: https://dev.to/yuridevat/how-to-create-a-good-readmemd-file-4pa2
[^7]: https://github.com/othneildrew/Best-README-Template
[^8]: https://dev.to/github/10-standout-github-profile-readmes-h2o
[^9]: https://github.com/matiassingers/awesome-readme
[^10]: https://github.com/topics/interpreter
[^11]: https://packaging.python.org/guides/making-a-pypi-friendly-readme/
