import logging
import pandas as pd
from pathlib import Path

# Create logger
logger = logging.getLogger(__name__)


def get_logfc_matrix(paths):
    """
    Combines contrast files and returns it as a matrix with a multi-level index.
    """

    # Output format
    #                      basemean, log2foldchange, lfcse, stat, pvalue, padj,
    #   treatment,   gene,
    # treatment_1, gene_1,   mean_1,           fc_1,  se_1, st_1,    p_1, pa_1,
    #              gene_2,   mean_2,           fc_2,  se_2, st_2,    p_2, pa_2,
    # treatment_2, gene_1,   mean_3,           fc_3,  se_3, st_3,    p_3, pa_3,
    #              gene_2,   mean_4,           fc_4,  se_4, st_4,    p_4, pa_4,

    concat_df = None

    for path in paths:
        logger.debug(f"Processing '{path.name}'")
        treatment_name = path.name.rsplit(".", 1)[0]

        df = pd.read_csv(path, sep=",")
        df = format_logfc_df(df, treatment_name)

        if concat_df is None:
            concat_df = df.copy()

        else:
            concat_df = pd.concat([concat_df, df])

    return concat_df


def format_logfc_df(df, treatment_name):
    """
    Formats logfc dataframe before concatenation.
    """

    # Clean column names, insert treatment name, and set multi-index
    df.columns = df.columns.str.lower()
    df.insert(0, "treatment", treatment_name)
    df.columns.values[1] = "gene"
    df.set_index(["treatment", "gene"], inplace=True)

    # Catch non-unique gene index
    try:
        if not df.index.is_unique:
            msg = (
                f"'{treatment_name}' has a non-unique index which may "
                "cause downstream errors. Please check that its gene list is "
                "unique"
            )
            raise IndexError(msg)

    except IndexError as error:
        logger.exception(error)
        raise

    return df
