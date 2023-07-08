import unittest
import string
import time
from random import choices, randint
from sbe_load_generator import generate_message, establish_session, send_message
from sbe_encoder_decoder import (
    SideType, OrdType, TimeInForceType, UTCTimestampNanos, ExecInstType,
    TradingCapacityType, PartiesGroup, ShortTwoSideBulkQuote,
    ShortTwoSidedQuote, MtpGroupIDType, MatchTradePreventionType, UINT16, PriceType,
    PartyID, PartyIDSource, PartyRoleType
)

class TestSbeLoadGenerator(unittest.TestCase):
    def setUp(self):
        self.session_name = "Session1"  # Update with your session name
        self.client_socket, self.session_id = establish_session(self.session_name)

    def tearDown(self):
        self.client_socket.close()

    def test_send_market_order(self):
        message_type = "NewOrderSingle"
        sending_time = UTCTimestampNanos(int(time.time() * 10**9))
        cl_ord_id = ''.join(choices(string.ascii_uppercase + string.digits, k=20))
        options_security_id = choices(security_ids)[0]
        side = SideType(value=SideType.BUY)
        order_qty = randint(1, 100)
        ord_type = OrdType(value=OrdType.MARKET)
        time_in_force = TimeInForceType(value=TimeInForceType.DAY)
        exec_inst = ExecInstType(value=ExecInstType.ParticipateDoNotInitiate)
        trading_capacity = TradingCapacityType(value=TradingCapacityType.CUSTOMER)
        efid = connection_config[self.session_name]['EFID']
        party_id = PartyID(efid)
        party_id_source = PartyIDSource('D')
        party_role = PartyRoleType('CUSTOMER')
        parties = [PartiesGroup(party_ids=[[party_id, party_id_source, party_role]])]

        kwargs = {
            'sending_time': sending_time,
            'cl_ord_id': cl_ord_id,
            'options_security_id': options_security_id,
            'side': side,
            'order_qty': order_qty,
            'ord_type': ord_type,
            'price': None,
            'time_in_force': time_in_force,
            'exec_inst': exec_inst,
            'trading_capacity': trading_capacity,
            'parties': parties
        }

        message = generate_message(message_type, self.session_name, **kwargs)
        self.assertIsNotNone(message)
        send_message(self.client_socket, message)

    def test_send_limit_order(self):
        message_type = "NewOrderSingle"
        sending_time = UTCTimestampNanos(int(time.time() * 10**9))
        cl_ord_id = ''.join(choices(string.ascii_uppercase + string.digits, k=20))
        options_security_id = choices(security_ids)[0]
        side = SideType(value=SideType.SELL)
        order_qty = randint(1, 100)
        ord_type = OrdType(value=OrdType.LIMIT)
        price = PriceType(112, 0)
        time_in_force = TimeInForceType(value=TimeInForceType.DAY)
        exec_inst = ExecInstType(value=ExecInstType.ParticipateDoNotInitiate)
        trading_capacity = TradingCapacityType(value=TradingCapacityType.CUSTOMER)
        efid = connection_config[self.session_name]['EFID']
        party_id = PartyID(efid)
        party_id_source = PartyIDSource('D')
        party_role = PartyRoleType('CUSTOMER')
        parties = [PartiesGroup(party_ids=[[party_id, party_id_source, party_role]])]

        kwargs = {
            'sending_time': sending_time,
            'cl_ord_id': cl_ord_id,
            'options_security_id': options_security_id,
            'side': side,
            'order_qty': order_qty,
            'ord_type': ord_type,
            'price': price,
            'time_in_force': time_in_force,
            'exec_inst': exec_inst,
            'trading_capacity': trading_capacity,
            'parties': parties
        }

        message = generate_message(message_type, self.session_name, **kwargs)
        self.assertIsNotNone(message)
        send_message(self.client_socket, message)

    def test_send_ioc_order(self):
        message_type = "NewOrderSingle"
        sending_time = UTCTimestampNanos(int(time.time() * 10**9))
        cl_ord_id = ''.join(choices(string.ascii_uppercase + string.digits, k=20))
        options_security_id = choices(security_ids)[0]
        side = SideType(value=SideType.BUY)
        order_qty = randint(1, 100)
        ord_type = OrdType(value=OrdType.LIMIT)
        price = PriceType(112, 0)
        time_in_force = TimeInForceType(value=TimeInForceType.IOC)
        exec_inst = ExecInstType(value=ExecInstType.ParticipateDoNotInitiate)
        trading_capacity = TradingCapacityType(value=TradingCapacityType.CUSTOMER)
        efid = connection_config[self.session_name]['EFID']
        party_id = PartyID(efid)
        party_id_source = PartyIDSource('D')
        party_role = PartyRoleType('CUSTOMER')
        parties = [PartiesGroup(party_ids=[[party_id, party_id_source, party_role]])]

        kwargs = {
            'sending_time': sending_time,
            'cl_ord_id': cl_ord_id,
            'options_security_id': options_security_id,
            'side': side,
            'order_qty': order_qty,
            'ord_type': ord_type,
            'price': price,
            'time_in_force': time_in_force,
            'exec_inst': exec_inst,
            'trading_capacity': trading_capacity,
            'parties': parties
        }

        message = generate_message(message_type, self.session_name, **kwargs)
        self.assertIsNotNone(message)
        send_message(self.client_socket, message)

    def test_send_day_order(self):
        message_type = "NewOrderSingle"
        sending_time = UTCTimestampNanos(int(time.time() * 10**9))
        cl_ord_id = ''.join(choices(string.ascii_uppercase + string.digits, k=20))
        options_security_id = choices(security_ids)[0]
        side = SideType(value=SideType.SELL)
        order_qty = randint(1, 100)
        ord_type = OrdType(value=OrdType.LIMIT)
        price = PriceType(112, 0)
        time_in_force = TimeInForceType(value=TimeInForceType.DAY)
        exec_inst = ExecInstType(value=ExecInstType.ParticipateDoNotInitiate)
        trading_capacity = TradingCapacityType(value=TradingCapacityType.CUSTOMER)
        efid = connection_config[self.session_name]['EFID']
        party_id = PartyID(efid)
        party_id_source = PartyIDSource('D')
        party_role = PartyRoleType('CUSTOMER')
        parties = [PartiesGroup(party_ids=[[party_id, party_id_source, party_role]])]

        kwargs = {
            'sending_time': sending_time,
            'cl_ord_id': cl_ord_id,
            'options_security_id': options_security_id,
            'side': side,
            'order_qty': order_qty,
            'ord_type': ord_type,
            'price': price,
            'time_in_force': time_in_force,
            'exec_inst': exec_inst,
            'trading_capacity': trading_capacity,
            'parties': parties
        }

        message = generate_message(message_type, self.session_name, **kwargs)
        self.assertIsNotNone(message)
        send_message(self.client_socket, message)

    def test_send_short_two_sided_bulk_quote_two_entries(self):
        message_type = "ShortTwoSideBulkQuote"
        sending_time = UTCTimestampNanos(int(time.time() * 10**9))
        cl_ord_id = ''.join(choices(string.ascii_uppercase + string.digits, k=20))
        time_in_force = TimeInForceType(1)
        exec_inst = ExecInstType(0)
        trading_capacity = TradingCapacityType(1)
        mtp_group_id = MtpGroupIDType(1)
        match_trade_prevention = MatchTradePreventionType(1)
        cancel_group_id = UINT16(1)
        risk_group_id = UINT16(1)
        efid = connection_config[self.session_name]['EFID']
        party_id = PartyID(efid)
        party_id_source = PartyIDSource('D')
        party_role = PartyRoleType('CUSTOMER')
        parties = [PartiesGroup(party_ids=[[party_id, party_id_source, party_role]])]
        quotes = [
            ShortTwoSidedQuote(list_seq_no=1, options_security_id='AAPL', bid_size=10, bid_mantissa=100, offer_size=20, offer_mantissa=150),
            ShortTwoSidedQuote(list_seq_no=2, options_security_id='TSLA123', bid_size=15, bid_mantissa=200, offer_size=25, offer_mantissa=250)
        ]

        kwargs = {
            'sending_time': sending_time,
            'cl_ord_id': cl_ord_id,
            'time_in_force': time_in_force,
            'exec_inst': exec_inst,
            'trading_capacity': trading_capacity,
            'mtp_group_id': mtp_group_id,
            'match_trade_prevention': match_trade_prevention,
            'cancel_group_id': cancel_group_id,
            'risk_group_id': risk_group_id,
            'parties': parties,
            'quotes': quotes
        }

        # Create an instance of ShortTwoSideBulkQuote and set the field values
        short_two_side_bulk_quote = ShortTwoSideBulkQuote(**kwargs)

        # Encode the ShortTwoSideBulkQuote instance
        encoded_message = short_two_side_bulk_quote.encode()

        # Print the encoded message
        print('ShortTwoSideBulkQuote:')
        print(encoded_message)

        # Send the encoded message on the session
        send_message(self.client_socket, encoded_message)

    def test_send_short_two_sided_bulk_quote_three_entries(self):
        message_type = "ShortTwoSideBulkQuote"
        sending_time = UTCTimestampNanos(int(time.time() * 10**9))
        cl_ord_id = ''.join(choices(string.ascii_uppercase + string.digits, k=20))
        time_in_force = TimeInForceType(1)
        exec_inst = ExecInstType(0)
        trading_capacity = TradingCapacityType(1)
        mtp_group_id = MtpGroupIDType(1)
        match_trade_prevention = MatchTradePreventionType(1)
        cancel_group_id = UINT16(1)
        risk_group_id = UINT16(1)
        efid = connection_config[self.session_name]['EFID']
        party_id = PartyID(efid)
        party_id_source = PartyIDSource('D')
        party_role = PartyRoleType('CUSTOMER')
        parties = [PartiesGroup(party_ids=[[party_id, party_id_source, party_role]])]
        quotes = [
            ShortTwoSidedQuote(list_seq_no=1, options_security_id='AAPL', bid_size=10, bid_mantissa=100, offer_size=20, offer_mantissa=150),
            ShortTwoSidedQuote(list_seq_no=2, options_security_id='TSLA123', bid_size=15, bid_mantissa=200, offer_size=25, offer_mantissa=250),
            ShortTwoSidedQuote(list_seq_no=3, options_security_id='GOOG', bid_size=30, bid_mantissa=300, offer_size=40, offer_mantissa=400)
        ]

        kwargs = {
            'sending_time': sending_time,
            'cl_ord_id': cl_ord_id,
            'time_in_force': time_in_force,
            'exec_inst': exec_inst,
            'trading_capacity': trading_capacity,
            'mtp_group_id': mtp_group_id,
            'match_trade_prevention': match_trade_prevention,
            'cancel_group_id': cancel_group_id,
            'risk_group_id': risk_group_id,
            'parties': parties,
            'quotes': quotes
        }

        # Create an instance of ShortTwoSideBulkQuote and set the field values
        short_two_side_bulk_quote = ShortTwoSideBulkQuote(**kwargs)

        # Encode the ShortTwoSideBulkQuote instance
        encoded_message = short_two_side_bulk_quote.encode()

        # Print the encoded message
        print('ShortTwoSideBulkQuote:')
        print(encoded_message)

        # Send the encoded message on the session
        send_message(self.client_socket, encoded_message)

    def test_send_short_two_sided_bulk_quote_twenty_one_entries(self):
        message_type = "ShortTwoSideBulkQuote"
        sending_time = UTCTimestampNanos(int(time.time() * 10**9))
        cl_ord_id = ''.join(choices(string.ascii_uppercase + string.digits, k=20))
        time_in_force = TimeInForceType(1)
        exec_inst = ExecInstType(0)
        trading_capacity = TradingCapacityType(1)
        mtp_group_id = MtpGroupIDType(1)
        match_trade_prevention = MatchTradePreventionType(1)
        cancel_group_id = UINT16(1)
        risk_group_id = UINT16(1)
        efid = connection_config[self.session_name]['EFID']
        party_id = PartyID(efid)
        party_id_source = PartyIDSource('D')
        party_role = PartyRoleType('CUSTOMER')
        parties = [PartiesGroup(party_ids=[[party_id, party_id_source, party_role]])]
        quotes = []

        for i in range(21):
            quote = ShortTwoSidedQuote(
                list_seq_no=i + 1,
                options_security_id=f'Security{i}',
                bid_size=10 + i,
                bid_mantissa=100 + i,
                offer_size=20 + i,
                offer_mantissa=150 + i
            )
            quotes.append(quote)

        kwargs = {
            'sending_time': sending_time,
            'cl_ord_id': cl_ord_id,
            'time_in_force': time_in_force,
            'exec_inst': exec_inst,
            'trading_capacity': trading_capacity,
            'mtp_group_id': mtp_group_id,
            'match_trade_prevention': match_trade_prevention,
            'cancel_group_id': cancel_group_id,
            'risk_group_id': risk_group_id,
            'parties': parties,
            'quotes': quotes
        }

        # Create an instance of ShortTwoSideBulkApologies, but it seems that I missed the completion of the code in my previous response. Here's the complete script with the remaining parts included:

