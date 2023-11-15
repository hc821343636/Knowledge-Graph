# -*- coding:utf-8 -*-
from neo4j import GraphDatabase
from py2neo import Graph, Node, Relationship
import pandas as pd
import csv
from tqdm import tqdm
# Neo4j数据库连接信息
uri = "bolt://localhost:7687"  # 替换为你的Neo4j数据库URI
username = "neo4j"  # 替换为你的数据库用户名
password = "12345678"  # 替换为你的数据库密码

# CSV文件路径
# csv_file_path = "output.csv"

# Cypher查询语句，根据你的数据模型进行调整
graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))
graph.delete_all()  # 清除neo4j中原有的结点等所有信息

# 创建结点
'''node1 = Node('person', name = 'chenjianbo')   #该结点语义类型是person  结点名字是chenjianbo  也是它的属性
node2 = Node('major',name = 'software')       #该结点语义类型是major  结点名字是software  也是它的属性
node3 = Node('person',name = 'bobo')          #该结点语义类型是person  结点名字是bobo   也是它的属性
node4= Node('person',name = 'bobo')
#给结点node1 添加一个属性 age
node1['age'] = 18
#给结点node2 添加一个属性 college
node2['college'] = 'software college'
#给结点node3 添加一个属性 sex
node3['sex'] = '男'

#把结点实例化 在Neo4j中显示出来
graph.create(node1)
graph.create(node4)
graph.create(node2)
graph.create(node3)
# 创建关系
maojor = Relationship(node1, '专业', node2)
friends = Relationship(node1, '朋友', node3)
maojor1 = Relationship(node3, '专业', node2)
#把关系实例化 在Neo4j中显示出来
graph.create(maojor)
graph.create(maojor1)
graph.create(friends)'''


def getEntitySet(filepath: str, columnIndex: int):
    # 读取CSV文件
    df = pd.read_csv(filepath, encoding='gb2312')

    # 获取第一列的值
    first_column = df.iloc[:, columnIndex]

    # 打印第一列的值
    print(set(first_column))


'''
filepath = 'output.csv'
getEntitySet(filepath,0)
'''


def get_node_count(uri, username, password, cypher_query):
    # 连接Neo4j数据库
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        # 打开会话
        with driver.session() as session:
            # 执行Cypher查询
            result = session.run(cypher_query)

            # 获取查询结果
            for record in result:
                node_count = record["node_count"]
                return node_count


# 读取 CSV 文件并创建节点和关系
def create_graph_from_csv(csv_file):
    created_nodes = {}
    with open(csv_file, 'r',encoding='gbk') as file:
        csv_reader = csv.reader(file)
        # 跳过表头
        next(csv_reader, None)

        for row in tqdm(csv_reader,position=0):
            # 获取节点的信息
            sender_name = row[0]
            action_name = row[1]
            receiver_name = row[2]
            #if action_name=='职责':
                #print('ll')
            # 检查节点是否已存在，如果不存在则创建
            sender_node = created_nodes.get(sender_name, Node("Person", name=sender_name))
            receiver_node = created_nodes.get(receiver_name, Node("Person", name=receiver_name))

            # 将节点添加到已创建的节点字典
            created_nodes[sender_name] = sender_node
            created_nodes[receiver_name] = receiver_node

            # 创建关系
            action_relationship = Relationship(sender_node, action_name, receiver_node)

            # 将节点和关系添加到图数据库
            graph.create(sender_node | receiver_node | action_relationship)

# 示例：使用包含节点关系信息的 CSV 文件
csv_file_path = '第一、二章小修.csv'
create_graph_from_csv(csv_file_path)
# 执行查询
'''
cypher_query = "MATCH (n) RETURN count(n) AS node_count"
node_count = get_node_count(uri, username, password, cypher_query)
print(f"当前节点数目: {node_count}")'''
