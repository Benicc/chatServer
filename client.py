from socket import *
import time
import sys
import threading


port = int(sys.argv[1])

address = ('localhost', port)

UdpSocket = socket(AF_INET, SOCK_DGRAM)

def refresh(UdpSocket=UdpSocket, address=address):
    UdpSocket.sendto("refresh".encode(), address)
    try:
        UdpSocket.settimeout(0.6)

        ack = UdpSocket.recv(1024).decode()
        print("CHAT ROOM")
        print("#######################")
        print(ack)
        print("Enter your message: ")
    except timeout:
        pass

def refresh_loop(UdpSocket=UdpSocket, address=address):
    while True:
        time.sleep(5)
        refresh(UdpSocket, address)

def udp_connection(UdpSocket=UdpSocket, address=address):

    #login user
    logged_in = False
    while not logged_in:
        username = input("Enter your name: ")

        login_request = f"login;;{username}"
        UdpSocket.sendto(login_request.encode(), address)
        
        try:
            UdpSocket.settimeout(0.6)

            ack = UdpSocket.recv(1024).decode()

            if ack == "200 OK":
                logged_in = True
                print("You have entered the chat say hello!!")
                refresh()
        except timeout:
            print("Connection Timed Out")

    #start refresh loop
    refresh_loop_thread.start()

    #ask for messages and send them to the server
    while True:
        message = input('')
        message_request = f"message;;{message}"
        UdpSocket.sendto(message_request.encode(), address)

        try:
            UdpSocket.settimeout(1)
            ack = UdpSocket.recv(1024).decode()
            if ack == "200 RECIEVED":
                refresh()
        except timeout:
            print("Connection Timed Out")



udp_thread = threading.Thread(target=udp_connection)
refresh_loop_thread = threading.Thread(target=refresh_loop)

udp_thread.start()

udp_thread.join()
refresh_loop_thread.join()

udp_connection()
