import os
import json
import pandas as pd
import copy
from tabulate import tabulate


def get_hist_data(file_path):
    """
    Read the JSON files from the given path and returns the data in Dataframe
    """
    json_files  = sorted_files(file_path)
    file_list   = []
    new_records = {}

    for index, js in enumerate(json_files):
        with open(js[1], 'r') as json_file:
            json_text   = json.load(json_file)
            current_id  = json_text["id"]
            records     = {}
            if "op" in json_text:
                if "data" in json_text and json_text["op"] == "c":
                    records     = {"id": json_text["id"], **json_text["data"], "ts": json_text["ts"]}
                    new_records = copy.copy(records)
                    file_list.append(new_records)
                elif json_text["op"] == "u":
                    records = {"id": json_text["id"], **json_text["set"], "ts": json_text["ts"]}
                    for i, data in enumerate(file_list):
                        if data["id"] == current_id:
                            new_records = copy.copy(data)
                            new_records.update(records)
                            file_list.append(new_records)
                            break
                        else:
                            continue

    return pd.DataFrame(file_list)


def sorted_files(file_path):
    """
    Get JSON files sorted by timestamp in the file and returns List[(int, str)]
    """
    ts_info = []
    json_files = [pos_json for pos_json in os.listdir(file_path) if pos_json.endswith('.json')]
    for index, js in enumerate(json_files):
        with open(os.path.join(file_path, js)) as json_file:
            json_text = json.load(json_file)
            file_info = (int(json_text['ts']), f'{file_path}{js}')
            ts_info.append(file_info)

    sorted_ts = sorted(ts_info, key=lambda x: x[0], reverse=False)
    return sorted_ts


if __name__ == "__main__":
    print("==== TASK 1 HAS STARTED ====")
    data_accounts         = get_hist_data(r'./data/accounts/')
    data_cards            = get_hist_data(r'./data/cards/')
    data_savings_accounts = get_hist_data(r'./data/savings_accounts/')

    print(tabulate(data_accounts, headers='keys', tablefmt='psql'))
    print(tabulate(data_cards, headers='keys', tablefmt='psql'))
    print(tabulate(data_savings_accounts, headers='keys', tablefmt='psql'))
    print("==== TASK 1 HAS FINISHED ====")