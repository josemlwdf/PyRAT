# Made by josemlwdf@github.com
# Pyrat.py is a "python RAT tool" designed to be used on CTF

import socket
import sys
from io import StringIO
import datetime
import os
import multiprocessing

manager = multiprocessing.Manager()
admins = manager.list()


def handle_client(client_socket, client_address):
    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                # Client disconnected
                break
            if is_http(data):
                send_data(client_socket, fake_http())
                continue

            switch_case(client_socket, str(data).strip())
    except:
        pass
    
    remove_socket(client_socket)


def switch_case(client_socket, data):
    if data == 'admin':
        get_admin(client_socket)
    else:
        # Check socket is admin and downgrade if is not aprooved
        uid = os.getuid()
        if (uid == 0) and (str(client_socket) not in admins):
            change_uid()
        if data == 'shell':
            shell(client_socket)
            remove_socket(client_socket)
        else:
            exec_python(client_socket, data)


# Tries to execute the random data with Python
def exec_python(client_socket, data):
    try:
        print(str(client_socket) + " : " + str(data))
        # Redirect stdout to capture the printed output
        captured_output = StringIO()
        sys.stdout = captured_output

        # Execute the received data as code
        exec(data)

        # Get the captured output
        exec_output = captured_output.getvalue()

        # Send the result back to the client
        send_data(client_socket, exec_output)
    except Exception as e:
        # Send the exception message back to the client
        send_data(client_socket, e)
    finally:
        # Reset stdout to the default
        sys.stdout = sys.__stdout__


# Handles the Admin endpoint
def get_admin(client_socket):
    global admins

    uid = os.getuid()
    if (uid != 0):
        send_data(client_socket, "Start a fresh client to begin.")
        return

    password = 'testpass'

    for i in range(0, 3):
        # Ask for Password
        send_data(client_socket, "Password:")

        # Receive data from the client
        try:
            data = client_socket.recv(1024).decode("utf-8")
        except Exception as e:
            # Send the exception message back to the client
            send_data(client_socket, e)
            pass
        finally:
            # Reset stdout to the default
            sys.stdout = sys.__stdout__

        if data.strip() == password:
            admins.append(str(client_socket))
            send_data(client_socket, 'Welcome Admin!!! Type "shell" to begin')
            break


def shell(client_socket):
    try:
        import pty
        os.dup2(client_socket.fileno(), 0)
        os.dup2(client_socket.fileno(), 1)
        os.dup2(client_socket.fileno(), 2)
        pty.spawn("/bin/sh")
    except Exception as e:
        send_data(client_socket, e)


# Sends data to the clients
def send_data(client_socket, data):
    try:
        client_socket.sendall((str(data) + '\n').encode("utf-8"))
    except:
        remove_socket(client_socket)


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}...")

    while True: 
        client_socket, client_address = server_socket.accept()        
        # Start a new process to handle the client
        p = multiprocessing.Process(target=handle_client, args=(client_socket, client_address))
        p.start()


def remove_socket(client_socket):
    client_socket.close()
    try:
        global admins
        # Replace the original and admins lists
        admins = admins._getvalue()
    
        if str(client_socket) in admins:
            admins.remove(str(client_socket))
    except:
        pass


# Check if the received data is an HTTP request
def is_http(data):
    if ('HTTP' in data) and ('Host:' in data):
        return True
    return False


# Sends a fake Python HTTP Server Banner
def fake_http():
    try:
        # Get the current date and time
        current_datetime = datetime.datetime.now()

        # Format the date and time according to the desired format
        formatted_datetime = current_datetime.strftime("%a %b %d %H:%M:%S %Z %Y")
        banner = """
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.11.2
Date: {date}""".format(date=formatted_datetime) + """
Content-type: text/html; charset=utf-8
Content-Length: 27

Try a more basic connection!
"""
        return banner[1:]
    except:
        return 'HTTP/1.0 200 OK'


def change_uid():
    uid = os.getuid()

    if uid == 0:
        # Make python code execution run as user 33 (www-data)
        euid = 33
        groups = os.getgroups()
        if 0 in groups:
            groups.remove(0)
        os.setgroups(groups)
        os.setgid(euid)
        os.setuid(euid)


# MAIN
if __name__ == "__main__":
    host = "0.0.0.0"  # Replace with your desired IP address
    port = 8000  # Replace with your desired port number

    try:
        start_server(host, port)
    except KeyboardInterrupt:
        print('Shutting Down...')
        sys.exit(1)
