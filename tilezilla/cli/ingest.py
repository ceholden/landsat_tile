# -*- coding: utf-8 -*-
""" Process an image or compressed tarball of images to tiles
"""
import logging
import os

import click

from . import cliutils, options
from .. import products, tilespec
from .._util import decompress_to, reproject_as_needed

logger = logging.getLogger('tilezilla')
echoer = cliutils.Echoer(message_indent=0)


@click.command(short_help='Ingest known products into tile dataset format')
@options.arg_sources
@options.opt_tilespec_str
@click.pass_context
def ingest(ctx, sources, tilespec_str):
    # TODO: add --tilespec-defn (a JSON/YAML config file with tile params)
    # TODO: add --tilespec-[attrs] where [attrs] are tilespec attributes
    if not tilespec_str:
        raise click.UsageError('Must specify a tile specification to use')

    spec = tilespec.TILESPECS[tilespec_str]

    for source in sources:
        _source = os.path.splitext(os.path.splitext(
                                   os.path.basename(source))[0])[0]
        with decompress_to(source) as tmpdir:
            # Handle archive name as inner folder
            inside_dir = os.listdir(tmpdir)
            if _source in inside_dir:
                tmpdir = os.path.join(tmpdir, _source)

            product = registry.sniff_product_type(tmpdir)
            print(product)
