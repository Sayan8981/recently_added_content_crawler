import mysql.connector
import sys
import os

#import pdb;pdb.set_trace
class createdb:

    def __init__(self):

        self.username='root'
        self.passwd="root@123"
        self.IP_addr='localhost'
        self.database_name='recently_added_content_service_wise'
        self.db_list=[]
        self.connection=''
        self.cursor=''

    def user_input(self):
        #import pdb;pdb.set_trace()
        self.username=self.username
        self.password=self.passwd

    def set_up_db_connection(self):
        #import pdb;pdb.set_trace()
        self.connection=mysql.connector.connect(host=self.IP_addr,user="%s"%self.username,passwd="%s"%self.password)
        self.cursor=self.connection.cursor()    

    def create_require_db(self):
        self.user_input()
        self.set_up_db_connection()
        self.cursor.execute("show databases;")
        for db in self.cursor:
            self.db_list.append(db[0].encode())
        #import pdb;pdb.set_trace() 
        if self.database_name not in self.db_list:
            self.cursor.execute("create database %s;"%self.database_name)           
        else:
            print("%s db is already exist"%self.database_name)
        self.connection.close()        
                           



createdb().create_require_db()