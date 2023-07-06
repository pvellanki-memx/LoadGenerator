from struct import pack, unpack_from


class SBEHeader:
    

    def __init__(self, block_length, template_id, schema_id, version, num_groups):
        self.block_length = block_length
        self.template_id = template_id
        self.schema_id = schema_id
        self.version = version
        self.num_groups = num_groups

    def encode(self):
        return pack('>HBBHB', self.block_length, self.template_id, self.schema_id, self.version, self.num_groups)

    def decode(self, buffer):
        block_length, template_id, schema_id, version, num_groups = unpack_from('>HBBHH', buffer)
        return block_length, template_id, schema_id, version, num_groups


class PriceType:
    def __init__(self, mantissa, exponent=None):
        self.mantissa = mantissa
        self.exponent = exponent

    def encode(self):
        buffer = pack('>Q',self.mantissa)
        return buffer

    def decode(self, buffer):
        self.exponent, _, self.mantissa = unpack_from('>Q', buffer)

class OrdType:
    MARKET = 1
    LIMIT = 2

    SIZE = 1
    def __init__(self, value):
        self.value = value

    def encode(self):
        buffer = pack('>B', self.value)
        return buffer

    def decode(self, buffer):
        self.value = unpack_from('>B', buffer)[0]

class BooleanType:
    FALSE = 0
    TRUE = 1

    SIZE = 1

    def __init__(self, value):
        self.value = value

    def encode(self):
        return pack('B', self.value)

    def decode(self, buffer):
        self.value, = unpack_from('B', buffer)


class SideType:
    BUY = 1
    SELL = 2
    SIZE = 1
    def __init__(self, value):
        self.value = value

    def encode(self):
        buffer = pack('>B', self.value)
        return buffer

    def decode(self, buffer):
        self.value = unpack_from('>B', buffer)[0]



class UINT32:
    def __init__(self, value):
        self.value = value

    def encode(self):
        buffer = pack('>I', self.value)
        return buffer

    def decode(self, buffer):
        self.value = unpack_from('>I', buffer)[0]

class UINT8:
    def __init__(self, value):
        self.value = value

    def encode(self):
        buffer = pack('>B', self.value)
        return buffer

    def decode(self, buffer):
        self.value = unpack_from('>B', buffer)[0]


    

class ShortPriceType:
    def __init__(self, mantissa, exponent):
        self.mantissa = mantissa
        self.exponent = exponent

    def encode(self):
        buffer = pack('>H',self.mantissa)
        return buffer

    def decode(self, buffer):
        self.exponent, _, self.mantissa = unpack_from('>H', buffer)

    def __str__(self):
        return f"Exponent: {self.exponent}, Mantissa: {self.mantissa}"



class UTCTimestampNanos:
    SIZE = 8

    def __init__(self, timestamp):
        self.timestamp = timestamp

    def encode(self):
        return pack('>Q', self.timestamp)

    def decode(self, buffer):
        self.timestamp, = unpack_from('>Q', buffer)

class Party:
    def __init__(self, party_id: str, party_id_source: str, party_role: str):
        self.party_id = party_id
        self.party_id_source = party_id_source
        self.party_role = party_role

    def encode(self):
        return pack('>4s2s2s', self.party_id.encode(), self.party_id_source.encode(), self.party_role.encode())

    @classmethod
    def decode(cls, buffer):
        party_id, party_id_source, party_role = unpack_from('>4s2s2s', buffer)
        return cls(party_id.decode(), party_id_source.decode(), party_role.decode())




class Char:
    SIZE = 1

    def __init__(self, value):
        self.value = value

    def encode(self):
        return pack('s', self.value.encode())

    def decode(self, buffer):
        value, = unpack_from('s', buffer)
        self.value = value.decode()


