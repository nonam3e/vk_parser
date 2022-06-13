import argparse
import requests
import csv
import json


def save_as_csv(content, file, format):
    output = open(f"{file}.{format}", "w", encoding="utf-8")
    writer = csv.DictWriter(output, content[0].keys())
    writer.writeheader()
    writer.writerows(content)
    output.close()


def save_as_tsv(content, file, format):
    output = open(f"{file}.{format}", "w", encoding="utf-8")
    writer = csv.DictWriter(output, content[0].keys(), delimiter='\t')
    writer.writeheader()
    writer.writerows(content)
    output.close()


def save_as_json(content, file, format):
    output = open(f"{file}.{format}", "w", encoding="utf-8")
    json.dump(content, output)
    output.close()


def parse():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("token", help="Authorization token")
    args_parser.add_argument("id", help="User id of target")
    args_parser.add_argument("-f", "--format", choices=["csv", "tsv", "json"],
                             default="csv", dest="format", help="Format of output file")
    args_parser.add_argument("-o", "--output", default="report", dest="output",
                             help="Output file location")
    args = args_parser.parse_args()
    # Use a breakpoint in the code line below to debug your script.
    query = f"https://api.vk.com/method/friends.get?access_token={args.token}&user_id={args.id}&order=name&fields=country,city,bdate,sex&v=5.131"
    save = {
        "csv": save_as_csv,
        "tsv": save_as_tsv,
        "json": save_as_json
    }
    data = requests.get(query).json()
    f_list = []
    for item in data["response"]["items"]:
        f_list.append({'first_name': item['first_name'], 'last_name': item['last_name'],
                       'country': item.get('country', {}).get('title', None),
                       'city': item.get('city', {}).get('title', None), 'bdate': item.get('bdate', None),
                       'sex': item['sex']})
    save[args.format](f_list, args.output, args.format)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parse()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
