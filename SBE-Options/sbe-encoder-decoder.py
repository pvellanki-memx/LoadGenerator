import struct

# Define the SBEHeader structure
class SBEHeader:
    def __init__(self):
        self.blockLength = 0
        self.templateID = 0
        self.schemaID = 0
        self.version = 0
        self.numGroups = 0

    def encode(self):
        # Pack the SBEHeader fields into a binary string
        header_format = '<HHHHL'
        buffer = struct.pack(
            header_format,
            self.blockLength,
            self.templateID,
            self.schemaID,
            self.version,
            self.numGroups,
        )
        return buffer

    def decode(self, buffer):
        # Unpack the binary string into the SBEHeader fields
        header_format = '<HHHHL'
        (
            self.blockLength,
            self.templateID,
            self.schemaID,
            self.version,
            self.numGroups,
        ) = struct.unpack(header_format, buffer)

    def size(self):
        # Calculate the size of the SBEHeader structure
        return struct.calcsize('<HHHHL')

# Define the QuoteEntry structure
class QuoteEntry:
    def __init__(self):
        self.listSeqNo = 0
        self.optionsSecurityID = ""
        self.bidSize = 0
        self.bidPx = 0.0
        self.offerSize = 0
        self.offerPx = 0.0

    def encode(self):
        # Pack the QuoteEntry fields into a binary string
        quote_format = '<B8sH2H'
        buffer = struct.pack(
            quote_format,
            self.listSeqNo,
            self.optionsSecurityID.encode(),
            self.bidSize,
            self.bidPx,
            self.offerSize,
            self.offerPx,
        )
        return buffer

    def decode(self, buffer):
        # Unpack the binary string into the QuoteEntry fields
        quote_format = '<B8sH2H'
        (
            self.listSeqNo,
            self.optionsSecurityID,
            self.bidSize,
            self.bidPx,
            self.offerSize,
            self.offerPx,
        ) = struct.unpack(quote_format, buffer)

    def size(self):
        # Calculate the size of the QuoteEntry structure
        return struct.calcsize('<B8sH2H')

# Define the ShortTwoSideBulkQuote message
class ShortTwoSideBulkQuote:
    def __init__(self):
        self.header = SBEHeader()
        self.sendingTime = 0
        self.clOrdID = ""
        self.timeInForce = 0
        self.execInst = 0
        self.tradingCapacity = 0
        self.mtpGroupID = 0
        self.matchTradePrevention = 0
        self.cancelGroupID = 0
        self.riskGroupID = 0
        self.partyIDs = []
        self.quoteEntries = []

    def encode(self):
        # Encode the ShortTwoSideBulkQuote message
        buffer = self.header.encode()
        buffer += struct.pack('<Q', self.sendingTime)
        buffer += self.clOrdID.encode()
        buffer += struct.pack('B', self.timeInForce)
        buffer += struct.pack('H', self.execInst)
        buffer += struct.pack('B', self.tradingCapacity)
        buffer += struct.pack('H', self.mtpGroupID)
        buffer += struct.pack('B', self.matchTradePrevention)
        buffer += struct.pack('H', self.cancelGroupID)
        buffer += struct.pack('H', self.riskGroupID)
        buffer += struct.pack('H', len(self.partyIDs))
        for partyID in self.partyIDs:
            buffer += partyID.encode()
        buffer += struct.pack('H', len(self.quoteEntries))
        for quoteEntry in self.quoteEntries:
            buffer += quoteEntry.encode()
        return buffer

    def decode(self, buffer):
        # Decode the ShortTwoSideBulkQuote message
        offset = 0
        self.header.decode(buffer[offset:])
        offset += self.header.size()
        self.sendingTime = struct.unpack('<Q', buffer[offset : offset + 8])[0]
        offset += 8
        self.clOrdID = buffer[offset : offset + 20].decode()
        offset += 20
        self.timeInForce = struct.unpack('B', buffer[offset : offset + 1])[0]
        offset += 1
        self.execInst = struct.unpack('H', buffer[offset : offset + 2])[0]
        offset += 2
        self.tradingCapacity = struct.unpack('B', buffer[offset : offset + 1])[0]
        offset += 1
        self.mtpGroupID = struct.unpack('H', buffer[offset : offset + 2])[0]
        offset += 2
        self.matchTradePrevention = struct.unpack('B', buffer[offset : offset + 1])[0]
        offset += 1
        self.cancelGroupID = struct.unpack('H', buffer[offset : offset + 2])[0]
        offset += 2
        self.riskGroupID = struct.unpack('H', buffer[offset : offset + 2])[0]
        offset += 2
        partyIDs_count = struct.unpack('H', buffer[offset : offset + 2])[0]
        offset += 2
        self.partyIDs = []
        for _ in range(partyIDs_count):
            partyID = PartyID()
            partyID.decode(buffer[offset:])
            self.partyIDs.append(partyID)
            offset += partyID.size()
        quoteEntries_count = struct.unpack('H', buffer[offset : offset + 2])[0]
        offset += 2
        self.quoteEntries = []
        for _ in range(quoteEntries_count):
            quoteEntry = QuoteEntry()
            quoteEntry.decode(buffer[offset:])
            self.quoteEntries.append(quoteEntry)
            offset += quoteEntry.size()

    def size(self):
        # Calculate the size of the ShortTwoSideBulkQuote message
        size = self.header.size() + 8 + 20 + 1 + 2 + 1 + 2 + 1 + 2 + 2
        size += 2 + sum(partyID.size() for partyID in self.partyIDs)
        size += 2 + sum(quoteEntry.size() for quoteEntry in self.quoteEntries)
        return size

