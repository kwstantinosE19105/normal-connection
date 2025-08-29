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
                    filename = filename_bytes.decode("utf-8",errors="strict")

                    #2)filesize (8-byte unsigned, big-endian)
                    (filesize,) = struct.unpack(!Q",recv_exact(conn,8))


                    #3)sha256 (32 bytes)
                    expected_sha256 = recv_exact(conn,32)

                    #4)file content (filesize bytes)
                    dest_path = SAVE_DIR / Path(filename).name # sanitize name
                    hasher = hashlib.sha256()
                    received = 0

                    with open(dest_path, "wb") as f:
                        while received < filesize:
                            chunk = conn.recv(min(1024 * 64, filesize - received))
                            if not chunk:
                                raise  ConnectionError("Connection dropped mid-file.)
                            f.write(chunk)
                            hasher.update(chunk)
                            received += len(chunk)
                                
                    actual_sha256 = hasher.digest()
                    if actual_sha256 == expected_sha256:
                        conn.sendall(b"OK")
                        print(f"saved {dest_path}({filesize} bytes) [OK]")
                    else:
                        conn.sendall(b"BAD_CHECKSUM")
                        print(f"Checksum mismatch for {dest_path}")
                

            except Exception as e:
                print(f"Error: {e}")
if__name__ == "__main__":
    main()


























