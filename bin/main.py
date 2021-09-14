# Standard library
import logging
import logging.config
from pathlib import Path

# Third-party libraries
import pandas as pd

# Personal modules
from rnafeatures.argparser import parser as my_parser
from rnafeatures.expression.logfc_matrix import get_logfc_matrix
from rnafeatures.expression.breadth import get_breadth_matrix
from rnafeatures.expression.mad_max_med import get_mad_max_med_matrix

# Setup logger
logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)


def expr_main(dir_paths, alpha=0.05):
    """
    Creates the expression dataset.

    The expression dataset consists of the breadth, maximum absolute deviation
    (MAD), maximum and median for each gene for each dataset.
    """
    processed_datasets = list()

    for dir in dir_paths:
        paths = dir.glob("*.csv")
        dataset_name = dir.name

        logger.info(f"Concatenating .csv files in '{dir}' into logfc matrix.")
        df = get_logfc_matrix(paths)

        logger.info("Getting breadth matrix.")
        breadth_df = get_breadth_matrix(df, alpha)

        logger.info("Getting mad max med matrix.")
        mmm_df = get_mad_max_med_matrix(df, alpha)

        # Combines breadth and mmm tables, adding a key for dataset
        logger.info("Joining breadth and mmm matrices.")
        exprs_df = pd.concat([breadth_df, mmm_df], axis=1)
        exprs_df = pd.concat([exprs_df], keys=[dataset_name], names=["dataset"])

        logger.info(f"Completed '{dataset_name}' expression matrix.\n")
        processed_datasets.append(exprs_df)

    # Combines multiple datasets
    if len(processed_datasets) > 1:
        logger.info("Concatenating all expression matrices.")
        combined_df = pd.concat(processed_datasets)
    else:
        logger.info("Returning single expression matrix.")
        combined_df = processed_datasets[0]

    logger.info("All expression features generated.\n\n")
    return combined_df


if __name__ == "__main__":
    test_arg = "-p 0.05 tests/data/input/set_1 tests/data/input/set_2"
    args = my_parser.parse_args(test_arg.split())
    out = expr_main(args.dir, args.p)
    print(out)
