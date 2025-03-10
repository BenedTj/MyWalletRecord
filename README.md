# MyWalletRecord (a work in progress)
A budgeting web app for daily personal use. This web app contains the following features:
1. Login and Register system to store your records;
2. Supervisor accounts to track the financial records of a selected user (the supervisee) based on their ID.
3. Two Factor Authentication for Adding Supervisee.
4. Tracking Supervisor's activities when supervising supervisee.

# Tech stack
- Frontend: HTML and Bootstrap 5
- Backend: Django
- Database: SQLite 3

# To try MyWalletRecord
1. Pull from the Github repository
```
git init .
git remote add origin https://github.com/BenedTj/MyWalletRecord.git
git pull origin main
```
2. Navigate to `src/manage.py` and replace the `SECRET_KEY` in code with one of your choosing
```python
# from dotenv import load_dotenv has become obsolete

# load_dotenv() should be deleted
SECRET_KEY = # A secret key of your choosing
```
3. Navigate to the directory where `.git` is located, ensure Python is installed on your local computer and install dependencies with pip
```
pip install -r requirements.txt
```
4. Run Web App on local machine
```
python manage.py runserver
```
5. Open `http://127.0.0.1:8000/register/` on browser of choice.
6. Hit `Ctrl+C` on command line to terminate the running of the Web App

# Future plans of features to be built
1. Enhance User Interface
2. Converting a normal user account to a supervisor account
3. Profile and settings pages for each user
4. Graphing financial records
5. Telegram Chatbot to input records more conveniently

# Dependencies
Dependencies this project relies on that are not included as built-in Python packages are Django and Bootstrap 5. For further information, **requirements.txt** can be consulted.
