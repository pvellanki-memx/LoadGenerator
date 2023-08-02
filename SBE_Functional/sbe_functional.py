import unittest
import socket
import struct
import time
from sbe_encoder_decoder import *


# Define the SBE message types
MESSAGE_TYPES = {
    "NewOrderSingle": 1,
    "ShortTwoSideBulkQuote": 2,
    "LongTwoSideBulkQuote": 3,
    "ShortOneSideBulkQuote": 4,
    "LongOneSideBulkQuote": 5,
}


# Function to establish SBE TCP session
def establish_session(session_name):
    def establish_session(session_name):
    # Get connection details for the specified session name
    host = connection_config[session_name]['host']
    port = int(connection_config[session_name]['port'])
    user = connection_config[session_name]['user']
    password = connection_config[session_name]['password']
    token = f'{user}:{password}'

    # Login request
    message_type = 100
    token_type = 'P'  # Assuming token type is always 'P'
    token_length = len(token)
    header = struct.pack('!BHB', message_type, token_length + 1, token_type.encode('utf-8')[0])
    message = header + token.encode('utf-8')

    # Create a socket and establish the connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Set socket to binary mode
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    # Send the login request
    client_socket.sendall(message)

    # Receive and handle the response
    response_header = client_socket.recv(3)
    response_type, response_length = struct.unpack('!B H', response_header)

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
        response_header = client_socket.recv(11)
        response_type, response_length, session_id = struct.unpack('!B H Q', response_header)

        if response_type == 3:  # Start of Session
            print("Start of Session. Session ID:", session_id)
            break
        else:
            print("Invalid response received.")

    # Stream Request
    stream_request_type = 103
    stream_request_length = 16  # 4 bytes for message type and length, 8 bytes for session ID, 8 bytes for next sequence number
    NEXT_SEQUENCE_NUMBER = 0
    stream_request_header = struct.pack('!BHQQ', stream_request_type, stream_request_length, session_id, NEXT_SEQUENCE_NUMBER)
    stream_request = stream_request_header

    # Send the Stream Request
    client_socket.sendall(stream_request)

    response_header = client_socket.recv(3)
    response_type, response_length = struct.unpack('!B H', response_header)

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
    elif response_type == 8:  # Stream Begin
        response_message = client_socket.recv(response_length - 2)
        NEXT_SEQUENCE_NUMBER  = struct.unpack('!Q', response_message[3:11])
        print("Stream Begin received")
    else:
        print("Invalid Message received")

    return client_socket, session_id


# Function to generate SBE messages based on the message type
def generate_sbe_message(message_type, session_name):
    if message_type == "NewOrderSingle":
        # Generate NewOrderSingle message
        # ... Your code to generate NewOrderSingle message ...

    elif message_type == "ShortTwoSideBulkQuote":
        # Generate ShortTwoSideBulkQuote message
        # ... Your code to generate ShortTwoSideBulkQuote message ...

    elif message_type == "LongTwoSideBulkQuote":
        # Generate LongTwoSideBulkQuote message
        # ... Your code to generate LongTwoSideBulkQuote message ...

    elif message_type == "ShortOneSideBulkQuote":
        # Generate ShortOneSideBulkQuote message
        # ... Your code to generate ShortOneSideBulkQuote message ...

    elif message_type == "LongOneSideBulkQuote":
        # Generate LongOneSideBulkQuote message
        # ... Your code to generate LongOneSideBulkQuote message ...

    else:
        raise ValueError(f"Invalid message type: {message_type}")

def send_and_receive(self, message_type, message):
    # Send the message over the TCP connection
    send_message(self.client_socket, message)

    # Receive the response message (for simplicity, let's assume the response is received immediately)
    response_header = self.client_socket.recv(3)
    response_type, response_length = struct.unpack('!B H', response_header)
    response_message = self.client_socket.recv(response_length)

    # TODO: Implement the logic to handle the response message based on message_type
    # For example, you can decode and verify the response message contents
    # based on the type of message sent.

class SBETestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Establish the session before running any test cases
        cls.client_socket, cls.session_id = establish_session('Session1')

    @classmethod
    def tearDownClass(cls):
        # Close the session after all test cases have been executed
        cls.client_socket.close()

    def send_and_receive(self, message_type, message):
        # Send the message over the TCP connection
        send_message(self.client_socket, message)

        # Receive the response message (for simplicity, let's assume the response is received immediately)
        response_header = self.client_socket.recv(3)
        response_type, response_length = struct.unpack('!B H', response_header)
        response_message = self.client_socket.recv(response_length)

        # TODO: Implement the logic to handle the response message based on message_type
        # For example, you can decode and verify the response message contents
        # based on the type of message sent.

    def test_new_order_single(self):
        message_type = 'NewOrderSingle'
        # Generate a message based on the message_type
        message = generate_message(message_type, 'Session1')

        # Send and receive the message
        self.send_and_receive(message_type, message)

    def test_short_two_sided_bulk_quote(self):
        message_type = 'ShortTwoSidedBulkQuote'
        # Generate a message based on the message_type
        message = generate_message(message_type, 'Session1')

        # Send and receive the message
        self.send_and_receive(message_type, message)

    # Implement similar test methods for other SBE message types...

if __name__ == '__main__':
    unittest.main()


if __name__ == "__main__":
    unittest.main()



