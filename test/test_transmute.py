import pytest
from transmute.transmute import Transmute
from transmute.collection import CollectionType

GLD_INFILE = "test/mtggoldfish.csv"
OUTFILE = "test/output.csv"

HEL_OUTFILE = "test/hel_output.csv"

def test_goldfish_to_helvault():
    # Setup
    t = Transmute(in_file=GLD_INFILE, out_file=OUTFILE)

    # Execute
    t.convert_collection(input_type=CollectionType("gld"), output_type=CollectionType("hel"))
    with open(OUTFILE) as output, open(HEL_OUTFILE) as expected_output:
        output_lines = output.readlines()
        expected_output_lines = expected_output.readlines()
        output_tuples = zip(output_lines, expected_output_lines)
    
    # Assert
    assert len(output_lines) == 2
    assert len(output_lines) == len(expected_output_lines)
    for (actual, expected) in output_tuples:
        assert actual == expected

def test_helvault_to_goldfish():
    pass
    # Setup

    # Execute
    
    # Assert


def test_file_dne():
    pass
    # Setup

    # Execute
    
    # Assert
