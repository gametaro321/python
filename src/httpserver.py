# -*- coding: utf-8 -*-
import cgi
import json
import http.server as s
from urllib.parse import urlparse
from urllib.parse import parse_qs

class MyHandler(s.BaseHTTPRequestHandler):

    def do_GET(self):
        self.make_data()
    def do_POST(self):
        self.make_data()

    def make_data(self):
        # urlパラメータを取得
        parsed = urlparse(self.path)
        # urlパラメータを解析
        params = parse_qs(parsed.query)
        # body部を取得
        A=self.headers.get("content-length")
        if self.headers.get("content-length") is not None:
            content_len  = int(self.headers.get("content-length"))
            req_body = self.rfile.read(content_len).decode("utf-8")
            # 返信を組み立て
            body  = "method: " + str(self.command) + "\n"
            body += "params: " + str(params) + "\n"
            body += "body  : " + req_body + "\n"
            self.wfile.write(body.encode())
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        if self.headers.get("content-length") is not None:
            self.send_header('Content-length', len(body.encode()))
        
        self.end_headers()
        
if __name__ == '__main__':
    
    server_address = ('127.0.0.1', 8000)
    httpd = s.HTTPServer(server_address, MyHandler)
    print('Serving HTTP on 0.0.0.0 port %d ...' % server_address[1])
    print('use <Ctrl-(C or break)> to stop')
    httpd.serve_forever()