Here is the complete, fully styled `README.md` text. You can just copy everything inside the code block below, open your `README.md` file on GitHub (or locally in your text editor), paste it over what's currently there, and save it!

````markdown
<div align="center">
  
  # ⏳ TimeTravel-Redis
  
  **A custom, in-memory caching database built from scratch using raw TCP sockets, Python `asyncio`, and the REdis Serialization Protocol (RESP).**

![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Next JS](https://img.shields.io/badge/Next-black?style=for-the-badge&logo=next.js&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)

</div>

<br />

> **The Forensic Difference:** Unlike standard Redis instances that permanently destroy expired keys, this engine intercepts data during lazy-eviction and routes it to a circular **Tombstone Vault**. This allows developers to inspect, audit, or restore recently expired session data in real-time.

---

## 🏗️ System Architecture

This project spans three distinct architectural layers, deliberately separating the low-level memory engine from the web visualization layer.

- **⚙️ Layer 1: The TCP Engine (Backend)**
  A custom event-loop server handling non-blocking I/O multiplexing via `asyncio`. It bypasses HTTP entirely, reading and writing raw RESP byte-streams directly over port `6379`.
- **🌉 Layer 2: The REST Bridge (Middleware)**
  A FastAPI microservice that opens local TCP sockets to the database engine, acting as a translator between raw RESP responses and clean JSON payloads over HTTP on port `8000`.
- **📊 Layer 3: The Telemetry UI (Frontend)**
  A Next.js and Tailwind CSS dashboard that aggressively polls the API bridge to visualize memory allocation, TTL decay, and vault archiving in real-time on port `3000`.

---

## ✨ Core Features

- **$O(1)$ Hash Map Store:** Instant read/write operations utilizing Python's internal dictionary structures.
- **Custom RESP Parser:** Manually decodes Redis arrays (`*`), bulk strings (`$`), and simple strings (`+`) straight from the raw TCP stream.
- **Lazy Eviction TTL:** Avoids blocking the main thread with expiration scans. Keys are validated against the system clock upon request and passively evicted if their Time-To-Live has expired.
- **Tombstone Vault:** Expired or overwritten keys are not deleted; they are dynamically archived into a bounded buffer, enabling a custom `RESTORE` command to retrieve lost data.

---

## 🚀 Getting Started

**Prerequisites:** Python 3.10+ and Node.js 18+.

Clone the repository and open three separate terminal windows to run the stack concurrently:

### 1. Start the TCP Engine

```bash
# Activate your virtual environment first
python backend/server.py
# Engine runs on 127.0.0.1:6379
```
````

### 2. Start the FastAPI Bridge

```bash
# Ensure venv is active
uvicorn backend.api:app --reload
# Bridge runs on [http://127.0.0.1:8000](http://127.0.0.1:8000)

```

### 3. Start the Telemetry Dashboard

```bash
cd frontend
npm install
npm run dev
# UI runs on http://localhost:3000

```

---

## 🧪 Running the Visual Simulation

Once all three services are running, open `http://localhost:3000` in your browser.

In a backend terminal, run the test script to inject data with strict 3-second TTLs:

```bash
python backend/test_client.py

```

_Watch the Next.js dashboard seamlessly track the data lifecycle: from active memory injection, to TTL countdown, to automatic lazy-eviction into the Tombstone Vault._

---

## 💻 Supported Commands

The raw TCP server currently accepts the following commands via standard RESP protocol:

| Command                  | Description                                                   |
| ------------------------ | ------------------------------------------------------------- |
| `PING`                   | Connection health check.                                      |
| `SET key value [EX sec]` | Store a key-value pair, optionally with a Time-To-Live.       |
| `GET key`                | Retrieve a value (triggers lazy eviction if expired).         |
| `DEL key`                | Manually remove a key and send it to the vault.               |
| `STATS`                  | Retrieve total key count, active TTLs, and vault size.        |
| `KEYS`                   | List all currently active keys in memory.                     |
| `RESTORE`                | Recover the most recently deleted/expired key from the vault. |

```

```