class OptionsSecurityID:
    SIZE = 8

    def __init__(self, value=''):
        self.value = value

    def encode(self):
        encoded_value = self.value.encode('utf-8')
        padding = b'\x00' * (self.SIZE - len(encoded_value))
        return encoded_value + padding

    def decode(self, buffer):
        encoded_value = buffer[:self.SIZE].rstrip(b'\x00')
        self.value = encoded_value.decode('utf-8')

    def __str__(self):
        return self.value


class OpenOrCloseType:
    OPEN ='o'
    CLOSE = 'c'
    NULL_VALUE = 'o'
    SIZE = 1

    def __init__(self, value):
        self.value = value

    def encode(self):
        return pack('s', self.value.encode())

    def decode(self, buffer):
        value, = unpack_from('s', buffer)
        self.value = value.decode()


class TimeInForceType:
    DAY = 0
    IMMEDIATE_OR_CANCEL = 3


    SIZE = 1

    def __init__(self, value):
        self.value = value

    def encode(self):
        return pack('B', self.value)

    def decode(self, buffer):
        self.value, = unpack_from('B', buffer)


class ExecInstType:
    ParticipateDoNotInitiate = 0
    IntermarketSweep = 1
    ExternalRoutingNotAllowed = 2
    SIZE = 2

    def __init__(self, value):
        self.value = value

    def encode(self):
        return pack('H', self.value)

    def decode(self, buffer):
        self.value, = unpack_from('H', buffer)


class TradingCapacityType:
    CUSTOMER = 1
    PROFESSIONAL_CUSTOMER = 2
    BROKER_DEALER = 3
    BROKER_DEALER_CUSTOMER = 4
    FIRM = 5
    MARKET_MAKER = 6
    AWAY_MARKET_MAKER = 7
    NULL_VALUE = 255

   
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
    CANCEL_NEWEST = 0
    CANCEL_OLDEST = 1
    CANCEL_BOTH = 3
    NULL_VALUE = 255

    SIZE = 1

    def __init__(self, value):
        self.value = value

    def encode(self):
        return pack('B', self.value)

    def decode(self, buffer):
        self.value, = unpack_from('B', buffer)

class RepriceFrequencyType:
    SINGLE_REPRICE = 0
    CONTINUOUS_REPRICE = 1
    NONE = 2
    NULL_VALUE = 255

    SIZE = 1

    def __init__(self, value):
        self.value = value

    def encode(self):
        return pack('B', self.value)

    def decode(self, buffer):
        self.value, = unpack_from('B', buffer)

class RepriceBehaviorType:
    REPRICE_LOCK_CANCEL_CROSS = 1
    REPRICE_LOCK_REPRICE_CROSS = 2
    NULL_VALUE = 255

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
    SIZE = 2

    def __init__(self, block_length,num_groups):
        self.block_length = block_length
        self.num_groups = num_groups

    def encode(self):
        return pack('>BB', self.block_length, self.num_groups)

    def decode(self, buffer):
        self.block_length,self.num_groups = unpack_from('>BB', buffer)


class PartyID:

    SIZE = 16

    def __init__(self, value):
        self.value = value

    def encode(self):
        return self.value.encode()[:16].ljust(16, b'\x00')

    def decode(self, buffer):
        self.value = buffer.decode().rstrip('\x00')

class PartyIDSource:
    SIZE = 1

    def __init__(self, value):
        self.value = value

    def encode(self):
        return self.value.encode()

    def decode(self, buffer):
        self.value = buffer.decode()


class PartyRoleType:
    SIZE = 1

    def __init__(self, value):
        self.value = value

    def encode(self):
        return self.value.encode()

    def decode(self, buffer):
        self.value = buffer.decode()


