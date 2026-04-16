import http.server
import socketserver
import os

PORT = 25147
FILE_NAME = "a.sk"

class InstantDownloadHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print("Request path:", self.path)
        if self.path in ["/", "/" + FILE_NAME]:
            try:
                with open(FILE_NAME, 'rb') as f:
                    self.send_response(200)
                    self.send_header("Content-Disposition", f"attachment; filename={FILE_NAME}")
                    self.send_header("Content-type", "application/octet-stream")
                    self.send_header("Content-Length", str(os.path.getsize(FILE_NAME)))
                    self.end_headers()
                    self.wfile.write(f.read())
            except Exception as e:
                self.send_error(500, f"Error reading file: {e}")
        else:
            self.send_error(404, "File not found.")

with socketserver.TCPServer(("", PORT), InstantDownloadHandler) as httpd:
    print(f"Serving {FILE_NAME} on port {PORT}...")
    httpd.serve_forever()
