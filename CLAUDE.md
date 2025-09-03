# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Thermal Printer API (v2) is a standalone REST API server for managing thermal printers locally.

## Development Commands

### Python Server Operations
```bash
# Development (with auto-reload)
uv run python dev.py

# Production
uv run python main.py

# Alternative using scripts
uv run thermal-printer-api-dev  # Development
uv run thermal-printer-api      # Production

# Install dependencies
uv sync
```

### Legacy Node.js Server Operations (deprecated)
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

**Main Server (`thermal_printer_api/main.py`)**
- FastAPI-based HTTP server on port 3000 (configurable)
- OpenAPI/Swagger documentation at `/docs`
- Health check endpoint at `/health`
- Graceful shutdown handling with Uvicorn

**Printer Management (`thermal_printer_api/printer.py`)**
- Core printer operations using `python-escpos`
- Configuration management via Pydantic models
- Support for text, QR codes, and raw buffer printing
- Printer status monitoring and connection testing

**API Routes (`thermal_printer_api/routes.py`)**
- REST endpoints for all printer operations
- Request validation using Pydantic models
- Automatic OpenAPI schema generation
- Type-safe error handling

**Configuration (`thermal_printer_api/config.py`)**
- Pydantic-based configuration management
- Environment variable support
- JSON file persistence for printer settings

### Legacy Components (Node.js - deprecated)

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

**Printer Configuration (`printer-config.json`)**
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
- `LOG_LEVEL` - Uvicorn logging level (default: info)

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

## Key Features in Python v2

- **Modern Stack**: FastAPI with automatic OpenAPI documentation generation
- **Type Safety**: Pydantic models for request/response validation
- **Async Support**: Full async/await support for better performance
- **Environment Config**: Pydantic-settings for configuration management
- **Cross-platform**: Python-escpos library supports multiple printer interfaces
- **Development Tools**: UV for fast dependency management
- **Testing Ready**: Built-in support for pytest and async testing

## Key Differences from Node.js v1

- **Language**: Migrated from Node.js to Python 3.9+
- **Framework**: Changed from Fastify to FastAPI
- **Printer Library**: Changed from `node-thermal-printer` to `python-escpos`
- **Package Manager**: Using UV instead of npm
- **Configuration**: Pydantic models instead of plain JSON validation
- **Type System**: Full type hints and validation throughout
- **Maintained Features**: All original REST API endpoints and functionality

## Supported Hardware

- Epson ESC/POS thermal printers
- Star thermal printers
- USB interface (`/dev/usb/lp0`)
- Serial interfaces (`/dev/ttyUSB0`, etc.)
- Network interfaces (`tcp://ip:port`)

## Development Notes

### Python Version
- Uses FastAPI for high-performance HTTP server with automatic documentation
- OpenAPI/Swagger UI provides interactive API testing at `/docs`
- All printer operations return consistent JSON responses with Pydantic models
- Configuration changes are applied immediately (no server restart required)
- No database or persistent storage required
- Full async support for better performance
- Type hints throughout for better IDE support and error catching

### Legacy Node.js Version (deprecated)
- Uses Fastify for high-performance HTTP server
- Swagger UI provides interactive API testing
- All printer operations return consistent JSON responses
- Configuration changes require server restart
- No database or persistent storage required