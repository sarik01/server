import json
import socket
import sqlite3

import random
import string
import time

connection = sqlite3.connect(':memory:')
cursor = connection.cursor()

create_table_query = """CREATE TABLE IF NOT EXISTS user 
                                    (address text, number text)"""

cursor.execute(create_table_query)


def insert_data(user_address: str, number: str):
    insert_data_query = "INSERT INTO user VALUES (?, ?)"
    cursor.executemany(insert_data_query, [(str(user_address), str(number))])
    connection.commit()


def generate_alphanum_random_string(length: int) -> str:
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, length))
    return rand_string


def get_data(addr: tuple) -> str:
    insert_data(addr[0], generate_alphanum_random_string(10))
    user = cursor.execute(f'SELECT * FROM user WHERE address = "{addr[0]}"')
    data = []

    for i in user:
        data.append(i[1])
    request = f"\r\nHTTP/1.1 200 OK\r\nContent-Type: application/json\r\nConnection-Length: {len(str(data))}\r\nConnection: close"
    text = f'{request}\r\n\r\n{data}'
    return text


def start_server():
    # gethostname -> localhost, port = 10000
    HOST = ('localhost', 10000)
    NUMBER_OF_CLIENTS = 4

    # endpoint AF_INET -> ipv4, SOCK_STREAM -> TCP responses for port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Avoid timeout
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind!
    s.bind(HOST)

    # Listen incoming TCP connections
    s.listen(NUMBER_OF_CLIENTS)
    print('I am listening your connections!')

    # Waiting for connections!
    while 1:
        # accept() is to accept connection from client
        # conn -> client Socket
        # addr ->  Address of client
        conn, addr = s.accept()
        print('Connected-', addr)
        data = conn.recv(1024)
        print(data.decode('utf-8'))

        user = cursor.execute(f'SELECT * FROM user WHERE address = "{addr[0]}"')
        if user.fetchone():
            choice = random.choice([15, 30, 60])
            timer = time.sleep(choice)
            data = get_data(addr)
            res = json.dumps(data)
            conn.send(res.encode('UTF-8'))
            conn.close()
            print('Waiting for request!')

        else:
            gen_num = generate_alphanum_random_string(10)
            request = f"\r\nHTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(gen_num)}\r\nConnection: close"
            text = f'{request}\r\n\r\n["{gen_num}"]'
            insert_data(addr[0], gen_num)

            res = json.dumps(text)
            # send msg to client
            conn.send(res.encode('UTF-8'))
            conn.close()

            print('Waiting for request!')

        # # close connection
        conn.close()


if __name__ == '__main__':
    start_server()
