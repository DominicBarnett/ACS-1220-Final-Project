# Homework 4: Grocery Store Site Part 2
## Purpose (Why should I do this?)
This project will allow you to practice adding authentication & authorization to an existing website using the Flask-Login library. After this assignment, you should be able to integrate sign-up & login functionality into your Flask projects!

If you have trouble with this assignment, I would highly recommend completing the SQLAlchemy Auth Lab (Books) which will guide you through step-by-step in adding login & sign-up to an existing website.

## Setup

Clone this repository to your computer. 

**Take a look at the code** - it looks a bit different than what you're used to. Namely, the code is now separated out into several files rather than being written in a single `app.py` file. Since we're now writing model and form code as well as route code, this will help us to maintain some structure and separation.

**To run the code**, navigate to the project folder and run the following to create a virtual environment and install the required packages:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then rename the `.env.example` file as `.env`:

```
cp .env.example .env
```

Then you can run the server:

```
python app.py
```
