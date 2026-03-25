#!/bin/bash
set -e

# Run migrations
echo "🚀 Running Redis OM migrations..."
python migrate.py || echo "⚠️ Migration notice: Migrations failed but continuing..."

# Start the application
echo "📡 Starting FastAPI application..."
exec "$@"
