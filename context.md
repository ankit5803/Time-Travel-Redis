# TimeTravel-Redis: Project Context & Architecture

**Developer:** Ankit Barik  
**Project Status:** Active Development (Resumed post-Sentinel deployment)  
**Primary Objective:** Build a custom, asynchronous in-memory data store from scratch using raw TCP sockets and the RESP protocol, featuring a unique "Time-Travel" recovery system and a full-stack management GUI.

## 1. Core Motivation & Differentiator

Standard in-memory caches silently drop keys upon expiration or deletion, complicating production debugging during cache stampedes. TimeTravel-Redis introduces a **Tombstone History Buffer**, a circular memory queue that temporarily retains expired/deleted keys. This allows developers to conduct forensic debugging and instantly restore critical dropped state via a custom web interface.

## 2. Technology Stack

- **Core Database Engine:** Python 3.10+ (using `asyncio` and raw socket programming)
- **Protocol:** Custom RESP (REdis Serialization Protocol) Parser
- **API Telemetry Bridge:** FastAPI
- **Frontend Dashboard:** Next.js with React and Tailwind CSS
- **Testing:** `pytest` and standard `redis-cli`

## 3. Architecture Breakdown

### A. The TCP Server & RESP Engine (Layer 1)

- An event-driven TCP server listening on port 6379 (or custom port).
- A custom binary parser that decodes incoming RESP byte streams into execution commands (`GET`, `SET`, `DEL`, `PING`) and encodes system responses.
- A thread-safe, in-memory storage dictionary handling concurrent read/write operations.

### B. The Time-Travel Tombstone Buffer (Layer 2)

- A secondary asynchronous process managing Time-To-Live (TTL) tracking.
- Upon key expiration, data is intercepted and pushed into a fixed-size circular buffer containing the key name, payload, and expiration timestamp.
- A custom RESP command (`RESTORE_TOMBSTONE`) integrated to pull keys from the buffer back into live memory.

### C. The API Bridge & Telemetry (Layer 3)

- A lightweight FastAPI sidecar service running concurrently with the TCP engine.
- Maintains a persistent connection to the raw socket server to query active keys, memory allocation, and tombstone history.
- Exposes HTTP/REST endpoints for the frontend interface.

### D. The Full-Stack Management GUI (Layer 4)

- A Next.js front-end serving as the control plane for the database.
- **Key Explorer:** Visual grid to search, filter, and manually purge live keys.
- **Time-Travel Vault:** Dedicated interface to view the tombstone buffer and single-click resurrect expired keys.
- **Web Console:** A built-in terminal for raw command execution directly in the browser.

## 4. Phased Development Roadmap

- **Phase 1:** Asynchronous TCP server setup and custom RESP protocol parser implementation.
- **Phase 2:** Core in-memory CRUD operations and the TTL-driven Tombstone History Buffer.
- **Phase 3:** FastAPI telemetry bridge development for real-time state extraction.
- **Phase 4:** Next.js custom dashboard construction and end-to-end integration testing.