class PartiesGroup:
    def __init__(self, party_ids=None):
        self.party_ids = party_ids or []
        print(party_ids)
     

    def encode(self):
        encoded_parties = b''.join(b''.join(party_obj.encode() for party_obj in nested_list) for nested_list in self.party_ids)
        return encoded_parties

    def decode(self, buffer):
        num_party_ids = len(buffer) // (PartyID.SIZE + PartyIDSource.SIZE + PartyRoleType.SIZE)
        self.party_ids = []
        for i in range(num_party_ids):
            offset = i * (PartyID.SIZE + PartyIDSource.SIZE + PartyRoleType.SIZE)
            party_id = PartyID('')
            party_id.decode(buffer[offset:offset + PartyID.SIZE])
            offset += PartyID.SIZE
            party_id_source = PartyIDSource('')
            party_id_source.decode(buffer[offset:offset + PartyIDSource.SIZE])
            offset += PartyIDSource.SIZE
            party_role = PartyRoleType('')
            party_role.decode(buffer[offset:offset + PartyRoleType.SIZE])
            self.party_ids.append([party_id, party_id_source, party_role])



class NewOrderSingle:
    TEMPLATE_ID = 1
    num_groups = 1
    schema_id = 1
    version = 266
    BLOCK_LENGTH = 54

    def __init__(self, **kwargs):
        self.sbe_header = SBEHeader(self.BLOCK_LENGTH, self.TEMPLATE_ID, self.schema_id, self.version, self.num_groups )
        self.sending_time = kwargs.get('sending_time', UTCTimestampNanos(0))
        self.cl_ord_id = kwargs.get('cl_ord_id', Char(''))
        self.options_security_id = kwargs.get('options_security_id', OptionsSecurityID(''))
        self.side = kwargs.get('side', SideType(''))
        self.order_qty = kwargs.get('order_qty', UINT32(0))
        self.ord_type = kwargs.get('ord_type', Char(''))
        self.price = kwargs.get('price', PriceType(0,0))
        self.time_in_force = kwargs.get('time_in_force', TimeInForceType(0))
        self.open_or_close = kwargs.get('open_or_close', OpenOrCloseType('O'))
        self.exec_inst = kwargs.get('exec_inst', ExecInstType(0))
        self.trading_capacity = kwargs.get('trading_capacity', TradingCapacityType(0))
        self.reprice_frequency = kwargs.get('reprice_frequency', RepriceFrequencyType(0))
        self.reprice_behavior = kwargs.get('reprice_behavior', RepriceBehaviorType(0))
        self.mtp_group_id = kwargs.get('mtp_group_id', MtpGroupIDType(0))
        self.match_trade_prevention = kwargs.get('match_trade_prevention', MatchTradePreventionType(0))
        self.cancel_group_id = kwargs.get('cancel_group_id', UINT16(0))
        self.risk_group_id = kwargs.get('risk_group_id', UINT16(0))
        self.RepeatingGroupDimensions = kwargs.get('repeating_group_dimensions', RepeatingGroupDimensions(18,3))
        self.parties_group = kwargs.get('parties_group',PartiesGroup())
        

    def encode(self):
        encoded_header = self.sbe_header.encode()
        encoded_sending_time = self.sending_time.encode()
        encoded_cl_ord_id = self.cl_ord_id.encode()
        encoded_options_security_id = self.options_security_id.encode()
        encoded_side = self.side.encode()
        encoded_order_qty = self.order_qty.encode()
        encoded_ord_type = self.ord_type.encode()
        encoded_price = self.price.encode()
        encoded_time_in_force = self.time_in_force.encode()
        encoded_open_or_close = self.open_or_close.encode()
        encoded_exec_inst = self.exec_inst.encode()
        encoded_trading_capacity = self.trading_capacity.encode()
        encoded_reprice_frequency = self.reprice_frequency.encode()
        encoded_reprice_behavior = self.reprice_behavior.encode()
        encoded_mtp_group_id = self.mtp_group_id.encode()
        encoded_match_trade_prevention = self.match_trade_prevention.encode()
        encoded_cancel_group_id = self.cancel_group_id.encode()
        encoded_risk_group_id = self.risk_group_id.encode()
        encoded_RepeatingGroupDimensions = self.RepeatingGroupDimensions.encode()
        encoded_parties = b''
        for party in self.parties:
                encoded_parties += party.encode()

        encoded_message = (
            encoded_header +
            encoded_sending_time +
            encoded_cl_ord_id +
            encoded_options_security_id +
            encoded_side +
            encoded_order_qty +
            encoded_ord_type +
            encoded_price +
            encoded_time_in_force +
            encoded_open_or_close +
            encoded_exec_inst +
            encoded_trading_capacity +
            encoded_reprice_frequency +
            encoded_reprice_behavior +
            encoded_mtp_group_id +
            encoded_match_trade_prevention +
            encoded_cancel_group_id +
            encoded_risk_group_id +
            encoded_RepeatingGroupDimensions +
            encoded_parties
        )

        return encoded_message

    def decode(self, buffer):
        offset = 0

        block_length, template_id = self.sbe_header.decode(buffer[offset:offset + SBEHeader.BL])
        offset += SBEHeader.BLOCK_LENGTH

        self.sending_time = UTCTimestampNanos(0)
        self.sending_time.decode(buffer[offset:])
        offset += UTCTimestampNanos.SIZE

        self.cl_ord_id = Char('')
        self.cl_ord_id.decode(buffer[offset:])
        offset += Char.SIZE

        self.options_security_id_35 = Char('')
        self.options_security_id_35.decode(buffer[offset:])
        offset += Char.SIZE

        self.side = Char('')
        self.side.decode(buffer[offset:])
        offset += Char.SIZE

        self.order_qty = UINT32(0)
        self.order_qty.decode(buffer[offset:])
        offset += UINT32.SIZE

        self.ord_type = Char('')
        self.ord_type.decode(buffer[offset:])
        offset += Char.SIZE

        self.price = PriceType(0)
        self.price.decode(buffer[offset:])
        offset += PriceType.SIZE

        self.time_in_force = TimeInForceType(0)
        self.time_in_force.decode(buffer[offset:])
        offset += TimeInForceType.SIZE

        self.open_or_close = OpenOrCloseType('O')
        self.open_or_close.decode(buffer[offset:])
        offset += OpenOrCloseType.SIZE

        self.exec_inst = ExecInstType(0)
        self.exec_inst.decode(buffer[offset:])
        offset += ExecInstType.SIZE

        self.trading_capacity = TradingCapacityType(0)
        self.trading_capacity.decode(buffer[offset:])
        offset += TradingCapacityType.SIZE

        self.reprice_frequency = RepriceFrequencyType(0)
        self.reprice_frequency.decode(buffer[offset:])
        offset += RepriceFrequencyType.SIZE

        self.reprice_behavior = RepriceBehaviorType(0)
        self.reprice_behavior.decode(buffer[offset:])
        offset += RepriceBehaviorType.SIZE

        self.mtp_group_id = MtpGroupIDType(0)
        self.mtp_group_id.decode(buffer[offset:])
        offset += MtpGroupIDType.SIZE

        self.match_trade_prevention = MatchTradePreventionType(0)
        self.match_trade_prevention.decode(buffer[offset:])
        offset += MatchTradePreventionType.SIZE

        self.cancel_group_id = UINT16(0)
        self.cancel_group_id.decode(buffer[offset:])
        offset += UINT16.SIZE

        self.risk_group_id = UINT16(0)
        self.risk_group_id.decode(buffer[offset:])
        offset += UINT16.SIZE

        self.decode_parties(buffer[offset:])




