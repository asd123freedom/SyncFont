#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi
import urlparse
import os
import base64

PORT_NUMBER = 8888

#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):

    #Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.parseUrl()
        self.wfile.write("We are ready!")

    def writeBase64File(self, str, filePath):
        f = open(filePath, "w")
        new_content = base64.decodestring(str)
        f.write(new_content)
        f.close()


    def do_POST(self):
        startIndex = self.path.index('fonteditor')
        endIndex = startIndex + len('fonteditor')
        pathName = self.path[startIndex:endIndex]
        query = urlparse.urlparse(self.path).query
        queryResult = urlparse.parse_qs(query)
        fontFile = queryResult['filepath'][0]
        fontPath = os.path.dirname(os.path.realpath(__file__)) + '/' + fontFile
        fontdir = os.path.dirname(fontPath)

        if pathName=="fonteditor" and (len(fontFile) > 0):

            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
            })
            fontName = form["fontName"].value
            fontType = form["fontType"].value
            fontType = fontType.split(",")
            for item in fontType:
                self.writeBase64File(form[item].value, fontdir + '/' + fontName + '.' + item)

            self.send_response(200)
            self.end_headers()
            self.wfile.write("Success!")
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write("Wrong path")

try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER

    #Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
