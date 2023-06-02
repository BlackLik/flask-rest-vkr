import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()

db_host = os.getenv("POSTGRESQL_HOST")
db_port = int(os.getenv("POSTGRESQL_PORT"))
db_name = os.getenv("POSTGRESQL_DB")
db_user = os.getenv("POSTGRESQL_USER")
db_password = os.getenv("POSTGRESQL_PASSWORD")
debug = True if os.getenv("DEBUG") == "1" else False
flask_host = os.getenv("FLASK_RUN_HOST")

db_url_connection = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
