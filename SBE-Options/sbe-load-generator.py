import configparser
import socket
import struct
import time
from random import choices, randint

from sbe_encoder_decoder import *

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Read connection details from connections.cfg
connection_config = configparser.ConfigParser()
connection_config.read(config['Default']['connection_config'])

# TCP/IP connection details
host = connection_config['Connection']['host']
port = int(connection_config['Connection']['port'])
user = connection_config['Connection']['user']
password = connection_config['Connection']['password']
token = f'{user}:{password}'

# Token and header details
token_type = 'P'  # Assuming token type is always 'P'
token_length = len(token)
header = struct.pack('!BHB', 100, token_length + 1, token_type.encode('utf-8')[0])
message = header + token.encode('utf-8')

# Read other configuration parameters
message_rates = config['Default'].getint('message_rates')
duration = config['Default'].getint('duration')
weights = {
    'NewOrderSingle': config['Default'].getint('NewOrderSingle_weight'),
    'ShortTwoSideBulkQuote': config['Default'].getint('ShortTwoSideBulkQuote_weight'),
    'LongTwoSideBulkQuote': config['Default'].getint('LongTwoSideBulkQuote_weight'),
    'ShortOneSideBulkQuote': config['Default'].getint('ShortOneSideBulkQuote_weight'),
    'LongOneSideBulkQuote': config['Default'].getint('LongOneSideBulkQuote_weight'),
}

# Read optionsSecurityID's from config.ini
options_security_ids = config['Default']['options_security_ids'].split(',')

# Load template.txt
template_file_path = config['Default']['template_file']
with open(template_file_path) as template_file:
    template = template_file.read()

# Establish SBE TCP session
def establish_session():
    # Create a socket and establish the connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Set socket to binary mode
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    # Send the login request
    client_socket.sendall(message)

    # Receive and handle the response
    response_header = client_socket.recv(2)
    response_type, response_length = struct.unpack('!BB', response_header)

    if response_type == 1:  # Login Accepted
        response_message = client_socket.recv(response_length)
        print("Login Accepted:", response_message.decode('utf-8'))
        session_id = None
    elif response_type == 2:  # Login Rejected
        response_message = client_socket.recv(response_length)
        print("Login Rejected:", response_message.decode('utf-8'))
        client_socket.close()
        exit()  # Exit the script gracefully after login rejection
    else:
        print("Invalid response received.")
        client_socket.close()
        exit()  # Exit the script if an invalid response is received

    # Continue with the session
    while True:
        response_header = client_socket.recv(2)
        response_type, response_length = struct.unpack('!BB', response_header)

        if response_type == 3:  # Start of Session
            response_message = client_socket.recv(response_length)
            session_id = struct.unpack('!Q', response_message[3:11])[0]
            print("Start of Session. Session ID:", session_id)
            break
        else:
            print("Invalid response received.")

    # Send the Stream Request
    stream_request_type = 103
    stream_request_length = 16  # 4 bytes for message type and length, 8 bytes for session ID, 8 bytes for next sequence number
    NEXT_SEQUENCE_NUMBER = 0
    stream_request_header = struct.pack('!BHBQQ', stream_request_type, stream_request_length, session_id, NEXT_SEQUENCE_NUMBER)
    stream_request = stream_request_header
    client_socket.sendall(stream_request)

    response_header = client_socket.recv(2)
    response_type, response_length = struct.unpack('!BB', response_header)

    if response_type == 9:  # Stream Rejected
        response_message = client_socket.recv(response_length)
        reject_code = response_message.decode('utf-8')
        print("Stream Rejected. Reject Code:", reject_code)
        client_socket.close()
        exit()
    elif response_type == 10:  # End of Stream
        response_message = client_socket.recv(response_length)
        print("End of Stream")
        client_socket.close()
        exit()
    else:
        print("Invalid response received.")

    return client_socket, session_id

# Generate a random message type based on the weights
def generate_message_type():
    message_types = list(weights.keys())
    return choices(message_types, weights=list(weights.values()), k=1)[0]

# Generate a random message based on the specified type
def generate_message(message_type):
    if message_type == 'NewOrderSingle':
        # Generate NewOrderSingle message
        # Implement the logic to generate the field values for this message type
        # Return an instance of the NewOrderSingle class with the generated field values
        pass

    elif message_type == 'ShortTwoSideBulkQuote':
        # Generate ShortTwoSideBulkQuote message
        # Implement the logic to generate the field values for this message type
        # Return an instance of the ShortTwoSideBulkQuote class with the generated field values
        pass

    elif message_type == 'LongTwoSideBulkQuote':
        # Generate LongTwoSideBulkQuote message
        # Implement the logic to generate the field values for this message type
        # Return an instance of the LongTwoSideBulkQuote class with the generated field values
        pass

    elif message_type == 'ShortOneSideBulkQuote':
        # Generate ShortOneSideBulkQuote message
        # Implement the logic to generate the field values for this message type
        # Return an instance of the ShortOneSideBulkQuote class with the generated field values
        pass

    elif message_type == 'LongOneSideBulkQuote':
        # Generate LongOneSideBulkQuote message
        # Implement the logic to generate the field values for this message type
        # Return an instance of the LongOneSideBulkQuote class with the generated field values
        pass

    else:
        raise ValueError(f"Invalid message type: {message_type}")

# Send the generated message over the TCP connection
def send_message(client_socket, message):
    encoded_message = message.encode()

    # Send the message
    client_socket.sendall(encoded_message)

    # Sleep for a short period to control the message rate
    time.sleep(1 / message_rates)

# Main execution
def main():
    # Establish SBE TCP session
    client_socket, session_id = establish_session()

    # Start time for calculating duration
    start_time = time.time()

    # Generate and send messages for the specified duration
    while time.time() - start_time < duration:
        # Generate a random message type
        message_type = generate_message_type()

        # Generate a message based on the random message type
        message = generate_message(message_type)

        # Send the generated message over the TCP connection
        send_message(client_socket, message)

    # Close the TCP connection
    client_socket.close()

if __name__ == '__main__':
    main()
