import socket
from _thread import *
import threading
print_lock = threading.Lock()

def threaded(c):
    key_value = {}
    while True:
        
        data = c.recv(1024).decode()
        if not data:
            break
        data_array = data.split("\n")
        
        print(data_array)
        if ("ECHO\r" in data_array or "echo\r" in data_array):
            resp = f"+{data_array[-2]}\n"
            c.send(resp.encode(encoding="UTF-8"))

        elif ("SET\r" in data_array or "set\r" in data_array):
            
            key_value[data_array[-4]] = data_array[-2]
            c.send('+OK\r\n'.encode(encoding="UTF-8"))
        
        elif ("GET\r" in data_array or "get\r" in data_array):
            print(key_value)
            if(data_array[-2].replace("\n"," ") in key_value):
                resp = f"+{key_value[data_array[-2]]}\n"
                c.send(resp.encode(encoding="UTF-8"))
            else:
                c.send("+key not found\r\n".encode(encoding="UTF-8"))

        else:
            c.send("+PONG\r\n".encode(encoding="UTF-8"))
        
def main():
   
    server_socket = socket.create_server(("localhost", 6379), reuse_port=False)
    server_socket.listen()
    while True:
        client, _ = server_socket.accept()
        threading.Thread(target=threaded,args=(client,), daemon=True).start()
    
if __name__ == "__main__":
    main()
