import struct

class SBEHeader:
    def __init__(self):
        self.blockLength = 0
        self.templateID = 0
        self.schemaID = 0
        self.version = 0
        self.numGroups = 0

    def encode(self):
        buffer = struct.pack('<HBBHH', self.blockLength, self.templateID, self.schemaID, self.version, self.numGroups)
        return buffer

    def decode(self, buffer):
        self.blockLength, self.templateID, self.schemaID, self.version, self.numGroups = struct.unpack('<HBBHH', buffer)

    def size(self):
        return struct.calcsize('<HBBHH')

class NewOrderSingle:
    def __init__(self):
        self.header = SBEHeader()
        self.sendingTime = 0
        self.clOrdID = ""
        self.optionsSecurityID = ""
        self.side = 0
        self.orderQty = 0
        self.ordType = 0
        self.price = 0.0
        self.timeInForce = 0
        self.openOrClose = 0
        self.execInst = 0
        self.tradingCapacity = 0
        self.repriceFrequency = 0
        self.repriceBehavior = 0
        self.mtpGroupID = 0
        self.matchTradePrevention = 0
        self.cancelGroupID = 0
        self.riskGroupID = 0
        self.partyIDs = []

    def encode(self):
        buffer = self.header.encode()
        buffer += struct.pack('<Q', self.sendingTime)
        buffer += self.clOrdID.encode()
        buffer += self.optionsSecurityID.encode()
        buffer += struct.pack('B', self.side)
        buffer += struct.pack('<I', self.orderQty)
        buffer += struct.pack('B', self.ordType)
        buffer += struct.pack('<d', self.price)
        buffer += struct.pack('B', self.timeInForce)
        buffer += struct.pack('B', self.openOrClose)
        buffer += struct.pack('H', self.execInst)
        buffer += struct.pack('B', self.tradingCapacity)
        buffer += struct.pack('B', self.repriceFrequency)
        buffer += struct.pack('B', self.repriceBehavior)
        buffer += struct.pack('H', self.mtpGroupID)
        buffer += struct.pack('B', self.matchTradePrevention)
        buffer += struct.pack('H', self.cancelGroupID)
        buffer += struct.pack('H', self.riskGroupID)
        buffer += struct.pack('H', len(self.partyIDs))
        for partyID in self.partyIDs:
            buffer += partyID.encode()
        return buffer

    def decode(self, buffer):
        offset = 0
        self.header.decode(buffer[offset:])
        offset += self.header.size()
        self.sendingTime = struct.unpack('<Q', buffer[offset : offset + 8])[0]
        offset += 8
        self.clOrdID = buffer[offset : offset + 20].decode()
        offset += 20
        self.optionsSecurityID = buffer[offset : offset + 8].decode()
        offset += 8
        self.side = struct.unpack('B', buffer[offset : offset + 1])[0]
        offset += 1
        self.orderQty = struct.unpack('<I', buffer[offset : offset + 4])[0]
        offset += 4
        self.ordType = struct.unpack('B', buffer[offset : offset + 1])[0]
        offset += 1
        self.price = struct.unpack('<d', buffer[offset : offset + 8])[0]
        offset += 8
        self.timeInForce = struct.unpack('B', buffer[offset : offset + 1])[0]
        offset += 1
        self.openOrClose = struct.unpack('B', buffer[offset : offset + 1])[0]
        offset += 1
        self.execInst = struct.unpack('H', buffer[offset : offset + 2])[0]
        offset += 2
        self.tradingCapacity = struct.unpack('B', buffer[offset : offset + 1])[0]
        offset += 1
        self.repriceFrequency = struct.unpack('B', buffer[offset : offset + 1])[0]
        offset += 1
        self.repriceBehavior = struct.unpack('B', buffer[offset : offset + 1])[0]
        offset += 1
        self.mtpGroupID = struct.unpack('H', buffer[offset : offset + 2])[0]
        offset += 2
        self.matchTradePrevention = struct.unpack('B', buffer[offset : offset + 1])[0]
        offset += 1
        self.cancelGroupID = struct.unpack('H', buffer[offset : offset + 2])[0]
        offset += 2
        self.riskGroupID = struct.unpack('H', buffer[offset : offset + 2])[0]
        offset += 2
        numPartyIDs = struct.unpack('H', buffer[offset : offset + 2])[0]
        offset += 2
        self.partyIDs = []
        for _ in range(numPartyIDs):
            partyID = PartyID()
            partyID.decode(buffer[offset:])
            self.partyIDs.append(partyID)
            offset += partyID.size()

    def size(self):
        size = self.header.size() + 8 + len(self.clOrdID) + len(self.optionsSecurityID) + 31
        size += len(self.partyIDs) * PartyID().size()
        return size

