import socket
import os
import json
from pathlib import Path
import subprocess

def main():
    
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_address = "0.0.0.0"
    server_port = 9001
    
    dpath = "temp"
    if not os.path.exists(dpath):
        os.makedirs(dpath)
    print("strating up on {} port {}".format(server_address,server_port))
        
    sock.bind((server_address,server_port))
    
    sock.listen(1)
    
    while True:
        connection, client_address = sock.accept()
        try: 
            print("connection from {}".format(client_address))
            
        
                
            connection.send("Starting program 'Video Compressor Service".encode("utf-8"))
            
            data = connection.recv(1024).decoe("utf-8")
                        
            receivedData = json.load(data)
            file_name = receivedData["file_name"]
            file_length = receivedData["file_length"]
            file_size = receivedData["file_size"]
            stream_rate = 4096
            
            print("Received file from client is: File name -> {}, File length => {}, File size -> {}".format(file_name,file_length,file_size))
            
            if file_size == 0:
                raise("No data to read from client.")
            
            with open(os.path.join(dpath,file_name), "wb+") as f:
                while file_length > 0:
                    data = connection.recv(file_size if file_size <= stream_rate else stream_rate)
                    
                    f.write(data)
                    file_size -= len(data)
                    
                    print("Finished downloading the file from clietn")
            connection.send("Upload finish".encode("utf-8"))

            while True:
                command = connection.recv(1024).decode("utf-8")
                command = command.split(" ")
                subprocess.run(command)

                connection.send("Process done! new file is ready.".encode("utf-8"))

                continue_question = connection.recv(1024).decode("utf-8")
                if continue_question == "0":
                    os.remove(file_name)
                    connection.send("Closed program 'Video Compressor Service".encode("utf-8"))
                    break
        
        except Exception as e:
            print("Error: " + str(e))
        
        finally:
            print("Closing current connection")
            connection.close()

if __name__ == "__main__":
    main()

