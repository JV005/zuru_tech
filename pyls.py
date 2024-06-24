import json
import argparse
import time
from typing import List, Dict, Any


def format_time(epoch_time: float) -> str:
    ''' Date format in Month Day Hour:Minute'''
    return time.strftime('%b %d %H:%M', time.localtime(epoch_time))


def filter_items(items: List[Dict[str, Any]], filter_option: str) -> List[Dict[str, Any]]:
    ''' Sort based on filter_option provided, valid values: file, dir'''

    if filter_option == 'file':
        return [item for item in items if item['permissions'][0] != 'd']
    elif filter_option == 'dir':
        return [item for item in items if item['permissions'][0] == 'd']

def sort_items(items: List[Dict[str, Any]], reverse_order: bool) -> List[Dict[str, Any]]:
    ''' Sort items based on time_modified and size'''
    return sorted(items, key=lambda x: (x['time_modified'], x['size']), reverse=reverse_order)


def print_detailed(items: List[Dict[str, Any]]) -> None:
    ''' Implement the argument -l, that prints the results vertically with additional
     information. Also takes -r parameter for reversing the order.'''
    for item in items:
        if not item['name'].startswith("."):
            permissions = item['permissions']
            size = item['size']
            time_modified = format_time(item['time_modified'])
            name = item['name']
            print(f"{permissions} {size:>10} {time_modified} {name}")


def print_detailed_sorted_filtered(directory: Dict[str, Any], reverse_order: bool, filter_option: str) -> None:
    ''' Implement the argument -t that prints the results sorted by time_modified. '''
    items = filter_items(directory['contents'], filter_option)
    items_sorted = sort_items(items, reverse_order)
    print_detailed(items_sorted)


def print_detailed_sort_time(directory: Dict[str, Any], flag: bool) -> None:
    '''Implement the argument -l, that prints the results vertically with additional information
    Also implement -r parameter to in reverse the results'''
    items = sort_items(directory['contents'], reverse_order=flag)
    print_detailed(items)


def print_name(data: Dict[str, Any], show_all: bool) -> None:
    ''' This lists out the top level (in the directory interpreter) directories and files.
    Also has -A functionality if the parameter is provided '''
    items = data['contents']
    if show_all:
        top_level_contents = [item['name'] for item in items]
    else:
        top_level_contents = [item['name'] for item in items if not item['name'].startswith(".")]
    print(' '.join(top_level_contents))


def main() -> None:
    parser = argparse.ArgumentParser(description='A simple argument parser example. Command:  python -m pyls')
    parser.add_argument('-A', action='store_true', help='List all files and directories including those starting with ".". Command:  python -m pyls -A')
    parser.add_argument('-l', action='store_true', help='Print detailed information. Command: python -m pyls -l')
    parser.add_argument('-r', action='store_true', help='Print in reverse order. Command: python -m pyls -l -r' )
    parser.add_argument('-t', action='store_true', help='Print in reverse order based on time')
    parser.add_argument('--filter', choices=['file', 'dir'], help='Filter by type (file or dir) ')
    args = parser.parse_args()

    path = "structure.json"
    try:
        with open(path) as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {path}")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON - {e}")
        return
    print(args)


    if args.A:
        print("1. print_name")
        print_name(data, True)

    elif args.l and not args.r and not args.t:
        print("2. print_detailed")
        print_detailed(data['contents'])

    elif args.l and args.r and not args.t:
        print("3. print_detailed")
        print_detailed(data['contents'][::-1])

    elif args.t and  not (args.r, args.filter):
        print("4. print_detailed_sort_time")
        print_detailed_sort_time(data, False)

    elif args.t and args.r and not args.filter:
        print("5. print_detailed_sort_time")
        print_detailed_sort_time(data, True)

    elif args.l and args.t and args.r and  args.filter:
        print("6. print_detailed_sorted_filtered")
        print_detailed_sorted_filtered(data, True, args.filter)

    elif args.l and args.t and  args.filter and not args.r:
        print("7. print_detailed_sorted_filtered")
        print_detailed_sorted_filtered(data, False, args.filter)

    elif args not in (args.l, args.r, args.t):
        print("8. print_name")
        print_name(data, False)

    else:
        raise ValueError("Invalid combination of arguments")




if __name__ == "__main__":
    main()