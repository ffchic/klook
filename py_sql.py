import pymysql


"""
CREATE TABLE `comments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `activity_id` INT  COMMENT '活动 ID',
  `content` TEXT  COMMENT '评论内容',
  `time` TEXT  COMMENT '评论时间',
  `sentiment_score` FLOAT COMMENT '情感得分',
  PRIMARY KEY (`id`)
);


-- 创建分词表
CREATE TABLE `words` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `word` VARCHAR(255) NOT NULL COMMENT '词语',
  `num` INT NOT NULL COMMENT '词语数量',
  PRIMARY KEY (`id`)
);

CREATE TABLE `scenic_spots` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `activity_id` INT  COMMENT '活动 ID',
  `title` TEXT  COMMENT '标题',
  `price` FLOAT  COMMENT '价格',
  `tags` TEXT  COMMENT '标签',
  `score` FLOAT  COMMENT '打分',
  `score_num` INT  COMMENT '打分人数',
  `heat` INT  COMMENT '热度',
  PRIMARY KEY (`id`)
);


"""

host = "127.0.0.1"
port = 3306
user = "root"
password = "123456"
database = "klook"

class Words:
    def __init__(self):
        """
        初始化数据库连接
        """
        self.conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
        self.cursor = self.conn.cursor()

    def __del__(self):
        """
        关闭数据库连接
        """
        self.cursor.close()
        self.conn.close()

    def insert(self, word, num):
        # 插入数据
        sql = """
        INSERT INTO `words` (`word`, `num`)
        VALUES (%s, %s)
        """
        self.cursor.execute(sql, (word, num))

        # 提交事务
        self.conn.commit()

    def update(self, word, num):
        # 更新数据
        sql = """
        UPDATE `words`
        SET `num` = %s
        WHERE `word` = %s
        """
        self.cursor.execute(sql, (num, word))

        # 提交事务
        self.conn.commit()

    def select(self):
        # 查询数据
        sql = "SELECT word, num FROM `words` "
        self.cursor.execute(sql)

        # 返回查询结果
        return self.cursor.fetchall()

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

    def delete(self, id):
        # 删除数据
        sql = "DELETE FROM `comments` WHERE `id` = ?"
        self.cursor.execute(sql, (id,))

        # 提交事务
        self.conn.commit()

    def update(self, id, activity_id, content, time, sentiment_score):
        # 更新数据
        sql = """
        UPDATE `comments`
        SET `activity_id` = %s, `content` = %s, `time` = %s, `sentiment_score` = %s
        WHERE `id` = %s
        """
        self.cursor.execute(sql, (activity_id, content, time, sentiment_score, id))

        # 提交事务
        self.conn.commit()

    def select(self, id=None):
        # 查询数据
        if id is None:
            sql = "SELECT * FROM `comments`"
        else:
            sql = "SELECT * FROM `comments` WHERE `id` = ?"
        self.cursor.execute(sql, (id,))

        # 返回查询结果
        return self.cursor.fetchall()

class ScenicSpots:

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

    def insert(self, activity_id, title, price, tags, score, score_num, heat):
        # 插入数据
        sql = """
        INSERT INTO `scenic_spots` (`activity_id`, `title`, `price`, `tags`, `score`, `score_num`, `heat`)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (activity_id, title, price, tags, score, score_num, heat))

        # 提交事务
        self.conn.commit()