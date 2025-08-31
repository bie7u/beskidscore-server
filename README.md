# BeskidScore Server

A Django REST API server for managing football match data, standings, and cron jobs for automatic updates.

## Features

- Match management with live status updates
- League and season standings calculation
- Automated cron jobs for:
  - Setting matches to live status when their scheduled time arrives
  - Updating standings based on match results
- RESTful API for data access

## Docker Setup

This project includes Docker support with separate containers for the web application, database, and cron jobs.

### Prerequisites

- Docker
- Docker Compose

### Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd beskidscore-server
```

2. Copy the environment file:
```bash
cp .env.example .env
```

3. Start the application:
```bash
docker compose up -d
```

This will start:
- **PostgreSQL database** on port 5432
- **Django web server** on port 8000
- **Cron service** for automated tasks

4. Access the application:
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

### Services

#### Web Service
- Runs Django development server
- Handles HTTP requests
- Automatically applies database migrations
- Collects static files

#### Database Service
- PostgreSQL 15
- Persistent data storage
- Health checks for proper startup ordering

#### Cron Service
- Runs django-cron jobs every minute
- Logs output to `/app/logs/cron.log`
- Handles automated match status updates and standings calculations

### Cron Jobs

The following cron jobs are configured:

1. **SetMatchToLiveCronJob** (runs every minute)
   - Updates match status from 'SCHEDULED' to 'LIVE' when the match time arrives

2. **UpdateStandingsCronJob** (runs every hour)
   - Recalculates league standings based on finished match results

### Environment Variables

Key environment variables (see `.env.example`):

- `DEBUG`: Enable/disable debug mode
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host (use 'db' for Docker)
- `DB_PORT`: Database port

### Development

#### View logs
```bash
# Web service logs
docker compose logs -f web

# Cron service logs
docker compose logs -f cron

# Database logs
docker compose logs -f db
```

#### Run management commands
```bash
# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# Run specific cron jobs
docker compose exec web python manage.py runcrons

# Access Django shell
docker compose exec web python manage.py shell
```

#### Stop services
```bash
docker compose down
```

#### Clean up (removes volumes)
```bash
docker compose down -v
```

### API Endpoints

The API provides endpoints for:
- Leagues: `/api/leagues/`
- Seasons: `/api/seasons/`
- Teams: `/api/teams/`
- Matches: `/api/matches/`
- Standings: `/api/standings/`

### Manual Cron Testing

To manually test cron jobs:

```bash
# Test all cron jobs
docker compose exec web python manage.py runcrons --force

# Test specific cron job
docker compose exec cron python manage.py runcrons --force
```

### Troubleshooting

1. **Database connection issues**: Ensure the database service is healthy before other services start
2. **Permission errors**: Make sure entrypoint scripts are executable
3. **Port conflicts**: Change port mappings in docker-compose.yml if needed
4. **Cron logs**: Check `/app/logs/cron.log` for cron job execution details