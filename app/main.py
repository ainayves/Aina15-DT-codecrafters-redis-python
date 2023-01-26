import socket


def main():
   
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    #server_socket.accept() # wait for client

    client, _ = server_socket.accept()  # wait for client
    client.sendall("+PONG\r\n".encode(encoding="UTF-8"))


if __name__ == "__main__":
    main()
