import pytest
from transmute.transmute import Transmute
from transmute.collection import CollectionType

def test_goldfish_to_helvault():
    # Setup
    t = Transmute(in_file="test/mtggoldfish.csv", out_file="test/output.csv")

    # Execute
    t.convert_collection(input_type=CollectionType("gld"), output_type=CollectionType("hel"))
    
    # Assert

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
