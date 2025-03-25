
Create Virtual Environment

Create docker-compose file for Postgres

Create Database 
```bash
set PGPASSWORD=postgres
createdb -U postgres -h localhost -p 5432 todo-fastapi
```

![alt text](image.png)

alembic init alembic

alembic revision -m "create todos table"

alembic upgrade head

![alt text](image-1.png)


![alt text](image-2.png)

![alt text](image-3.png)