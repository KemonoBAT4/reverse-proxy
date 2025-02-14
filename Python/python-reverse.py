import http.server
import socketserver
import urllib.request
import urllib.parse
import urllib.error

class ReverseProxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Define the backend server URL
        backend_url = 'http://localhost:8001'  # Change this to your backend server

        # Construct the full URL to forward the request to
        url = urllib.parse.urljoin(backend_url, self.path)

        try:
            # Forward the request to the backend server
            with urllib.request.urlopen(url) as response:
                # Read the response from the backend server
                content = response.read()
                self.send_response(response.getcode())
                self.send_header('Content-Type', response.headers.get('Content-Type'))
                self.end_headers()
                self.wfile.write(content)
        except urllib.error.HTTPError as e:
            self.send_error(e.code, e.reason)
        except Exception as e:
            self.send_error(500, str(e))

    def do_POST(self):
        # Define the backend server URL
        backend_url = 'http://localhost:8001'  # Change this to your backend server

        # Construct the full URL to forward the request to
        url = urllib.parse.urljoin(backend_url, self.path)

        # Read the content length and the body of the request
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            # Forward the request to the backend server
            req = urllib.request.Request(url, data=post_data, method='POST')
            with urllib.request.urlopen(req) as response:
                # Read the response from the backend server
                content = response.read()
                self.send_response(response.getcode())
                self.send_header('Content-Type', response.headers.get('Content-Type'))
                self.end_headers()
                self.wfile.write(content)
        except urllib.error.HTTPError as e:
            self.send_error(e.code, e.reason)
        except Exception as e:
            self.send_error(500, str(e))

if __name__ == '__main__':
    PORT = 8000
    with socketserver.TCPServer(("", PORT), ReverseProxy) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
