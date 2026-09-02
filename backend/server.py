import asyncio
import json
from parser import (
    parse_resp, encode_resp_simple_string, encode_resp_error, 
    encode_resp_bulk_string, encode_resp_integer, encode_resp_null
)
from store import DataStore

db = DataStore()

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    addr = writer.get_extra_info('peername')
    print(f"[+] Connection accepted from {addr}")

    try:
        while True:
            command_parts = await parse_resp(reader)
            if not command_parts:
                break
                
            cmd = command_parts[0].upper()
            
            if cmd == "PING":
                writer.write(encode_resp_simple_string("PONG"))
                
            elif cmd == "ECHO" and len(command_parts) > 1:
                writer.write(encode_resp_simple_string(command_parts[1]))
                
            elif cmd == "SET" and len(command_parts) >= 3:
                key, value = command_parts[1], command_parts[2]
                ex_seconds = None
                
                if len(command_parts) == 5 and command_parts[3].upper() == "EX":
                    try:
                        ex_seconds = int(command_parts[4])
                    except ValueError:
                        writer.write(encode_resp_error("invalid expire time"))
                        await writer.drain()
                        continue

                db.set(key, value, ex_seconds)
                writer.write(encode_resp_simple_string("OK"))
                
            elif cmd == "GET" and len(command_parts) == 2:
                key = command_parts[1]
                val = db.get(key)
                if val is not None:
                    writer.write(encode_resp_bulk_string(val))
                else:
                    writer.write(encode_resp_null())
                    
            elif cmd == "DEL" and len(command_parts) == 2:
                key = command_parts[1]
                result = db.delete(key)
                writer.write(encode_resp_integer(result))
                
            elif cmd == "EXISTS" and len(command_parts) == 2:
                key = command_parts[1]
                result = db.exists(key)
                writer.write(encode_resp_integer(result))

            elif cmd == "RESTORE" and len(command_parts) == 1:
                restored_key = db.restore_latest()
                if restored_key:
                    writer.write(encode_resp_simple_string(f"Restored {restored_key}"))
                else:
                    writer.write(encode_resp_error("Vault is empty"))
                    
            elif cmd == "STATS" and len(command_parts) == 1:
                stats_data = json.dumps(db.stats())
                writer.write(encode_resp_bulk_string(stats_data))
                
            elif cmd == "KEYS" and len(command_parts) == 1:
                keys_list = json.dumps(db.keys())
                writer.write(encode_resp_bulk_string(keys_list))
                    
            else:
                writer.write(encode_resp_error(f"unknown command '{cmd}'"))
                
            await writer.drain()

    except ConnectionResetError:
        pass
    finally:
        print(f"[-] Connection closed from {addr}")
        writer.close()
        await writer.wait_closed()

async def main():
    host = '127.0.0.1'
    port = 6379
    server = await asyncio.start_server(handle_client, host, port)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f"[*] TimeTravel-Redis server running on {addrs}...")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[*] Server shutting down.")