class QuoteEntry:
    def __init__(self):
        self.listSeqNo = 0
        self.optionsSecurityID = ""
        self.bidSize = 0
        self.bidPx = 0.0
        self.offerSize = 0
        self.offerPx = 0.0

    def encode(self):
        buffer = struct.pack('B', self.listSeqNo)
        buffer += self.optionsSecurityID.encode()
        buffer += struct.pack('<H', self.bidSize)
        buffer += struct.pack('<H', self.bidPx)
        buffer += struct.pack('<H', self.offerSize)
        buffer += struct.pack('<H', self.offerPx)
        return buffer

    def decode(self, buffer):
        self.listSeqNo = struct.unpack('B', buffer[0:1])[0]
        self.optionsSecurityID = buffer[1:9].decode()
        self.bidSize = struct.unpack('<H', buffer[9:11])[0]
        self.bidPx = struct.unpack('<H', buffer[11:13])[0]
        self.offerSize = struct.unpack('<H', buffer[13:15])[0]
        self.offerPx = struct.unpack('<H', buffer[15:17])[0]

    def size(self):
        return 17

class PartyID:
    def __init__(self):
        self.partyID = ""
        self.partyIDSource = ""

    def encode(self):
        buffer = self.partyID.encode()
        buffer += self.partyIDSource.encode()
        return buffer

    def decode(self, buffer):
        self.partyID = buffer[0:4].decode()
        self.partyIDSource = buffer[4:8].decode()

    def size(self):
        return 8


# User input for template ID
templateID = int(input("Enter the Template ID for SBE Header: "))

# Create an instance of SBEHeader based on user input
header = SBEHeader()
header.templateID = templateID

# Create an instance of NewOrderSingle
newOrderSingle = NewOrderSingle()

# Assign values to NewOrderSingle fields
newOrderSingle.header = header
newOrderSingle.sendingTime = 1624567890000000000
newOrderSingle.clOrdID = "ABC123"
newOrderSingle.optionsSecurityID = "XYZ"
newOrderSingle.side = 1
newOrderSingle.orderQty = 100
newOrderSingle.ordType = 2
newOrderSingle.price = 10.5
newOrderSingle.timeInForce = 1
newOrderSingle.openOrClose = 0
newOrderSingle.execInst = 2
newOrderSingle.tradingCapacity = 1
newOrderSingle.repriceFrequency = 0
newOrderSingle.repriceBehavior = 0
newOrderSingle.mtpGroupID = 0
newOrderSingle.matchTradePrevention = 0
newOrderSingle.cancelGroupID = 0
newOrderSingle.riskGroupID = 0

# Create an instance of QuoteEntry
quoteEntry = QuoteEntry()
quoteEntry.listSeqNo = 1
quoteEntry.optionsSecurityID = "XYZ"
quoteEntry.bidSize = 10
quoteEntry.bidPx = 10.25
quoteEntry.offerSize = 5
quoteEntry.offerPx = 10.5

# Add QuoteEntry to NewOrderSingle
newOrderSingle.quoteEntries.append(quoteEntry)

# Encode NewOrderSingle
encodedMessage = newOrderSingle.encode()

# Decode NewOrderSingle
decodedMessage = NewOrderSingle()
decodedMessage.decode(encodedMessage)

# Print encoded and decoded messages
print("Encoded Message:", encodedMessage)
print("Decoded Message:")
print("Header Template ID:", decodedMessage.header.templateID)
print("Sending Time:", decodedMessage.sendingTime)
print("ClOrdID:", decodedMessage.clOrdID)
print("OptionsSecurityID:", decodedMessage.optionsSecurityID)
print("Side:", decodedMessage.side)
print("OrderQty:", decodedMessage.orderQty)
print("OrdType:", decodedMessage.ordType)
print("Price:", decodedMessage.price)
print("TimeInForce:", decodedMessage.timeInForce)
print("OpenOrClose:", decodedMessage.openOrClose)
print("ExecInst:", decodedMessage.execInst)
print("TradingCapacity:", decodedMessage.tradingCapacity)
print("RepriceFrequency:", decodedMessage.repriceFrequency)
print("RepriceBehavior:", decodedMessage.repriceBehavior)
print("MtpGroupID:", decodedMessage.mtpGroupID)
print("MatchTradePrevention:", decodedMessage.matchTradePrevention)
print("CancelGroupID:", decodedMessage.cancelGroupID)
print("RiskGroupID:", decodedMessage.riskGroupID)
print("QuoteEntry ListSeqNo:", decodedMessage.quoteEntries[0].listSeqNo)
print("QuoteEntry OptionsSecurityID:", decodedMessage.quoteEntries[0].optionsSecurityID)
print("QuoteEntry BidSize:", decodedMessage.quoteEntries[0].bidSize)
print("QuoteEntry BidPx:", decodedMessage.quoteEntries[0].bidPx)
print("QuoteEntry OfferSize:", decodedMessage.quoteEntries[0].offerSize)
print("QuoteEntry OfferPx:", decodedMessage.quoteEntries[0].offerPx)
