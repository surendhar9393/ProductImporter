#!/bin/bash
set -e
cmd="$@"

# Copy angular build based on evnironment
# echo "Removing all files in website/static/myfleets/"
# rm -f website/static/myfleets/*.*

# echo "copying angular files from $DEST_PATH"
# cp -f website_product/"$DEST_PATH"/*.* website/static/myfleets/
# rm -f website/static/myfleets/*.html

# This entrypoint is used to play nicely with the current cookiecutter configuration.
# Since docker-compose relies heavily on environment variables itself for configuration, we'd have to define multiple
# environment variables just to support cookiecutter out of the box. That makes no sense, so this little entrypoint
# does all this for us.

# the official postgres image uses 'postgres' as default user if not set explicitly.
if [ -z "$POSTGRES_USER" ]; then
    export POSTGRES_USER=postgres
fi

# using postgres as default host (in dev env) if not set explicitly.
if [ -z "$POSTGRES_HOST" ]; then
    export POSTGRES_HOST=postgres
fi

export DATABASE_URL=postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:5432/$POSTGRES_DB


function postgres_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="$POSTGRES_DB", user="$POSTGRES_USER", password="$POSTGRES_PASSWORD", host="$POSTGRES_HOST")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing..."
exec $cmd
