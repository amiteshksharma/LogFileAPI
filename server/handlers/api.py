from tornado.web import RequestHandler
import json
import glob

class APIFileHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def post(self, path):
        full_path = self.get_argument("pathname")
        count = self.get_argument("count")

        int_count = 0
        try:
            int_count = int(count) * -1
        except ValueError: 
            self.write(json.dumps({'error': "Invalid value for the query parameter [ count ]"}))
            return
        
        p = full_path + "\\" + path
        f = open(p, 'r')
        text = f.read()
        f.close()

        if not count:
            data = json.dumps({'text': text})
        else:
            data = json.dumps({'text': text[int_count:]}) 
        self.write(data)

# Get all files from a specified path
class APIFileListHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def post(self, path=None):
        full_path = self.get_argument("pathname")
        
        l = []
        for f in glob.iglob(full_path+"/*.txt", recursive=True):
            l.append(f.split("\\")[-1])

        data = json.dumps({"file_list": l})
        self.write(data)
