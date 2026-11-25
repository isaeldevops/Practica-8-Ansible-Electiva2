import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


PAGE = """<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Practica 8 - Ansible y Docker</title>
  </head>
  <body>
    <main>
      <h1>Practica 8 - Ansible y Docker</h1>
      <p>Aplicacion web desplegada desde una imagen Docker con GitHub Actions.</p>
    </main>
  </body>
</html>
""".encode("utf-8")


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            body = b"ok\n"
            content_type = "text/plain; charset=utf-8"
        elif self.path == "/":
            body = PAGE
            content_type = "text/html; charset=utf-8"
        else:
            self.send_error(404)
            return

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


port = int(os.environ.get("PORT", "8080"))
ThreadingHTTPServer(("0.0.0.0", port), RequestHandler).serve_forever()
