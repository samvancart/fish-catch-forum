# Setup

## Local setup

To clone the project, use the command line to open the desired directory on your computer.

Then type in the following command. Use git bash to do this on a windows os.

```
$ git@github.com:samvancart/fish-catch-forum.git
``` 
The source code will now be available in the `fish-catch-forum` directory.

## Runnng the app locally

### 1. Requirements

* python3
* sqlite3

The `DATABASE_URL` environment variable needs to be defined for the application to work.

### 2. Python virtual environment

type the following:

```
$ python3 -m venv venv
```
The python virtual environment to which the project dependencies will be installed, is now ready.

To activate on linux type:

```
$ source venv/bin/activate
```
on windows:

```
$ venv/Scripts/activate.bat
```

### 3. Flask

Install pip
```
$ pip install --upgrade pip
```
then 
```
$ pip install Flask
```
to install the Flask library

### 4. Installing dependencies

The project dependencies can be found in the `requirements.txt` file. This file can be found in the project directory.
Type:
```
$ pip install -r requirements.txt
```
### 5. Starting the app 

Go to the root directory and type:
```
$ python3 run.py
```
or

```
$ python run.py
```

The app will be running at [http://localhost:5000](http://localhost:5000)

The app can be viewed at this address using a web browser.

## Running the app with Heroku

For the app to work with Heroku, it is important that the app has been set up locally as described above.
Heroku credentials and the Heroku CLI are also required.
The Heroku CLI can be installed for linux with the following command:

```
$ sudo snap install --classic heroku
```
To download the CLI for windows go to [https://devcenter.heroku.com/articles/heroku-cli](Heroku CLI)

### 1. Log in to Heroku and create a project

```
$ heroku login
```

Go to the root directory of the project and type:
```
$ heroku create <projektin nimi>
```

### 2. Initiate the Heroku project
```
$ git remote add heroku
$ git add .
$ git commit -m "Inital heroku-commit"
$ git push heroku master
```

### 3. Add a PostreSQL database to the project

```
$ heroku config:set HEROKU=1
$ heroku addons:add heroku-postgresql:hobby-dev
```
The app should now be running on Heroku.





