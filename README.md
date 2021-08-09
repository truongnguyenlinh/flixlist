# FlixList
A Web application which implements CRUD operations and PE tools/infrastructure

### Installation
1. Install `pip` and `python3.8` or greater
2. Create virtual environment 
    ```bash
    $ python3 -m venv python3-virtualenv
    ```
3. Activate virtual environment
    ```bash
    $ source python3-virtualenv/bin/activate
    ```
4. Install dependencies
    ```bash
    $ pip3 install -r requirements.txt
    ```

### Usage
Below are instructions to run the application, and obtaining the database schema locally:

1. Running a Flask development server
    ```bash
    $ FLASK_DEBUG=1 python wsgi.py run
    ```

2. Running docker-compose
    ```bash
    $ docker-compose up --build -d
    ```

3. Obtain and inspect database:
    ```bash 
    $ docker-compose exec web python wsgi.py create_db
    $ docker-compose exec db psql --username=admin --dbname=flixlist
    ```
    ```postgres
    flixlist=# \dt
    ```