```python
from sbe_encoder_decoder import PriceType

# Existing code...

class TestSbeLoadGenerator(unittest.TestCase):
    # Existing code...

    def test_send_short_two_sided_bulk_quote_two_entries(self):
        message_type = "ShortTwoSideBulkQuote"
        sending_time = UTCTimestampNanos(int(time.time() * 10**9))
        cl_ord_id = ''.join(choices(string.ascii_uppercase + string.digits, k=20))
        time_in_force = TimeInForceType(1)
        exec_inst = ExecInstType(0)
        trading_capacity = TradingCapacityType(1)
        mtp_group_id = MtpGroupIDType(1)
        match_trade_prevention = MatchTradePreventionType(1)
        cancel_group_id = UINT16(1)
        risk_group_id = UINT16(1)
        efid = connection_config[self.session_name]['EFID']
        party_id = PartyID(efid)
        party_id_source = PartyIDSource('D')
        party_role = PartyRoleType('CUSTOMER')
        parties = [PartiesGroup(party_ids=[[party_id, party_id_source, party_role]])]
        quotes = [
            ShortTwoSidedQuote(list_seq_no=1, options_security_id='AAPL', bid_size=10, bid_mantissa=100, offer_size=20, offer_mantissa=150),
            ShortTwoSidedQuote(list_seq_no=2, options_security_id='TSLA123', bid_size=15, bid_mantissa=200, offer_size=25, offer_mantissa=250)
        ]

        kwargs = {
            'sending_time': sending_time,
            'cl_ord_id': cl_ord_id,
            'time_in_force': time_in_force,
            'exec_inst': exec_inst,
            'trading_capacity': trading_capacity,
            'mtp_group_id': mtp_group_id,
            'match_trade_prevention': match_trade_prevention,
            'cancel_group_id': cancel_group_id,
            'risk_group_id': risk_group_id,
            'parties': parties,
            'quotes': quotes
        }

        # Create an instance of ShortTwoSideBulkQuote and set the field values
        short_two_side_bulk_quote = ShortTwoSideBulkQuote(**kwargs)

        # Encode the ShortTwoSideBulkQuote instance
        encoded_message = short_two_side_bulk_quote.encode()

        # Print the encoded message
        print('ShortTwoSideBulkQuote:')
        print(encoded_message)

        # Send the encoded message on the session
        send_message(self.client_socket, encoded_message)

    def test_send_short_two_sided_bulk_quote_three_entries(self):
        message_type = "ShortTwoSideBulkQuote"
        sending_time = UTCTimestampNanos(int(time.time() * 10**9))
        cl_ord_id = ''.join(choices(string.ascii_uppercase + string.digits, k=20))
        time_in_force = TimeInForceType(1)
        exec_inst = ExecInstType(0)
        trading_capacity = TradingCapacityType(1)
        mtp_group_id = MtpGroupIDType(1)
        match_trade_prevention = MatchTradePreventionType(1)
        cancel_group_id = UINT16(1)
        risk_group_id = UINT16(1)
        efid = connection_config[self.session_name]['EFID']
        party_id = PartyID(efid)
        party_id_source = PartyIDSource('D')
        party_role = PartyRoleType('CUSTOMER')
        parties = [PartiesGroup(party_ids=[[party_id, party_id_source, party_role]])]
        quotes = [
            ShortTwoSidedQuote(list_seq_no=1, options_security_id='AAPL', bid_size=10, bid_mantissa=100, offer_size=20, offer_mantissa=150),
            ShortTwoSidedQuote(list_seq_no=2, options_security_id='TSLA123', bid_size=15, bid_mantissa=200, offer_size=25, offer_mantissa=250),
            ShortTwoSidedQuote(list_seq_no=3, options_security_id='GOOG', bid_size=30, bid_mantissa=300, offer_size=40, offer_mantissa=400)
        ]

        kwargs = {
            'sending_time': sending_time,
            'cl_ord_id': cl_ord_id,
            'time_in_force': time_in_force,
            'exec_inst': exec_inst,
            'trading_capacity': trading_capacity,
            'mtp_group_id': mtp_group_id,
            'match_trade_prevention': match_trade_prevention,
            'cancel_group_id': cancel_group_id,
            'risk_group_id': risk_group_id,
            'parties': parties,
            'quotes': quotes
        }

        # Create an instance of ShortTwoSideBulkQuote and set the field values
        short_two_side_bulk_quote = ShortTwoSideBulkQuote(**kwargs)

        # Encode the ShortTwoSideBulkQuote instance
        encoded_message = short_two_side_bulk_quote.encode()

        # Print the encoded message
        print('ShortTwoSideBulkQuote:')
        print(encoded_message)

        # Send the encoded message on the session
        send_message(self.client_socket, encoded_message)

    def test_send_short_two_sided_bulk_quote_twenty_one_entries(self):
        message_type = "ShortTwoSideBulkQuote"
        sending_time = UTCTimestampNanos(int(time.time() * 10**9))
        cl_ord_id = ''.join(choices(string.ascii_uppercase + string.digits, k=20))
        time_in_force = TimeInForceType(1)
        exec_inst = ExecInstType(0)
        trading_capacity = TradingCapacityType(1)
        mtp_group_id = MtpGroupIDType(1)
        match_trade_prevention = MatchTradePreventionType(1)
        cancel_group_id = UINT16(1)
        risk_group_id = UINT16(1)
        efid = connection_config[self.session_name]['EFID']
        party_id = PartyID(efid)
        party_id_source = PartyIDSource('D')
        party_role = PartyRoleType('CUSTOMER')
        parties = [PartiesGroup(party_ids=[[party_id, party_id_source, party_role]])]
        quotes = []

        for i in range(21):
            quote = ShortTwoSidedQuote(
                list_seq_no=i + 1,
                options_security_id=f'Security{i}',
                bid_size=10 + i,
                bid_mantissa=100 + i,
                offer_size=20 + i,
                offer_mantissa=150 + i
            )
            quotes.append(quote)

        kwargs = {
            'sending_time': sending_time,
            'cl_ord_id': cl_ord_id,
            'time_in_force': time_in_force,
            'exec_inst': exec_inst,
            'trading_capacity': trading_capacity,
            'mtp_group_id': mtp_group_id,
            'match_trade_prevention': match_trade_prevention,
            'cancel_group_id': cancel_group_id,
            'risk_group_id': risk_group_id,
            'parties': parties,
            'quotes': quotes
        }

        # Create an instance of ShortTwoSideBulkQuote and set the field values
        short_two_side_bulk_quote = ShortTwoSideBulkQuote(**kwargs)

        # Encode the ShortTwoSideBulkQuote instance
        encoded_message = short_two_side_bulk_quote.encode()

        # Print the encoded message
        print('ShortTwoSideBulkQuote:')
        print(encoded_message)

        # Send the encoded message on the session
        send_message(self.client_socket, encoded_message)
