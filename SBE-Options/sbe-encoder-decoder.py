from struct import pack, unpack_from


class SBEHeader:
    BLOCK_LENGTH = 7

    def __init__(self, template_id):
        self.template_id = template_id

    def encode(self):
        return pack('B6s', self.BLOCK_LENGTH, self.template_id.to_bytes(6, 'big'))

    def decode(self, buffer):
        block_length, template_id = unpack_from('B6s', buffer)
        return block_length, int.from_bytes(template_id, 'big')


class UTCTimestampNanos:
    SIZE = 8

    def __init__(self, timestamp):
        self.timestamp = timestamp

    def encode(self):
        return pack('>Q', self.timestamp)

    def decode(self, buffer):
        self.timestamp, = unpack_from('>Q', buffer)


class Char:
    SIZE = 1

    def __init__(self, value):
        self.value = value

    def encode(self):
        return pack('s', self.value.encode())

    def decode(self, buffer):
        value, = unpack_from('s', buffer)
        self.value = value.decode()


class TimeInForceType:
    SIZE = 1

    def __init__(self, value):
        self.value = value

    def encode(self):
        return pack('B', self.value)

    def decode(self, buffer):
        self.value, = unpack_from('B', buffer)


class ExecInstType:
    SIZE = 2

    def __init__(self, value):
        self.value = value

    def encode(self):
        return pack('H', self.value)

    def decode(self, buffer):
        self.value, = unpack_from('H', buffer)


class TradingCapacityType:
    SIZE = 1

    def __init__(self, value):
        self.value = value

    def encode(self):
        return pack('B', self.value)

    def decode(self, buffer):
        self.value, = unpack_from('B', buffer)


class MtpGroupIDType:
    SIZE = 2

    def __init__(self, value):
        self.value = value

    def encode(self):
        return pack('>H', self.value)

    def decode(self, buffer):
        self.value, = unpack_from('>H', buffer)


class MatchTradePreventionType:
    SIZE = 1

    def __init__(self, value):
        self.value = value

    def encode(self):
        return pack('B', self.value)

    def decode(self, buffer):
        self.value, = unpack_from('B', buffer)


class UINT16:
    SIZE = 2

    def __init__(self, value):
        self.value = value

    def encode(self):
        return pack('>H', self.value)

    def decode(self, buffer):
        self.value, = unpack_from('>H', buffer)


class RepeatingGroupDimensions:
    SIZE = 4

    def __init__(self, count):
        self.count = count

    def encode(self):
        return pack('>I', self.count)

    def decode(self, buffer):
        self.count, = unpack_from('>I', buffer)


class PartyID:
    SIZE = 2

    def __init__(self, value):
        self.value = value

    def encode(self):
        return pack('>H', self.value)

    def decode(self, buffer):
        self.value, = unpack_from('>H', buffer)


class PartiesGroup:
    def __init__(self, party_ids):
        self.party_ids = party_ids

    def encode(self):
        encoded_parties = b''.join(party_id.encode() for party_id in self.party_ids)
        return encoded_parties

    def decode(self, buffer):
        num_party_ids = len(buffer) // PartyID.SIZE
        self.party_ids = []
        for i in range(num_party_ids):
            offset = i * PartyID.SIZE
            party_id_value, = unpack_from('>H', buffer, offset)
            self.party_ids.append(PartyID(party_id_value))


