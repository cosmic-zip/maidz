from http.server import BaseHTTPRequestHandler, HTTPServer
import logging, json, os
from datetime import datetime
from urllib.parse import urlparse
from urllib.parse import parse_qs



class HttpHandler(BaseHTTPRequestHandler):
    def maid_log_for_me(self, log):
        log["datetime"] = str(datetime.now())

        url = log["path"]
        parsed_url = urlparse(url)
        captured_value = parse_qs(parsed_url.query)
        log["keys"] = dict(captured_value)
        print("captured_value", captured_value)

        parsed = json.dumps(log, indent=4, sort_keys=True)
        logging.info(parsed)

        f = open("apron/output/mitm_log.jsonl", "a")
        f.write(f"{parsed}\n")
        f.close()

    def set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self.maid_log_for_me(
            {
                "type": "GET",
                "path": str(self.path),
                "headers": str(self.headers),
            }
        )
        self.set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        self.maid_log_for_me(
            {
                "type": "POST",
                "path": str(self.path),
                "headers": str(self.headers),
                "body": post_data.decode('utf-8'),
            }
        )
        self.set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=HttpHandler, address="localhost" port=8000):
    logging.basicConfig(level=logging.INFO)
    server_address = (address, port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
