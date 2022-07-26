import sys
import time
import signal
import socket
import pandas as pd
from datetime import datetime
from _thread import start_new_thread

s = None

# Defining a function for handling the SIGINT signal
def signal_handler(signal, frame):

    """
    Description:
    -----------
    This function is used to handle the SIGINT signal.

    Parameters:
    -----------
    signal: The signal (int)
    frame: The frame (frame)

    Returns:
    --------
    None
    """

    global s

    # Accessing the socker object and closing it. This will cause the server to shut down.
    print("Ctrl + C pressed. Shutting down the server")
    s.close()

    # Exit the program
    sys.exit(1)

# Catch the SIGINT signal
signal.signal(signal.SIGINT, signal_handler)

# Defining a function for handling the data from a client
def client_handler(conn, addr):

    """
    Description:
    -----------
    This function is used to handle each client, recieve and export a dataframe.

    Parameters:
    -----------
    conn: The connection of the client (socket)
    addr: The address of the client (tuple)

    Returns:
    --------
    None
    """

    # List to hold the data from the client
    data_list = []

    while True:
        
        with conn:

            print('Connected by', addr)
            
            while True:
                
                try:
                    # Receive the data from the client
                    packet = conn.recv(1024)                

                    # If the packet is empty, export the data and break the loop
                    if not packet:

                        # Create a dataframe from the data_list    
                        df = pd.DataFrame(data_list, columns =['values'])

                        # File name convention: <client_ip>_<client_port>_<date>_<time>.csv
                        f_name = addr[0] + "_" + str(addr[1]) + "_" + datetime.now().strftime("%d-%m-%Y_%H-%M-%S.csv")
                        df.to_csv(f_name, index = False)
                        print("The dataframe has been saved to: " + f_name)
                        break
                    
                    # If the packet is not empty, append the data to the list after decoding it
                    data_list.append(packet.decode())
                    print(f"Received {packet!r}")
                
                # Handle any excpetions
                except Exception as e:
                    print(e)

                    break
            
            # Close the connection and print a message
            print("The client disconnected from the server")
            break

    return    

# Defining a function for accepting connections from clients
def accept_connections(s):
    
        """
        Description:
        -----------
        This function is used to accept connections from mulitple clients and spawn a thread for each new client.
            
        Parameters:
        -----------
        s: The socket of the server (socket)
        
        Returns:
        --------
        None
        """
        
        # Accept a connection from a client
        conn, addr = s.accept()

        # Spawn a thread for the client
        start_new_thread(client_handler, (conn, addr))

# Defining a function for starting a multi-threaded server
def collect(host = "127.0.0.1", port = 5999):

    """
    Description:
    -----------
    This function is used to collect create a server capable of collecing data from multiple clients.

    Parameters:
    -----------
    host: The hostname of the client (str)
    port: The port of the client (int)

    Returns:
    --------
    None
    """
    # localhost IP Address
    HOST = host

    # Port to listen on
    PORT = port

    global s
    
    try:

        # Create a socket (SOCK_STREAM means a TCP socket)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind the socket to the port
        s.bind((HOST, PORT))
        s.listen()

        # Setting a timeout for the socket to close if there are no connections for 30s
        # s.settimeout(30)

        print("Listening on port: " + str(PORT))  
        
        # Accept connections from clients
        while True:
                
            accept_connections(s)
            time.sleep(1)   

    # Handle any exceptions
    except Exception as e:

        # Close the socket
        print("Shutting down the server due to no activity")
        s.close()