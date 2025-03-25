# Backend Service

Here you find all the important development information about the backend service.

## Dependencies

- [fastapi](https://fastapi.tiangolo.com/)
- [psycopg](https://www.psycopg.org/psycopg3/docs/)
- [sqlmodel](https://sqlmodel.tiangolo.com/)

Development:
- [pytest]()
- [scarlett]()
- [ruff]()

## Development

### Backend Setup

1. Install [uv](https://docs.astral.sh/uv/):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. Install python version 3.13:
   ```bash
   uv python install 3.13
   ```
3. Run the backend:
   ```bash
   uv run fastapi dev
   ```


## Testing

