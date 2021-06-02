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

class HomeHandler(RequestHandler):

    def get(self):
        self.render("home.html")

class LogHandler(RequestHandler):

    def get(self):
        with con:
            paths = con.execute("SELECT * FROM DATAPATHS")

        self.render("log_view_list.html", file_paths=paths)

class LogViewHandler(RequestHandler):

    def post(self):
        # get the file names from the log folder
        path = self.get_body_argument('filepath')

        with con:
            data = con.execute("SELECT * FROM DATAPATHS WHERE paths = :f", {'f': path})
            if len(data.fetchall()) == 0:
                con.execute('INSERT INTO DATAPATHS (paths) values(?)', (path, ))
                self.write('Added Successfully')
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

        self.render("log_view.html", file_names=l)

class LogViewFileHandler(RequestHandler):

    def get(self, path):
        p = self.get_argument("pathname")
        count = self.get_argument("count")

        # read the last 1000 characters of the file
        f = open(p, 'r')
        text = f.read()

        self.write(text[-1000:])

    
    def post(self, path):
        # current_file = self.get_argument("filename")
        p = self.get_argument("filepath")

        # open and read the file
        f = open(p, 'r')
        text = f.read()
        f.close()

        self.render("log_view_file.html",
            file_name=path,
            path_name=p,
            log_text=text
        )
