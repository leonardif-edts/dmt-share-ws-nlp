#################### Scraper ####################
# How to Run:
#   python run.py [DATE] [RESULT_PREFIX]
#
# *DEFAULT value for DATE is current date.
# *DEFAULT value for RESULT_PREFIX is 'scraping_result'.
#
# Example:
#   python run.py 2021-09-07
#################################################
import os
from datetime import datetime

from job import scraping_job

from shared.params import get_args, get_config_json
from shared.aggregator import aggregate_result

if __name__ == "__main__":
    # Get configuration values
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(script_dir, "config.json")
    config = get_config_json(config_path)
    driver = config.get("driver")
    output_dir = config.get("output_dir")
    scraper_config = config.get("scraper")

    # Get arguments values
    [date_str, filename] = get_args(params_count = 2)
    date = datetime.strptime(date_str, "%Y-%m-%d") if (date_str) else datetime.now()
    filename = filename if (filename) else "scraping_result"

    # Create output_dir if not exists
    if (not os.path.exists(output_dir)):
        os.makedirs(output_dir)

    # Run kompas scraper
    scraping_job(
        scraper_id = "kompas",
        config = scraper_config["kompas"],
        date = date,
        output_dir = output_dir
    )

    # Run cnn scraper
    scraping_job(
        scraper_id = "cnn",
        config = scraper_config["cnn"],
        date = date,
        output_dir = output_dir,
        driver = driver
    )

    # Aggregate result
    print(f"Aggreating result into single file: {filename}.csv")
    aggregate_result(output_dir, filename)
