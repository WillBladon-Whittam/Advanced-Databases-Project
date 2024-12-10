# Advanced-Databases-Project
Advanced Data Structures project for COM519

# Enviroment Setup

Created with Python 3.12.

Clone the master branch of the project:

 > git clone https://github.com/WillBladon-Whittam/Advanced-Databases-Project.git

Go into the Advanced-Databases-Project directory

> cd Advanced-Databases-Project

Create a virtual enviroment:

 > python -m venv .venv

Activate virtual enviroment:

 > .\\.venv\Scripts\activate

Install Dependencies:

 > pip install -r requirements.txt

 Install The Project as a Library:

 > pip install -e .

 Run from main.py

 > python advanced_database_project\main.py

 # Details of execution

 ## Database management
 
 When the steps above have been followed, the application should execute and the Login Page should be displayed.
 There is no need to configure / setup the database as the python application automatically does this.
 If the database does not exists, it is created and the .sql script creates the tables and the data. The script then automatically updates the fields that store images in the database.
 
 ## Reset database

 To reset the database, the database can either be deleted, then the application will automatically create a new one.

 OR

 running python with the argument "-r" or "--reload-db" will reset the database

 > python advanced_database_project\main.py -r

 > python advanced_database_project\main.py --reload-db

 This is handy for debugging when wanting to start with a fresh db per execution.