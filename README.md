````markdown
# TimeTravel-Redis ⏳

A custom, in-memory caching database built from scratch using raw TCP sockets, Python `asyncio`, and the REdis Serialization Protocol (RESP), complete with a modern web telemetry dashboard.

Unlike standard Redis instances that permanently destroy expired keys, this engine intercepts data during lazy-eviction and routes it to a circular **Tombstone Vault**, allowing developers to inspect or restore recently expired data.

## 🏗️ System Architecture

This project is built across three distinct architectural layers to separate the low-level memory engine from the web visualization layer:

1. **The TCP Engine (Backend):** A custom event-loop server handling non-blocking I/O multiplexing via `asyncio`. It bypasses HTTP entirely, reading and writing raw RESP byte-streams directly over port 6379.
2. **The REST Bridge (Middleware):** A FastAPI microservice that opens local TCP sockets to the database engine, acting as a translator between raw RESP responses and clean JSON payloads over HTTP (port 8000).
3. **The Telemetry UI (Frontend):** A Next.js (App Router) and Tailwind CSS v4 dashboard that aggressively polls the API bridge to visualize memory allocation, TTL decay, and vault archiving in real-time.

## ✨ Core Features

- **$O(1)$ Hash Map Store:** Instant read/write operations utilizing Python's internal dictionary structures.
- **Custom RESP Parser:** Manually decodes Redis arrays (`*`), bulk strings (`$`), and simple strings (`+`) straight from the TCP stream.
- **Lazy Eviction TTL:** Avoids blocking the main thread with expiration scans. Keys are validated against the system clock upon request and passively evicted if their Time-To-Live has expired.
- **Forensic Tombstone Vault:** Expired or overwritten keys are not deleted; they are archived into a bounded buffer, enabling a custom `RESTORE` command to retrieve lost session data.

## 🚀 Getting Started

**Prerequisites:** Python 3.10+ and Node.js 18+.

Clone the repository and open three separate terminal windows to run the stack concurrently:

**Terminal 1: Start the TCP Engine**

```bash
# Activate your virtual environment first
python backend/server.py
# Engine runs on 127.0.0.1:6379
```
````

**Terminal 2: Start the FastAPI Bridge**

```bash
# Ensure venv is active
uvicorn backend.api:app --reload
# Bridge runs on [http://127.0.0.1:8000](http://127.0.0.1:8000)

```

**Terminal 3: Start the Telemetry Dashboard**

```bash
cd frontend
npm install
npm run dev
# UI runs on http://localhost:3000

```

## 🧪 Running the Visual Simulation

Once all three services are running, open `http://localhost:3000` in your browser.

In a backend terminal, run the test script to inject data with strict 3-second TTLs:

```bash
python backend/test_client.py

```

Watch the Next.js dashboard seamlessly track the data lifecycle: from active memory injection, to TTL countdown, to automatic lazy-eviction into the Tombstone Vault.

## 💻 Supported Commands

The raw TCP server currently accepts the following commands via standard RESP protocol:

- `PING` - Connection health check.
- `SET key value [EX seconds]` - Store a key-value pair, optionally with a Time-To-Live.
- `GET key` - Retrieve a value (triggers lazy eviction if expired).
- `DEL key` - Manually remove a key and send it to the vault.
- `STATS` - Retrieve total key count, active TTLs, and vault size.
- `KEYS` - List all currently active keys in memory.
- `RESTORE` - Recover the most recently deleted/expired key from the vault.

```

```
