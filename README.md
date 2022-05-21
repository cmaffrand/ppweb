# ppweb

A Python prode webpage for Qatar WorldCup 2022

## Description

## Dependencies

The webpage is developed using flask over python. 

[Flask](https://flask.palletsprojects.com/en/2.1.x/)
[bootstrap](https://getbootstrap.com/docs/4.1/getting-started/introduction/)
[uiGradients](https://uigradients.com)
[Heroku](https://dashboard.heroku.com/apps)
[Heroku Cli](https://devcenter.heroku.com/articles/heroku-cli)
[gunivorn](https://gunicorn.org)
[Werkzeug](https://werkzeug.palletsprojects.com/en/2.1.x/installation/)
[Flask-login](https://flask-login.readthedocs.io/en/latest/#installation)
[Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#installation)

## Docker

Open shell and type this code into the command line.
IMPORTANT: Docker commands should be runed as a sudo.
First create docker container by doing:

```
cd src
docker build -t ppweb:latest .
```

Then run the container:

```
docker-compose up -d
```

You can view the webpage in your URL bar:

http://localhost:8000

## Version History

* 0.1
    * Initial Release

## Roadmap

- [ ] First webpage version

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
