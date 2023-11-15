# 指定文本文件路径
txt_file_path = '第一章.txt'

# 打开文本文件
with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
    # 读取文件内容
    file_content = txt_file.read()

# 输出文件内容
print(file_content)
