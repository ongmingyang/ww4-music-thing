ww4-music-thing
===============

Crappy music server running in senior house ww4

Dependencies
----------

1. Flask
2. Flask-login
3. cmus

How to
----------

1. git pull
2. touch queue
3. touch config
4. write configuration parameters, see section below
5. python web.py

Configuration parameters
-------------

```
[secretvars]
key: (your secret key)

[pathvars]
uploads: (your uploads folder)

[shadow]
username: password
username2: password2
```
