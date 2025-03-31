# Backend Service

Here you find all the important development information about the backend service.

## Dependencies

- [fastapi](https://fastapi.tiangolo.com/)
- [psycopg](https://www.psycopg.org/psycopg3/docs/)
- [sqlmodel](https://sqlmodel.tiangolo.com/)

Development:
- [pytest](https://docs.pytest.org/en/stable/)
- [scarlett](https://www.starlette.io/)
- [ruff](https://docs.astral.sh/ruff/)

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

## Linting
Use the following command to reformat the files:
```bash
uv run ruff format app/
```

Use the following command to show the lint results:
```bash
uv run ruff check app/
```

Use the following command to fix fixable mistakes:
```bash
uv run ruff check app/ --fix
```

## Testing
Here is a link to a fastapi tutorial [link](https://fastapi.tiangolo.com/how-to/testing-database/)
Here is a link to the pytest documentation [link](https://docs.pytest.org/en/stable/)

Use the following command to run the tests:
```bash
uv run pytest
```
