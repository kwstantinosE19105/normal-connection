import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1",65432))
client_socket.sendall(b"Hello, Server!")
data = client_socket.recv(1024)
print("server says:",data.decode())
client_socket.close()
