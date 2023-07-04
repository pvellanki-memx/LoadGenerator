import unittest
import fix
import time


def replace_placeholders(template_message, placeholders):
    """
    Replaces the placeholders in the given template message with the provided values.
    """
    replaced_message = template_message
    for placeholder, value in placeholders.items():
        replaced_message = replaced_message.replace(placeholder, value)
    return replaced_message


def validate_execution_report(exec_report, order_qty, symbol, order_type, tif, price):
    """
    Validates the fields on the execution report against the provided values.
    """
    # Check OrderQty
    received_order_qty = exec_report.getField(38)
    assert received_order_qty == str(order_qty), f"Expected OrderQty: {order_qty}, Received: {received_order_qty}"

    # Check Symbol
    received_symbol = exec_report.getField(55)
    assert received_symbol == symbol, f"Expected Symbol: {symbol}, Received: {received_symbol}"

    # Check OrdType
    received_order_type = exec_report.getField(40)
    assert received_order_type == order_type, f"Expected OrdType: {order_type}, Received: {received_order_type}"

    # Check TimeInForce
    received_tif = exec_report.getField(59)
    assert received_tif == tif, f"Expected TimeInForce: {tif}, Received: {received_tif}"

    # Check Price
    received_price = exec_report.getField(44)
    assert received_price == str(price), f"Expected Price: {price}, Received: {received_price}"


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = MyApplication('template_file.txt', read_config_file('config.ini'))

        settings = fix.SessionSettings('connections.cfg')
        store_factory = fix.FileStoreFactory(settings)
        log_factory = fix.FileLogFactory(settings)
        self.initiator = fix.SocketInitiator(self.app, store_factory, settings, log_factory)
        self.initiator.start()
        time.sleep(2)

    def tearDown(self):
        self.initiator.stop()
        time.sleep(2)

    def test_send_market_order_with_DAY(self):
        # Read template messages from file
        with open(self.app.template_file, 'r') as file:
            template_messages = file.readlines()

        # Iterate over template messages
        for template_message in template_messages:
            # Replace placeholders in the message template
            placeholders = {'<ClOrdID>': self.app.generate_clordid()}
            message = replace_placeholders(template_message, placeholders)

            # Create and send the NewOrderSingle message with Market order type and DAY time-in-force
            new_order_message = fix.Message()
            new_order_message.setString(message, False, self.app.message_factory)
            new_order_message.setField(40, '1')  # Market order type
            new_order_message.setField(59, '0')  # DAY time-in-force
            fix.Session.sendToTarget(new_order_message, self.session_id)

            # Wait for execution report
            time.sleep(2)

            # Assert that the execution report was received
            self.assertTrue(self.app.execution_report_received)

            # Get the ClOrdID from the execution report
            exec_report = self.app.last_execution_report
            cl_ord_id = exec_report.getField(11)

            # Validate the fields on the execution report
            validate_execution_report(exec_report, order_qty=100, symbol='AAPL', order_type='1', tif='0', price=0.0)

            # Add assertions or further verifications as needed

    def test_send_market_order_with_IOC(self):
        # Read template messages from file
        with open(self.app.template_file, 'r') as file:
            template_messages = file.readlines()

        # Iterate over template messages
        for template_message in template_messages:
            # Replace placeholders in the message template
            placeholders = {'<ClOrdID>': self.app.generate_clordid()}
            message = replace_placeholders(template_message, placeholders)

            # Create and send the NewOrderSingle message with Market order type and IOC time-in-force
            new_order_message = fix.Message()
            new_order_message.setString(message, False, self.app.message_factory)
            new_order_message.setField(40, '1')  # Market order type
            new_order_message.setField(59, '3')  # IOC time-in-force
            fix.Session.sendToTarget(new_order_message, self.session_id)

            # Wait for execution report
            time.sleep(2)

            # Assert that the execution report was received
            self.assertTrue(self.app.execution_report_received)

            # Get the ClOrdID from the execution report
            exec_report = self.app.last_execution_report
            cl_ord_id = exec_report.getField(11)

            # Validate the fields on the execution report
            validate_execution_report(exec_report, order_qty=100, symbol='AAPL', order_type='1', tif='3', price=0.0)

            # Add assertions or further verifications as needed

    def test_send_limit_order_with_DAY(self):
        # Read template messages from file
        with open(self.app.template_file, 'r') as file:
            template_messages = file.readlines()

        # Iterate over template messages
        for template_message in template_messages:
            # Replace placeholders in the message template
            placeholders = {'<ClOrdID>': self.app.generate_clordid()}
            message = replace_placeholders(template_message, placeholders)

            # Create and send the NewOrderSingle message with Limit order type and DAY time-in-force
            new_order_message = fix.Message()
            new_order_message.setString(message, False, self.app.message_factory)
            new_order_message.setField(40, '2')  # Limit order type
            new_order_message.setField(59, '0')  # DAY time-in-force
            fix.Session.sendToTarget(new_order_message, self.session_id)

            # Wait for execution report
            time.sleep(2)

            # Assert that the execution report was received
            self.assertTrue(self.app.execution_report_received)

            # Get the ClOrdID from the execution report
            exec_report = self.app.last_execution_report
            cl_ord_id = exec_report.getField(11)

            # Validate the fields on the execution report
            validate_execution_report(exec_report, order_qty=100, symbol='AAPL', order_type='2', tif='0', price=100.0)

            # Add assertions or further verifications as needed

    def test_send_limit_order_with_IOC(self):
        # Read template messages from file
        with open(self.app.template_file, 'r') as file:
            template_messages = file.readlines()

        # Iterate over template messages
        for template_message in template_messages:
            # Replace placeholders in the message template
            placeholders = {'<ClOrdID>': self.app.generate_clordid()}
            message = replace_placeholders(template_message, placeholders)

            # Create and send the NewOrderSingle message with Limit order type and IOC time-in-force
            new_order_message = fix.Message()
            new_order_message.setString(message, False, self.app.message_factory)
            new_order_message.setField(40, '2')  # Limit order type
            new_order_message.setField(59, '3')  # IOC time-in-force
            fix.Session.sendToTarget(new_order_message, self.session_id)

            # Wait for execution report
            time.sleep(2)

            # Assert that the execution report was received
            self.assertTrue(self.app.execution_report_received)

            # Get the ClOrdID from the execution report
            exec_report = self.app.last_execution_report
            cl_ord_id = exec_report.getField(11)

            # Validate the fields on the execution report
            validate_execution_report(exec_report, order_qty=100, symbol='AAPL', order_type='2', tif='3', price=100.0)

            # Add assertions or further verifications as needed

    def test_send_limit_order_with_ISO(self):
        # Read template messages from file
        with open(self.app.template_file, 'r') as file:
            template_messages = file.readlines()

        # Iterate over template messages
        for template_message in template_messages:
            # Replace placeholders in the message template
            placeholders = {'<ClOrdID>': self.app.generate_clordid()}
            message = replace_placeholders(template_message, placeholders)

            # Create and send the NewOrderSingle message with Limit order type and ISO modifier
            new_order_message = fix.Message()
            new_order_message.setString(message, False, self.app.message_factory)
            new_order_message.setField(40, '2')  # Limit order type
            new_order_message.setField(18, 'f')  # ISO modifier
            fix.Session.sendToTarget(new_order_message, self.session_id)

            # Wait for execution report
            time.sleep(2)

            # Assert that the execution report was received
            self.assertTrue(self.app.execution_report_received)

            # Get the ClOrdID from the execution report
            exec_report = self.app.last_execution_report
            cl_ord_id = exec_report.getField(11)

            # Validate the fields on the execution report
            validate_execution_report(exec_report, order_qty=100, symbol='AAPL', order_type='2', tif='0', price=100.0)
            self.assertEqual(exec_report.getField(18), 'f')  # Check if ISO modifier is present

          

def test_send_market_order_ISO_rejected(self):
    # Read template messages from file
    with open(self.app.template_file, 'r') as file:
        template_messages = file.readlines()

    # Iterate over template messages
    for template_message in template_messages:
        # Replace placeholders in the message template
        placeholders = {'<ClOrdID>': self.app.generate_clordid()}
        message = replace_placeholders(template_message, placeholders)

        # Create and send the NewOrderSingle message with Market order type
        new_order_message = fix.Message()
        new_order_message.setString(message, False, self.app.message_factory)
        new_order_message.setField(40, '1')  # Market order type
        fix.Session.sendToTarget(new_order_message, self.session_id)

        # Wait for execution report
        time.sleep(2)

        # Assert that the execution report was received
        self.assertTrue(self.app.execution_report_received)

        # Get the ClOrdID from the execution report
        exec_report = self.app.last_execution_report
        cl_ord_id = exec_report.getField(11)

        # Validate the fields on the execution report
        validate_execution_report(exec_report, order_qty=100, symbol='AAPL', order_type='1', tif='0')
        self.assertEqual(exec_report.getField(39), '8') 
  

if __name__ == '__main__':
    unittest.main()

