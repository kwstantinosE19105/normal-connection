import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socker.bind(("127.0.0.1",65432))
server_socket.listen()
print("Server is listening on 127.0.0.1:65432...")
