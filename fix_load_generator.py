import configparser
import random
import time
import datetime
import os
import quickfix as fix
import quickfix44 as fix44



# Global variables
sessions = {}

# Class representing the FIX application
class MyApplication(fix.Application):
    def __init__(self, message_weights, message_rate):
        super().__init__()
        self.message_weights = message_weights
        self.message_rate = message_rate
        self.sessions = {}
        self.log_directory = "log"

    def onCreate(self, sessionID):
        print("Session created -", sessionID.toString())
        self.sessions[sessionID] = fix.Session.lookupSession(sessionID)

    def toAdmin(self, message, sessionID):
        if message.getHeader().getField(fix.MsgType()).getString() == fix.MsgType_Logon:
            message.getHeader().setField(1408, "1.3")
            message.getHeader().setField(43, "Y")
            print("sent admin message", message.toString())
        return True

    def toApp(self, message, sessionID):
        session_id = sessionID.toString()
        with open(self.get_log_file(), "a") as file:
            file.write(f"Session: {session_id}\n")
            file.write(message.toString() + '\n')
        print("sent application message", message.toString())

    def fromApp(self, message, sessionID):
        session_id = sessionID.toString()
        with open(self.get_log_file(), "a") as file:
            file.write(f"Session: {session_id}\n")
            file.write(message.toString() + '\n')
        print("received application message", message.toString())

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
        with open(self.get_log_file(), 'a') as file:
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

def generate_message(self, message_type, session_id):
    with open('instrument_definitions.json', 'r') as file:
        instrument_definitions = json.load(file)

    if message_type.lower() == "logon":
        message = fix.Message()
        message.getHeader().setField(fix.BeginString(fix.BeginString_FIXT11))
        message.getHeader().setField(fix.MsgType(fix.MsgType_Logon))

        # Set other required fields for Logon message
        message.setField(fix.EncryptMethod(0))
        message.setField(fix.HeartBtInt(30))
        message.setField(fix.ResetSeqNumFlag(False))
        message.setField(fix.DefaultApplVerID("FIX.5.0SP2"))
        message.setField(fix.DefaultCstmApplVerID("1.3"))

    elif message_type.lower() == "newordersingle":
        message = fix.Message()
        message.getHeader().setField(fix.BeginString(session_id.getBeginString().getString()))
        message.getHeader().setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        message.getHeader().setField(fix.SenderCompID(session_id.getSenderCompID().getString()))
        message.getHeader().setField(fix.TargetCompID(session_id.getTargetCompID().getString()))
        message.getHeader().setField(fix.MsgSeqNum(self.get_outgoing_seq_num(session_id)))

        # Set other required fields for NewOrderSingle message
        message.setField(fix.Symbol("AMD"))
        message.setField(fix.Side(fix.Side_BUY))
        message.setField(fix.OrderQty(100))
        message.setField(fix.Price(8))
        message.setField(fix.OrdType(fix.OrdType_LIMIT))
        message.setField(fix.TimeInForce(fix.TimeInForce_DAY))
        message.setField(fix.ClOrdID(self.generate_clordid()))
        message.setField(fix.ExecInst("h"))

        option_id = None
        for item in instrument_definitions:
            if item['underlyingSymbolId'] == symbol:
                option_id = item['optionId']
                break

        if option_id:
            instrument_definition = next((item for item in instrument_definitions if item["optionId"] == option_id), None)
            if instrument_definition:
                message.setField(fix.PutOrCall(instrument_definition["putCall"]))
                message.setField(fix.StrikePrice(instrument_definition["strikePrice"]))
                message.setField(21035, option_id)

        # Create the repeating group for PartyIDs
        party_group = fix44.NewOrderSingle.NoPartyIDs()
        party_group.setField(448, "QAX3")
        party_group.setField(447, "D")
        party_group.setField(452, "1")
        message.addGroup(party_group)



            elif message_type.lower() == "orderreplace":
                pass
                # ...
                # Code for other message types
                # ...

            elif message_type.lower() == "ordercancel":
                pass
                #..
                # Code for other message types
                # ...

            else:
                # Unknown message type
                return None

            return message



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
        load = []
        for message_type, weight in self.message_weights.items():
            weight = int(weight)
            print(weight)
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
        
    def get_log_file(self):
        os.makedirs(self.log_directory, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file_name = f"log_file_{timestamp}.log"
        print(os.path.join(self.log_directory, log_file_name))
        return os.path.join(self.log_directory, log_file_name)

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
connection_config_file = config.get("LoadGenerator", "connection_config_file")
log_file = config.get("LoadGenerator", "log_file")
message_rate = float(config.get("LoadGenerator", "message_rate"))
send_duration = int(config.get("LoadGenerator", "send_duration"))
symbol = config.get("LoadGenerator", "symbol")

message_weights = dict(config.items("MessageTypes"))

# Initialize the FIX application
app = MyApplication(message_weights, message_rate)
app.connection_config_file = connection_config_file
app.send_duration = send_duration

# Run the FIX application
app.run()












def generate_message(self, message_type, session_id):
    with open('instrument_definitions.json', 'r') as file:
        instrument_definitions = json.load(file)

    if message_type.lower() == "logon":
        message = fix.Message()
        message.getHeader().setField(fix.BeginString(fix.BeginString_FIXT11))
        message.getHeader().setField(fix.MsgType(fix.MsgType_Logon))

        # Set other required fields for Logon message
        message.setField(fix.EncryptMethod(0))
        message.setField(fix.HeartBtInt(30))
        message.setField(fix.ResetSeqNumFlag(False))
        message.setField(fix.DefaultApplVerID("FIX.5.0SP2"))
        message.setField(fix.DefaultCstmApplVerID("1.3"))

    elif message_type.lower() == "newordersingle":
        message = fix.Message()
        message.getHeader().setField(fix.BeginString(session_id.getBeginString().getString()))
        message.getHeader().setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        message.getHeader().setField(fix.SenderCompID(session_id.getSenderCompID().getString()))
        message.getHeader().setField(fix.TargetCompID(session_id.getTargetCompID().getString()))
        message.getHeader().setField(fix.MsgSeqNum(self.get_outgoing_seq_num(session_id)))

        # Set other required fields for NewOrderSingle message
        message.setField(fix.Symbol("AMD"))
        message.setField(fix.Side(fix.Side_BUY))
        message.setField(fix.OrderQty(100))
        message.setField(fix.Price(8))
        message.setField(fix.OrdType(fix.OrdType_LIMIT))
        message.setField(fix.TimeInForce(fix.TimeInForce_DAY))
        message.setField(fix.ClOrdID(self.generate_clordid()))
        message.setField(fix.ExecInst("h"))

        option_id = None
        for item in instrument_definitions:
            if item['underlyingSymbolId'] == symbol:
                option_id = item['optionId']
                break

        if option_id:
            instrument_definition = next((item for item in instrument_definitions if item["optionId"] == option_id), None)
            if instrument_definition:
                message.setField(fix.PutOrCall(instrument_definition["putCall"]))
                message.setField(fix.StrikePrice(instrument_definition["strikePrice"]))
                message.setField(21035, option_id)

        # Create the repeating group for PartyIDs
        party_group = fix44.NewOrderSingle.NoPartyIDs()
        party_group.setField(448, "QAX3")
        party_group.setField(447, "D")
        party_group.setField(452, "1")
        message.addGroup(party_group)