class ShortTwoSidedQuote:
    SIZE = 25

    def __init__(self, list_seq_no=None, options_security_id=None, bid_size=None, bid_exponent=None,bid_mantissa=None, offer_size=None,offer_exponent=None,offer_mantissa=None):
        self.list_seq_no = UINT8(list_seq_no)
        self.options_security_id = OptionsSecurityID(options_security_id)
        self.bid_size = UINT16(bid_size)
        self.bid_px = ShortPriceType(bid_mantissa,bid_exponent)
        self.offer_size = UINT16(offer_size)
        self.offer_px = ShortPriceType(offer_mantissa,offer_exponent)

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

        self.options_security_id = Char('')
        self.options_security_id.decode(buffer[offset:])
        offset += Char.SIZE

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
    num_groups = 2
    schema_id = 1
    version = 266
    BLOCK_LENGTH = 39

    def __init__(self, **kwargs):
        self.sbe_header = SBEHeader(self.BLOCK_LENGTH, self.TEMPLATE_ID, self.schema_id, self.version, self.num_groups)
        self.sending_time = kwargs.get('sending_time', UTCTimestampNanos(0))
        self.cl_ord_id = kwargs.get('cl_ord_id', Char(''))
        self.time_in_force = kwargs.get('time_in_force', TimeInForceType(0))
        self.exec_inst = kwargs.get('exec_inst', ExecInstType(0))
        self.trading_capacity = kwargs.get('trading_capacity', TradingCapacityType(0))
        self.mtp_group_id = kwargs.get('mtp_group_id', MtpGroupIDType(0))
        self.match_trade_prevention = kwargs.get('match_trade_prevention', MatchTradePreventionType(0))
        self.cancel_group_id = kwargs.get('cancel_group_id', UINT16(0))
        self.risk_group_id = kwargs.get('risk_group_id', UINT16(0))
        quote_entries = len(kwargs.get('quotes', []))
        party_entries = len(kwargs.get('parties', []))
        self.no_party_ids = kwargs.get('repeating_group_dimensions', RepeatingGroupDimensions(18, party_entries))
        self.parties = kwargs.get('parties', PartiesGroup())
        self.no_quote_entries = kwargs.get('no_quote_entries', RepeatingGroupDimensions(15, quote_entries))
        self.quotes = kwargs.get('quotes',ShortTwoSidedQuote())

    def encode(self):
        encoded_header = self.sbe_header.encode()
        encoded_sending_time = self.sending_time.encode()
        encoded_cl_ord_id = self.cl_ord_id.encode()
        encoded_time_in_force = self.time_in_force.encode()
        encoded_exec_inst = self.exec_inst.encode()
        encoded_trading_capacity = self.trading_capacity.encode()
        encoded_mtp_group_id = self.mtp_group_id.encode()
        encoded_match_trade_prevention = self.match_trade_prevention.encode()
        encoded_cancel_group_id = self.cancel_group_id.encode()
        encoded_risk_group_id = self.risk_group_id.encode()
        encoded_no_party_ids =  self.no_party_ids.encode()
        encoded_parties = b''
        for party in self.parties:
                encoded_parties += party.encode()


        encoded_no_quote_entries =  self.no_quote_entries.encode()
        encoded_quotes = b''
        for quote in self.quotes:
                encoded_quotes += quote.encode()


        encoded_message = (
            encoded_header
            + encoded_sending_time
            + encoded_cl_ord_id
            + encoded_time_in_force
            + encoded_exec_inst
            + encoded_trading_capacity
            + encoded_mtp_group_id
            + encoded_match_trade_prevention
            + encoded_cancel_group_id
            + encoded_risk_group_id
            + encoded_no_party_ids
            + encoded_parties
            + encoded_no_quote_entries
            + encoded_quotes
        )

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

    def __init__(self, list_seq_no=None, options_security_id=None, bid_size=None, bid_px=None, offer_size=None, offer_px=None):
        self.list_seq_no = UINT8(list_seq_no)
        self.options_security_id = OptionsSecurityID(options_security_id)
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

        self.options_security_id = Char('')
        self.options_security_id.decode(buffer[offset:])
        offset += Char.SIZE

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
    num_groups = 2
    schema_id = 1
    version = 266
    BLOCK_LENGTH = 39

    def __init__(self, **kwargs):
        self.sbe_header = SBEHeader(self.BLOCK_LENGTH, self.TEMPLATE_ID, self.schema_id, self.version, self.num_groups)
        self.sending_time = kwargs.get('sending_time', UTCTimestampNanos(0))
        self.cl_ord_id = kwargs.get('cl_ord_id', Char(''))
        self.time_in_force = kwargs.get('time_in_force', TimeInForceType(0))
        self.exec_inst = kwargs.get('exec_inst', ExecInstType(0))
        self.trading_capacity = kwargs.get('trading_capacity', TradingCapacityType(0))
        self.mtp_group_id = kwargs.get('mtp_group_id', MtpGroupIDType(0))
        self.match_trade_prevention = kwargs.get('match_trade_prevention', MatchTradePreventionType(0))
        self.cancel_group_id = kwargs.get('cancel_group_id', UINT16(0))
        self.risk_group_id = kwargs.get('risk_group_id', UINT16(0))
        quote_entries = len(kwargs.get('quotes', []))
        party_entries = len(kwargs.get('parties', []))
        self.no_party_ids = kwargs.get('repeating_group_dimensions', RepeatingGroupDimensions(18, party_entries))
        self.parties = kwargs.get('parties', PartiesGroup())
        self.no_quote_entries = kwargs.get('no_quote_entries', RepeatingGroupDimensions(15, quote_entries))
        self.quotes = kwargs.get('quotes',LongTwoSidedQuote())

    def encode(self):
        encoded_header = self.sbe_header.encode()
        encoded_sending_time = self.sending_time.encode()
        encoded_cl_ord_id = self.cl_ord_id.encode()
        encoded_time_in_force = self.time_in_force.encode()
        encoded_exec_inst = self.exec_inst.encode()
        encoded_trading_capacity = self.trading_capacity.encode()
        encoded_mtp_group_id = self.mtp_group_id.encode()
        encoded_match_trade_prevention = self.match_trade_prevention.encode()
        encoded_cancel_group_id = self.cancel_group_id.encode()
        encoded_risk_group_id = self.risk_group_id.encode()
        encoded_no_party_ids =  self.no_party_ids.encode()
        encoded_parties = b''
        for party in self.parties:
                encoded_parties += party.encode()


        encoded_no_quote_entries =  self.no_quote_entries.encode()
        encoded_quotes = b''
        for quote in self.quotes:
                encoded_quotes += quote.encode()


        encoded_message = (
            encoded_header
            + encoded_sending_time
            + encoded_cl_ord_id
            + encoded_time_in_force
            + encoded_exec_inst
            + encoded_trading_capacity
            + encoded_mtp_group_id
            + encoded_match_trade_prevention
            + encoded_cancel_group_id
            + encoded_risk_group_id
            + encoded_no_party_ids
            + encoded_parties
            + encoded_no_quote_entries
            + encoded_quotes
        )

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


