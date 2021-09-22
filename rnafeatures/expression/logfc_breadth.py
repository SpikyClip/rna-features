import numpy as np
import pandas as pd


def get_breadth_matrix(df, alpha=0.05):
    """
    Counts the number of significantly DE genes in each category.

    Categories include 'up' (log2fc >= 1), 'down' (log2fc <= -1), and
    'neither' (-1 < log2fc < 1)
    """

    # Define conditions and labels supplied to np.select()
    conditions = [
        df["log2foldchange"] >= 1,
        df["log2foldchange"] <= -1,
    ]
    labels = ["up", "down"]

    # Create categorical regulation column
    df["regulation"] = np.select(conditions, labels, default="neither")
    df["regulation"] = df["regulation"].astype("category")

    # Significance filter
    sig = df["padj"] <= alpha

    # Group significant rows by 'gene' and 'regulation', count the
    # frequency a gene falls into a 'regulation' category, and unstack
    # the 'regulation' index into columns for final feature format
    breadth_df = (
        df[sig]
        .groupby(["gene", "regulation"])["log2foldchange"]
        .count()
        .unstack(level="regulation")
    )

    # Switch column index to multiindex for later merging
    midx = pd.MultiIndex.from_product(
        [[breadth_df.columns.name], breadth_df.columns.categories]
    )
    breadth_df.columns = midx

    return breadth_df


if __name__ == "__main__":
    df = pd.read_csv("../../tests/data/output/logfc_matrix.csv")
    df.set_index(["treatment", "gene"], inplace=True)
    breadth_df = get_breadth_matrix(df)
    print(breadth_df)