# Example usage
quoteEntry1 = QuoteEntry()
quoteEntry1.listSeqNo = 1
quoteEntry1.optionsSecurityID = "ABCXYZ"
quoteEntry1.bidSize = 100
quoteEntry1.bidPx = 10.5
quoteEntry1.offerSize = 200
quoteEntry1.offerPx = 11.0

quoteEntry2 = QuoteEntry()
quoteEntry2.listSeqNo = 2
quoteEntry2.optionsSecurityID = "DEF123"
quoteEntry2.bidSize = 150
quoteEntry2.bidPx = 9.75
quoteEntry2.offerSize = 175
quoteEntry2.offerPx = 10.0

quoteEntries = [quoteEntry1, quoteEntry2]

shortTwoSideBulkQuote = ShortTwoSideBulkQuote()
shortTwoSideBulkQuote.header.templateID = 2
shortTwoSideBulkQuote.sendingTime = 1625164800000000000
shortTwoSideBulkQuote.clOrdID = "ORDER001"
shortTwoSideBulkQuote.timeInForce = 1
shortTwoSideBulkQuote.execInst = 2
shortTwoSideBulkQuote.tradingCapacity = 1
shortTwoSideBulkQuote.mtpGroupID = 123
shortTwoSideBulkQuote.matchTradePrevention = 0
shortTwoSideBulkQuote.cancelGroupID = 456
shortTwoSideBulkQuote.riskGroupID = 789
shortTwoSideBulkQuote.partyIDs = []
shortTwoSideBulkQuote.quoteEntries = quoteEntries

encoded_buffer = shortTwoSideBulkQuote.encode()

decoded_shortTwoSideBulkQuote = ShortTwoSideBulkQuote()
decoded_shortTwoSideBulkQuote.decode(encoded_buffer)

# Print the decoded message
print("Template ID:", decoded_shortTwoSideBulkQuote.header.templateID)
print("Sending Time:", decoded_shortTwoSideBulkQuote.sendingTime)
print("ClOrdID:", decoded_shortTwoSideBulkQuote.clOrdID)
print("Time In Force:", decoded_shortTwoSideBulkQuote.timeInForce)
print("Exec Inst:", decoded_shortTwoSideBulkQuote.execInst)
print("Trading Capacity:", decoded_shortTwoSideBulkQuote.tradingCapacity)
print("Mtp Group ID:", decoded_shortTwoSideBulkQuote.mtpGroupID)
print("Match Trade Prevention:", decoded_shortTwoSideBulkQuote.matchTradePrevention)
print("Cancel Group ID:", decoded_shortTwoSideBulkQuote.cancelGroupID)
print("Risk Group ID:", decoded_shortTwoSideBulkQuote.riskGroupID)
print("Party IDs:")
for partyID in decoded_shortTwoSideBulkQuote.partyIDs:
    print("  - Party ID:", partyID.partyID)
print("Quote Entries:")
for quoteEntry in decoded_shortTwoSideBulkQuote.quoteEntries:
    print("  - List Seq No:", quoteEntry.listSeqNo)
    print("    Options Security ID:", quoteEntry.optionsSecurityID)
    print("    Bid Size:", quoteEntry.bidSize)
    print("    Bid Px:", quoteEntry.bidPx)
    print("    Offer Size:", quoteEntry.offerSize)
    print("    Offer Px:", quoteEntry.offerPx)
