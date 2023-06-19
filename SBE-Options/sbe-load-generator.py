import struct

# SBE Header
sending_time = 12345678
cl_ord_id = "ORDER001"
options_security_id = "OPT123"
side = 1
order_qty = 100
order_type = 2
price = 99.99
time_in_force = 1
open_or_close = 2
exec_inst = 3
trading_capacity = 4
reprice_frequency = 5
reprice_behavior = 6
mtp_group_id = 7
match_trade_prevention = 8
cancel_group_id = 9
risk_group_id = 10

# Repeating Group: Parties
no_party_ids = 2
party_data = [
    {"party_id": "PARTY001", "party_id_source": "S", "party_role": 1},
    {"party_id": "PARTY002", "party_id_source": "T", "party_role": 2}
]

# SBE Message Construction
sbe_header = struct.pack('>q20s8sBIfBHBHBBH',
                         sending_time,
                         cl_ord_id.encode('ascii'),
                         options_security_id.encode('ascii'),
                         side,
                         order_qty,
                         order_type,
                         price,
                         time_in_force,
                         open_or_close,
                         exec_inst,
                         trading_capacity,
                         reprice_frequency,
                         reprice_behavior,
                         mtp_group_id,
                         match_trade_prevention,
                         cancel_group_id,
                         risk_group_id)

sbe_message = struct.pack('>H', no_party_ids)

for party in party_data:
    party_id = party['party_id'].encode('ascii')
    party_id_source = party['party_id_source'].encode('ascii')
    party_role = party['party_role']

    sbe_party = struct.pack('16s1sB', party_id, party_id_source, party_role)
    sbe_message += sbe_party

print(sbe_header + sbe_message)