class NewOrderSingle:
    TEMPLATE_ID = 1

    def __init__(self, sending_time, cl_ord_id, time_in_force, exec_inst, trading_capacity, mtp_group_id,
                 match_trade_prevention, cancel_group_id, risk_group_id):
        self.sbe_header = SBEHeader(self.TEMPLATE_ID)
        self.sending_time = sending_time
        self.cl_ord_id = cl_ord_id
        self.time_in_force = time_in_force
        self.exec_inst = exec_inst
        self.trading_capacity = trading_capacity
        self.mtp_group_id = mtp_group_id
        self.match_trade_prevention = match_trade_prevention
        self.cancel_group_id = cancel_group_id
        self.risk_group_id = risk_group_id

    def encode(self):
        encoded_header = self.sbe_header.encode()
        encoded_sending_time = self.sending_time.encode()
        encoded_cl_ord_id = self.cl_ord_id.encode()
        encoded_time_in_force = self.time_in_force.encode()
        encoded_exec_inst = self.exec_inst.encode()
        encoded_trading_capacity = self.trading_capacity.encode()
        encoded_mtp_group_id = b'' if self.mtp_group_id is None else self.mtp_group_id.encode()
        encoded_match_trade_prevention = b'' if self.match_trade_prevention is None else self.match_trade_prevention.encode()
        encoded_cancel_group_id = b'' if self.cancel_group_id is None else self.cancel_group_id.encode()
        encoded_risk_group_id = b'' if self.risk_group_id is None else self.risk_group_id.encode()

        encoded_message = encoded_header + encoded_sending_time + encoded_cl_ord_id + encoded_time_in_force + \
            encoded_exec_inst + encoded_trading_capacity + encoded_mtp_group_id + encoded_match_trade_prevention + \
            encoded_cancel_group_id + encoded_risk_group_id

        return encoded_message

    def decode(self, buffer):
        offset = 0

        block_length, template_id = self.sbe_header.decode(buffer[offset:])
        offset += SBEHeader.BLOCK_LENGTH

        self.sending_time = UTCTimestampNanos(0)
        self.sending_time.decode(buffer[offset:])
        offset += UTCTimestampNanos.SIZE

        self.cl_ord_id = Char('')
        self.cl_ord_id.decode(buffer[offset:])
        offset += Char.SIZE

        self.time_in_force = TimeInForceType(0)
        self.time_in_force.decode(buffer[offset:])
        offset += TimeInForceType.SIZE

        self.exec_inst = ExecInstType(0)
        self.exec_inst.decode(buffer[offset:])
        offset += ExecInstType.SIZE

        self.trading_capacity = TradingCapacityType(0)
        self.trading_capacity.decode(buffer[offset:])
        offset += TradingCapacityType.SIZE

        if template_id >= 2:
            self.mtp_group_id = MtpGroupIDType(0)
            self.mtp_group_id.decode(buffer[offset:])
            offset += MtpGroupIDType.SIZE

            if template_id >= 4:
                self.match_trade_prevention = MatchTradePreventionType(0)
                self.match_trade_prevention.decode(buffer[offset:])
                offset += MatchTradePreventionType.SIZE

                if template_id >= 6:
                    self.cancel_group_id = UINT16(0)
                    self.cancel_group_id.decode(buffer[offset:])
                    offset += UINT16.SIZE

                    if template_id >= 8:
                        self.risk_group_id = UINT16(0)
                        self.risk_group_id.decode(buffer[offset:])
                        offset += UINT16.SIZE


class ShortTwoSidedQuote:
    SIZE = 25

    def __init__(self, list_seq_no, options_security_id, bid_size, bid_px, offer_size, offer_px):
        self.list_seq_no = UINT8(list_seq_no)
        self.options_security_id = CHAR(options_security_id)
        self.bid_size = UINT16(bid_size)
        self.bid_px = ShortPriceType(bid_px)
        self.offer_size = UINT16(offer_size)
        self.offer_px = ShortPriceType(offer_px)

    def encode(self):
        encoded_list_seq_no = self.list_seq_no.encode()
        encoded_options_security_id = self.options_security_id.encode()
        encoded_bid_size = self.bid_size.encode()
        encoded_bid_px = self.bid_px.encode()
        encoded_offer_size = self.offer_size.encode()
        encoded_offer_px = self.offer_px.encode()

        return encoded_list_seq_no + encoded_options_security_id + encoded_bid_size + encoded_bid_px + \
               encoded_offer_size + encoded_offer_px

    def decode(self, buffer):
        offset = 0

        self.list_seq_no = UINT8(0)
        self.list_seq_no.decode(buffer[offset:])
        offset += UINT8.SIZE

        self.options_security_id = CHAR('')
        self.options_security_id.decode(buffer[offset:])
        offset += CHAR.SIZE

        self.bid_size = UINT16(0)
        self.bid_size.decode(buffer[offset:])
        offset += UINT16.SIZE

        self.bid_px = ShortPriceType(0)
        self.bid_px.decode(buffer[offset:])
        offset += ShortPriceType.SIZE

        self.offer_size = UINT16(0)
        self.offer_size.decode(buffer[offset:])
        offset += UINT16.SIZE

        self.offer_px = ShortPriceType(0)
        self.offer_px.decode(buffer[offset:])
        offset += ShortPriceType.SIZE


