import configparser
import random
import time
import datetime
import quickfix as fix

# Global variables
sessions = {}

# Class representing the FIX application
class MyApplication(fix.Application):
    def __init__(self, message_weights, message_rate):
        super().__init__()
        self.message_weights = message_weights
        self.message_rate = message_rate
        self.sessions = {}
        self.log_file = "./log/load_generator.log"

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

    def generate_message(self, message_type, session_id):
        if message_type.lower() == "logon":
            message = fix.Message()
            message.getHeader().setField(fix.MsgType(fix.MsgType_Logon))
        elif message_type.lower() == "newordersingle":
            message = fix.Message()
            message.getHeader().setField(fix.MsgType(fix.MsgType_NewOrderSingle))
            # Set other required fields for NewOrderSingle message
        elif message_type.lower() == "orderreplace":
            message = fix.Message()
            message.getHeader().setField(fix.MsgType(fix.MsgType_OrderCancelReplaceRequest))
            # Set other required fields for OrderCancelReplaceRequest message
        elif message_type.lower() == "ordercancel":
            message = fix.Message()
            message.getHeader().setField(fix.MsgType(fix.MsgType_OrderCancelRequest))
            # Set other required fields for OrderCancelRequest message
        else:
            # Unknown message type
            return None

        # Set the ClOrdID
        message.setField(fix.ClOrdID(self.generate_clordid()))

        # Get the outgoing sequence number
        seq_num = self.get_outgoing_seq_num(session_id)

        # Set the MsgSeqNum
        message.getHeader().setField(fix.MsgSeqNum(seq_num))

        # Generate the SendingTime in the desired format
        sending_time = datetime.datetime.utcnow().strftime('%Y%m%d-%H:%M:%S.%f')[:-3]
        message.getHeader().setField(fix.SendingTime(sending_time))

        # Calculate the CheckSum
        message.calculateString()
        message.setField(fix.CheckSum(self.calculate_checksum(message.toString())))

        return message

    def increment_outgoing_seq_num(self, session_id):
        session = fix.Session.lookupSession(fix.SessionID(session_id))
        if session is not None:
            session.incrementNextSenderMsgSeqNumContinuation of the `MyApplication` class:

```python
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
        load = []
        for message_type, weight in self.message_weights.items():
            weight = int(weight)
            template = self.generate_template_for_message_type(message_type)
            if template:
                load.extend([message_type.lower()] * weight)

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

    def generate_template_for_message_type(self, message_type):
        if message_type.lower() == "logon":
            return "logon"
        elif message_type.lower() == "newordersingle":
            return "new_order_template"
        elif message_type.lower() == "orderreplace":
            return "order_replace_template"
        elif message_type.lower() == "ordercancel":
            return "order_cancel_template"
        else:
            return None

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
app = MyApplication(message_weights, message_rate)
app.template_file = template_file
app.connection_config_file = connection_config_file
app.send_duration = send_duration

# Run the FIX application
app.run()
