#! /bin/bash
# Save the weather data from yesterday in the database
date_yesterday=$(date -d "yesterday" "+%Y-%m-%d")
/usr/local/bin/python /app/src/__main__.py store-openmeteo-data --start-date "$date_yesterday" --end-date "$date_yesterday" --host "postgresql"