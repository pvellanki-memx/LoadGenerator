import configparser
import random
import time
import quickfix as fix

# Global variables
sessions = {}

# Function to handle the fromAdmin message
def fromAdmin(message, session):
    global sessions
    session_id = session.getSessionID()
    incoming_msg_seq_num = int(message.getHeader().getField(34))
    msg_type = message.getHeader().getField(35)

    if msg_type == fix.MsgType_Logon:  # Logon message
        if incoming_msg_seq_num == 1:
            print(f"Session established for {session_id}")
            sessions[session_id] = True
    elif msg_type == fix.MsgType_Logout:  # Logout message
        print(f"Session disconnected for {session_id}")
        sessions[session_id] = False

# Function to generate a random ClOrdID
def generate_clordid():
    return str(random.randint(100000, 999999))

# Function to generate a random message based on weightage
def generate_message(template, message_weights, session_id):
    # Calculate total weightage
    total_weight = sum(message_weights.values())
    
    # Generate a random number within the total weightage
    random_num = random.randint(1, total_weight)
    
    # Find the message type based on the random number
    cumulative_weight = 0
    for msg_type, weight in message_weights.items():
        cumulative_weight += weight
        if random_num <= cumulative_weight:
            # Replace placeholders in the template with the message type, ClOrdID, and outgoing sequence number
            message = template.replace('<MsgType>', msg_type)
            message = message.replace('<ClOrdID>', generate_clordid())
            message = message.replace('<SeqNum>', str(get_outgoing_seq_num(session_id)))
            message = message.replace('<SendingTime>', fix.UtcTimeStamp().getString())
            
            # Calculate the message length (excluding SOH characters)
            message_length = len(message) - message.count('|')
            
            # Replace the placeholders for message length and CheckSum
            message = message.replace('<BodyLength>', str(message_length))
            message = message.replace('<CheckSum>', checksum)
            
            # Calculate the CheckSum
            checksum = calculate_checksum(message)
            
            # Append the CheckSum to the message
            message += f'|10={checksum}|'
            
            return message

# Function to calculate the CheckSum (Tag 10) for a given FIX message
def calculate_checksum(message):
    checksum = sum(ord(c) for c in message) % 256
    return f'{checksum:03}'  # Ensure the CheckSum is three digits

# Function to get the outgoing sequence number for a session
def get_outgoing_seq_num(session_id):
    session = fix.Session.lookupSession(fix.SessionID(session_id))
    if session is not None:
        return session.getNextSenderMsgSeqNum()

# Function to increment the outgoing sequence number for a session
def increment_outgoing_seq_num(session_id):
    session = fix.Session.lookupSession(fix.SessionID(session_id))
    if session is not None:
        session.incrementNextSenderMsgSeqNum()

# Function to send heartbeat messages at a specified interval
def send_heartbeats(session_id, interval):
    while sessions[session_id]:
        session = fix.Session.lookupSession(fix.SessionID(session_id))
        if session is not None:
            heartbeat_message = fix.Message()
            heartbeat_message.getHeader().setField(34, str(get_outgoing_seq_num(session_id)))
            fix.Session.sendToTarget(heartbeat_message, session_id)
            increment_outgoing_seq_num(session_id)
        time.sleep(interval)

# Function to send messages at the specified rate for a duration
def send_messages(template, message_weights, rate, duration):
    start_time = time.time()
    end_time = start_time + duration

    while time.time() < end_time:
        for session_id in sessions:
            if sessions[session_id]:
                session = fix.Session.lookupSession(fix.SessionID(session_id))
                if session is not None:
                    message = fix.Message(generate_message(template, message_weights, session_id))
                    fix.Session.sendToTarget(message, session_id)
                    increment_outgoing_seq_num(session_id)
                    time.sleep(1 / rate)

# Read configuration from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

template_file = config.get('LoadGenerator', 'template_file')
connection_config_file = config.get('LoadGenerator', 'connection_config_file')
message_rate = float(config.get('LoadGenerator', 'message_rate'))
heartbeat_interval = float(config.get('LoadGenerator', 'heartbeat_interval'))

# Load the template file
with open(template_file, 'r') as file:
    template = file.read()

# Load the connection configuration file
connections = configparser.ConfigParser()
connections.read(connection_config_file)

# Get the message types and their weights
message_weights = dict(connections.items('MessageTypes'))

# Initialize FIX settings
settings = fix.SessionSettings(connection_config_file)
initiator = fix.SocketInitiator(fromAdmin, None, settings)

# Start the FIX sessions
initiator.start()

# Establish the sessions
for section in connections.sections():
    session_id = connections.get(section, 'SessionID')
    sessions[session_id] = False

# Wait for sessions to be established
while not all(sessions.values()):
    time.sleep(1)

# Send messages and heartbeats
send_duration = 60  # Duration in seconds
send_messages(template, message_weights, message_rate, send_duration)

# Stop the FIX sessions
initiator.stop()
