from database import create_db_and_tables
from service.app.models import plan, user


def main() -> None:
    create_db_and_tables()
    print("Database tables created!")


if __name__ == "__main__":
    main()
