from database import create_db_and_tables
from models import User, Plan


def main():
    create_db_and_tables()
    print("Database tables created!")


if __name__ == "__main__":
    main()
