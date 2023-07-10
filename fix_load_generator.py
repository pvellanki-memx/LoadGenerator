import configparser
import random
import time
import datetime
import quickfix as fix

# Global variables
sessions = {}

# Class representing the FIX application
class MyApplication(fix.Application):
    def __init__(self, template_file, message_weights, message_rate):
        super().__init__()
        self.template_file = template_file
        self.message_weights = message_weights
        self.message_rate = message_rate
        self.sessions = {}
        self.log_file = log_file

    def onCreate(self, sessionID):
        print("Session created -", sessionID.toString())
        self.sessions[sessionID] = fix.Session.lookupSession(sessionID)

    def toAdmin(self, message, sessionID):
        if message.getHeader().getField(fix.MsgType()).getString() == fix.MsgType_Logon:
            message.getHeader().setField(1408, "1.3")
            print("sent admin message", message.toString())
        return True

    def toApp(self, message, sessionID):
        session_id = sessionID.toString()
        with open(self.log_file, "a") as file:
                file.write(f"Session: {session_id}\n")
                file.write(message.toString() + '\n')
        print("sent application message", message.toString())

    def fromApp(self, message, sessionID):
        session_id = sessionID.toString()
        with open(self.log_file, "a") as file:
                file.write(f"Session: {session_id}\n")
                file.write(message.toString() + '\n')
        print("sent application message", message.toString())

    def fromAdmin(self, message, sessionID):
        global sessions
        session_id = sessionID.toString()
        incoming_msg_seq_num = int(message.getHeader().getField(34))
        msg_type = message.getHeader().getField(35)
        print(message)

        if msg_type == 'A':  # Logon message
            if incoming_msg_seq_num == 1:
                print(f"Session established for {session_id}")
                sessions[session_id] = True
        elif msg_type == '5':  # Logout message
            print(f"Session disconnected for {session_id}")
            sessions[session_id] = False
        with open(self.log_file, 'a') as file:
            file.write(f"Received fromAdmin message:{message.toString()}\n")

    def onLogout(self, sessionID):
        print("Logout initiated -", sessionID.toString())

    def onLogon(self, sessionID):
        print("Logon Successful -", sessionID.toString())

    def generate_clordid(self):
        return str(random.randint(100000, 999999))

    def calculate_checksum(self, message):
        checksum = sum(ord(c) for c in message) % 256
        return f"{checksum:03}"  # Ensure the CheckSum is three digits

    def get_outgoing_seq_num(self, session_id):
        session = fix.Session.lookupSession(session_id)
        if session is not None:
            return session.getExpectedSenderNum()
        return 0

    def generate_message(self, template, session_id):
            # Replace placeholders in the message template
            message = template.replace('<ClOrdID>', self.generate_clordid())

            # Get the outgoing sequence number
            seq_num = str(self.get_outgoing_seq_num(session_id))
            print(seq_num)

            # Replace the <SeqNum> placeholder with the sequence number
            message = message.replace('<MsgSeqNum>', seq_num)

            # Generate the SendingTime in the desired format
            sending_time = datetime.datetime.utcnow().strftime('%Y%m%d-%H:%M:%S.%f')[:-3]
            message = message.replace('<SendingTime>', sending_time)


            # Create the repeating group fields
            party_group_fields = [
                "453=1",
                "448=QAX1",
                "447=D",
                "452=66"
            ]

            # Insert the repeating group into the message
            repeating_group = "|".join(party_group_fields)
            message = message.replace('<RepeatingGroup>', repeating_group)
        
            # Replace the field delimiter from '|' to SOH character
            message = message.replace('|', chr(0x01))


            # Calculate the CheckSum
            #message_factory = fix.MessageFactory()
            fix_message = fix.Message(message, False)
            #fix_message.setString(message, False, message_factory)
            checksum = self.calculate_checksum(fix_message.toString())

            #fix_message.setField(10, checksum)
            print("generated_message",fix_message)

            # Calculate the message length (excluding SOH characters)
            #body_start_index = message.index('9=')
            #body_end_index = message.index('10=')
            body_length = fix_message.getHeader().getField(9)
            #print("generated_message",fix_message)
            #print(body_length)

            # Replace the placeholders for message length and CheckSum
            #message = message.replace('<BodyLength>', str(body_length))
            #message = message.replace('<CheckSum>', checksum)
            #print(message)

            return fix_message

    def increment_outgoing_seq_num(self, session_id):
        session = fix.Session.lookupSession(fix.SessionID(session_id))
        if session is not None:
            session.incrementNextSenderMsgSeqNum()

    def send_heartbeats(self, session_id, interval):
        while sessions[session_id]:
            session = fix.Session.lookupSession(fix.SessionID(session_id))
            if session is not None:
                heartbeat_message = fix.Message()
                heartbeat_message.getHeader().setField(34, str(self.get_outgoing_seq_num(session_id)))
                fix.Session.sendToTarget(heartbeat_message, session_id)
                self.increment_outgoing_seq_num(session_id)
            time.sleep(interval)

    def generate_load(self):
        with open(self.template_file, "r") as file:
            templates = file.readlines()

        load = []
        for template in templates:
            message_type = self.get_message_type(template)
            if message_type and message_type in self.message_weights:
                weight = int(self.message_weights[message_type])
                load.extend([template.strip()] * weight)

        print(f"Generated load: {load}")
        random.shuffle(load)
        load_length = len(load)
        iterations = int(self.message_rate * self.send_duration)

        if iterations > load_length:
            quotient, remainder = divmod(iterations, load_length)
            print(f"Repeating load: {quotient} times, with remainder: {remainder}")
            load = load * quotient + load[:remainder]
        else:
            load = load[:iterations]

        return load

    def get_message_type(self, message):
        fields = message.split("|")
        for field in fields:
            if field.startswith("35="):
                return field.split("=")[1].lower()
        return
    

    """
    def run(self):
        settings = fix.SessionSettings(self.connection_config_file)
        application = fix.SocketInitiator(self, fix.FileStoreFactory(settings), settings)
        application.start()

        while not all(sessions.values()):
            time.sleep(1)

        load = self.generate_load()

        start_time = time.time()
        message_count = 0

        while True:
            elapsed_time = time.time() - start_time

            if elapsed_time >= self.send_duration:
                break

            if message_count >= len(load):
                message_count = 0
            print(sessions)

            for session_id in sessions:
                session = fix.Session.lookupSession(session_id)
                print(session)

                if session is not None and session.isLoggedOn():
                   message = self.generate_message(load[message_count])
                   fix.Session.sendToTarget(message, self.session_id)

            message_count += 1

            time.sleep(1)

        application.stop()

    """
        
    def run(self):
        settings = fix.SessionSettings(self.connection_config_file)
        application = fix.SocketInitiator(self, fix.FileStoreFactory(settings), settings)
        application.start()

        while not all(session.isLoggedOn() for session in self.sessions.values()):
            time.sleep(1)

        load = self.generate_load()

        start_time = time.time()
        message_count = 0

        while True:
            elapsed_time = time.time() - start_time

            if elapsed_time >= self.send_duration:
                break

            if message_count >= len(load):
                message_count = 0
            print(self.sessions)

            for session_id in self.sessions:
                session = self.sessions[session_id]
                print(session)   

                if session is not None and session.isLoggedOn():
                    message = self.generate_message(load[message_count], session_id)
                    fix.Session.sendToTarget(message, session_id)
            message_count += 1

            time.sleep(1)

        application.stop()


# Read configuration from config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# Load configuration values
template_file = config.get("LoadGenerator", "template_file")
connection_config_file = config.get("LoadGenerator", "connection_config_file")
log_file = config.get("LoadGenerator", "log_file")
message_rate = float(config.get("LoadGenerator", "message_rate"))
send_duration = int(config.get("LoadGenerator", "send_duration"))

message_weights = dict(config.items("MessageTypes"))



# Initialize the FIX application
app = MyApplication(template_file, message_weights, message_rate)
app.connection_config_file = connection_config_file
app.send_duration = send_duration

# Run the FIX application
app.run()
