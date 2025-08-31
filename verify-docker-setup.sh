#!/bin/bash

# Docker Setup Verification Script
echo "BeskidScore Server - Docker Setup Verification"
echo "==============================================="

# Check if Docker and Docker Compose are available
echo "1. Checking Docker availability..."
if command -v docker &> /dev/null; then
    docker --version
    echo "✓ Docker is available"
else
    echo "✗ Docker is not available"
    exit 1
fi

echo
echo "2. Checking Docker Compose availability..."
if docker compose version &> /dev/null; then
    docker compose version
    echo "✓ Docker Compose is available"
else
    echo "✗ Docker Compose is not available"
    exit 1
fi

echo
echo "3. Validating docker-compose.yml configuration..."
if docker compose config &> /dev/null; then
    echo "✓ docker-compose.yml configuration is valid"
else
    echo "✗ docker-compose.yml configuration has errors"
    exit 1
fi

echo
echo "4. Checking required files..."
files=("Dockerfile" "docker-compose.yml" "docker-entrypoint-web.sh" "docker-entrypoint-cron.sh" "requirements.txt" ".env.example")

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file exists"
    else
        echo "✗ $file is missing"
        exit 1
    fi
done

echo
echo "5. Checking entrypoint script permissions..."
if [ -x "docker-entrypoint-web.sh" ]; then
    echo "✓ docker-entrypoint-web.sh is executable"
else
    echo "✗ docker-entrypoint-web.sh is not executable"
fi

if [ -x "docker-entrypoint-cron.sh" ]; then
    echo "✓ docker-entrypoint-cron.sh is executable"
else
    echo "✗ docker-entrypoint-cron.sh is not executable"
fi

echo
echo "6. Testing Django configuration..."
if python3 manage.py check --deploy --settings=beskidscore.settings &> /dev/null; then
    echo "✓ Django configuration is valid"
else
    echo "⚠ Django configuration has warnings (expected without database)"
    python3 manage.py check --settings=beskidscore.settings 2>&1 | head -5
fi

echo
echo "7. Testing cron job configuration..."
if python3 manage.py help runcrons &> /dev/null; then
    echo "✓ Django cron jobs are configured"
else
    echo "✗ Django cron jobs are not configured"
fi

echo
echo "==============================================="
echo "Docker Setup Verification Complete!"
echo
echo "To start the application:"
echo "  docker compose up -d"
echo
echo "To view logs:"
echo "  docker compose logs -f web"
echo "  docker compose logs -f cron"
echo
echo "To stop the application:"
echo "  docker compose down"
echo
echo "For more information, see README.md"