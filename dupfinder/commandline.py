import argparse
import sys

from dupfinder import core


parser = argparse.ArgumentParser(
    prog="dupfinder",
    description="Finds duplicate files below one or more root directories."
)

parser.add_argument(
    "root_paths", nargs="*", default=["."], metavar="rootpath",
    help=("Top level directories to search for duplicate files within. "
          "Defaults to current directory if none are specified.")
)


def print_lnln(s):
    print(s, end="\n\n")


def run():
    root_paths = parser.parse_args().root_paths

    try:
        root_paths = core.get_absolute_root_paths(root_paths)
    except FileNotFoundError as ex:
        print_lnln("The path {} does not exist.".format(ex.filename))
        sys.exit(1)

    print_lnln("Comparing files (this may take some time)...")

    duplicates = core.run(root_paths)

    if not duplicates:
        print_lnln("No duplicates were found.")
        sys.exit()

    print_lnln(
        "The following duplicate files were found.\n"
        "Files listed in **** demarcated blocks are duplicates of each other."
    )

    group_sep = "*" * 79
    for dup_group in duplicates:
        print(group_sep)
        for duplicate in dup_group:
            print(duplicate)
        print_lnln(group_sep)