import socket
import struct
import hashlib
from pathlib import Path

Host = "127.0.0.1"
PORT = 65432
SAVE_DIR = Path("uploads")
SAVE_DIR.mkdir(exist_ok=True)

def recv_exact(conn, n: int) -> bytes:
    """Receive exactly n bytes or raise ConnectionError."""
    buf = bytearray()
    while len(buf) < n:
        chunk = conn.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Connection Closed while receivibg data.")
        buf.extend(chunk)
    return bytes(buf)

def recv_prefixed_bytes(conn) -> bytes:
    """Receive a 4-byte big-endian length followed by that many bytes."""
    (length,) = struct.unpack("!I",recv)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        while TRUE:
            conn,addr = s.accept()
            print(f"Connected by {addr}")
            try:
                with conn:
                    #1)filename (len + bytes)
                    filename_bytes = recv_prefixed_bytes(conn)
                    filename = filename_bytes.decode("utf-8"