class ShortTwoSideBulkQuote:
    TEMPLATE_ID = 2

    def __init__(self, sending_time, cl_ord_id, time_in_force, exec_inst, trading_capacity, mtp_group_id,
                 match_trade_prevention, cancel_group_id, risk_group_id, parties, quotes):
        self.sbe_header = SBEHeader(self.TEMPLATE_ID)
        self.sending_time = sending_time
        self.cl_ord_id = cl_ord_id
        self.time_in_force = time_in_force
        self.exec_inst = exec_inst
        self.trading_capacity = trading_capacity
        self.mtp_group_id = mtp_group_id
        self.match_trade_prevention = match_trade_prevention
        self.cancel_group_id = cancel_group_id
        self.risk_group_id = risk_group_id
        self.no_party_ids = RepeatingGroupDimensions(len(parties))
        self.parties = parties
        self.no_quote_entries = RepeatingGroupDimensions(len(quotes))
        self.quotes = quotes

    def encode(self):
        encoded_header = self.sbe_header.encode()
        encoded_sending_time = self.sending_time.encode()
        encoded_cl_ord_id = self.cl_ord_id.encode()
        encoded_time_in_force = self.time_in_force.encode()
        encoded_exec_inst = self.exec_inst.encode()
        encoded_trading_capacity = self.trading_capacity.encode()
        encoded_mtp_group_id = b'' if self.mtp_group_id is None else self.mtp_group_id.encode()
        encoded_match_trade_prevention = b'' if self.match_trade_prevention is None else \
            self.match_trade_prevention.encode()
        encoded_cancel_group_id = b'' if self.cancel_group_id is None else self.cancel_group_id.encode()
        encoded_risk_group_id = b'' if self.risk_group_id is None else self.risk_group_id.encode()

        encoded_parties = b''
        for party in self.parties:
            encoded_parties += party.encode()

        encoded_quotes = b''
        for quote in self.quotes:
            encoded_quotes += quote.encode()

        encoded_message = encoded_header + encoded_sending_time + encoded_cl_ord_id + encoded_time_in_force + \
            encoded_exec_inst + encoded_trading_capacity + encoded_mtp_group_id + encoded_match_trade_prevention + \
            encoded_cancel_group_id + encoded_risk_group_id + encoded_parties + encoded_quotes

        return encoded_message

    def decode(self, buffer):
        offset = 0

        block_length, template_id = self.sbe_header.decode(buffer[offset:])
        offset += SBEHeader.BLOCK_LENGTH

        self.sending_time = UTCTimestampNanos(0)
        self.sending_time.decode(buffer[offset:])
        offset += UTCTimestampNanos.SIZE

        self.cl_ord_id = Char('')
        self.cl_ord_id.decode(buffer[offset:])
        offset += Char.SIZE

        self.time_in_force = TimeInForceType(0)
        self.time_in_force.decode(buffer[offset:])
        offset += TimeInForceType.SIZE

        self.exec_inst = ExecInstType(0)
        self.exec_inst.decode(buffer[offset:])
        offset += ExecInstType.SIZE

        self.trading_capacity = TradingCapacityType(0)
        self.trading_capacity.decode(buffer[offset:])
        offset += TradingCapacityType.SIZE

        if template_id >= 2:
            self.mtp_group_id = MtpGroupIDType(0)
            self.mtp_group_id.decode(buffer[offset:])
            offset += MtpGroupIDType.SIZE

            if template_id >= 4:
                self.match_trade_prevention = MatchTradePreventionType(0)
                self.match_trade_prevention.decode(buffer[offset:])
                offset += MatchTradePreventionType.SIZE

                if template_id >= 6:
                    self.cancel_group_id = UINT16(0)
                    self.cancel_group_id.decode(buffer[offset:])
                    offset += UINT16.SIZE

                    if template_id >= 8:
                        self.risk_group_id = UINT16(0)
                        self.risk_group_id.decode(buffer[offset:])
                        offset += UINT16.SIZE

        self.no_party_ids = RepeatingGroupDimensions(0)
        self.no_party_ids.decode(buffer[offset:])
        offset += RepeatingGroupDimensions.SIZE

        self.parties = []
        for i in range(self.no_party_ids.value):
            party = Party()
            party.decode(buffer[offset:])
            self.parties.append(party)
            offset += Party.SIZE

        self.no_quote_entries = RepeatingGroupDimensions(0)
        self.no_quote_entries.decode(buffer[offset:])
        offset += RepeatingGroupDimensions.SIZE

        self.quotes = []
        for i in range(self.no_quote_entries.value):
            quote = ShortTwoSidedQuote(0, '', 0, 0.0, 0, 0.0)
            quote.decode(buffer[offset:])
            self.quotes.append(quote)
            offset += ShortTwoSidedQuote.SIZE


