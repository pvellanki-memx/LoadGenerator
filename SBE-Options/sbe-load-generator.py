import configparser
import socket
import struct
import time
from sbe-encoder-decoder import UTCTimestampNanos, NewOrderSingle, ShortTwoSideBulkQuote, LongTwoSideBulkQuote, ShortOneSideBulkQuote, LongOneSideBulkQuote
from sbe-encoder-decoder import UINT32, OrdType, TimeInForceType, ExecInstType, TradingCapacityType, SideType
from random import choices, randint
import string
from random import choices, randint

from sbe-encoder-decoder import *

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Read connection details from connections.cfg
connection_config = configparser.ConfigParser()
connection_config.read(config['Server']['config_file'])

# TCP/IP connection details
host = connection_config['Session1']['host']
port = int(connection_config['Session1']['port'])
user = connection_config['Session1']['user']
password = connection_config['Session1']['password']
token = f'{user}:{password}'

# Token and header details
token_type = 'P'  # Assuming token type is always 'P'
token_length = len(token)
header = struct.pack('!BHB', 100, token_length + 1, token_type.encode('utf-8')[0])
message = header + token.encode('utf-8')

# Read other configuration parameters
message_rate = config.getint('Load', 'message_rate')
duration = config.getint('Load', 'duration')

weights = {
    'NewOrderSingle': config.getfloat('Weights', 'NewOrderSingle'),
    'ShortTwoSideBulkQuote': config.getfloat('Weights', 'ShortTwoSideBulkQuote'),
    'LongTwoSideBulkQuote': config.getfloat('Weights', 'LongTwoSideBulkQuote'),
    'ShortOneSideBulkQuote': config.getfloat('Weights', 'ShortOneSideBulkQuote'),
    'LongOneSideBulkQuote': config.getfloat('Weights', 'LongOneSideBulkQuote')
}

security_ids = config.get('OptionsSecurityIDs', 'security_ids').split(',')

template_file = config.get('Template', 'template_file')

# Load template.txt
with open(template_file) as template_file:
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

def generate_message(message_type)
    if message_type == 'NewOrderSingle':
        sending_time = UTCTimestampNanos()
        cl_ord_id = ''.join(choices(string.ascii_uppercase + string.digits, k=20))
        options_security_id = choices(security_ids)[0]
        side = SideType.BUY  # Assuming a BUY order, you can customize this
        order_qty = UINT32(randint(1, 100))
        ord_type = OrdType.LIMIT  # Assuming a LIMIT order, you can customize this
        time_in_force = TimeInForceType.GOOD_TILL_CANCEL  # Assuming a GTC order, you can customize this
        exec_inst = [ExecInstType.PRIMARY_PEG, ExecInstType.DISPLAY_PRICE]  # Assuming primary peg and display price instructions, you can customize this
        trading_capacity = TradingCapacityType.PRINCIPAL  # Assuming principal capacity, you can customize this
    
        # Create an instance of NewOrderSingle and set the field values
        new_order_single = NewOrderSingle()
        new_order_single.sending_time = sending_time
        new_order_single.cl_ord_id = cl_ord_id
        new_order_single.options_security_id = options_security_id
        new_order_single.side = side
        new_order_single.order_qty = order_qty
        new_order_single.ord_type = ord_type
        new_order_single.time_in_force = time_in_force
        new_order_single.exec_inst = exec_inst
        new_order_single.trading_capacity = trading_capacity

        return new_order_single


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
    time.sleep(1 / message_rate)

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
