import pytest
import itertools as it
from rnafeatures.utils.argparser import parser as main_parser


class TestParser:
    true_pval = ["0.005", "0.05", "0.1", "0.5", "0.99"]
    false_pval = [
        pytest.param(0, marks=pytest.mark.xfail),
        pytest.param("string", marks=pytest.mark.xfail),
        pytest.param("&$", marks=pytest.mark.xfail),
        pytest.param(-0.1, marks=pytest.mark.xfail),
        pytest.param(1, marks=pytest.mark.xfail),
    ]

    pvals = true_pval + false_pval

    true_dir = ["set_1", "set_2"]
    false_dir = [
        pytest.param("false_dir1", marks=pytest.mark.xfail),
        pytest.param("false_dir2", marks=pytest.mark.xfail),
    ]
    empty_dir = [pytest.param("empty", marks=pytest.mark.xfail)]

    dirs = true_dir + false_dir + empty_dir

    @pytest.fixture(scope="class")
    def temp(self, tmp_path_factory):
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

    @pytest.mark.parametrize("pval", pvals)
    def test_pval(self, temp, pval):
        dirs = [str(temp / dir) for dir in self.true_dir]
        input = ["-p", pval] + dirs
        main_parser.parse_args(input)

    @pytest.mark.parametrize("dir1", dirs)
    @pytest.mark.parametrize("dir2", dirs)
    def test_dirs(self, temp, dir1, dir2):
        dir1 = str(temp / dir1)
        dir2 = str(temp / dir2)
        input = [dir1, dir2]
        main_parser.parse_args(input)
