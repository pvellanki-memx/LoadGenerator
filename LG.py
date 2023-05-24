import random

class FIXSession:
    def __init__(self, session_id, host, port, sender, target):
        self.session_id = session_id
        self.host = host
        self.port = port
        self.sender = sender
        self.target = target


def generate_message(templates):
    # Randomly select a message template based on probabilities
    message_type = random.choices(
        population=list(templates.keys()),
        weights=list(templates.values()),
        k=1
    )[0]

    # Get the selected message template
    template = templates[message_type]

    # Replace placeholder values in the template with random values
    message = template.replace('<Sender>', session.sender)
    message = message.replace('<Target>', session.target)
    message = message.replace('<ClOrdID>', str(random.randint(1, 1000000)))
    message = message.replace('<Price>', str(round(random.uniform(1, 100), 2)))
    message = message.replace('<Quantity>', str(random.randint(1, 100)))
    return message

def load_generator(config_file):
    # Read and parse the configuration from the file
    config = configparser.ConfigParser()
    config.read(config_file)

    # Configure the FIX connection settings
    sessions = []
    for section in config.sections():
        session_id = section
        host = config.get(section, 'host')
        port = config.getint(section, 'port')
        sender = config.get(section, 'sender')
        target = config.get(section, 'target')
        session = FIXSession(session_id, host, port, sender, target)
        sessions.append(session)

    # Configure the message rate
    message_rate = config.getfloat('Load', 'message_rate')

    # Configure the message templates and their probabilities
    templates = {}
    for section in config.sections():
        if section.startswith('Message'):
            message_type = section
            probability = config.getfloat('MessageTemplates', message_type)
            template_file = config.get(section, 'template_file')
            with open(template_file, 'r') as file:
                template = file.read()
            templates[message_type] = {
                'template': template,
                'probability': probability
            }
    
    # Track the number of established sessions
    num_established_sessions = 0

    # Establish connections for all sessions
    for session in sessions:
        session.establish_connection()
        if session.is_established:
            num_established_sessions += 1

    # Start the initial load generation
    is_paused = False  # Variable to track the load generator's pause state

    # Main loop for load generation
    while True:
        if not is_paused:
            for session in sessions:
                message = generate_message(templates)
                print(f"Sending message for session {session.session_id}:")
                print(message)
                time.sleep(1 / message_rate)
        else:
            print("Load generation paused.")
            print("To resume the load generation, enter 'r'.")
            print("To change the message rate, enter 'c' followed by the new rate.")
            print("To quit, enter 'q'.")
            user_input = input()

            if user_input.lower() == 'r':
                print("Resuming load generation...")
                is_paused = False
            elif user_input.lower().startswith('c'):
                new_rate = float(user_input[1:].strip())
                message_rate = new_rate
                print("Changing the message rate to", message_rate)
                print("Resuming load generation...")
                is_paused = False
