# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Thermal Printer API (v2) is a standalone REST API server for managing thermal printers locally.

## Development Commands

### Server Operations
```bash
# Development (with auto-reload)
cd server && npm run dev

# Production
cd server && npm start

# Install dependencies
cd server && npm install
```

### Testing
```bash
# Test printer connection
curl -X POST http://localhost:3000/api/printer/test

# Check printer status
curl http://localhost:3000/api/printer/status

# Print test text
curl -X POST http://localhost:3000/api/print/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World!", "cut": true}'
```

## Architecture

### Core Components

**Main Server (`server/index.js`)**
- Fastify-based HTTP server on port 3000 (configurable)
- Swagger/OpenAPI documentation at `/docs`
- Health check endpoint at `/health`
- Graceful shutdown handling

**Printer Management (`server/scripts/printer.js`)**
- Core printer operations using `node-thermal-printer`
- Configuration management via JSON files
- Support for text, QR codes, and raw buffer printing
- Printer status monitoring

**API Routes (`server/routes/printer.js`)**
- REST endpoints for all printer operations
- Request validation and error handling
- Swagger schema definitions for documentation

### Configuration System

**Printer Configuration (`server/printer-config.json`)**
```json
{
  "type": "EPSON",
  "interface": "/dev/usb/lp0",
  "width": 60,
  "timeout": 5000
}
```

**Environment Variables**
- `PORT` - Server port (default: 3000)
- `HOST` - Server host (default: 0.0.0.0)
- `LOG_LEVEL` - Fastify logging level

## API Endpoints

### Print Operations
- `POST /api/print/text` - Print formatted text with alignment, styling
- `POST /api/print/qr` - Print QR codes with customizable size/correction
- `POST /api/print/buffer` - Print raw byte arrays

### Management
- `GET /api/printer/status` - Check connection and configuration
- `PUT /api/printer/config` - Update printer settings
- `POST /api/printer/test` - Print test page

### System
- `GET /health` - Service health check
- `GET /docs` - Interactive API documentation
- `GET /` - API overview

## Key Differences from v1

- **Removed**: Pusher WebSocket integration
- **Removed**: Wi-Fi configuration interface
- **Removed**: Bash scripts and system integration
- **Added**: REST API with Swagger documentation
- **Added**: JSON-based configuration
- **Simplified**: Pure Node.js application, no external services

## Supported Hardware

- Epson ESC/POS thermal printers
- Star thermal printers
- USB interface (`/dev/usb/lp0`)
- Serial interfaces (`/dev/ttyUSB0`, etc.)
- Network interfaces (`tcp://ip:port`)

## Development Notes

- Uses Fastify for high-performance HTTP server
- Swagger UI provides interactive API testing
- All printer operations return consistent JSON responses
- Configuration changes require server restart
- No database or persistent storage required