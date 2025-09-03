#!/usr/bin/env python3
"""Entry point for thermal printer API server."""

if __name__ == "__main__":
    from thermal_printer_api.main import start_server

    start_server()
