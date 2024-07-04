import json
import logging
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from core.core import puts, key_value

class HttpHandler(BaseHTTPRequestHandler):
    def maid_log_for_me(self, log):
        log["datetime"] = str(datetime.now())
        url = log["path"]
        parsed_url = urlparse(url)
        captured_value = parse_qs(parsed_url.query)
        log["keys"] = dict(captured_value)
        parsed = json.dumps(log, sort_keys=True)

        with open("data/output/mitm_log.jsonl", "a") as f:
            f.write(f"{parsed}\n")
            f.close()

        puts(f"captured values: {captured_value}", "yellow")
        print("")
        parsed = json.dumps(log, sort_keys=True, indent=4)
        puts(parsed, "yellow")
        print("")

    def set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
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
        self.wfile.write("GET request for {}".format(self.path).encode("utf-8"))

    def do_POST(self):
        content_length = int(
            self.headers["Content-Length"]
        )  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        self.maid_log_for_me(
            {
                "type": "POST",
                "path": str(self.path),
                "headers": str(self.headers),
                "body": post_data.decode("utf-8"),
            }
        )
        self.set_response()
        self.wfile.write("POST request for {}".format(self.path).encode("utf-8"))


def mint_server(args):
    server_class = HTTPServer
    handler_class = HttpHandler
    address = "localhost"
    port = 8000

    if key_value("address", args):
        address = key_value("address", args)

    if key_value("port", args):
        port = key_value("port", args)

    logging.basicConfig(level=logging.INFO)
    server_address = (address, port)
    httpd = server_class(server_address, handler_class)
    puts(f"Start server :: {address}:{port}", "green")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        puts(f"Stopping server :: {address}:{port}", "green")