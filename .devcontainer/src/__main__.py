import logging.config
import os

import click
import yaml
from click_commands.fetch_database import fetch_database
from click_commands.store_openmeteo_data import store_openmeteo_data


@click.group
def main():
    pass

# Add new Click Commands that can be invoked with e.g.
# >>> python __main__.py store_openmeteo_data --option1 arg1
main.add_command(store_openmeteo_data)
main.add_command(fetch_database)

if __name__ == "__main__":
    try:
        with open(f"{os.path.dirname(os.path.realpath(__file__))}/logger_config.yaml", "r") as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
    except (FileNotFoundError, Exception) as err:
        raise Exception(f"Error occured: {err}\nCurrent path of this file is: {os.path.dirname(os.path.realpath(__file__))}")
    logger = logging.getLogger("SampleLogger")
    main()