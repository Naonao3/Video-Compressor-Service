import socket
import os
import json
import subprocess

def main():
    
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host = "localhost"
    port = 9001

    print("strating up on {} port {}".format(host,port))
    
    sock.bind((host,port))
    
    sock.listen(1)
    
    while True:
        connection, address = sock.accept()
        print("Connected to client: {}".format(address))
        try: 
            print("connection from {}".format(host))
            
            connection.send("Welcom to the program 'Video Compressor Service!".encode("utf-8"))
            
            data = connection.recv(1024).decode("utf-8")
            print(data)
 
            receivedData = json.loads(data)
            

            file_name = receivedData["file_name"]
            file_length = receivedData["file_length"]
            file_size = receivedData["file_size"]
            stream_rate = 4096
            
            print("Received file from client is: File name -> {}, File length => {}, File size -> {}".format(file_name,file_length,file_size))
            
            if file_size == 0:
                raise("No data to read from client.")
            
            
            with open(os.path.join(file_name), "wb+") as f:
                while file_size > 0:
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
