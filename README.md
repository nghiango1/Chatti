# ChattingChit
A in-memory only back-end chating app with UI

## Sample user:

|User|username/password|Role|
|---|---|---|
|Admin | admin/1|admin|
|User01 | user01/1||
|User02 | user02/1||

## Route
- `/` : Main chat menu
- `/auth/login` : Loging
- `/auth/register` : Create new user

## Api
- `/api/iam` : Return user infomation (name and roles) 
- `/api/user` : Get all user 
- `/api/room` : Get all room and it's message
- `/api/createroom` : Create new room and return it's id

## Using
- _Backend_: python, flask (socketio, template, authenticate decoration)
- _Frontend_: html (flask tenplate), js (for socket), tailwindcss

To generate my `requirement.txt`, I used pip freeze > requirements.txt

## How to use
### Prod
Install Requirement
```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Start server, after activating `(venv)` venv
```sh
source venv/bin/activate
pnpm start
```

### Dev 
**Tailwind watch mode**
`pnpm isn't nessesary, you can use `npm` or `yarn`. This is required just to install tailwindcss
The tailwindcss need to be in watch mode so you can have the css file auto generate automaticaly on every change

> The `static` route handle in `flask_app.py` is writen so that every request will using fresh css file that generated from tailwindcli

```sh
pnpm css-watch
```
**Start debug server**
You will want to use second session to start the server
```sh
source venv/bin/activate
pnpm dev
```
