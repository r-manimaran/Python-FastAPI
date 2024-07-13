# Todo App with FastAPI and Postgresql

### Create the Albemic migration for the Models
```bash
    # Initialize the alembic migration environment
    > alembic init "alembic_todoapp"
    # Create the initial revision and auto-generate the models to table
    > alembic revision -m "Initial_TableCreation" --autogenerate
    # Apply the revision to the Postgresql database
    > alembic upgrade head
```

