from tornado.web import RequestHandler
import sqlite3 as sl
import tornado
import glob
import json

con = sl.connect('datapaths.db')

# with con:
#     con.execute("""
#         CREATE TABLE DATAPATHS (
#             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#             paths TEXT
#         );
#     """)

class LogHandler(RequestHandler):
    """Render the template for the loading page"""

    def get(self):
        """Handle a GET request to load the client-view application"""
        self.render("home.html")

class LogViewHandler(RequestHandler):
    """Render the template to view all log files available"""
    def post(self):
        # get the file names from the log folder
        path = self.get_body_argument('filepath')
        with con:
            data = con.execute("SELECT * FROM DATAPATHS WHERE paths = :f", {'f': path})
            if len(data.fetchall()) == 0:
                con.execute('INSERT INTO DATAPATHS (paths) values(?)', (path, ))
            
            

        """Handle a GET request to render all file names"""
        self.write('added successfully')
    
    def get(self):
        path = ''
        with con:
            data = con.execute("SELECT * FROM DATAPATHS")
            for row in data:
                path = row

        l = []
        for f in glob.iglob(path[1], recursive=True):
            # split the string to only get the file name, not the whole path
            l.append(f.split("/")[-1])
        
        self.render("logview.html", file_names=l)
