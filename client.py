import socket
import os
import json
import sys


def main():
    
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host = "localhost"
    port = 9001
    
    print('connecting to {}'.format(host))
    
    try:
        sock.connect((host,port))
    except socket.error as err:
        print(err)
        sys.exit(1)
    
    try:
        print(sock.recv(1024).decode("utf-8"))

        filepath = input("Type in a file to upload --> ")
        
        with open(filepath,"rb") as f:

            f.seek(0,os.SEEK_END)
            file_size = f.tell()
            f.seek(0,0)
            
            if file_size > pow(2,32):
                raise Exception("File must be below 2GB.")
            
            file_name = os.path.basename(f.name)

            if file_name[-3:] != "mp4":
                raise Exception("File must be `mp4'.")
            
            data_json ={
                "file_name":file_name,
                "file_length": len(file_name),
                "file_size": file_size
            }
            
            sock.send(json.dumps(data_json).encode("utf-8"))
            
            data = f.read(1400)
            print("Sending....")

            while data:
                
                sock.send(data)
                data = f.read(1400)
    
        while True:
            select_service = input("Please select service from 1 to 5...\n" + \
                                    "1 --> compress video file\n" + \
                                    "2 --> change video resolution\n" + \
                                    "3 --> change the video aspect ration\n" + \
                                    "4 --> conver video to audio\n" + \
                                    "5 --> create Gif from video\n")
            if select_service == 1:
                compression_level = input("Please select compression level from 1 to 3...\n" + \
                                        "1 --> high\n" + \
                                        "2 --> medium\n" + \
                                        "3 --> low\n")
                if compression_level == 1:
                    command = "ffmpeg -i " + file_name + "-c:v libx265 -b:v output/output_high.mp4"
                elif compression_level == 2:
                    command =  "ffmpeg -i " + file_name + "-c:v libx265 output/output_medium.mp4"
                elif compression_level == 3:
                    command = "ffmpeg -i " + file_name + "-c:v libx264 output/output_low.mp4"
                else:
                    print("Please select from 1 to 3")
            
            elif select_service == 2:
                print("Please input width and height.\n" + \
                    "For example \n" + \
                    "8K -> width:7680, height:4320\n" + \
                    "4k ->width:3840, height:2160\n")
                width = input ("Please input the width --> ")
                height = input("Please input the height -- > ")
                command = "ffmpeg -i " + file_name + " -s " +  width + ":" + height + " output/output_resolution.mp4"
            
            elif select_service == 3:
                height = input('Please enter the height --> ')
                width = input('Please enter the width --> ')
                command = 'ffmpeg -i ' + file_name + ' -pix_fmt yuv420p -aspect ' + height + ':' + width + ' output/output_aspect.mp4'
            
            elif select_service == '4':
                    command = 'ffmpeg -i ' + file_name + ' -vn output/output_audio.mp3'

            elif select_service == '4':
                start = input('Input start position (ex. 00:00:20) --> ')
                end = input('Input end position (ex. 10) --> ')
                flamerate = input('Input flame rate (ex. 10) --> ')
                resize = input('Input resize (ex. 300) : ')
                command = 'ffmpeg -ss ' + start + ' -i ' + file_name + ' -to ' + end + ' -r ' + flamerate + ' -vf scale=' + \
                    resize + ':-1 output/output_gif.gif'
            
            else:
                print("Please input from 1 to 5")
            
            sock.send(command.encode("utf-8"))
            
            print(sock.recv(1024).decode("utf-8"))

                
            continue_question = input('Do you want to continue ?\n' + \
                                    '0 : No\n' + \
                                    '1 : Yes\n')
                
            sock.send(continue_question.encode("utf-8"))
            
            if continue_question == "0":
                print(sock.recv(1024).decode("utf-8"))
                break
                

    finally:
        print("Closing socket")
        sock.close()

if __name__ == "__main__":
    main()
