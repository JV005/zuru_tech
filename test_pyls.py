import pytest
from pyls import (
    format_time,
    filter_items,
    sort_items,
    print_detailed,
    print_detailed_sorted_filtered,
    print_detailed_sort_time,
    print_name,
)
@pytest.fixture
def directory_data():
    return {
        "contents": [
            {
                "name": "file1.txt",
                "size": 1234,
                "time_modified": 1625097600,
                "permissions": "-rw-r--r--"
            },
            {
                "name": "file2.txt",
                "size": 5678,
                "time_modified": 1625184000,
                "permissions": "-rw-r--r--"
            },
            {
                "name": "dir1",
                "size": 4096,
                "time_modified": 1625270400,
                "permissions": "drwxr-xr-x"
            },
            {
                "name": ".hiddenfile",
                "size": 123,
                "time_modified": 1625270400,
                "permissions": "-rw-r--r--"
            }
        ]
    }

@pytest.fixture
def setup_data():
    return directory_data.copy()


def test_format_time():
    assert format_time(1641693600) == "Jan 09 07:30"
    assert format_time(1641697200) == "Jan 09 08:30"


def test_filter_items(directory_data):
    items = directory_data["contents"]

    filtered_files = filter_items(items, "file")
    assert len(filtered_files) == 3
    assert all("file" in item["name"] for item in filtered_files)

    filtered_dirs = filter_items(items, "dir")
    assert len(filtered_dirs) == 1
    assert all("dir" in item["name"] for item in filtered_dirs)


def test_sort_items(directory_data):
    items = directory_data["contents"]

    sorted_items = sort_items(items, reverse_order=False)
    assert sorted_items[0]["name"] == "file1.txt"
    assert sorted_items[-1]["name"] == "dir1"

    sorted_items_rev = sort_items(items, reverse_order=True)
    assert sorted_items_rev[0]["name"] == "dir1"
    assert sorted_items_rev[-1]["name"] == "file1.txt"


def test_print_detailed(directory_data, capfd):
    items = directory_data["contents"]
    print_detailed(items)
    captured = capfd.readouterr()
    assert "file1.txt" in captured.out
    assert "file2.txt" in captured.out
    assert "dir1" in captured.out

def test_print_detailed_sorted_filtered(directory_data, capfd):
    print_detailed_sorted_filtered(directory_data, False, "file")
    captured = capfd.readouterr()
    assert "file1.txt" in captured.out
    assert "file2.txt" in captured.out
    assert "dir1" not in captured.out

def test_print_detailed_sort_time(directory_data, capfd):
    print_detailed_sort_time(directory_data, False)
    captured = capfd.readouterr()
    assert "file1.txt" in captured.out
    assert "file2.txt" in captured.out
    assert "dir1" in captured.out

def test_print_name(directory_data, capfd):
    print_name(directory_data, True)
    captured = capfd.readouterr()
    assert "file1.txt" in captured.out
    assert "file2.txt" in captured.out
    assert ".hiddenfile" in captured.out

    print_name(directory_data, False)
    captured = capfd.readouterr()
    assert "file1.txt" in captured.out
    assert "file2.txt" in captured.out
    assert ".hiddenfile" not in captured.out