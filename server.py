#  coding: utf-8 
import socketserver, os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)  

        # tranfer the data to python readable 
        data_in_string = self.data.decode('utf-8')
        #print("data in string: ", data_in_string)

        request_command = data_in_string.split('\r\n')[0]
        #print("request command: ", request_command)

        command = request_command.split(' ')[0]
        #print("command: ", command,"++")

        Request_URI = request_command.split(' ')[1]
        #print("Request URI: ",Request_URI)

        path = " "

        if command == "GET":
            #print("GGGGGEt")
            # not css
            if "css" not in Request_URI:

                if "index.html" not in Request_URI:
                    if Request_URI[-1] == "/":
                        Request_URI = Request_URI + "index.html"
                    else:
                        ## return erro 301 
                        #print("301")
                        #print(f"HTTP/1.1 301 Moved Permanently\r\nLocation:{Request_URI +'/'}\r\n\r\n301 Moved Permanently",'utf-8')
                        self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation:" + Request_URI +'/' +"\r\n\r\n301 Moved Permanently",'utf-8'))
                        return
            path = "./www" + Request_URI
        else:
            #print("405")
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n\r\n405 Method Not Allowed",'utf-8'))
            return

        if ".html" in Request_URI:
            self.Test_web_server(path,"text/html")
        elif ".css" in Request_URI:
            self.Test_web_server(path,"text/css")


    def Test_web_server(self,path,type):
        #print("path: ",path)
        if os.path.exists(path):
           file = open(path,'r')
           data = file.read()
           #print("200",type)
           self.request.sendall(bytearray('HTTP/1.1 200 OK\r\n'+"Content-Type:" +type +"\r\n"  +"\r\n\r\n"+data,'utf-8'))
           return
        else:
            #print("404")
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n\r\n404 Not Found",'utf-8'))
            return




if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    # for the TCP server the first parameter is address and t
    # the second is request handler class 
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    # call the handler in infinite time
    server.serve_forever()
