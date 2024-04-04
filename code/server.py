import socket
import random
import re


def validPort():
    while True:
        try:
            port = int(input("Enter port: "))
            if port <= 0 or port > 65535:
                raise ValueError
            return port
        except ValueError:
            print("Error: Invalid input. Please enter a valid port number (1-65535).")
            
def server():
    server_hostname = socket.gethostname()  # Automatically obtain the server's hostname
    server_ip = socket.gethostbyname(server_hostname)
    print("Server hostname:", server_hostname)
    print("Server IP:", server_ip)
    server_port = validPort()

    server_name = "Server of Abhinay Lavu"
    min_number = 1
    max_number = 100
    num_of_connections = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_ip, server_port))
        

        server_socket.listen()

        while True:
            print("Server is listening on port", server_port)
            connection, addr = server_socket.accept()
            print('Connected by', addr)

            with connection:
                data = connection.recv(1024).decode()

                match = re.search(r'^(.*?)\s+(\d+)$', data) # Use regex for client info
                if match:
                    client_name = match.group(1)
                    client_number = int(match.group(2))
                else:
                    print("Error: Could not extract client name and number.")
                    continue
                
                num_of_connections += 1
                server_number = random.randint(min_number, max_number)
                
                print("Client's name:", client_name)
                print("Server's name:", server_name)
                print("Client's number:", client_number)
                if client_number < min_number or client_number > max_number:
                    print("Client's number is out of range. Terminating.")
                    return 
                print("Server's number:", server_number)
                print("Sum of numbers:", client_number + server_number)
                print("Number of connections:", num_of_connections)

                response = f"{server_name} {server_number}"
                connection.sendall(response.encode())
                print("Sent message to client")

if __name__ == "__main__":
    server()
