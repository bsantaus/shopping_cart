# Shopping Cart API

This repository contains an API which provides a relatively simple shopping cart interface.
The project is based on [FastAPI](https://fastapi.tiangolo.com/) and uses [SQLModel](https://sqlmodel.tiangolo.com/) to interface with a PostgreSQL database.
Instrumentation for Prometheus metrics scraping is also implemented using the [Prometheus-FastAPI-Instrumentator](https://pypi.org/project/prometheus-fastapi-instrumentator)

The route structure is defined in the `openapi.yaml` file in the root directory and can also be viewed in the Swagger API documentation page provided through FastAPI.

The skeleton for the API and models was generated using the [FastAPI-Code-Generator](https://pypi.org/project/fastapi-code-generator/) package, which has dependency conflicts with the rest of the requirements and is therefore commented out in `requirements.txt`

In total, it took approximately 6.5 hours to complete the code present in this repository.

## Setup

After creating a Python environment of your choice (the application was built in a [Miniforge3](https://github.com/conda-forge/miniforge) environment on Python 3.10), you can run `make install` to install all necessary Python dependencies.

The application also relies on a working Docker Container Engine installation that includes the Docker Compose plugin. 

Alternative instructions for running the API locally are also available in the later section.

## Running the Application

### Docker Compose

If your environment has a working Docker Compose setup, you may run `make start` to run both the database and API components of the application.
The API will then be available at [http://localhost:8000](http://localhost:8000) for you to use as you like.

If you would like to browse the Swagger documentation for the Shopping Cart API, you can do so at [http://localhost:8000/docs](http://localhost:8000/docs).

The database runs on `localhost:5432` and credentials for it are viewable in the `.env.compose` file if you would like to view the database through a browser like [DBeaver](https://dbeaver.io/).

### Running the API Directly

The API and database can also be run separately.
To run the database as a standalone, you can use `make start-db`, and remove it with `make kill-db`.
When the database is running, you can use `make start-local-api` to run the API as a process directly.

The URLs and ports for both services are the same as in the Docker Compose setup.

## Testing

To run the unit tests for the application, you can use `make test`.
Note that running `make test` will attempt to start the Postgres database, so before running the tests you should run `make kill-db` if you have a standalone database running or `make kill` if you have a Docker Compose version of the application running.

## Repository Structure

The Shopping Cart API repository is divided into a few helpful folders for code clarity.
Descriptions of each are present here:

- `config`: Contains the Settings for the application using `pydantic-settings`. Variables from the `.env` file are loaded into the `Settings` object here, and provided to the rest of the application through the exported `settings` instance of that object.
- `routers`: Contains implementations of the routes provided through the application, except for the Healthcheck and Metrics routes (implemented in `main.py`). Provides a `cart_router` and an `item_router` which offer the routes in the `/cart` and `/item` families, respectively.
- `services`: Contains both the singleton database interface (exported to the application as `sc_database`) and custom metrics for Prometheus. The implementations of the metrics are present in `services/metrics.py` and are provided to the application through the `custom_metrics` list.
- `tests`: Contains the unit tests for the application. Tests for creating and deleting Carts are present in `test_cart_cd.py`, those that test the create/retrieve/update/delete routes for Items are in `test_item_crud.py`, and those that test adding and removing Items from Carts are present in `test_items_in_cart.py`. Tests are written and run using [pytest](https://docs.pytest.org/en/8.2.x/)
