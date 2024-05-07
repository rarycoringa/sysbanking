# Sysbanking

![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/rarycoringa/sysbanking)
![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/rarycoringa/sysbanking/django)
![GitHub Release](https://img.shields.io/github/v/release/rarycoringa/sysbanking)
![GitHub Tag](https://img.shields.io/github/v/tag/rarycoringa/sysbanking)
![GitHub License](https://img.shields.io/github/license/rarycoringa/sysbanking)

***Your Friendly Banking***

## Summary

- [Sysbanking](#sysbanking)
  - [Summary](#summary)
  - [About](#about)
  - [Installation and Configuration](#installation-and-configuration)
    - [Python](#python)
    - [Pipenv](#pipenv)
    - [Database](#database)
  - [Features and Usage](#features-and-usage)
    - [List of accounts](#list-of-accounts)
    - [Creation of an account](#creation-of-an-account)
    - [Details of an account](#details-of-an-account)
    - [Deposit into an account](#deposit-into-an-account)
    - [Withdraw from an account](#withdraw-from-an-account)
    - [Transfer between two accounts](#transfer-between-two-accounts)

## About

## Installation and Configuration

### Python
Before everything, please certify that you already have Python installed in your system.
In our project, we are using the version ```3.11.3```, you can verify the version from you computer by using the command:
```python3 --version```.

If you don't have python installed, please refer to [this link](https://www.python.org/downloads/).


### Pipenv
With python now installed, test the command ```pip --version```, if it doesn't work, please refer to [this link](https://pypi.org/project/pip/) and follow its instructions.

With pip installed, run ```pip install pipenv```.

Now, inside the project folder, run ```pipenv install```, now you have the project enviroment all set up in your computer!

### Running the Server
Considering you followed all the instructions above, to run the server you must open the project folder and run the command ```pipenv shell``` to run your virtual enviroment.

We're almost there! To set up the database, use the command ```python manage.py migrate``` (you only need to run this command once).

Now simply run ```python manage.py runserver``` and open your browser at ```http://127.0.0.1:8000/accounts/```.

Keep in mind that you can only run ```python manage.py runserver``` if you're inside the virtual enviroment.

## Features and Usage

### List of accounts

### Creation of an account

### Details of an account

### Deposit into an account

### Withdraw from an account

### Transfer between two accounts