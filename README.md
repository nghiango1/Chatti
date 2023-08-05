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
