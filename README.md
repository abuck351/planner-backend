# planner-backend

## Getting Started

- Navigate into `planner-backend` from the command line
- To install dependencies, type `pipenv shell` and then `pipenv install`
  - You will have to install `pipenv` using `pip3`, if it isn't already
  - Had some issues installing `psycopg2` on a Mac with an M1 chip
    - Followed [this GitHub issue](https://github.com/psycopg/psycopg2/issues/1200)
- Before running, create a file called `.env` for environment variables:

```
DATABASE_URL=sqlite:///data.db
PLANNER_SECRET_KEY=xxx
```

- To run the app, type `python3 app.py`

## Departments

Must run a `POST` request with no body to `/api/depts` in order to populate the database

## API Documentation

[Postman Docs](https://documenter.getpostman.com/view/9613028/TVCmQjqt)
