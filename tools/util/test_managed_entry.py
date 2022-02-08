#!/bin/python3

import pytest
from managed_entry import ManagedEntry

def test_edit_editable():
    test_dict = {"a" : 1}
    entry = ManagedEntry (test_dict, True)

    entry["a"] = 2
    assert (entry["a"] == 2)

def test_edit_non_editable():
    test_dict = {"a" : 1}
    entry = ManagedEntry (test_dict, False)

    try:
        entry["a"] = 2
    except KeyError:
        assert (True)
    else:
        assert(False)

def test_edit_non_key():
    test_dict = {"a" : 1}
    entry = ManagedEntry (test_dict, False)

    try:
        entry["b"] = 2
    except KeyError:
        assert (True)
    else:
        assert(False)
