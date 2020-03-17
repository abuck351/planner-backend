# planner-backend

## Getting Started

- Navigate into `planner-backend` from the command line
- To install dependencies, type `pipenv shell` and then `pipenv install`
  - You will have to install `pipenv` using `pip`, if it isn't already
- Before running, create a file called `.env` for environment variables:

```
DB_URI=sqlite:///data.db
PLANNER_SECRET_KEY=xxx
```

- To run the app, type `python3 app.py`
