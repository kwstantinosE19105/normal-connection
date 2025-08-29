import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socker.bind(("127.0.0.1",65432))
server_socket.listen()
print("Server is listening on 127.0.0.1:65432...")

conn, addr = server_socket.accept()
print(f"Connected by {addr})

while True:
    data = conn.recv(1024)
    if not data:
      break
    print("Client says:",data.decode())
    conn.sendall(b"Message received")

conn.close()
