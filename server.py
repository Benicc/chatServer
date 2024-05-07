from socket import *
import sys
import os
import threading


N_UDP_THREADS = 10

try:
    os.remove('messages.txt')
except FileNotFoundError:
    pass

port = int(sys.argv[1])

users = {
    #address:username
}


#Open a UdpSocket
UdpSocket = socket(AF_INET, SOCK_DGRAM) #create socket
UdpSocket.bind(('localhost', port))

def append_message(username, message):
    try:
        messages = open("messages.txt", 'a')
        messages.write(f"{username}: {message}\n")
        messages.close()
        return True
    except Exception:
        return False

def send_messages(UdpSocket, num_mesages, address):
    try:
        message_file = open("messages.txt", 'r')
        messages = message_file.readlines()
        messages_string = ''
        n_messages = len(messages)
        for count, message in enumerate(messages):
            if count > n_messages - num_mesages:
                messages_string = messages_string + message

        
        UdpSocket.sendto(messages_string.encode(), address)
    except FileNotFoundError:
        UdpSocket.sendto("There are no current messages".encode(), address)
    



def udp_connection(UdpSocket):
    while True:
        #get data from udp
        data, address = UdpSocket.recvfrom(1024)
        decode_data = data.decode().split(';;')

        if decode_data[0] == "login":
            print(f"Login request as {decode_data[1]} recieved from {address}.")
            users[address] = decode_data[1]
            print(users)
            UdpSocket.sendto("200 OK".encode(), address)

        if decode_data[0] == "message":
            if decode_data[1] != '' and \
                append_message(users[address], decode_data[1]):
                
                print(f"{users[address]}: {decode_data[1]}")
            UdpSocket.sendto("200 RECIEVED".encode(), address)

        if decode_data[0] == "refresh":
            send_messages(UdpSocket, 10, address)


cpu_threads = []

print("Server Listening...")

#set up udp threads
for i in range(N_UDP_THREADS):
    udp_thread = threading.Thread(target=udp_connection, args=(UdpSocket,))
    cpu_threads.append(udp_thread)

#start all the cpu threads
for cpu_thread in cpu_threads:
    cpu_thread.start()

#wait for all cpu threads to finish
for cpu_thread in cpu_threads:
    cpu_thread.join()


