import socket, time
from enum import Enum
from _thread import *
import threading
print_lock = threading.Lock()

class Commands(Enum):
    ECHO = "ECHO\r"
    SET = "SET\r"
    GET = "GET\r"
    PX = "PX\r"
    UTF = "UTF-8"
    NILL = "$-1\r\n"
    OK = '+OK\r\n'
    PONG = "+PONG\r\n"


class Counter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()
        self.last_time = time.time()

    def increment(self):
        with self.lock:
            current_time = time.time()
            elapsed_time = current_time - self.last_time
            if elapsed_time >= 0.001:  # 1 millisecond
                self.count += 1
                self.last_time = current_time

    def get_count(self):
        with self.lock:
            return self.count

def counter_thread(counter):
    while True:
        counter.increment()

counter = Counter()


def threaded(c):
    key_value = {}
    
    while True:
        
        
        data = c.recv(1024).decode()
        if not data:
            break
        data_array = data.split("\n")
        
        
        if (Commands.ECHO.value in data_array or Commands.ECHO.value.lower() in data_array):
            resp = f"+{data_array[-2]}\n"
            c.send(resp.encode(encoding=Commands.UTF.value))

        elif (Commands.SET.value in data_array or Commands.SET.value.lower() in data_array):

            if (Commands.PX.value in data_array or Commands.PX.value.lower() in data_array):
                key_value[data_array[-8]] = (data_array[-6], data_array[-2])
                t = threading.Thread(target=counter_thread, args=(counter,), daemon=True)
                t.start()
                
                
            key_value[data_array[-4]] = data_array[-2]
    
            c.send(Commands.OK.value.encode(encoding=Commands.UTF.value))
        
        elif (Commands.GET.value in data_array or Commands.GET.value.lower() in data_array):
            
            
            reskey = data_array[-2].replace("\n"," ")
            
            if len(data_array) == 6 and reskey in key_value:

                
                if type(key_value[reskey]) is tuple:


                    if counter.get_count() > int(key_value[reskey][1].replace("\r","")):

                        c.send(Commands.NILL.value.encode(encoding=Commands.UTF.value))

                    else:

                        result = key_value[reskey][0].replace("\r","")
                        resp = f"+{result}\n"
                        c.send(resp.encode(encoding=Commands.UTF.value))
                    
                else:
                    
                    resp = f"+{key_value[reskey]}\n"
                    c.send(resp.encode(encoding=Commands.UTF.value))
            
            elif len(data_array) == 11 and data_array[-8].replace("\r"," ") in key_value :
                
                element = key_value[data_array[-8]][0]
                resp = f"+{element}\n"
                c.send(resp.encode(encoding=Commands.UTF.value))

            else:
                c.send("+key not found\r\n".encode(encoding=Commands.UTF.value))

        else:
            c.send(Commands.PONG.value.encode(encoding=Commands.UTF.value))
        
def main():
   
    server_socket = socket.create_server(("localhost", 6379), reuse_port=False)
    server_socket.listen()
    while True:
        client, _ = server_socket.accept()
        threading.Thread(target=threaded,args=(client,), daemon=True).start()
    
if __name__ == "__main__":
    main()
