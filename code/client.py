import socket
import re

def validNum(): # For input validation of client number
    while True:
        try:
            number = int(input("Enter an integer between 1 and 100[0 to exit]: "))
            return number
        except ValueError:
            print("Error: Invalid input. Please enter an integer.")

def validPort():
    while True:
        try:
            port = int(input("Enter port: "))
            if port <= 0 or port > 65535:
                raise ValueError("Port number out of range (1-65535).")
            return port
        except ValueError as ve:
            print(f"Error: {ve}")
        
def validName(): # For input validation of client name
    while True:
        name = input("Enter your name: ")
        if name.strip():  # Check if name is not empty
            return name
        else:
            print("You need to enter your name.")

def client():
    while True:
        while True: # Gets valid hostname/IP Address
            server_hostname = input("Enter server hostname or IP address: ")
            try:
                server_ip = socket.gethostbyname(server_hostname)
                break
            except socket.gaierror:
                print("Error: Invalid hostname or IP address. Please try again.")
        
        print("Client hostname:", socket.gethostname())
        print("Client IP:", socket.gethostbyname(socket.gethostname()))
        server_port = validPort()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_ip, server_port))
            print("Connected to server: " )

            name = validName()
            number = validNum()
            message = f"{name} {number}"
            client_socket.sendall(message.encode())
            print("Sent message to server.")

            data = client_socket.recv(1024).decode()

            # Extract server name and number using regular expressions
            match = re.search(r'^(.*?)\s+(\d+)$', data)
            if match:
                server_name = match.group(1)
                server_number = int(match.group(2))
            else:
                print("Terminated connection with server.") # Did not get data from server, so ends connection
                return
            
            print("Received message from server:") # The message from server
            print("Server's name:", server_name)
            print("Server's number:", server_number)
            print("Your number:", number)
            print("Sum of numbers:", server_number + number)

if __name__ == "__main__":
    client()
