
import time
import socket

# Defining a function for sending the data to a server
def stream(data, host = "127.0.0.1", port = 5999, interval = 1):

    """
    Description:
    -----------
    This function is used to stream the data to a server.

    Parameters:
    -----------
    data: The data to be streamed (pandas.DataFrame)
    host: The hostname of the server (str)
    port: The port of the server (int)
    interval: The interval between successive data packets (int)

    Returns:
    --------
    None
    """

    # localhost IP Address
    HOST = host  

    # Port to listen on
    PORT = port

    # Create a socket (SOCK_STREAM means a TCP socket) 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # Try connecting to the server
        try:
            s.connect((HOST, PORT))
        # If the connection fails, print the error message
        except Exception as e:
            print(e)
            print("Try again by entering the correct HOST and PORT. Re-check if your server is running.")
            return
        
        # If the connection is successful, iterate through the rows and send the data to the server
        for i, r in data.iterrows():

            s.send(str(r['kW']).encode())
            print("Sent: ", str(r['kW']).encode())

            # Wait for the interval to pass
            time.sleep(interval)
        
        print("Finished sending data")

        # Close the socket
        s.close()