class LongTwoSidedQuote:
    SIZE = 33

    def __init__(self, list_seq_no, options_security_id, bid_size, bid_px, offer_size, offer_px):
        self.list_seq_no = UINT8(list_seq_no)
        self.options_security_id = CHAR(options_security_id)
        self.bid_size = UINT32(bid_size)
        self.bid_px = PriceType(bid_px)
        self.offer_size = UINT32(offer_size)
        self.offer_px = PriceType(offer_px)

    def encode(self):
        encoded_list_seq_no = self.list_seq_no.encode()
        encoded_options_security_id = self.options_security_id.encode()
        encoded_bid_size = self.bid_size.encode()
        encoded_bid_px = self.bid_px.encode()
        encoded_offer_size = self.offer_size.encode()
        encoded_offer_px = self.offer_px.encode()

        return encoded_list_seq_no + encoded_options_security_id + encoded_bid_size + encoded_bid_px + \
               encoded_offer_size + encoded_offer_px

    def decode(self, buffer):
        offset = 0

        self.list_seq_no = UINT8(0)
        self.list_seq_no.decode(buffer[offset:])
        offset += UINT8.SIZE

        self.options_security_id = CHAR('')
        self.options_security_id.decode(buffer[offset:])
        offset += CHAR.SIZE

        self.bid_size = UINT32(0)
        self.bid_size.decode(buffer[offset:])
        offset += UINT32.SIZE

        self.bid_px = PriceType(0.0)
        self.bid_px.decode(buffer[offset:])
        offset += PriceType.SIZE

        self.offer_size = UINT32(0)
        self.offer_size.decode(buffer[offset:])
        offset += UINT32.SIZE

        self.offer_px = PriceType(0.0)
        self.offer_px.decode(buffer[offset:])
        offset += PriceType.SIZE


