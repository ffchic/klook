import pymysql
import re
import jieba

def stop_words(path):
    with open(path,'r',encoding='utf-8',errors='ignore') as f:
        return[l.strip() for l in f]

def fenci(text):
    return list(jieba.cut(text))


def remove_punctuation(text):
    punc = r'[^\w\s]'
    text = re.sub(punc,'',text)
    return text


# 数据库配置
config = {
    'host': 'localhost',   # 主机名
    'port': 3306,          # 端口号
    'user': 'root',        # 用户名
    'password': 'root',    # 密码
    'database': 'jd_spider',  # 数据库名
    'charset': 'utf8mb4',     # 设置编码为 utf8mb4
}

# 创建连接
connection = pymysql.connect(**config)

try:
    # 创建游标对象
    with connection.cursor() as cursor:
        # SQL 查询语句
        sql = "SELECT content FROM jd_comment limit 1000;"

        # 执行SQL语句
        cursor.execute(sql)

        # 获取查询结果
        result = cursor.fetchall()
        resp = {}
        # 打印结果
        for row in result:
            text = remove_punctuation(row[0])
            for i in fenci(text):
                if i in resp:
                    resp[i] = resp[i]+1
                else:
                    resp[i] = 1
        content = stop_words('/opt/jd_spider/stopworlds.txt')
        print(content)
        for k,v in resp.items():
            if k in content or len(k) <= 1:
                continue
            sqla = f"insert into part(part,count) values('{k}',{v})"
            cursor.execute(sqla)
            connection.commit()

finally:
    # 关闭数据库连接
    connection.close()
