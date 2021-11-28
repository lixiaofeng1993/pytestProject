#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：pytestProject 
@File ：oracle_operate.py.py
@Author ：李永峰
@Date ：2021/11/3 9:39 
@Version：1.0
@Desc：oracle链接
"""
import cx_Oracle
from public.read_data import ReadFileData


class OracleDb:

    def __init__(self):
        # 通过字典拆包传递配置信息，建立数据库连接
        db_conf = ReadFileData().get_oracle_config()
        self.conn = cx_Oracle.connect(
            user=db_conf.get("user"),
            password=db_conf.get("password"),
            dsn=db_conf.get("dsn"),
            encoding="UTF-8"
        )
        # 通过 cursor() 创建游标对象
        self.cur = self.conn.cursor()

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
                return
            except cx_Oracle.DatabaseError as error:
                # 回滚所有更改
                self.conn.rollback()
                msg = f"操作Oracle出现错误 ==>> 错误原因：{error}"
                raise cx_Oracle.DatabaseError(msg)
        # 使用 fetchall()/fetchone() 获取查询结果
        fetchall = self.cur.fetchone() if not num and data_type == "str" else self.cur.fetchall()
        if data_type == "dict":
            date = dict()
            # self.cur.description 列名
            cols = [d[0] for d in self.cur.description]
            for row in fetchall:
                date.update(dict(zip(cols, row)))
        elif data_type == "list":
            date = list()
            for row in fetchall:
                if isinstance(row, tuple):
                    date.append(row[0])
        else:
            date = fetchall[0]
        return date
