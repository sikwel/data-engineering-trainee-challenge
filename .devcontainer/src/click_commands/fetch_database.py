import logging
import pprint

import click
import psycopg2


@click.command()
@click.option("--host", default="localhost", type=click.STRING, help="Following options for database connection")
@click.option("--port", default=5432, type=click.INT)
@click.option("--user", default="sikwel", type=click.STRING)
@click.option("--password", default="secret#s1kw3lPW", type=click.STRING)
@click.option("--database", default="sikwel_db", type=click.STRING)
@click.option("--table-name", default="openmeteo_data", type=click.STRING, help="Save data to this table in the database")
@click.option("--num-entries", default=5, type=click.INT, help="How many entries should be fetched with .fetchmany()?")
def fetch_database(host, port, user, password, database, table_name, num_entries):
    logger = logging.getLogger("SampleLogger")
    # Log all current Options, pretty print used for better command line output
    ctx = click.get_current_context()
    logger.info("Options used:\n"+pprint.pformat(ctx.params))

    try:
        with psycopg2.connect(host=host,port=port,user=user,password=password,database=database) as connection:
            with connection.cursor() as cursor:
                sql3=f"select * from {table_name};"
                cursor.execute(sql3)
                for i in cursor.fetchmany(num_entries):
                    print(i)
    except (Exception, psycopg2.DatabaseError):
         logger.exception(
            "Error occured while fetching database entries:", exc_info=True
        )