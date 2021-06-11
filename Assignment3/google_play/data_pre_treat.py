import csv
import datetime
import pathlib
import numpy as np
import re
import math

import pandas as pd

month = {
    "Jan": "1",
    "Feb": "2",
    "Mar": "3",
    "Apr": "4",
    "May": "5",
    "Jun": "6",
    "Jul": "7",
    "Aug": "8",
    "Sep": "9",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
}

Content_Rating_COLORS = [
    "#FFEDA0",
    "#FA9FB5",
    "#A1D99B",
    "#67BD65",
    "#BFD3E6",
    "#B3DE69",
    "#FDBF6F",
    "#FC9272",
    "#D0D1E6",
    "#ABD9E9",
    "#3690C0",
    "#F87A72",
    "#CA6BCC",
    "#DD3497",
    "#4EB3D3",
    "#FFFF33",
    "#FB9A99",
    "#A6D853",
    "#D4B9DA",
    "#AEB0B8",
    "#CCCCCC",
    "#EAE5D9",
    "#C29A84"]

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()


def pre_treat_ori_csv():
    ori_csv_file = open(DATA_PATH.joinpath("googleplaystore.csv"), newline="", encoding="utf-8")
    ori_csv = csv.reader(ori_csv_file)

    new_csv_file = open(DATA_PATH.joinpath("googleplaystore_new.csv"), "w+", newline="", encoding="utf-8")
    new_csv = csv.writer(new_csv_file)

    category_list = ["ALL"]
    android_ver_list = set()

    for index, line in enumerate(ori_csv):
        if index == 0:
            continue
        for key, val in month.items():
            if str(key) in line[10]:
                line[10] = line[10].replace(str(key), str(val))
                break
        line[10] = line[10].rsplit("-", 1)[0] + "-20" + line[10].rsplit("-", 1)[1]
        line[10] = datetime.datetime.strptime(line[10], "%d-%m-%Y").date()
        line[10] = datetime.date.strftime(line[10], "%Y-%m-%d")
        line[12] = line[12].replace("and up", "+")
        line[7] = line[7].strip().replace("$", "")
        new_csv.writerow(line)

        # category
        if line[1] in category_list:
            continue
        else:
            category_list.append(line[1])

        # android ver
        android_ver_list.add(line[12])

    ori_csv_file.seek(0)
    new_csv_file.seek(0)

    ori_csv_file.close()
    new_csv_file.close()

    android_ver_list = list(android_ver_list)
    android_ver_list.sort()

    return category_list, android_ver_list


def load_new_csv():
    new_csv = csv.reader(open(DATA_PATH.joinpath("googleplaystore_new.csv"), encoding="utf-8"))
    return new_csv


def get_data_by_categoryandlastupdated(new_csv_reader, category_list, year_month_slider):
    year_month = []
    np_list = np.arange(year_month_slider[0], year_month_slider[1], 1 / 12)
    np_list = np_list * 12 + 1
    year = np_list // 12
    month = np_list % 12
    for i in range(len(np_list)):
        year_month.append(str(round(year[i])) + "-" + str(round(month[i])))

    left_time = datetime.date(year=round(year[0]), month=round(month[0]), day=1)

    right_time = datetime.date(year=round(year[-1]), month=round(month[-1]), day=1)

    res = []

    for index, line in enumerate(new_csv_reader):
        if line[1] in category_list or "ALL" in category_list:
            now_date = datetime.datetime.strptime(line[10], "%Y-%m-%d").date()
            if now_date >= left_time and now_date <= right_time:
                res.append(line)

    return year_month, res


# Helper functions


def get_data_by_priceandrating(new_csv_reader, price, rating):
    res = []
    for line in new_csv_reader:
        if str(price) == line[7] and line[2] == str(rating):
            res.append(line)
    return res


def get_data_by_android_ver(res):
    reviews = {}
    installs = {}
    for line in res:
        if line[12] in reviews:
            reviews[line[12]] += int(line[3])
            installs[line[12]] += int(line[5])
        else:
            reviews[line[12]] = 0
            installs[line[12]] = 0
    reviews = dict(sorted(reviews.items(), key=lambda x: x[0]))
    installs = dict(sorted(installs.items(), key=lambda x: x[0]))

    return reviews, installs


def human_format(num):
    if num == 0:
        return "0"

    magnitude = int(math.log(num, 1000))
    mantissa = str(int(num / (1000 ** magnitude)))
    return mantissa + ["", "K", "M", "G", "T", "P"][magnitude]


def cnt_aggregate(new_csv_reader, category_list, year_month_slider):
    apps = 0
    reviews = 0
    installs = 0

    _, res = get_data_by_categoryandlastupdated(new_csv_reader, category_list, year_month_slider)

    for line in res:
        apps += 1
        line3_num = re.findall(r"\d+\.?\d*", line[3].strip())[0]
        line5_num = re.findall(r"\d+\.?\d*", line[5].strip())[0]
        if line3_num == "":
            pass
        else:
            reviews += int(line3_num)
        if line5_num == "":
            pass
        else:
            installs += int(line5_num)

    return apps, reviews, installs
