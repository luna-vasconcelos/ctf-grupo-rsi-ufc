import socketserver

BANNER = (
    b"== simple tcp chat ==\n"
    b"type something and hit enter; 'quit' to exit\n\n"
)

class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        # greet on connect
        self.wfile.write(BANNER)
        self.wfile.flush()

        for line in self.rfile:
            msg = line.strip().decode(errors="ignore")
            if not msg:
                continue
            if msg.lower() in ("quit", "exit"):
                self.wfile.write(b"bye\n")
                self.wfile.flush()
                break
            self.wfile.write(f"echo: {msg}\n".encode())
            self.wfile.flush()

if __name__ == "__main__":
    with socketserver.ThreadingTCPServer(("0.0.0.0", 1337), Handler) as srv:
        srv.allow_reuse_address = True
        srv.serve_forever()
