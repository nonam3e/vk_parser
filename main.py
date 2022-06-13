import argparse


def parse():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("Token", help="Authorization token")
    args_parser.add_argument("id", help="User id of target")
    args_parser.add_argument("-f", "--format", choices=["csv", "tsv", "json"],
                             default="csv", help="Format of output file")
    args_parser.add_argument("-o", "--output", default="report",
                             help="Output file location")
    args = args_parser.parse_args()
    # Use a breakpoint in the code line below to debug your script.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parse()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
