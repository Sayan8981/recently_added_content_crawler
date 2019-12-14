import mysql.connector
import sys
import os
import db_detail
import datetime
import csv
from datetime import datetime,timedelta

class db_output_stats:

    def __init__(self):
        
        self.db_list=[]
        self.connection=''
        self.cursor=''
        self.fieldnames=["title","Show_type","Source","Subscription","content_type","Added_to_site","Updated_at_DB"]

    def set_up_db_connection(self):
        #import pdb;pdb.set_trace()
        self.connection=mysql.connector.connect(host=db_detail.IP_addr,user="%s"%db_detail.username,passwd="%s"%db_detail.passwd,db=db_detail.database_name)
        self.cursor=self.connection.cursor()     

    #TODO: creating file for writing
    def create_csv(self,result_sheet):
        if (os.path.isfile(os.getcwd()+result_sheet)):
            os.remove(os.getcwd()+result_sheet)
        csv.register_dialect('csv',lineterminator = '\n',skipinitialspace=True,escapechar='')
        output_file=open(os.getcwd()+result_sheet,"wa")
        return output_file

    def main(self):
        #import pdb;pdb.set_trace()
        self.set_up_db_connection()
        result_sheet='/attachments/recently_added_content_%s.csv'%(datetime.now().strftime('%b %d, %Y'))
        output_file=self.create_csv(result_sheet)
        
        with output_file as outputcsvfile:
            self.writer= csv.writer(outputcsvfile,dialect="csv",lineterminator = '\n')
            self.writer.writerow(self.fieldnames)
            query="select * from crawler_model_recent_content where Added_to_site='%s'"
            self.cursor.execute(query%(datetime.now() - timedelta(days=1)).strftime('%b %d, %Y'))
            result=self.cursor.fetchall()
            self.writer.writerows(result)

        output_file.close()
        self.connection.close() 
        self.cursor.close()   


db_output_stats().main()  



