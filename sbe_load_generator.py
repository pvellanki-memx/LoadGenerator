from sbe import Encoder, Decoder
from sbe.schemaparser import SchemaParser

# Load the SBE schema file
schema_file = 'path/to/SBE.xml'
parser = SchemaParser()
sbe_schema = parser.parse_file(schema_file)

# Create an encoder and decoder based on the SBE schema
encoder = Encoder(sbe_schema)
decoder = Decoder(sbe_schema)

# Example encoding and decoding
input_message = {
    'field1': 123,
    'field2': 'example',
    # ...
}

# Encode the message
encoded_message = encoder.encode(input_message)

# Decode the message
decoded_message = decoder.decode(encoded_message)

# Print the input and decoded messages
print("Input Message:")
print(input_message)
print("\nDecoded Message:")
print(decoded_message)