class ShortOneSideQuote:
    SIZE = 18

    def __init__(self, list_seq_no=None, options_security_id=None, side=None, quantity=None, price=None):
        self.list_seq_no = UINT8(list_seq_no)
        self.options_security_id = OptionsSecurityID(options_security_id)
        self.side = SideType(side)
        self.quantity = UINT32(quantity)
        self.price = ShortPriceType(price,0)

    def encode(self):
        encoded_list_seq_no = self.list_seq_no.encode()
        encoded_options_security_id = self.options_security_id.encode()
        encoded_side = self.side.encode()
        encoded_quantity = self.quantity.encode()
        encoded_price = self.price.encode()

        return encoded_list_seq_no + encoded_options_security_id + encoded_side + encoded_quantity + encoded_price

    def decode(self, buffer):
        offset = 0

        self.list_seq_no = UINT8(0)
        self.list_seq_no.decode(buffer[offset:])
        offset += UINT8.SIZE

        self.options_security_id = Char('')
        self.options_security_id.decode(buffer[offset:])
        offset += Char.SIZE

        self.side = Char('')
        self.side.decode(buffer[offset:])
        offset += Char.SIZE

        self.quantity = UINT32(0)
        self.quantity.decode(buffer[offset:])
        offset += UINT32.SIZE

        self.price = PriceType(0.0)
        self.price.decode(buffer[offset:])
        offset += PriceType.SIZE


