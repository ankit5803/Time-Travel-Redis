import asyncio

async def parse_resp(reader: asyncio.StreamReader):
    """Parses a RESP array from the raw socket stream."""
    try:
        line = await reader.readline()
        if not line:
            return None 
        
        line_str = line.decode('utf-8').strip()

        if not line_str.startswith('*'):
            print(f"[!] Unrecognized protocol format: {line_str}")
            return None
            
        num_args = int(line_str[1:])
        command_args = []

        for _ in range(num_args):
            length_line = await reader.readline()
            length_str = length_line.decode('utf-8').strip()
            
            if not length_str.startswith('$'):
                return None
                
            byte_length = int(length_str[1:])
            
            data = await reader.readexactly(byte_length)
            await reader.readexactly(2) 
            
            command_args.append(data.decode('utf-8'))
            
        return command_args
        
    except Exception as e:
        print(f"[!] Parsing error: {e}")
        return None

def encode_resp_simple_string(text: str) -> bytes:
    """Encodes a simple string response (e.g., +OK)"""
    return f"+{text}\r\n".encode('utf-8')

def encode_resp_error(text: str) -> bytes:
    """Encodes an error response (e.g., -ERR unknown command)"""
    return f"-ERR {text}\r\n".encode('utf-8')

def encode_resp_bulk_string(text: str) -> bytes:
    """Encodes a bulk string response (e.g., $5\r\nvalue\r\n)"""
    if text is None:
        return encode_resp_null()
    encoded_text = text.encode('utf-8')
    return f"${len(encoded_text)}\r\n".encode('utf-8') + encoded_text + b"\r\n"

def encode_resp_integer(num: int) -> bytes:
    """Encodes an integer response (e.g., :1\r\n)"""
    return f":{num}\r\n".encode('utf-8')

def encode_resp_null() -> bytes:
    """Encodes a null response when a key is not found"""
    return b"$-1\r\n"