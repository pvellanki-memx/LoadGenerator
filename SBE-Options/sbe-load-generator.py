import configparser
import socket
import struct
import time
from sbe_encoder_decoder import UTCTimestampNanos, NewOrderSingle, ShortTwoSideBulkQuote, LongTwoSideBulkQuote, ShortOneSideBulkQuote, LongOneSideBulkQuote, ShortTwoSidedQuote,MatchTradePreventionType,MtpGroupIDType
from sbe_encoder_decoder import UINT32,UINT16, OrdType, TimeInForceType, ExecInstType, TradingCapacityType, SideType, Party, PartiesGroup
from random import choices, randint
import string
from random import choices, randint



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
    print(response_type, response_length)

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
        print(response_header, response_type, response_length)

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
    print(response_type, response_length)

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
        print(response_message)
        NEXT_SEQUENCE_NUMBER  = struct.unpack('!Q', response_message[3:11])
        print("Stream Begin received")
    else:
        print("Invalid Message received")
    

    return client_socket, session_id

# Generate a random message type based on the weights
def generate_message_type():
    message_types = list(weights.keys())
    return choices(message_types, weights=list(weights.values()), k=1)[0]

def generate_message(message_type):
    if message_type == 'NewOrderSingle':
        # Generate values for the fields
        sending_time = UTCTimestampNanos(int(time.time() * 10**9))
        cl_ord_id = ''.join(choices(string.ascii_uppercase + string.digits, k=20))
        options_security_id = choices(security_ids)[0]
        side = SideType(value=SideType.BUY)  # Set the side to "Buy"
        order_qty = UINT32(value=randint(1, 100))
        ord_type = OrdType(value=OrdType.LIMIT)  # Set the order type to "Limit"
        time_in_force = TimeInForceType(value=TimeInForceType.DAY)  # Set the time in force to "Day"
        exec_inst = ExecInstType(value=ExecInstType.ParticipateDoNotInitiate)  # Set the execution instructions
        trading_capacity = TradingCapacityType(value=TradingCapacityType.CUSTOMER)  # Set the trading capacity
        parties = [PartiesGroup(party_id='EFID', party_id_source='D', party_role='CUSTOMER')]  # Set the parties

        # Create an instance of NewOrderSingle and set the field values
        new_order_single = NewOrderSingle(
            sending_time=sending_time,
            cl_ord_id=cl_ord_id,
            options_security_id_35=options_security_id,
            side=side,
            order_qty=order_qty,
            ord_type=ord_type,
            time_in_force=time_in_force,
            exec_inst=exec_inst,
            trading_capacity=trading_capacity,
            parties=parties
        )

        unsequenced_message = struct.pack('!BH', 104, 102)  # MessageType=104, MessageLength=6, TCP Header Length=102
        # Encode the NewOrderSingle instance
        encoded_message = new_order_single.encode()
        message = unsequenced_message + encoded_message

        # Print the encoded message
        print(encoded_message)

        return message

        


    elif message_type == 'ShortTwoSideBulkQuote':
        # Generate ShortTwoSideBulkQuote message
        sending_time = UTCTimestampNanos(int(time.time() * 10**9))
        cl_ord_id = ''.join(choices(string.ascii_uppercase + string.digits, k=20))
        time_in_force = TimeInForceType(0)
        exec_inst = ExecInstType(0)
        trading_capacity = TradingCapacityType(0)
        mtp_group_id = MtpGroupIDType(0)
        match_trade_prevention = MatchTradePreventionType(0)
        cancel_group_id = UINT16(0)
        risk_group_id = UINT16(0)
        parties = [PartiesGroup(party_id='EFID', party_id_source='D', party_role='CUSTOMER')]  # Update with the desired party details
        quotes = [
            ShortTwoSidedQuote(1, 'ABC', 10, 100.0, 15, 110.0),  # Quote 1
            ShortTwoSidedQuote(2, 'XYZ', 20, 200.0, 25, 210.0),  # Quote 2
        ]

        Short_Two_Side_Bulk_Quote = ShortTwoSideBulkQuote(
            sending_time=sending_time,
            cl_ord_id=cl_ord_id,
            time_in_force=time_in_force,
            exec_inst=exec_inst,
            trading_capacity=trading_capacity,
            mtp_group_id=mtp_group_id,
            match_trade_prevention=match_trade_prevention,
            cancel_group_id=cancel_group_id,
            risk_group_id=risk_group_id,
            parties=parties,
            quotes=quotes
        )

        # Encode the ShortTwoSideBulkQuote instance
        encoded_message = Short_Two_Side_Bulk_Quote.encode()
        unsequenced_message = struct.pack('!BH', 104, 102)  # MessageType=104, MessageLength=6, TCP Header Length=102
        message = unsequenced_message + encoded_message

        # Print the encoded message
        print(message)
        return message


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


    # Send the message
    client_socket.sendall(message)

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

        # Sleep for a short period to control the message rate
        time.sleep(1 / message_rate)

    # Close the TCP connection
    client_socket.close()

if __name__ == '__main__':
    main()











