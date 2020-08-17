#!/usr/bin/env python3

import sys
import json
import argparse

import singer
from singer import metadata

from tap_insided.client import InSidedClient
from tap_insided.discover import discover
from tap_insided.sync import sync

LOGGER = singer.get_logger()

REQUIRED_CONFIG_KEYS = [
]

def do_discover(client):
    LOGGER.info('Testing authentication')
    try:
        client.request('GET', path='/user')
    except:
        raise Exception('Error could not authenticate with InSided')

    LOGGER.info('Starting discover')
    catalog = discover()
    json.dump(catalog.to_dict(), sys.stdout, indent=2)
    LOGGER.info('Finished discover')

@singer.utils.handle_top_exception(LOGGER)
def main():
    parsed_args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

    with InSidedClient(parsed_args.config) as client:
        if parsed_args.discover:
            do_discover(client)
        else:
            sync(client,
                 parsed_args.config,
                 parsed_args.catalog,
                 parsed_args.state)
