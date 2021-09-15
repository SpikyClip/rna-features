import pytest
from rnafeatures.utils.argparser import parser as main_parser

#
# Define test inputs
#

# P-values
true_pval = ["0.005", "0.05", "0.1", "0.5", "0.99"]
false_pval = [
    pytest.param(0, marks=pytest.mark.xfail),
    pytest.param("string", marks=pytest.mark.xfail),
    pytest.param("&$", marks=pytest.mark.xfail),
    pytest.param(-0.1, marks=pytest.mark.xfail),
    pytest.param(1, marks=pytest.mark.xfail),
]

pvals = true_pval + false_pval

# Directories
true_dir = ["set_1", "set_2"]
false_dir = [
    pytest.param("false_dir1", marks=pytest.mark.xfail),
    pytest.param("false_dir2", marks=pytest.mark.xfail),
]
empty_dir = [pytest.param("empty", marks=pytest.mark.xfail)]

dirs = true_dir + false_dir + empty_dir

#
# Create fixtures
#

# Create fixture for directory structure
@pytest.fixture(scope="module")
def temp(tmp_path_factory):
    temp = tmp_path_factory.mktemp("data")
    datasets = ["set_1", "set_2", "empty"]

    for dataset in datasets:
        dir = temp / dataset
        dir.mkdir()
        if dataset != "empty":
            for i in range(1, 4):
                csv = dir / f"{i}.csv"
                csv.write_text("blank\n")

    return temp


#
# Tests
#

# Test p-values
@pytest.mark.parametrize("pval", pvals)
def test_pval(temp, pval):
    dirs = [str(temp / dir) for dir in true_dir]
    input = ["-p", pval] + dirs
    main_parser.parse_args(input)


# Test directories
@pytest.mark.parametrize("dir1", dirs)
@pytest.mark.parametrize("dir2", dirs)
def test_dirs(temp, dir1, dir2):
    dir1 = str(temp / dir1)
    dir2 = str(temp / dir2)
    input = [dir1, dir2]
    main_parser.parse_args(input)