class ShortOneSideBulkQuote:
    TEMPLATE_ID = 4
    num_groups = 2
    schema_id = 1
    version = 266
    BLOCK_LENGTH = 39

    def __init__(self, **kwargs):
        self.sbe_header = SBEHeader(self.BLOCK_LENGTH, self.TEMPLATE_ID, self.schema_id, self.version, self.num_groups)
        self.sending_time = kwargs.get('sending_time', UTCTimestampNanos(0))
        self.cl_ord_id = kwargs.get('cl_ord_id', Char(''))
        self.time_in_force = kwargs.get('time_in_force', TimeInForceType(0))
        self.exec_inst = kwargs.get('exec_inst', ExecInstType(0))
        self.trading_capacity = kwargs.get('trading_capacity', TradingCapacityType(0))
        self.mtp_group_id = kwargs.get('mtp_group_id', MtpGroupIDType(0))
        self.match_trade_prevention = kwargs.get('match_trade_prevention', MatchTradePreventionType(0))
        self.cancel_group_id = kwargs.get('cancel_group_id', UINT16(0))
        self.risk_group_id = kwargs.get('risk_group_id', UINT16(0))
        quote_entries = len(kwargs.get('quotes', []))
        party_entries = len(kwargs.get('parties', []))
        self.no_party_ids = kwargs.get('repeating_group_dimensions', RepeatingGroupDimensions(18, party_entries))
        self.parties = kwargs.get('parties', PartiesGroup())
        self.no_quote_entries = kwargs.get('no_quote_entries', RepeatingGroupDimensions(15, quote_entries))
        self.quotes = kwargs.get('quotes',ShortOneSideQuote())

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
        encoded_no_party_ids =  self.no_party_ids.encode()
        encoded_parties = b''
        for party in self.parties:
            encoded_parties += party.encode()

        encoded_no_quote_entries =  self.no_quote_entries.encode()
        encoded_quotes = b''
        for quote in self.quotes:
            encoded_quotes += quote.encode()

        encoded_message = encoded_header + encoded_sending_time + encoded_cl_ord_id + encoded_time_in_force + \
            encoded_exec_inst + encoded_trading_capacity + encoded_mtp_group_id + encoded_match_trade_prevention + \
            encoded_cancel_group_id + encoded_risk_group_id + encoded_no_party_ids + encoded_parties + encoded_no_quote_entries + encoded_quotes

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
            quote = ShortOneSideQuote(0, '', '', 0, 0.0)
            quote.decode(buffer[offset:])
            self.quotes.append(quote)
            offset += ShortOneSideQuote.SIZE


