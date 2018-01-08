import os
import json
import torch
from word2vec import word2vec
import random

transformer = word2vec()
accusation_list = []
accusation_dict = {}
f = open("result/result_bac.txt", "r")
for line in f:
    data = int(line[:-1].replace("\n", "").split(" ")[1])
    accusation_list.append(data)
    accusation_dict[data] = len(accusation_list) - 1

law_list1 = []
law_dict1 = {}
f = open("result/law_result1.txt", "r")
for line in f:
    arr = line[:-1].replace("\n", "").split(" ")
    data = int(arr[0]), int(arr[1])
    law_list1.append(data)
    law_dict1[data] = len(law_list1) - 1

law_list2 = []
law_dict2 = {}
f = open("result/law_result2.txt", "r")
for line in f:
    arr = line[:-1].replace("\n", "").split(" ")
    data = int(arr[0]), int(arr[1]), int(arr[2])
    law_list2.append(data)
    law_dict2[data] = len(law_list2) - 1


def get_data_list(d):
    return d.replace(" ", "").split(",")


def analyze_crit(data, config):
    return accusation_dict[data[0]]


def check_law(data):
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
        return False
    if not((arr1[0][0],arr2[0][2]) in law_dict1):
        return False
    if not((arr2[0][0],arr2[0][2],arr2[0][1]) in law_dict2):
        return False
    return True


def analyze_law1(data, config):
    return law_dict1[(data[0][0], data[0][2])]


def analyze_law2(data, config):
    return law_dict2[(data[0][0], data[0][2], data[0][1])]


def analyze_time(data, config):
    if data["sixing"]:
        return 0
    if data["wuqi"]:
        return 1
    v = 0
    for x in data["youqi"]:
        v = max(x, v)
    for x in data["juyi"]:
        v = max(x, v)
    for x in data["guanzhi"]:
        v = max(x, v)
    if v > 10 * 12:
        return 2
    if v > 7 * 12:
        return 3
    if v > 5 * 12:
        return 4
    if v > 3 * 12:
        return 5
    if v > 2 * 12:
        return 6
    if v > 1 * 12:
        return 7
    if v > 9:
        return 8
    if v > 6:
        return 9
    if v > 0:
        return 10
    return 11
    # print(data)
    # gg
    if data["sixing"]:
        return 0
    if data["wuqi"]:
        return 1
    v = 0
    for x in data["youqi"]:
        v = max(x, v)
    for x in data["juyi"]:
        v = max(x, v)
    for x in data["guanzhi"]:
        v = max(x, v)
    if v > 25 * 12:
        return 2
    if v > 15 * 12:
        return 3
    if v > 10 * 12:
        return 4
    if v > 7 * 12:
        return 5
    if v > 5 * 12:
        return 6
    if v > 3 * 12:
        return 7
    if v > 2 * 12:
        return 8
    if v > 1 * 12:
        return 9
    if v > 9:
        return 10
    if v > 6:
        return 11
    if v > 0:
        return 12
    return 13


word_dict = {}


def get_word_vec(x, config):
    # if not (x in word_dict):
    #    word_dict[x] = torch.rand(config.getint("data", "vec_size"))
    vec = transformer.load(x)
    # print(type(vec))
    return vec

    # return word_dict[x], True


cnt1 = 0
cnt2 = 0


def parse_sentence(data, config):
    global cnt1, cnt2
    # data = data.split("\t")
    result = data
    if result is None:
        return False
    lastp = 0
    if len(result) == 0:
        return False

    if len(result) > config.getint("data", "sentence_num"):
        cnt1 += 1
        # print("cnt1 %d" % cnt1)
        return False
    for a in range(0, len(result)):
        if len(result[a]) > config.getint("data", "sentence_len"):
            cnt2 += 1
            # print("cnt2 %d" % cnt2)
            return False

    return True


def generate_vector(data, config):
    # data = parse_sentence(data, config)
    vec = []
    len_vec = [0, 0]
    for x in data:
        temp_vec = []
        len_vec.append(len(x))
        len_vec[1] += 1
        for y in x:
            len_vec[0] += 1
            z = get_word_vec(y, config)
            temp_vec.append(torch.from_numpy(z))
        while len(temp_vec) < config.getint("data", "sentence_len"):
            temp_vec.append(torch.from_numpy(transformer.load("BLANK")))
        vec.append(torch.stack(temp_vec))

    temp_vec = []
    while len(temp_vec) < config.getint("data", "sentence_len"):
        temp_vec.append(torch.from_numpy(transformer.load("BLANK")))

    while len(vec) < config.getint("data", "sentence_num"):
        vec.append(torch.stack(temp_vec))
        len_vec.append(1)
    if len_vec[1] > 32:
        gg
    for a in range(2, len(len_vec)):
        if len_vec[a] > 128:
            gg
    if len(len_vec) != 34:
        gg

    return torch.stack(vec), torch.LongTensor(len_vec)

    data = data.split("\t")
    vec = []
    for x in data:
        y = get_word_vec(x, config)
        vec.append(torch.from_numpy(y))
        if len(vec) == config.getint("data", "pad_length"):
            break
    len_vec = len(vec)
    while len(vec) < config.getint("data", "pad_length"):
        vec.append(torch.from_numpy(transformer.load("BLANK")))

    # print(torch.stack(vec))
    return torch.stack([torch.stack(vec)]), len_vec


def parse(data, config):
    label_list = config.get("data", "type_of_label").replace(" ", "").split(",")
    label = []
    for x in label_list:
        if x == "crit":
            label.append(analyze_crit(data["meta"]["crit"], config))
        if x == "law1":
            label.append(analyze_law1(data["meta"]["law"], config))
        if x == "law2":
            label.append(analyze_law2(data["meta"]["law"], config))
        if x == "time":
            label.append(analyze_time(data["meta"]["time"], config))
    # print(data)
    vector, len_vec = generate_vector(data["content"], config)
    # print(data)
    # print(vector)
    # print(len_vec)
    # print(label)
    return vector, len_vec, torch.LongTensor(label)


def check(data, config):
    if len(data["meta"]["crit"]) > 1 or len(data["meta"]["crit"]) == 0:
        return False
    if not (int(data["meta"]["crit"][0]) in accusation_dict):
        return False
    # if len(data["content"].split("\t")) > config.getint("data", "pad_length"):
    #    return False
    if not (parse_sentence(data["content"], config)):
        return False

    if not (check_law(data["meta"]["law"])):
        return False

    return True
