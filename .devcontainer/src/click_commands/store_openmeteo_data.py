import logging
import pprint
from datetime import date

import click
import openmeteo_requests
import pandas as pd
import psycopg2
import requests_cache
from retry_requests import retry


def correct_datetime_format(ctx, param, value):
    print(value)
    value = value.strftime("%Y-%m-%d")


@click.command()
@click.option("-lat", "--latitude", type=click.FLOAT, default=53.1412)
@click.option("-lon", "--longitude", type=click.FLOAT, default=8.2147)
@click.option(
    "-sd",
    "--start-date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    required=True,
    help="Use format YYYY-MM-DD"
)
@click.option(
    "-ed",
    "--end-date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=date.today().strftime("%Y-%m-%d"),
)
@click.option(
    "--hourly-params",
    multiple=True,
    default=[
        "temperature_2m",
        "relative_humidity_2m",
        "rain",
        "weather_code",
        "surface_pressure",
        "wind_speed_10m",
    ],
    help="List of Weather Parameters for hourly data",
    # callback=lambda ctx, param, value: list(value)
)
@click.option(
    "-wm",
    "--weather-model",
    default="dwd-icon",
    help="For all possible Weather Models: https://open-meteo.com/en/docs/",
)
@click.option("--host", default="localhost", type=click.STRING, help="Following options for database connection")
@click.option("--port", default=5432, type=click.INT)
@click.option("--user", default="sikwel", type=click.STRING)
@click.option("--password", default="secret#s1kw3lPW", type=click.STRING)
@click.option("--database", default="sikwel_db", type=click.STRING)
@click.option("--drop-table", is_flag=True, default=False, help="First drop all the data specified in --table-name")
@click.option("--table-name", default="openmeteo_data", type=click.STRING, help="Save data to this table in the database")
@click.option(
    "-tz",
    "--timezone",
    type=click.Choice(
        [
            "America/Anchorage",
            "America/Los_Angeles",
            "America/Denver",
            "America/Chicago",
            "America/New_York",
            "America/Sao_Paulo",
            "GMT",
            "Europe/London",
            "Europe/Berlin",
            "Europe/Moscow",
            "Africa/Cairo",
            "Asia/Bangkok",
            "Asia/Singapore",
            "Asia/Tokyo",
            "Australia/Sydney",
            "Pacific/Auckland",
            "auto",
        ],
    ),
    default="GMT",
    show_default=True,
)
def store_openmeteo_data(
    latitude,
    longitude,
    start_date,
    end_date,
    timezone,
    hourly_params,
    host, port, user, password, database, drop_table, table_name,
    weather_model,
):
    logger = logging.getLogger("SampleLogger")

    # Log all current Options, pretty print used for better command line output
    ctx = click.get_current_context()
    logger.info("Options used:\n"+pprint.pformat(ctx.params))

    # Default behaviour from openmeteo website
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Openmeteo uses "YYYY-MM-DD" format without time format
    start_date = start_date.date()
    end_date = end_date.date()

    url = f"https://api.open-meteo.com/v1/{weather_model}"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": hourly_params,
        "timezone": timezone,
        "start_date": start_date,
        "end_date": end_date,
    }
    try:
        logger.info(f"Fetching data from {url}")
        responses = openmeteo.weather_api(url, params=params)
    except Exception:
        logger.exception(
            "Error occured while requesting from openmeteo API:", exc_info=True
        )

    # List for multiple weather models and locations
    response = responses[0]

    # Create DataFrame with Timestamp and weather data
    hourly = response.Hourly()
    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}

    for i, parameter in enumerate(params["hourly"]):
        hourly_data[parameter] = hourly.Variables(i).ValuesAsNumpy()

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    
    # Save to PostgresSQL Database
    logger.info("Saving data to database")
    try:
        with psycopg2.connect(host=host,port=port,user=user,password=password,database=database) as connection:
            with connection.cursor() as cursor:
                
                table_query_columns = ""
                if drop_table:
                    cursor.execute(f"DROP TABLE {table_name}")

                for col_name in params["hourly"]:
                    table_query_columns += f"{col_name} FLOAT,"
                # Remove unnecessary last comma
                table_query_columns = table_query_columns[:-1]

                # Create Query that automatically changes with different weather parameters
                create_table_query = f"""
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        id SERIAL PRIMARY KEY,
                        date TIMESTAMP,
                        {table_query_columns}
                    );
                """
                cursor.execute(create_table_query)
                connection.commit()
                
                query_part_params = ", ".join(params["hourly"])
                query_part_perc_s = ", ".join(["%s"]*len(hourly_dataframe.columns))
                insert_query = f"INSERT INTO {table_name} (date, {query_part_params}) VALUES ({query_part_perc_s})"
                
                for row in hourly_dataframe.values:
                    cursor.execute(insert_query, row)
                connection.commit()
        logger.info("Data successfully stored")
    except (Exception, psycopg2.DatabaseError):
                logger.exception(
            "Error occured during database operation:", exc_info=True
        )

    