class LongOneSideQuote:
    SIZE = 20

    def __init__(self, list_seq_no=None, options_security_id=None, side=None, quantity=None, price=None):
        self.list_seq_no = UINT8(list_seq_no)
        self.options_security_id = OptionsSecurityID(options_security_id)
        self.side = SideType(side)
        self.quantity = UINT32(quantity)
        self.price = PriceType(price)

    def encode(self):
        encoded_list_seq_no = self.list_seq_no.encode()
        encoded_options_security_id = self.options_security_id.encode()
        encoded_side = self.side.encode()
        encoded_quantity = self.quantity.encode()
        encoded_price = self.price.encode()

        return encoded_list_seq_no + encoded_options_security_id + encoded_side + encoded_quantity + encoded_price

    def decode(self, buffer):
        offset = 0

        self.list_seq_no = UINT8(0)
        self.list_seq_no.decode(buffer[offset:])
        offset += UINT8.SIZE

        self.options_security_id = Char('')
        self.options_security_id.decode(buffer[offset:])
        offset += Char.SIZE

        self.side = Char('')
        self.side.decode(buffer[offset:])
        offset += Char.SIZE

        self.quantity = UINT32(0)
        self.quantity.decode(buffer[offset:])
        offset += UINT32.SIZE

        self.price = PriceType(0.0)
        self.price.decode(buffer[offset:])
        offset += PriceType.SIZE

