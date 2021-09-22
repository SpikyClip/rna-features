import argparse
import logging
from pathlib import Path


logger = logging.getLogger(__name__)

#
# Type functions for parser
#


def p_val_type(arg):
    """
    Checks if p_val is a float within the range {0, 1}.
    """

    try:
        p_val = float(arg)

    except ValueError:
        msg = f"P-value '{arg}' is not a floating point number."
        raise argparse.ArgumentTypeError(msg)

    if not (0 < p_val < 1):
        msg = f"P-value '{p_val}' is outside the range (0 < p-value < 1)"
        raise argparse.ArgumentTypeError(msg)

    return p_val


def path_type(arg):
    """
    Checks if supplied paths are exist and contain .csv files.
    """
    try:
        dir = Path(arg)

    except TypeError as e:
        logger.exception(e)
        raise

    if not dir.is_dir():
        msg = f"'{dir}' is not a valid directory"
        raise argparse.ArgumentTypeError(msg)

    elif not list(dir.glob("*.csv")):
        msg = f"'{dir}' does not contain any *.csv files."
        raise argparse.ArgumentTypeError(msg)

    elif not list(dir.glob("*tpm.tsv")):
        msg = f"'{dir}' does not contain a *tpm.tsv file."
        raise argparse.ArgumentTypeError(msg)

    elif len(list(dir.glob("*tpm.tsv"))) > 1:
        msg = f"'{dir}' contains more than one *tpm.tsv file:\n {list(dir.glob('*tpm.tsv'))}"
        raise argparse.ArgumentTypeError(msg)

    else:
        return dir


#
# Instantiate parser
#

desc = (
    "Generates machine-learning features from a list of dataset "
    "directories containing DESeq2 log2 fold change data in .csv format."
)

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-p",
    default=0.05,
    metavar="p-value",
    type=p_val_type,
    help="A p-value cutoff for filtering log2 fold change values before feature generation",
)
parser.add_argument(
    "dir",
    nargs="+",
    type=path_type,
    help="A list of dataset directories containing .csv DESeq2 log2 fold change output",
)
