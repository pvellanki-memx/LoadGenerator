import xml.etree.ElementTree as ET
import struct


def load_schema(schema_file):
    tree = ET.parse(schema_file)
    root = tree.getroot()
    messages = {}

    # Find the XML namespace
    namespace = root.tag.split('}')[0] + '}'

    for message_elem in root.findall(f'{namespace}message'):
        message_id = int(message_elem.get('id'))
        message_name = message_elem.get('name')
        fields = {}

        for field_elem in message_elem.findall(f'.//{namespace}field'):
            field_id = int(field_elem.get('id'))
            field_type = field_elem.get('type')
            fields[field_id] = field_type

        messages[message_name] = {'id': message_id, 'fields': fields}

    return messages




def encode_field(field_type, value):
    if field_type == 'char':
        return struct.pack('>c', value.encode('ascii'))
    elif field_type == 'int8':
        return struct.pack('>b', value)
    elif field_type == 'int16':
        return struct.pack('>h', value)
    elif field_type == 'int32':
        return struct.pack('>i', value)
    elif field_type == 'int64':
        return struct.pack('>q', value)
    elif field_type == 'uint8':
        return struct.pack('>B', value)
    elif field_type == 'uint16':
        return struct.pack('>H', value)
    elif field_type == 'uint32':
        return struct.pack('>I', value)
    elif field_type == 'uint64':
        return struct.pack('>Q', value)
    elif field_type == 'float':
        return struct.pack('>f', value)
    elif field_type == 'double':
        return struct.pack('>d', value)
    elif field_type == 'string':
        return value.encode('ascii')
    else:
        raise ValueError(f"Unknown field type: {field_type}")


def encode_message(schema, message_name, field_values):
    if message_name not in schema:
        raise ValueError(f"Message '{message_name}' not found in the schema.")

    message = schema[message_name]
    message_id = message['id']
    fields = message['fields']

    encoded_fields = []
    for field_id, field_type in fields.items():
        if field_id in field_values:
            value = field_values[field_id]
            encoded_field = encode_field(field_type, value)
            encoded_fields.append((field_id, encoded_field))

    encoded_message = struct.pack('>H', message_id)
    encoded_message += struct.pack('>H', len(encoded_fields))

    for field_id, encoded_field in encoded_fields:
        encoded_message += struct.pack('>H', field_id)
        encoded_message += struct.pack('>H', len(encoded_field))
        encoded_message += encoded_field

    return encoded_message


if __name__ == '__main__':
    schema_file = 'sbe-schema.xml'
    schema = load_schema(schema_file)

    message_name = 'NewOrderSingle'
    field_values = {
        52: 1623322435000000000,
        11: "CLORD12345",
        21035: "SECURITY123",
        54: "BUY",
        38: 100,
        40: "LIMIT",
        44: 99.99,
        59: "DAY",
        77: "OPEN",
        18: "ADD",
        1815: "MEDIUM",
        21020: 1,
        21021: 2,
        2362: 123,
        21001: "PREVENT",
        21000: 456,
        21005: 789,
        453: [
            {
                448: "PARTY1",
                447: "SRC1",
                452: 1
            },
            {
                448: "PARTY2",
                447: "SRC2",
                452: 2
            }
        ]
    }

    encoded_message = encode_message(schema, message_name, field_values)
    print(f"Encoded message: {encoded_message}")
