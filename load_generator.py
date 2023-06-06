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

    if msg_type == 'A':  # Logon message
        if incoming_msg_seq_num == 1:
            print(f"Session established for {session_id}")
            sessions[session_id] = True
    elif msg_type == '5':  # Logout message
        print(f"Session disconnected for {session_id}")
        sessions[session_id] = False

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
            # Replace placeholders in the template with the message type and outgoing sequence number
            message = template.replace('<MessageType>', msg_type)
            message = message.replace('<SeqNum>', str(get_outgoing_seq_num(session_id)))
            return message

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

# Load the template file
with open(template_file, 'r') as file:
    template = file.read()

# Load message weights from config.ini
message_weights = dict(config.items('MessageTypes'))

# Load connection configuration from connections.cfg file
settings = fix.SessionSettings(connection_config_file)
application = fix.Application()
storeFactory = fix.FileStoreFactory(settings)
logFactory = fix.ScreenLogFactory(settings)
initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)

# Start the FIX sessions
initiator.start()

# Get the session IDs
session_ids = initiator.getSessions()

# Initialize session state
for session_id in session_ids:
    sessions[session_id] = False

# Wait for sessions to be established
while not all(sessions.values()):
    time.sleep(1)

# Send messages
send_duration = 60  # Duration in seconds
send_messages(template, message_weights, message_rate, send_duration)

# Stop the FIX sessions
initiator.stop()
