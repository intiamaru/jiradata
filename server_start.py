import tornado.ioloop
import tornado.web
import os.path
import json
import bson.json_util
from bson.objectid import ObjectId
from pymongo import MongoClient
#Developer Jorge Boneu Libert

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("This is SNG General purpose API")

class ApiHandler(tornado.web.RequestHandler):
    def get(self, text):
        values = []
        client = MongoClient('mongodb://jorgeboneu:4343870@kahana.mongohq.com:10084/HLDB')
        db = client['HLDB']
        id = None
        elems = text.split('/')
        elem = elems[0]
        if len(elems) > 1:
          id = elems[1]
        
        collection = db[elem]
        print('id = '+str(elem))
	elems = text.split('/')
        if id == None:
          for item in collection.find({}).limit(100):
            values.append(item)
          self.write(json.dumps(values, default=bson.json_util.default))
        else:
          for item in collection.find({'_id':ObjectId(id)}).limit(100):
            values.append(item)
          self.write(json.dumps(values, default=bson.json_util.default))

        
    def post(self, elem):
        client = MongoClient('mongodb://jorgeboneu:4343870@kahana.mongohq.com:10084/HLDB')
        db = client['HLDB']
        print(self.request.body)
        input = json.loads(self.request.body)
        collection = db[elem]
        post_id = collection.insert(input)
        
        self.write('{"ok":"' + str(post_id) +  '"}')
        #self.write(self.request.body)

class QueryHandler(tornado.web.RequestHandler):
    def get(self, text):
        values = []
        client = MongoClient('mongodb://jorgeboneu:4343870@kahana.mongohq.com:10084/HLDB')
        db = client['HLDB']
        id = None
        elems = text.split('/')
        elem = elems[0]
        if len(elems) > 1:
          id = elems[1]
        
        collection = db[elem]
        print('id = '+str(elem))
        elems = text.split('/')
        for item in collection.find({'_id':ObjectId(id)}).limit(100):
          values.append(item)
        self.write(json.dumps(values, default=bson.json_util.default))

        
    def post(self, elem):
        client = MongoClient('mongodb://jorgeboneu:4343870@kahana.mongohq.com:10084/HLDB')
        values = []
        db = client['HLDB']
        print(self.request.body)
        input = json.loads(self.request.body)
        
        collection = db[elem]
        print('id = '+str(elem))
        #elems = text.split('/')
        for item in collection.find(input).limit(100):
          values.append(item)
        self.write(json.dumps(values, default=bson.json_util.default))
        #self.write(self.request.body)
		

static_path=os.path.join(os.path.dirname(__file__), "front")
application = tornado.web.Application(
    [
        (r"/", MainHandler),
        (r"/api/(.*)", ApiHandler),
        (r"/query/(.*)", QueryHandler),
        (r'/(.*)', tornado.web.StaticFileHandler, {'path': static_path}),
    ],
    )

if __name__ == "__main__":
    application.listen(9999)
    print "Tornado listening in port 9999"
    tornado.ioloop.IOLoop.instance().start()
