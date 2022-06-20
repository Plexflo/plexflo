import time
import socket
import pandas as pd

# Defining a function for sending the data to a server
def collect(dataframe_name = "new.csv", host = "127.0.0.1", port = 5999):

    """
    Description:
    -----------
    This function is used to stream the data to a server.

    Parameters:
    -----------
    dataframe_name: The name of the dataframe (str)
    host: The hostname of the server (str)
    port: The port of the server (int)
    interval: The interval between successive data packets (int)

    Returns:
    --------
    None
    """

    HOST = host

    PORT = port

    data_list = []

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()

    print("Listening on port: " + str(PORT))

    conn, addr = s.accept()

    while True:

        with conn:

            print('Connected by', addr)

            while True:

                try:
                    packet = conn.recv(1024)                

                    if not packet:

                        df = pd.DataFrame(data_list, columns =['values'])
                        df.to_csv(dataframe_name, index = False)
                        break

                    data_list.append(packet.decode())
                    print(f"Received {packet!r}")
                except Exception as e:
                    print(e)
                    break

            print("The client disconnected from the server")
            print("The dataframe has been saved to: " + dataframe_name)
            break