# Addd a mgiration
alembic revision --rev-id 004 --autogenerate -m "Add new 211 fields."
alembic revision --autogenerate -m "Add Form211 table"
alembic upgrade head

# To make changes and deploy manually
docker login
docker build -t wagoneerguy/fsar211-backend:latest .
docker push wagoneerguy/fsar211-backend:latest

# If not just code change
docker stop fsar211-postgres 2>/dev/null || true
docker rm fsar211-postgres 2>/dev/null || true
docker run -d --name fsar211-postgres \
  --network fsar211-network \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=fsar211 \
  -v /var/lib/postgresql/data:/var/lib/postgresql/data \
  postgres:15

# If just a code change.
# Pull and run the backend container
docker pull wagoneerguy/fsar211-backend:latest

# Stop and remove existing container if it exists
docker stop fsar211-backend 2>/dev/null || true
docker rm fsar211-backend 2>/dev/null || true

# Run new container with environment variables
docker run -d --name fsar211-backend \
  --network fsar211-network \
  -p 8000:8000 \
  --env-file /tmp/backend.env \
  wagoneerguy/fsar211-backend:latest

docker exec -it fsar211-backend bash -c "cd /app && alembic upgrade head"

## What Github needs to run to auto update the server on merge.
# Rebuild and push the latest
docker login
docker build -t wagoneerguy/fsar211-backend:latest .
docker push wagoneerguy/fsar211-backend:latest

# Login to the production server
This is just a test. 
# Pull the latest version of the image
docker pull wagoneerguy/fsar211-backend:latest

# Restart the database
docker stop fsar211-postgres 2>/dev/null || true
docker rm fsar211-postgres 2>/dev/null || true
docker run -d --name fsar211-postgres \
  --network fsar211-network \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=fsar211 \
  -v /var/lib/postgresql/data:/var/lib/postgresql/data \
  postgres:15

# Restart the backend
docker stop fsar211-backend 2>/dev/null || true
docker rm fsar211-backend 2>/dev/null || true

docker run -d --name fsar211-backend \
  --network fsar211-network \
  -p 8000:8000 \
  --env-file /tmp/backend.env \
  wagoneerguy/fsar211-backend:latest

# Run database migrations
docker exec -it fsar211-backend bash -c "cd /app && alembic upgrade head"

# API Docs
http://localhost:8000/redoc