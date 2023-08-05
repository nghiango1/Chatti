# ChattingChit
A in-memory only back-end chating app with simple UI

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

## Using
- _Backend_: python, flask (socketio, template, authenticate decoration)
- _Frontend_: html (flask tenplate), js (for socket), tailwindcss

To generate my `requirement.txt`, I used pip freeze > requirements.txt

## How to use
Install Requirement
```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Start server, after activating `(venv)` venv (Already hardcode config as `debug` mode)
```sh
python src/main.py
```

### Dev 
`pnpm isn't nessesary, you can use `npm` or `yarn`. This is required just to install tailwindcss
The tailwindcss need to be in watch mode so you can have the css file auto generate automaticaly on every change

> The `static` route handle in `main.py` is writen so that every request will using fresh css file that generated from tailwindcli

```sh
pnpm css-watch
```

Then open our `main.py`

```sh
python main.py
```