class LongTwoSideBulkQuote:
    TEMPLATE_ID = 3

    def __init__(self, sending_time, cl_ord_id, time_in_force, exec_inst, trading_capacity, mtp_group_id,
                 match_trade_prevention, cancel_group_id, risk_group_id, parties, quotes):
        self.sbe_header = SBEHeader(self.TEMPLATE_ID)
        self.sending_time = sending_time
        self.cl_ord_id = cl_ord_id
        self.time_in_force = time_in_force
        self.exec_inst = exec_inst
        self.trading_capacity = trading_capacity
        self.mtp_group_id = mtp_group_id
        self.match_trade_prevention = match_trade_prevention
        self.cancel_group_id = cancel_group_id
        self.risk_group_id = risk_group_id
        self.no_party_ids = RepeatingGroupDimensions(len(parties))
        self.parties = parties
        self.no_quote_entries = RepeatingGroupDimensions(len(quotes))
        self.quotes = quotes

    def encode(self):
        encoded_header = self.sbe_header.encode()
        encoded_sending_time = self.sending_time.encode()
        encoded_cl_ord_id = self.cl_ord_id.encode()
        encoded_time_in_force = self.time_in_force.encode()
        encoded_exec_inst = self.exec_inst.encode()
        encoded_trading_capacity = self.trading_capacity.encode()
        encoded_mtp_group_id = b'' if self.mtp_group_id is None else self.mtp_group_id.encode()
        encoded_match_trade_prevention = b'' if self.match_trade_prevention is None else \
            self.match_trade_prevention.encode()
        encoded_cancel_group_id = b'' if self.cancel_group_id is None else self.cancel_group_id.encode()
        encoded_risk_group_id = b'' if self.risk_group_id is None else self.risk_group_id.encode()

        encoded_parties = b''
        for party in self.parties:
            encoded_parties += party.encode()

        encoded_quotes = b''
        for quote in self.quotes:
            encoded_quotes += quote.encode()

        encoded_message = encoded_header + encoded_sending_time + encoded_cl_ord_id + encoded_time_in_force + \
            encoded_exec_inst + encoded_trading_capacity + encoded_mtp_group_id + encoded_match_trade_prevention + \
            encoded_cancel_group_id + encoded_risk_group_id + encoded_parties + encoded_quotes

        return encoded_message

    def decode(self, buffer):
        offset = 0

        block_length, template_id = self.sbe_header.decode(buffer[offset:])
        offset += SBEHeader.BLOCK_LENGTH

        self.sending_time = UTCTimestampNanos(0)
        self.sending_time.decode(buffer[offset:])
        offset += UTCTimestampNanos.SIZE

        self.cl_ord_id = Char('')
        self.cl_ord_id.decode(buffer[offset:])
        offset += Char.SIZE

        self.time_in_force = TimeInForceType(0)
        self.time_in_force.decode(buffer[offset:])
        offset += TimeInForceType.SIZE

        self.exec_inst = ExecInstType(0)
        self.exec_inst.decode(buffer[offset:])
        offset += ExecInstType.SIZE

        self.trading_capacity = TradingCapacityType(0)
        self.trading_capacity.decode(buffer[offset:])
        offset += TradingCapacityType.SIZE

        if template_id >= 2:
            self.mtp_group_id = MtpGroupIDType(0)
            self.mtp_group_id.decode(buffer[offset:])
            offset += MtpGroupIDType.SIZE

            if template_id >= 4:
                self.match_trade_prevention = MatchTradePreventionType(0)
                self.match_trade_prevention.decode(buffer[offset:])
                offset += MatchTradePreventionType.SIZE

                if template_id >= 6:
                    self.cancel_group_id = UINT16(0)
                    self.cancel_group_id.decode(buffer[offset:])
                    offset += UINT16.SIZE

                    if template_id >= 8:
                        self.risk_group_id = UINT16(0)
                        self.risk_group_id.decode(buffer[offset:])
                        offset += UINT16.SIZE

        self.no_party_ids = RepeatingGroupDimensions(0)
        self.no_party_ids.decode(buffer[offset:])
        offset += RepeatingGroupDimensions.SIZE

        self.parties = []
        for i in range(self.no_party_ids.value):
            party = Party()
            party.decode(buffer[offset:])
            self.parties.append(party)
            offset += Party.SIZE

        self.no_quote_entries = RepeatingGroupDimensions(0)
        self.no_quote_entries.decode(buffer[offset:])
        offset += RepeatingGroupDimensions.SIZE

        self.quotes = []
        for i in range(self.no_quote_entries.value):
            quote = LongTwoSidedQuote(0, '', 0, 0.0, 0, 0.0)
            quote.decode(buffer[offset:])
            self.quotes.append(quote)
            offset += LongTwoSidedQuote.SIZE

