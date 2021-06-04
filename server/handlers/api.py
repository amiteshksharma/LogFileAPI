from tornado.web import RequestHandler
import json
import glob

class APIFileHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def post(self, path):
        full_path = self.get_argument("pathname")
        count = self.get_argument("count", None)
        lines = self.get_argument("lines", None)
        
        p = full_path + "\\" + path
        f = open(p, 'r')
        data = {}

        if (count) and (lines):
            self.write(json.dumps({'error': "Can't have both keys 'lines' and 'count'"}))
        elif lines:
            get_lines = f.readlines()
            f.close()
            int_lines = int(lines) * -1
            data = json.dumps({'text': get_lines[int_lines:]})     
        else:
            text = f.read()
            f.close()
            if count:
                int_count = int(count) * -1  
                data = json.dumps({'text': text[int_count:]}) 
            else:
                data = json.dumps({'text': text})
        
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
