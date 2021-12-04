from pymysql import *
from config import *


class DB(object):

    def __init__(self):

        # 连接到数据库
        self.conn = connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_DATABASE,
            user=DB_USER,
            password=DB_PASSWORD,
            charset='utf8'
        )
        # 获取数据库游标
        self.cursor = self.conn.cursor()

    def close(self):
        # 关闭数据库
        self.conn.close()
        self.cursor.close()

    def get_one(self, sql):
        """

        :param sql: 待执行的sql语句
        """
        # 执行sql语句
        self.cursor.execute(sql)
        # 获取结果
        query_result = self.cursor.fetchone()
        # 判断是否有结果
        if not query_result:
            return NULL
        # 获取字段名称列表
        fileds = [filed[0] for filed in self.cursor.description]
        # 将字段名称和查询到的数据组合成字典，供返回使用
        return_data = {}
        for filed, value in zip(fileds, query_result):
            return_data[filed] = value

        return return_data

    def update_one(self, sql):
        """更改数据库信息"""

        # 执行sql语句
        self.cursor.execute(sql)
        # 返回状态码
        self.conn.commit()


if __name__ == '__main__':
    db = DB()
    # data = db.get_one("select * from users where user_name='瞿壮'")
    data = db.update_one("update users set user_nickname='七号技师很非常高兴为您服务' where user_name='瞿1壮'")
    db.close()
