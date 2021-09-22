import logging
import os
import pandas as pd
import numpy as np
from pathlib import Path


# Create logger
logger = logging.getLogger(__name__)


def get_logfc_mmm_matrix(df, alpha=0.05):
    """
    For each gene, get the logfc median absolute deviation (MAD), max, and
    median values across treatments.
    """
    # Significance filter
    sig = df["padj"] <= alpha

    # Filter by significance, group by gene, and aggregate
    # log2foldchange by mad, max and median statistics
    mmm_df = (
        df[sig]
        .groupby(["gene"])
        .agg({"log2foldchange": ["mad", "max", "median"]})
    )

    return mmm_df


if __name__ == "__main__":
    df = pd.read_csv("../../tests/data/output/logfc_matrix.csv")
    df.set_index(["treatment", "gene"], inplace=True)
    mmm_df = get_mad_max_med_matrix(df)
    print(mmm_df)
