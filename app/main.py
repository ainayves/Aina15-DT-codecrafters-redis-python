import socket
from _thread import *
import threading
print_lock = threading.Lock()

def threaded(c):
    while True:
        data = c.recv(1024).decode()
        if not data:
            break
        data_array = data.split("\n")

        if ("ECHO\r" in data_array or "echo\r" in data_array):
            resp = f"+{data_array[-2]}\n"
            c.send(resp.encode(encoding="UTF-8"))
        
        else:
            c.send("+PONG\r\n".encode(encoding="UTF-8"))
        
def main():
   
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    server_socket.listen()
    while True:
        client, _ = server_socket.accept()
        threading.Thread(target=threaded,args=(client,), daemon=True).start()
    
if __name__ == "__main__":
    main()
