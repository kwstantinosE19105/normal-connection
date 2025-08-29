import socket
import struct
import hashlib
from pathlib import Path

HOST = "127.0.0.1"
PORT = 65432

def send_prefix(sock,data:bytes):
    """Send a 4-byte big-endian length followed by bytes."""
    sock.sendall(struct.pack("!I",len(data)))
    sock.sendall(data)

def send_file(filepath: str):
  path = Path(filepath)
  if not path.is_file():
    raise FileNotFoundError(f"No such file: {filepath}")

  filesize = path.stat().st_size
  # Precompute sha256 to verify integrity on the server
  
  hasher = hashlib.sha256()
  with open(path,"rb") as f:
    for chuck in iter(lambda: f.read(1024 * 64),b""):
        hasher.update(chunk)
  file_hash = hasher.digest()

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST,PORT))
    print("Connected to {HOST}:{PORT}")
    #1)filename
    send_prefixed_bytes(sock, path.name.encode("utf-8))

    #2)filesize(8 bytes)
    sock.sendall(struct.pack("!Q",filesize))

    #3)sha256(32 bytes)
    sock.sendall(file_hash)

    #4)file content
    sent = 0
    with open(path, "rb") as f:
        while True:
          chunk = f.read(1024 * 64)
          if not chunk:
            break
          sock.sendall(chunk)
          sent += len(chunk)
     # simple inline progress
          print(f"\rSent {sent}/{filesize} bytes", end="")
    print()

    #Server response
    resp = sock.recv(1024).decode()
    if resp == "OK":
      print("✅ Upload complete and verified.")
    else:
      print("❌ Upload failed:", resp)

if __name__ == "__main__":
    # Example: change to any local file, e.g., "test.jpg"
    send_file("example.txt")
    





                                               
  
      
  














