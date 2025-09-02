# Thermal Printer API

A standalone REST API server for managing thermal printers locally.

## Features

- 🖨️ **Direct Printer Control** - Send text, QR codes, and raw buffers to thermal printers
- 📚 **REST API** - Clean HTTP endpoints with JSON responses
- 📖 **Auto-Documentation** - Built-in Swagger UI at `/docs`
- ⚙️ **Configurable** - JSON-based printer configuration
- 🔧 **Local Deployment** - No external service dependencies
- 📊 **Status Monitoring** - Check printer connectivity and configuration

## Quick Start

### Installation

```bash
cd v2/server
npm install
```

### Configuration

1. Copy the environment template:
```bash
cp ../.env.example ../.env
```

2. Edit `printer-config.json` to match your printer:
```json
{
  "type": "EPSON",
  "interface": "/dev/usb/lp0",
  "width": 60,
  "timeout": 5000
}
```

### Running

```bash
# Development with auto-reload
npm run dev

# Production
npm start
```

The server starts on `http://localhost:3000` by default.

## API Endpoints

### Core Endpoints

- `GET /` - API overview and available endpoints
- `GET /health` - Service health check
- `GET /docs` - Interactive API documentation

### Printer Operations

- `POST /api/print/text` - Print formatted text
- `POST /api/print/qr` - Print QR codes
- `POST /api/print/buffer` - Print raw buffer data
- `GET /api/printer/status` - Get printer status
- `PUT /api/printer/config` - Update printer configuration
- `POST /api/printer/test` - Print test page

## Usage Examples

### Print Text
```bash
curl -X POST http://localhost:3000/api/print/text \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello World!",
    "align": "center",
    "bold": true,
    "cut": true
  }'
```

### Print QR Code
```bash
curl -X POST http://localhost:3000/api/print/qr \
  -H "Content-Type: application/json" \
  -d '{
    "data": "https://example.com",
    "align": "center",
    "cellSize": 5,
    "cut": true
  }'
```

### Check Printer Status
```bash
curl http://localhost:3000/api/printer/status
```

### Test Printer
```bash
curl -X POST http://localhost:3000/api/printer/test
```

## Configuration

### Printer Configuration (`printer-config.json`)

```json
{
  "type": "EPSON",          // Printer type: EPSON or STAR
  "interface": "/dev/usb/lp0", // Printer interface path
  "width": 60,              // Paper width in characters
  "timeout": 5000           // Connection timeout in ms
}
```

### Environment Variables

- `PORT` - Server port (default: 3000)
- `HOST` - Server host (default: 0.0.0.0)
- `LOG_LEVEL` - Logging level (default: info)

## Supported Printers

This API uses the `node-thermal-printer` library and supports:

- **Epson** thermal printers (ESC/POS protocol)
- **Star** thermal printers
- Most ESC/POS compatible printers

### Common Interfaces

- USB: `/dev/usb/lp0`, `/dev/usb/lp1`
- Serial: `/dev/ttyUSB0`, `/dev/ttyAMA0`
- Network: `tcp://192.168.1.100:9100`

## Development

### Project Structure

```
v2/
├── server/
│   ├── index.js           # Main server file
│   ├── package.json       # Dependencies
│   ├── printer-config.json # Printer configuration
│   ├── routes/
│   │   └── printer.js     # API route handlers
│   └── scripts/
│       └── printer.js     # Printer management logic
├── .env.example          # Environment template
└── README.md            # This file
```

### API Documentation

Visit `http://localhost:3000/docs` when the server is running to see the interactive Swagger UI with all available endpoints, request/response schemas, and testing interface.

## Troubleshooting

### Printer Not Connected

1. Check USB connection
2. Verify interface path in `printer-config.json`
3. Check system permissions: `ls -la /dev/usb/lp0`
4. Test with: `curl -X POST http://localhost:3000/api/printer/test`

### Permission Issues

```bash
# Add user to lp group for printer access
sudo usermod -a -G lp $USER

# Or set permissions directly
sudo chmod 666 /dev/usb/lp0
```
