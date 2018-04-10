#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging.config
import yaml
import os
import sys
from argparse import ArgumentParser

# Set modules and configuration path
LIBS_PATH = "{}/libs/".format(os.path.dirname(os.path.realpath(__file__)))
CONF_PATH = "{}/configurations/".format(os.path.dirname(os.path.realpath(__file__)))


"""
    Try to import logging configuration
    and submodules.
"""
try:
    # Init logging module
    with open("{}logging.yaml".format(CONF_PATH), 'r') as f:
        log_conf = yaml.load(f)
        log_conf.setdefault('version', 1)
        logging.config.dictConfig(log_conf)

    logger = logging.getLogger(__name__)

    # Load submodules
    sys.path.append(LIBS_PATH)

    from gui import Gui
    from configuration import Configuration

except Exception as e:
    raise Exception("Failed to load annexes.")


def check_output_directory(directory):
    """
    Check if output directory exist and is writable.
    :param directory: Path where to store pictures.
    """
    try:
        testing_file = os.path.join(directory, os.path.basename(__file__))
        open(testing_file, 'a').close()

        os.remove(testing_file)
    except NotADirectoryError:
        logger.error("{} not a valid directory.".format(directory), exc_info=True)
        exit(2)
    except Exception as e:
        logger.error("Unexpected error",  exc_info=True)
        exit(2)


def run(lang):
    """
    Run Photobooth application.
    :param lang: Define with language to use
    :type lang: str
    """
    # Init configuration
    configuration = Configuration("{}config.yaml".format(CONF_PATH))

    # Check output directory
    check_output_directory(configuration.pictures_directory)

    try:
        # Create Gui
        photobooth_app = Gui(configuration.resolution['width'],
                             configuration.resolution['height'],
                             getattr(configuration, lang))

        # Run Photobooth.
        logger.info("Photobooth apps running ...")
        photobooth_app.run()

    except Exception as e:
        logger.error("Failed to run Photobooth app: {}", exc_info=True)
        exit(1)


if __name__ == "__main__":
    # Create script arguments parser
    args_parse = ArgumentParser("Run photobooth.")
    args_parse.add_argument("--language", "-l", metavar="language", default="fr", help="choose application language.")

    params = args_parse.parse_args()

    run(lang=params.language)
