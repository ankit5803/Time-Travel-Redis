import socket

def send_command(command_parts):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 6379))
    resp = f"*{len(command_parts)}\r\n"
    for part in command_parts:
        str_part = str(part)
        resp += f"${len(str_part)}\r\n{str_part}\r\n"
        
    s.sendall(resp.encode('utf-8'))
    response = s.recv(1024)
    print(f"Sent: {command_parts} -> Server replied: {response!r}")
    s.close()

# Populate the database with test data
send_command(["SET", "user:1", "ankit"])
send_command(["SET", "project:1", "timetravel-redis"])
send_command(["SET", "session:abc", "active", "EX", 300])

# Verify the custom commands work over TCP
send_command(["KEYS"])
send_command(["STATS"])