class LongOneSideBulkQuote:
    TEMPLATE_ID = 5
    num_groups = 2
    schema_id = 1
    version = 266
    BLOCK_LENGTH = 39

    def __init__(self, **kwargs):
        self.sbe_header = SBEHeader(self.BLOCK_LENGTH, self.TEMPLATE_ID, self.schema_id, self.version, self.num_groups)
        self.sending_time = kwargs.get('sending_time', UTCTimestampNanos(0))
        self.cl_ord_id = kwargs.get('cl_ord_id', Char(''))
        self.time_in_force = kwargs.get('time_in_force', TimeInForceType(0))
        self.exec_inst = kwargs.get('exec_inst', ExecInstType(0))
        self.trading_capacity = kwargs.get('trading_capacity', TradingCapacityType(0))
        self.mtp_group_id = kwargs.get('mtp_group_id', MtpGroupIDType(0))
        self.match_trade_prevention = kwargs.get('match_trade_prevention', MatchTradePreventionType(0))
        self.cancel_group_id = kwargs.get('cancel_group_id', UINT16(0))
        self.risk_group_id = kwargs.get('risk_group_id', UINT16(0))
        quote_entries = len(kwargs.get('quotes', []))
        party_entries = len(kwargs.get('parties', []))
        self.no_party_ids = kwargs.get('repeating_group_dimensions', RepeatingGroupDimensions(18, party_entries))
        self.parties = kwargs.get('parties', PartiesGroup())
        self.no_quote_entries = kwargs.get('no_quote_entries', RepeatingGroupDimensions(15, quote_entries))
        self.quotes = kwargs.get('quotes',LongOneSideQuote())

    def encode(self):
        encoded_header = self.sbe_header.encode()
        encoded_sending_time = self.sending_time.encode()
        encoded_cl_ord_id = self.cl_ord_id.encode()
        encoded_time_in_force = self.time_in_force.encode()
        encoded_exec_inst = self.exec_inst.encode()
        encoded_trading_capacity = self.trading_capacity.encode()
        encoded_mtp_group_id = self.mtp_group_id.encode()
        encoded_match_trade_prevention = self.match_trade_prevention.encode()
        encoded_cancel_group_id = self.cancel_group_id.encode()
        encoded_risk_group_id = self.risk_group_id.encode()
        encoded_no_party_ids =  self.no_party_ids.encode()
        encoded_parties = b''
        for party in self.parties:
                encoded_parties += party.encode()


        encoded_no_quote_entries =  self.no_quote_entries.encode()
        encoded_quotes = b''
        for quote in self.quotes:
                encoded_quotes += quote.encode()


        encoded_message = (
            encoded_header
            + encoded_sending_time
            + encoded_cl_ord_id
            + encoded_time_in_force
            + encoded_exec_inst
            + encoded_trading_capacity
            + encoded_mtp_group_id
            + encoded_match_trade_prevention
            + encoded_cancel_group_id
            + encoded_risk_group_id
            + encoded_no_party_ids
            + encoded_parties
            + encoded_no_quote_entries
            + encoded_quotes
        )

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
            quote = LongOneSideQuote(0, '', '', 0, 0.0)
            quote.decode(buffer[offset:])
            self.quotes.append(quote)
            offset += LongOneSideQuote.SIZE
