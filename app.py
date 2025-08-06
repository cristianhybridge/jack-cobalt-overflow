from app import create_app
from sqlalchemy import create_engine, NullPool
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)