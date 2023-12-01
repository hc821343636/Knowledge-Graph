import csv
from AtoA import AtoA
#import torch
from ltp import LTP,StnSplit

# 默认 huggingface 下载，可能需要代理

if __name__ == '__main__':

    ltp = LTP("../base2")  # 默认加载 Small 模型
    atoa = AtoA(ltp)
    txt_file_path = '../data/冒号测试'
    txt = atoa.getTxt(txt_file_path=txt_file_path + '.txt')
    #print(txt)

    sents = StnSplit().split(txt)
    result = ltp.pipeline(sents, tasks=["cws", "srl"])
    print(result.srl)
