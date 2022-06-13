import argparse
import requests
import csv
import json
import logging

logging.basicConfig(filename='logger.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def save_as_csv(content, file, fmt, new=True):
    if new:
        output = open(f"{file}.{fmt}", "w", encoding="utf-8")
    else:
        output = open(f"{file}.{fmt}", "a", encoding="utf-8")
    writer = csv.DictWriter(output, ['first_name', 'last_name', 'country', 'city', 'bdate', 'sex'])
    if new:
        writer.writeheader()
    writer.writerows(content)
    output.close()


def save_as_tsv(content, file, fmt, new=True):
    if new:
        output = open(f"{file}.{fmt}", "w", encoding="utf-8")
    else:
        output = open(f"{file}.{fmt}", "a", encoding="utf-8")
    writer = csv.DictWriter(output, ['first_name', 'last_name', 'country', 'city', 'bdate', 'sex'], delimiter='\t')
    if new:
        writer.writeheader()
    writer.writerows(content)
    output.close()


def save_as_json(content, file, fmt, new=True):
    if new:
        output = open(f"{file}.{fmt}", "w", encoding="utf-8")
        output.write("[\n")
    else:
        output = open(f"{file}.{fmt}", "a", encoding="utf-8")
    for item in content:
        json.dump(item, output, indent=4, separators=(',', ': '), )
        output.write(",\n")
    output.close()


# different funcs for different formats makes code flexible
save = {
    "csv": save_as_csv,
    "tsv": save_as_tsv,
    "json": save_as_json
}


def parse():
    args_parser = argparse.ArgumentParser(description="Parses list of friends")
    args_parser.add_argument("token", help="Authorization token")
    args_parser.add_argument("id", help="User id of target")
    args_parser.add_argument("-f", "--format", choices=["csv", "tsv", "json"],
                             default="csv", dest="format", help="Format of output file")
    args_parser.add_argument("-o", "--output", default="report", dest="output",
                             help="Output file location")
    args = args_parser.parse_args()

    try:
        n = requests.get(
            f"https://api.vk.com/method/friends.get?access_token={args.token}&user_id={args.id}&count=1&v=5.131").json()
        if n.get("error", 0) != 0:  # checking input
            logging.warning(n["error"]["error_msg"])
            raise SystemExit(n["error"]["error_msg"])
        n = n["response"]["count"]  # getting number of friends
        for i in range(0, n, 1000):  # stores 1000 friends and appends to file
            query = f"https://api.vk.com/method/friends.get?access_token={args.token}&user_id={args.id}&order=name" \
                    f"&offset={i}&count=1000&fields=country,city,bdate,sex&v=5.131 "
            data = requests.get(query).json()
            f_list = []
            for item in data["response"]["items"]:
                f_list.append({'first_name': item['first_name'], 'last_name': item['last_name'],
                               'country': item.get('country', {}).get('title', None),
                               'city': item.get('city', {}).get('title', None), 'bdate': item.get('bdate', None),
                               'sex': item['sex']})
            save[args.format](f_list, args.output, args.format, not i)
    except requests.exceptions.Timeout as e:
        logging.error("Timeout ", e)
        raise SystemExit(e)
    except requests.exceptions.TooManyRedirects as e:
        logging.error("bad url ", e)
        raise SystemExit(e)
    except requests.exceptions.RequestException as e:
        logging.error(e)
        raise SystemExit(e)
    if args.format == "json":
        output = open(f"{args.output}.{args.format}", "a")
        output.write("]")  # JSON end
        output.close()
    logging.info(f"{args.id} parsed {n} friends")
    print("Parsed")


if __name__ == '__main__':
    parse()
