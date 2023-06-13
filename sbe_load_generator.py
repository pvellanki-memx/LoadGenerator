
import configparser
import socket
import time
from sbe-tool import encode_message

config = configparser.ConfigParser()
config.read('config.ini')

# Load the schema for encoding and decoding messages
schema_file = 'sbe-schema.xml'
schema = load_schema(schema_file)

# Get the default configuration for message rate and duration
default_config = config['default']
default_message_rate = int(default_config['message_rate'])
default_duration = int(default_config['duration'])

# Loop through all the session configurations
for session_name in config.sections():
    if session_name == 'default':
        continue

    # Get the session configuration
    session_config = config[session_name]

    # Extract the connection details
    server_ip = session_config['ip']
    server_port = int(session_config['port'])

    # Establish the TCP connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    # Set the TCP connection to binary mode
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

   # Login process
login_request_fields = {}
login_request_fields[3] = 100  # Message Type
login_request_fields[4] = len(session_config['token'])  # Token Type
login_request_fields[5] = connection_config['token']  # Token
login_request_message = encode_message(schema, 'LoginRequest', login_request_fields)
client_socket.sendall(login_request_message)

# Receive the login response
login_response_message = client_socket.recv(4096)
_, login_response_fields = decode_message(schema, login_response_message)

# Check if the login was accepted
if login_response_fields.get(3) == 1:  # Login Accepted
    print("Login accepted.")
else:
    print("Login rejected. Exiting.")
    client_socket.close()
    exit(1)

    # Calculate message rate per session
    message_rate = int(session_config.get('message_rate', default_message_rate))
    duration = int(session_config.get('duration', default_duration))
    message_interval = 1 / message_rate

    # Send NewOrderSingle messages
    start_time = time.time()
    end_time = start_time + duration

    while time.time() < end_time:
        # Generate and send NewOrderSingle message
        message_name = 'NewOrderSingle'
        field_values = {
            # ... (populate the required fields for NewOrderSingle)
        }
        encoded_message = encode_message(schema, message_name, field_values)
        client_socket.sendall(encoded_message)

        # Wait for the next message interval
        time.sleep(message_interval)

    # Close the TCP connection
    client_socket.close()

