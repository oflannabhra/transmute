import pytest
import os

from transmute.transmute import Transmute
from transmute.collection import CollectionType

GLD_INFILE = "test/mtggoldfish.csv"
HEL_INFILE = "test/helvault.csv"
OUTFILE = "test/output.csv"

HEL_OUTFILE = "test/hel_output.csv"
GLD_OUTFILE = "test/gld_output.csv"

@pytest.fixture(scope='session', autouse=True)
def outfile():
    # create the output file if it doesn't exist
    if not os.path.isfile(OUTFILE):
        open(OUTFILE, 'w').close()

    # open and yield the file handle
    with open(OUTFILE) as outfile:
        yield outfile
    
    # close and delete the test file
    outfile.close()
    if os.path.isfile(OUTFILE):
        os.remove(OUTFILE)


def test_goldfish_to_helvault(outfile):
    # Setup
    t = Transmute(in_file=GLD_INFILE, out_file=OUTFILE)

    # Execute
    t.convert_collection(input_type=CollectionType("gld"), output_type=CollectionType("hel"))
    with open(HEL_OUTFILE) as expected_output:
        output_lines = outfile.readlines()
        expected_output_lines = expected_output.readlines()
        output_tuples = zip(output_lines, expected_output_lines)
    
    # Assert
    assert len(output_lines) == 2
    assert len(output_lines) == len(expected_output_lines)
    for (actual, expected) in output_tuples:
        assert actual == expected

def test_helvault_to_goldfish(outfile):
    # Setup
    t = Transmute(in_file=HEL_INFILE, out_file=OUTFILE)

    # Execute
    t.convert_collection(input_type=CollectionType("hel"), output_type=CollectionType("gld"))
    with open(GLD_OUTFILE) as expected_output:
        output_lines = outfile.readlines()
        expected_output_lines = expected_output.readlines()
        output_tuples = zip(output_lines, expected_output_lines)
    
    # Assert
    assert len(output_lines) == 2
    assert len(output_lines) == len(expected_output_lines)
    for (actual, expected) in output_tuples:
        assert actual == expected


def test_double_convert_goldfish(outfile):
    t = Transmute(in_file=GLD_INFILE, out_file=OUTFILE)

    t.convert_collection(input_type=CollectionType("gld"), output_type=CollectionType("gld"))



def test_file_dne():
    pass
    # Setup

    # Execute
    
    # Assert
