import pymysql
import redis


host = "127.0.0.1"
port = 3306
user = "root"
password = "123456"
database = "klook"

redis_host = "127.0.0.1"
redis_port = 6379
redis_db = 0

class Comments:

    def __init__(self):
        # 创建数据库连接
        self.conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database)

        # 创建游标对象
        self.cursor = self.conn.cursor()

    def __del__(self):
        # 关闭游标对象
        self.cursor.close()

        # 关闭数据库连接
        self.conn.close()

    def insert(self, data):
        # 插入数据
        sql = """
        INSERT INTO `comments` (`activity_id`, `content`, `time`, `sentiment_score`)
        VALUES (%s, %s, %s, %s)
        """
        self.cursor.executemany(sql, data)

        # 提交事务
        self.conn.commit()



class RedisConn:
    def __init__(self):
        self.redis_conn = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True, charset='UTF-8', encoding='UTF-8')

    def __del__(self):
        # 关闭 Redis 连接
        self.redis_conn.close()
    def get_keys(self):
        return self.redis_conn.keys()

    def get_value(self,key):
        return self.redis_conn.get(key)

def main():
    r = RedisConn()
    c = Comments()
    all_key = r.get_keys()
    data = []
    r_data = {}
    for key in all_key:
        num = r.get_value(key)
        if len(r_data) > 20:
            l = [[k,v] for k,v in r_data.items()]
            min_k,min_v = min(l, key=lambda k:k[1])
            if num < min_v:
                continue
            else:
                r_data.pop(min_k)
                r_data[key] = num
        else:
            r_data[key] = num
    for k,v in r_data.items():
        data.append([k,v])
    c.insert(data)

if __name__ == '__main__':
    main()