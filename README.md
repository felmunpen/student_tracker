# Student Tracker

A simple web application that displays the grades of a group of students in the mathematics subject.

The grades are separated by subject blocks and displayed in graphs.

In this application, you take on the role of a teacher and, instead of having to navigate through tables, you directly ask a chatbot for the data you're looking for.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Author](#author)
- [Technologies Used](#technologies-used)

## Installation

Follow these steps to install and run the project:

```bash
git clone https://github.com/felmunpen/student_tracker.git
cd student_tracker
```

I recommend to use a virtual environment.

```bash
python -m venv venv
source venv/bin/activate  #Linux/macOS
venv\Scripts\activate     #Windows
```

Install dependencies.

```bash
pip install -r requirements.txt
```

## Usage

Execute the server (if you are using this project locally):

```bash
pip install -r requirements.txt
```

You can access to the documentation through your browser:

- http://127.0.0.1:8000/docs 

> ⚠️ **Note:** When running the project locally, the IP address and port may vary depending on each user's configuration. Make sure to check your terminal output or server logs to confirm the correct address (e.g., `http://127.0.0.1:8000` or `http://localhost:3000`).

In order to use the chatbot, you must have an active OpenAI API Key. Use it in the main.py file or in your .env (or env) file through the OPENAI_API_KEY variable.
## Authors

- Felipe Muñiz - [@felmunpen](https://github.com/felmunpen/)
## Technologies Used

- FastAPI
- OpenAI API
