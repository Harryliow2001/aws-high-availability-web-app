from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import socket


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        hostname = socket.gethostname()

        message = f"""
        <html>
        <head>
            <title>AWS High Availability Web App</title>
        </head>
        <body>
            <h1>AWS High Availability Web Application</h1>
            <p>Deployed with GitHub Actions CI/CD version 2</p>
            <p>Server: {hostname}</p>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(message.encode())


server = ThreadingHTTPServer(("0.0.0.0", 80), Handler)

print("Server running on port 80...")
server.serve_forever()
