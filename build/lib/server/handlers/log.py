from tornado.web import RequestHandler
import sqlite3 as sl
import glob
from pathlib import Path

con = sl.connect('datapaths.db')

# with con:
#     con.execute("""
#         CREATE TABLE DATAPATHS (
#             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#             paths TEXT
#         );
#     """)

# con.execute("DELETE FROM DATAPATHS")

class LogHandler(RequestHandler):

    def get(self):
        with con:
            paths = con.execute("SELECT * FROM DATAPATHS")

        self.render("log_view_list.html", file_paths=paths)

class LogViewHandler(RequestHandler):

    def post(self):
        # get the file names from the log folder
        path = self.get_body_argument('filepath')
        print(path)
        with con:
            data = con.execute("SELECT * FROM DATAPATHS WHERE paths = :f", {'f': path})
            if len(data.fetchall()) == 0:
                con.execute('INSERT INTO DATAPATHS (paths) values(?)', (path, ))
                self.write('Added successfully')
            else:
                self.write('Entry already exists!')
        
        con.commit()
    
    def get(self):
        paths = self.get_arguments("paths")[0]

        with con:
            data = con.execute("SELECT * FROM DATAPATHS WHERE paths = :f", {'f': paths})
            for row in data:
                path = row

        l = []
        for f in glob.iglob(path[1]+"/*.txt", recursive=True):
            l.append(f.split("/")[-1])

        self.render("logview.html", file_names=l)
