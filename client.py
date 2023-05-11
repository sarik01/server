import socket
import json

def client_start():
    HOST = ('localhost', 10000)
    try:
        # endpoint AF_INET -> ipv4, SOCK_STREAM -> TCP responses for port
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(HOST)
        print('Connected to ', HOST)

        request = f"\r\nHTTP/1.1 200 OK".encode('utf-8')
        request_byte = bytes(request)

        client.sendall(request_byte)
        print('Sent msg!')

        msg = ''
        while 1:

            data = client.recv(8)
            msg += data.decode('UTF-8')
            if not len(data):
                break

        json_load = json.loads(msg)
        print(json_load)
    except ConnectionError:
        print('Connection is Interrupted!')


if __name__ == '__main__':
    client_start()