# mail_relay

## Getting started

* Clone repo
* Set env variables (TODO: Add description on all variables)
* Run `docker compose up`


### Project Structure Explanation:

- **project_root/**: This is the root directory of the entire project.
  - **backend/**: Contains all the backend related code.
    - **app/**: The main backend application directory.
      - **api/**: Contains the API routes or endpoints.
        - **aliases.py**: Endpoints related to aliases.
        - **users.py**: Endpoints related to users.
      - **core/**: Core components.
        - **config.py**: General configuration for the application.
        - **database.py**: Database configurations and initializations.
        - **security.py**: Security configurations, including hashing and token operations.
      - **crud/**: CRUD (Create, Read, Update, Delete) operations.
        - **crud_aliases.py**: CRUD operations for aliases.
        - **crud_users.py**: CRUD operations for users.
      - **models/**: ORM (Object Relational Mapping) models.
        - **aliases.py**: ORM model for aliases.
        - **users.py**: ORM model for users.
        - **webauth_keys.py**: ORM model for web authentication keys.
      - **tests/**: Contains all the tests for the application.
        - **test_aliases.py**: Tests for alias endpoints.
        - **test_users.py**: Tests for user endpoints.
      - **main.py**: The main entry point for the application.
  - **frontend/**: Contains all frontend related files and directories
  - **db-init-scripts/**: Contains scripts that are executed during the initialization of the database container.
  - **.env**: Environment variables of the project.
  - **docker-compose.yml**: Configuration for Docker Compose. Used to define and run multi-container Docker applications.