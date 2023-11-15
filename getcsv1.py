# -*- coding:utf-8 -*-
import csv

import torch
from ltp import LTP,StnSplit
from typing import List
from tqdm import tqdm

# 默认 huggingface 下载，可能需要代理




# 也可以传入模型的路径，ltp = LTP("/path/to/your/model")
# /path/to/your/model 应当存在 config.json 和其他模型文件
def getTxt(txt_file_path: str):
    # txt_file_path = '第一章.txt'

    # 打开文本文件
    with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
        # 读取文件内容
        file_content = txt_file.read()
        return file_content
    # 输出文件内容
    # print(file_content)


def srl_AtoA(sent):
    result = ltp.pipeline([sent], tasks=["cws", "srl"])
    #print(result.srl)
    result = result.srl
    triples = []
    for sentence in result:
        for frame in sentence:
            predicate = frame['predicate']
            a0, a1 = None, None
            for arg in frame['arguments']:
                if arg[0] == 'A0':
                    a0 = arg[1]
                elif arg[0] == 'A1':
                    a1 = arg[1]
            if a0 is not None and a1 is not None:
                triples.append((a0, predicate, a1))


    return triples
# 获取三元组
def getCsv(csv_file_path: str, sents: List[str]):
    #csv_file_path = 'output.csv'

    # 打开CSV文件，如果文件不存在会被创建，如果已存在会被覆盖

    # 将tuple数据写入CSV文件

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        for sent in tqdm(sents,position=0):
            result = srl_AtoA(sent)
            # 创建CSV写入器
            csv_writer.writerows(result)

if __name__ == '__main__':
    ltp = LTP()  # 默认加载 Small 模型
    txt_file_path='第一、二章'
    txt = getTxt(txt_file_path=txt_file_path+'.txt')
    sents = StnSplit().split(txt)
    getCsv(csv_file_path = f'{txt_file_path}hchchchch.csv',sents=sents)
