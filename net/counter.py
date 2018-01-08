# coding: UTF-8

import os
import json
import re
from data_formatter import check, analyze_time
import configparser

configFilePath = "../config/multi_lstm_crit_baseline_small.config"
config = configparser.RawConfigParser()
config.read(configFilePath)

# in_path = r"D:\work\law_pre\test\in"
# out_path = r"D:\work\law_pre\test\out"
in_path = r"/data/disk1/private/zhonghaoxi/law/data"
out_path = r"/disk/mysql/law_data/count_data"
mid_text = u"  _(:з」∠)_  "
title_list = ["docId", "caseNumber", "caseName", "spcx", "court", "time", "caseType", "bgkly", "yuanwen", "document",
              "cause", "docType", "keyword", "lawyer", "punishment", "result", "judge"]

accusation_file = r"../data_processor/accusation_list2.txt"
accusation_f = open(accusation_file, "r", encoding='utf8')
accusation_list = json.loads(accusation_f.readline())
# for a in range(0, len(accusation_list)):
#    accusation_list[a] = accusation_list[a].replace("[", "").replace("]", "")
# accusation_list = []
# for line in accusation_f:
#    accusation_list.append(line[:-1])

num_file = 20
num_process = 1

total_cnt = 0

crit_list = []
for a in range(0, len(accusation_list)):
    crit_list.append(0)
time_dict = {}


def analyze_times(data):
    x = analyze_time(data, None)
    if not (x in time_dict):
        time_dict[x] = 0
    time_dict[x] += 1


def analyze_crit(data):
    if len(data) == 0:
        return
    for x in data:
        crit_list[x] += 1


law_list = [{}, {}]

cnt1 = 0
cnt2 = 0


def analyze_law(data):
    arr1 = []
    arr2 = []
    global cnt1, cnt2
    for x, y, z in data:
        if x < 102:
            continue
        arr1.append((x, z))
        arr2.append((x, z, y))

    arr1 = list(set(arr1))
    arr1.sort()
    arr2 = list(set(arr2))
    arr2.sort()
    if len(arr1) != 1 or len(arr2) != 1:
        return
    if len(arr1) == 1:
        cnt1 += 1
        if not (arr1[0] in law_list[0]):
            law_list[0][arr1[0]] = 0
        law_list[0][arr1[0]] += 1

    if len(arr2) == 1:
        cnt2 += 1
        if not (arr2[0] in law_list[1]):
            law_list[1][arr2[0]] = 0
        law_list[1][arr2[0]] += 1


def count(data):
    global total_cnt
    total_cnt += 1

    analyze_crit(data["crit"])
    analyze_times(data["time"])
    analyze_law(data["law"])


def draw_out(in_path, out_path):
    print(in_path)
    inf = open(in_path, "r")

    cnt = 0
    for line in inf:
        data = json.loads(line)
        if not (check(data, config)):
            continue
        count(data["meta"])
        cnt += 1
        if cnt % 500000 == 0:
            print(cnt)


def work(from_id, to_id):
    global cnt1,cnt2
    for a in range(int(from_id), int(to_id)):
        print(str(a) + " begin to work",cnt1,cnt2)
        draw_out(os.path.join(in_path, str(a)), os.path.join(out_path, str(a)))
        print(str(a) + " work done",cnt1,cnt2)


if __name__ == "__main__":
    work(0, 20)

    ouf = open("result/law_result.txt", "w")
    data = {}
    print(total_cnt)
    gg = 0
    for a in range(0, len(crit_list)):
        # if crit_list[a] > 1000:
        # print(accusation_list[a], a, crit_list[a],file=ouf)
        gg += crit_list[a]
    print(gg)
    data["total"] = total_cnt

    data["crit"] = crit_list
    data["law"] = law_list
    data["time"] = time_dict

    # for x in time_dict.keys():
    #    print(x, time_dict[x])
    # print(json.dumps(data), file=ouf)

    print(cnt1)
    print(cnt2)

    ouf = open("result/law_result1.txt", "w")
    arr = []
    for x in law_list[0].keys():
        arr.append((x, law_list[0][x]))
    arr.sort()
    for x in arr:
        if x[1] > 1000:
            print(x[0][0],x[0][1],x[1], file=ouf)

    ouf = open("result/law_result2.txt", "w")
    arr = []
    for x in law_list[1].keys():
        arr.append((x, law_list[1][x]))
    arr.sort()
    for x in arr:
        if x[1]>1000:
            print(x[0][0],x[0][1],x[0][2],x[1], file=ouf)
