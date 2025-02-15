#!/bin/bash

if [ -f .env ]; then
  export $(cat .env | xargs)
fi

psql -d $POSTGRES_DB -c "TRUNCATE TABLE $TABLE_NAME;"

psql -d $POSTGRES_DB -c "\copy $TABLE_NAME FROM '$CSV_FILE' DELIMITER ',' CSV HEADER;"
