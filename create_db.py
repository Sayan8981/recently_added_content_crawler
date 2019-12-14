import mysql.connector
import sys
import os
import db_detail

#import pdb;pdb.set_trace
class createdb:

    def __init__(self):

        self.db_list=[]
        self.connection=''
        self.cursor=''

    def set_up_db_connection(self):
        #import pdb;pdb.set_trace()
        self.connection=mysql.connector.connect(host=db_detail.IP_addr,user="%s"%db_detail.username,passwd="%s"%db_detail.passwd)
        self.cursor=self.connection.cursor()    

    def create_require_db(self):
        self.set_up_db_connection()
        self.cursor.execute("show databases;")
        for db in self.cursor:
            self.db_list.append(db[0].encode())
        #import pdb;pdb.set_trace() 
        if db_detail.database_name not in self.db_list:
            self.cursor.execute("create database %s;"%db_detail.database_name)           
        else:
            print("%s db is already exist"%db_detail.database_name)
        self.connection.close() 
        self.cursor.close()       
                           



createdb().create_require_db()