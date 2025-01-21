# Network Coverage API

Network Coverage API is designed to retrieve and manage 2G/3G/4G network coverage data. The API is built using Django 5.1.5, Django REST Framework (DRF), and PostgreSQL 17.2, offering a robust backend solution for network coverage information.

## Features
- Exposes API endpoints for retrieving network coverage data.
- Built on a partial hexagonal architecture with a clear separation of concerns.
- Dockerized for easy deployment and setup.
- Swagger documentation available at the root path.

## Requirements
- **Python**: 3.12
- **PostgreSQL**: 17.2
- **Docker**: Tested on Intel-based processors.

## Installation and Setup
### Docker Deployment
1. Copy the Docker environment file:
   ```sh
   cp .env_docker .env
   ```
2. Build and start the containers:
   ```sh
   docker-compose build
   docker-compose up -d
   ```

### Local Development
1. Copy the development environment file:
   ```sh
   cp .env_dev .env
   ```
2. Build and start the containers:
   ```sh
   docker-compose build
   docker-compose up -d
   ```

## API Documentation
The root path of the API redirects to the Swagger UI, which provides interactive documentation for all available endpoints:
- Swagger Path: [http://localhost:8000/api/schema/swagger-ui](http://localhost:8000/api/schema/swagger-ui) (assuming default configuration).

## Project Architecture
The project follows a solid architectural approach with a focus on separation of responsibilities:

### Apps
1. **`network_coverage`**
    - Core application that exposes API endpoints and contains:
        - Models
        - Serializers
        - Main business logic (use cases)

2. **`address_lookup`**
    - Responsible for retrieving address information from external sources.
    - Contains services used by the `network_coverage` app's use cases.

### Design Patterns
- **Use Cases**: Encapsulate the main business logic.
- **Separation of Concerns**: Partial hexagonal architecture (frontend-facing only).
- **Dockerization**:
    - Dockerfile builds the Django project.
    - `scripts/init.sh` creates a superuser.
    - `docker-compose.yml` serves Django and PostgreSQL.

## Notes
- Tested on an Intel processor. Docker containers might not work on other architectures without adjustments.

## Future Enhancements / TODOs
1. **Tests**:
   - Since there are 2 endpoints, testing wouldn't be a huge deal, using pytest-django or DRF's APiTestCaseUse.

2. **Dynamic Operator Names**:
   - Use a web scraper or external API to dynamically map Operator IDs to proper names (currently hardcoded in a dictionary).

3. **Periodic Data Updates**:
    - Implement a batch job to retrieve data from providers such as [Adresse Data Gouv](https://adresse.data.gouv.fr/outils) to keep the database up to date.

4. **Data Cleaning**:
    - Introduce pre-storage validation, e.g., ensuring no duplicate coordinate pairs.

5. **Code Quality**:
    - Add linters and type checkers like `mypy` for better code quality and maintainability.

6. **Geographical Library**:
    - Replace `geopy` with a more Django-PostgreSQL-friendly geographical library, such as **PostGIS**, and store geolocation points in the database alongside the coordinates.

7. **Admin panel setup**:
   - Set up admin panel to manage records from there.
   
8. **Auth**:
   - If necessary, add a Bearer token to make the API access safer and controlled.


