#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：pytestProject 
@File ：mysql_operate.py.py
@Author ：李永峰
@Date ：2021/11/3 9:27 
@Version：1.0
@Desc：mysql链接
"""
import pymysql
from public.log import logger
from public.read_data import ReadFileData


class MysqlDb:

    def __init__(self):
        db_conf = ReadFileData().get_mysql_config()
        # 通过字典拆包传递配置信息，建立数据库连接
        self.conn = pymysql.connect(**db_conf, autocommit=True)
        # 通过 cursor() 创建游标对象，并让查询结果以字典格式输出
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):  # 对象资源被释放时触发，在对象即将被删除时的最后操作
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()

    def execute_db(self, sql, data_type="str", num: bool = False):
        """
        查询数据
        @param sql: 查询sql
        @param data_type: str<默认返回一个值>、list、dict
        @param num: True 返回多个值、False 返回一个值
        @return: list
        """
        # 检查连接是否断开，如果断开就进行重连
        self.conn.ping()
        # 使用 execute() 执行sql
        self.cur.execute(sql)
        if "select" not in sql.lower():
            try:
                # 提交事务
                self.conn.commit()
            except Exception as e:
                logger.info("操作MySQL出现错误 ==>> 错误原因：{}".format(e))
                # 回滚所有更改
                self.conn.rollback()
                return
        # 使用 fetchall()/fetchone() 获取查询结果
        fetchall = self.cur.fetchone() if not num and data_type == "str" else self.cur.fetchall()
        if fetchall:
            if data_type == "str":
                data = list(fetchall.values())[0]
            else:
                data = fetchall
            return data


if __name__ == '__main__':
    db = MysqlDb()
    print(db.execute_db("SELECT u.username from `user` u LIMIT 1"))
