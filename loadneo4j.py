from neo4j import GraphDatabase
from py2neo import Graph, Node, Relationship
import pandas as pd
import csv
from tqdm import tqdm

uri = "bolt://localhost:7687"  # 替换为你的Neo4j数据库URI
username = "neo4j"  # 替换为你的数据库用户名
password = "12345678"  # 替换为你的数据库密码
<<<<<<< HEAD
name='neo4j1113'
graph = Graph(uri, auth=(username, password),name=name)
=======

graph = Graph(uri, auth=(username, password))
>>>>>>> 1778416 (mac第二次提交)
graph.delete_all()  # 清除neo4j中原有的结点等所有信息


def create_graph_from_csv(csv_file):
    created_nodes = {}

    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        # 跳过表头
        next(csv_reader, None)

        for row in tqdm(csv_reader, position=0):
            sender_name, action_name, receiver_name, sender_number, receiver_number = row[:5]

            # 检查节点是否已存在，如果不存在则创建
            if action_name=='_':
                nodetype='Conjunction'
            else:
                nodetype='Person'
            sender_node = created_nodes.get(sender_number, Node('Person', name=sender_name, number=sender_number))
            receiver_node = created_nodes.get(receiver_number,
                                              Node(nodetype, name=receiver_name, number=receiver_number))

            # 将节点添加到已创建的节点字典
            created_nodes[sender_number] = sender_node
            created_nodes[receiver_number] = receiver_node

            # 创建关系
            action_relationship = Relationship(sender_node, action_name, receiver_node)

            # 将节点和关系添加到图数据库
            graph.create(sender_node | receiver_node | action_relationship)
        print(created_nodes)


# 示例：使用包含节点关系信息的 CSV 文件
<<<<<<< HEAD
csv_file_path = '../data/mainoutputassign_numbers.csv'
=======
csv_file_path = 'output_file.csv'
>>>>>>> 1778416 (mac第二次提交)
create_graph_from_csv(csv_file_path)
