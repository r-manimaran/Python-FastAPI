
### Create the Alembic environment
```bash
# initialize the Alembic Migration
> alembic init name
# create the initial revision wwith a meaningfull migration message
> alembic revision -m "Initial_create_emp_table"

# Apply the migration to the database
> alembic upgrade head

# shows the history of migration
> alembic history

# Check the current revision of the migration applied in the database
> alembic current

# Downgrade one revision from the current revision with relative downgrade
> alembic downgrade -1

# check the revision details now
> alembic current

# Apply again the migration, up one level
> alembic upgrade +1

# completely revert to the base migration
# caution: this will remove all the tables from your db
> alembic downgrade base

# Apply all the revisions
> alembic upgrade head
# To Autogenerate the revisions with upgrade and downgrade details of our model
> alembic revision -m "Initial_Create_emp_table" --autogenerate

# Now apply the revision to the database
> alembic upgrade head
```

### To view the script
To view the DB script that is generating by Alembic during the migration, set the below in the alembic.ini file, below sqlalchemy db details
```ini
#generate the SQL
sqlalchemy.echo = True
```

### Created Initial Migration DB view
![alt text](image.png)

### Added Departments table and Reference
![alt text](image-1.png)