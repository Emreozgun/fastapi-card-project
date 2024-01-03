# Case Study (Card System)

## NOTES
- Some TODOS not completed. But I know the problems. I can fix them.
- I didnt completed tests part properly and not complete for all modules.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Documentation](#documentation)
- [Usage](#usage)
- [Commands](#commands)

## Introduction

The user registers in the system. The system automatically creates a card for the user. 
When the user logs into the system, the automatically created card is 
updated with status='ACTIVE'. 
The user can perform operations such as creating, 
deleting, updating, and listing cards using the API. 
The user can also perform transactions with specific cards.

## Features

- There are some modules and these modules includes some endpoints within the API.
  - auth/
    - register
    - login
  - card/
    - create
    - update
    - delete
    - find
  - transaction/
    - create
    - stats
    - details
- All enpoints for card and transaction covered with authentication jwt token. 
Firstly register and use that token for all operations. 

## Documentation

- You can view the Swagger documentation using the link 'http://localhost:8000/doc'.
- You can try all endpoints on Swagger documentation
  - Firstly register with email and password.
  - Then authorize that user from right side of screen. Enter the email address(as a username) and password you used to register.
  - Then try other enpoints.
  
## Usage
- The necessary configuration information is in the .env.sample file. 
You need to create the **".env"** file and copy the data inside the sample.
- Before starting the service, run the command "**pip install -r requirements.txt**" or **"pip3 install -r requirements.txt"**.
- To start the service, use the **uvicorn --reload app.main:app"** or **sh run.sh"** or **bash run.sh"**.

## Commands

Run pwd command to be sure correct path
```bash
pwd
```

Firstly, Install packages: 

```bash
pip3 install -r requirements.txt
```

To run service

```bash
uvicorn --reload app.main:app
```

To run test code(It is not completed. It will not working properly):

```bash
pytest -s
```