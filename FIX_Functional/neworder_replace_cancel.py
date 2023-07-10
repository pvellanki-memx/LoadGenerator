import unittest
import time
import fix
from fix_validator import validate_execution_report, replace_placeholders

class TestFIXSession(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = fix.Application()
        cls.settings = fix.SessionSettings("config.cfg")
        cls.storeFactory = fix.FileStoreFactory(cls.settings)
        cls.logFactory = fix.ScreenLogFactory(cls.settings)
        cls.initiator = fix.SocketInitiator(cls.app, cls.storeFactory, cls.settings, cls.logFactory)
        cls.initiator.start()
        time.sleep(1)
        cls.session_id = cls.app.session_id

    @classmethod
    def tearDownClass(cls):
        cls.initiator.stop()

def send_new_order_single(self, order_type, time_in_force, order_qty, symbol, exec_inst=''):
    with open(self.app.template_file, 'r') as file:
        template_messages = file.readlines()

    for template_message in template_messages:
        placeholders = {
            '<ClOrdID>': self.app.generate_clordid(),
            '<OrderQty>': str(order_qty),
            '<Symbol>': symbol,
            '<OrdType>': order_type,
            '<TimeInForce>': time_in_force,
            '<ExecInst>': exec_inst
        }
        message = replace_placeholders(template_message, placeholders)

            party_group_fields = [
                "448=QAX1",
                "447=D",
                "452=66"
            ]

            # Insert the repeating group into the message
            repeating_group = "|".join(party_group_fields)
            message = message.replace('<RepeatingGroup>', repeating_group)
        
            # Replace the field delimiter from '|' to SOH character
            message = message.replace('|', chr(0x01))

        new_order_message = fix.Message()
        new_order_message.setString(message, False, self.app.message_factory)


        fix.Session.sendToTarget(new_order_message, self.session_id)

        time.sleep(2)

        self.assertTrue(self.app.execution_report_received)
        exec_report = self.app.last_execution_report
        cl_ord_id = exec_report.getField(11)

        validate_execution_report(exec_report, order_qty=order_qty, symbol=symbol, order_type=order_type, tif=time_in_force)
        self.assertEqual(exec_report.getField(39), '0')


    def send_cancel_replace_request(self, orig_cl_ord_id, new_price=None, new_order_qty=None):
        with open(self.app.template_file, 'r') as file:
            template_messages = file.readlines()

        for template_message in template_messages:
            placeholders = {
                '<ClOrdID>': self.app.generate_clordid(),
                '<OrigClOrdID>': orig_cl_ord_id,
                '<Price>': str(new_price) if new_price else '',
                '<OrderQty>': str(new_order_qty) if new_order_qty else ''
            }
            message = replace_placeholders(template_message, placeholders)

            cancel_replace_message = fix.Message()
            cancel_replace_message.setString(message, False, self.app.message_factory)
            fix.Session.sendToTarget(cancel_replace_message, self.session_id)

            time.sleep(2)

            self.assertTrue(self.app.execution_report_received)
            exec_report = self.app.last_execution_report
            cl_ord_id = exec_report.getField(11)

            validate_execution_report(exec_report, order_qty=new_order_qty, symbol='', order_type='', tif='')
            self.assertEqual(exec_report.getField(39), '0')

    def send_order_cancel_request(self, orig_cl_ord_id):
        with open(self.app.template_file, 'r') as file:
            template_messages = file.readlines()

        for template_message in template_messages:
            placeholders = {
                '<ClOrdID>': self.app.generate_clordid(),
                '<OrigClOrdID>': orig_cl_ord_id
            }
            message = replace_placeholders(template_message, placeholders)

            order_cancel_message = fix.Message()
            order_cancel_message.setString(message, False, self.app.message_factory)
            fix.Session.sendToTarget(order_cancel_message, self.session_id)

            time.sleep(2)

            self.assertTrue(self.app.execution_report_received)
            exec_report = self.app.last_execution_report
            cl_ord_id = exec_report.getField(11)

            validate_execution_report(exec_report, order_qty=0, symbol='', order_type='', tif='')
            self.assertEqual(exec_report.getField(39), '4')

    def test_market_order_with_day_tif(self):
        self.send_new_order_single(order_type='1', time_in_force='0', order_qty=100, symbol='AAPL')

    def test_market_order_with_ioc_tif(self):
        self.send_new_order_single(order_type='1', time_in_force='3', order_qty=100, symbol='AAPL')

    def test_limit_order_with_day_tif(self):
        self.send_new_order_single(order_type='2', time_in_force='0', order_qty=100, symbol='AAPL')

    def test_limit_order_with_ioc_tif(self):
        self.send_new_order_single(order_type='2', time_in_force='3', order_qty=100, symbol='AAPL')

    def test_limit_order_with_iso_modifier(self):
        self.send_new_order_single(order_type='2', time_in_force='0', order_qty=100, symbol='AAPL', exec_inst='F')

    def test_rejected_market_order_with_iso_modifier(self):
        self.send_new_order_single(order_type='1', time_in_force='0', order_qty=100, symbol='AAPL', exec_inst='F')
        self.assertEqual(self.app.last_execution_report.getField(39), '8')

    def test_cancel_replace_price(self):
        self.send_new_order_single(order_type='2', time_in_force='0', order_qty=100, symbol='AAPL')
        orig_cl_ord_id = self.app.last_execution_report.getField(11)
        self.send_cancel_replace_request(orig_cl_ord_id, new_price=150)

    def test_cancel_replace_qty(self):
        self.send_new_order_single(order_type='2', time_in_force='0', order_qty=100, symbol='AAPL')
        orig_cl_ord_id = self.app.last_execution_report.getField(11)
        self.send_cancel_replace_request(orig_cl_ord_id, new_order_qty=50)

    def tearDown(self):
        orig_cl_ord_id = self.app.last_execution_report.getField(11)
        self.send_order_cancel_request(orig_cl_ord_id)

if __name__ == '__main__':
    unittest.main()
