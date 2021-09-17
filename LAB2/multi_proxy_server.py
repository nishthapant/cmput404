#!/usr/bin/env python3
import socket, time, sys
from multiprocessing import Process

HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def get_remote_ip(host):
    print(f'getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Hostname could not be resolved')
        sys.exit()

    print(f'IP address of {host} is {remote_ip}')
    return remote_ip

def handle_request(conn, proxy_end):
    #send data
    full_data = conn.recv(BUFFER_SIZE)
    print(f'Sending receiverd data {full_data} to Google')
    proxy_end.sendall(full_data)

    #shut down
    proxy_end.shutdown(socket.SHUT_WR)

    data = proxy_end.recv(BUFFER_SIZE)
    print(f'Sending received data {data} to client')

    #send data back
    conn.sendall(data)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

def main():
# establish localhost, extern_host(google), port, buffer size
    extern_host = "www.google.com"
    port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        # bind and set to listening mode
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)

        while True:
            # accept incoming connections from proxy_start, print information about connection
            conn, addr = proxy_start.accept()
            print("Connected by", addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                # get remote ip of google, connect proxy_end to it
                remote_ip = get_remote_ip(extern_host)
                proxy_end.connect((remote_ip, port))

                # allow for multiple connections with a Process daemon
                p = Process(target=handle_request, args=(conn, proxy_end))
                p.daemon = True
                p.start()
                print("Started process", p)

            # close the connection.
            conn.close()

if __name__ == "__main__":
    main()