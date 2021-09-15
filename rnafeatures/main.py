# Standard library
import logging
import logging.config
import pkgutil
import io

# Third-party libraries
import pandas as pd
from pathlib import Path

# Personal modules
from rnafeatures.utils.argparser import parser as main_parser
from rnafeatures.expression.main import expr_main

# Setup logger
logging_conf = pkgutil.get_data("rnafeatures", "logging.conf").decode("utf-8")
logging_conf = io.StringIO(logging_conf)
logging.config.fileConfig(logging_conf, disable_existing_loggers=False)

logger = logging.getLogger(__name__)


def main():
    args = main_parser.parse_args()
    out = expr_main(args.dir, args.p)
    print(out)


if __name__ == "__main__":
    args = main_parser.parse_args(
        ["../tests/data/input/set_1", "../tests/data/input/set_2"]
    )
    out = expr_main(args.dir, args.p)
    print(out)
