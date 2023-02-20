import pprint

import requests
import json


class Train(object):
    def __init__(self, train_no='', emu_no='', train_type=''):    # emu_no应当仅包括数字，如5033
        self.TrainNO = train_no
        self.EMUNo = emu_no
        self.TrainType = train_type

    def GetInfoByTrnNo(self):
        try:
            url = f'https://api.moerail.ml/train/{self.TrainNO}'
            response = requests.get(url)
            response.raise_for_status()
            item_list = list()
            if json.loads(response.text):
                for item_dict in json.loads(response.text)[0:7]:
                    item_list.append(f'车次号：{item_dict["train_no"]}，车组号：{item_dict["emu_no"]}，时间：{item_dict["date"]}')
                return '\n'.join(item_list)
            else:
                return '访问异常，无车次车组信息或输入错误，请检查后重试\n'
        # except (IndexError, ValueError):
            # return '访问异常，无车次车组信息或输入错误，请检查后重试'
        except:
            return '访问异常，无车次车组信息或输入错误，请检查后重试\n'

    def GetInfoByEMUNo(self):
        try:
            url = f'https://api.moerail.ml/emu/{self.EMUNo}'
            response = requests.get(url)
            response.raise_for_status()
            item_list = list()
            if json.loads(response.text):
                for item_dict in json.loads(response.text)[0:7]:
                    item_list.append(f'车次号：{item_dict["train_no"]}，车组号：{item_dict["emu_no"]}，时间：{item_dict["date"]}')
                return '\n'.join(item_list)
            else:
                return '访问异常，无车次车组信息或输入错误，请检查后重试\n'
        # except (IndexError, ValueError):
            # return '访问异常，无车次车组信息或输入错误，请检查后重试'
        except:
            return '访问异常，无车次车组信息或输入错误，请检查后重试\n'

    def GetMatchInfo(self):
        try:
            url = f'http://passearch.info/emu.php?type=number&keyword={self.EMUNo}'
            response = requests.get(url=url)
            response.raise_for_status()
            sep1 = response.text.splitlines(keepends=False)[41].split(sep='</td><td>')    # sep1 and sep2 is list
            sep2 = list()
            sep3 = list()
            for item in sep1:
                items = item.split(sep='keyword=')
                for sep in items:
                    sep2.append(sep)
            for sepitem in sep2:
                if sepitem[0:2] != '<a' or sepitem[2:4] != '共有':
                    sep3.append(sepitem)
            MatchInfo = list()
            MatchInfo.append(f'检索到{sep1[0][11:12]}条相关信息')
            MatchInfo.append(f'')
            for i in range(0, int(sep1[0][11:12])):
                MatchInfo.append(f'车型：{sep3[1 + 10 * i].split(sep=">")[0]}')
                MatchInfo.append(f'车组号：{sep3[2 + 10 * i]}')
                MatchInfo.append(f'标识：{sep3[1 + 10 * i].split(sep=">")[0]}-{sep3[2 + 10 * i]}')
                MatchInfo.append(f'配属路局：{sep3[4 + 10 * i].split(sep=">")[0]}')
                MatchInfo.append(f'配属动车所：{sep3[6 + 10 * i].split(sep=">")[0]}')
                MatchInfo.append(f'生产方：{sep3[7 + 10 * i]}')
                MatchInfo.append(f'备注：{sep3[8 + 10 * i]}')
                MatchInfo.append(f'--------\n')

            return '\n'.join(MatchInfo)
        except (IndexError, ValueError):
            return '访问异常，无车组信息和配属信息。这可能是网络异常或输入错误，请检查后重试\n'
        except:
            return '访问异常，无车组信息和配属信息。这可能是网络异常或输入错误，请检查后重试\n'


# 不使用
def getinfo(num):
    url = f'http://passearch.info/emu.php?type=number&keyword={num}'
    response = requests.get(url=url)
    response.raise_for_status()                  # php文件的42行，逐行切片索引41
    gotinfo = response.text.splitlines(keepends=False)[41].split(sep='</td><td>')
    alist = list()
    for item in gotinfo:
        items = item.split(sep='keyword=')
        for sep in items:
            alist.append(sep)
    infolist = list()
    infolist.append(f'检索到{gotinfo[0][11:12]}条相关信息')
    for i in range(0, int(gotinfo[0][11:12])):        # 相关信息数
        infolist.append(f'车型：{gotinfo[0]}')
    with open('../testdoc/sep2.txt', 'w') as f:
        f.write('\n'.join(alist))

