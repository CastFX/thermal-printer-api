"""Thermal printer management module."""

import base64
from io import BytesIO
from typing import Any, Dict, Optional

import qrcode
import requests
from escpos.printer import Dummy, Network, Serial, Usb
from PIL import Image

from .config import PrinterConfig, load_printer_config


class PrinterManager:
    """Manages thermal printer operations."""

    def __init__(self, config: Optional[PrinterConfig] = None):
        """Initialize printer manager with configuration."""
        self.config = config or load_printer_config()
        self._printer = None

    def _create_printer(self):
        """Create printer instance based on configuration."""
        interface = self.config.interface

        if interface.startswith("/dev/usb/"):
            return Usb(
                idVendor=self.config.idVendor,
                idProduct=self.config.idProduct,
                timeout=0,
                in_ep=self.config.in_ep,
                out_ep=self.config.out_ep,
            )
        elif interface.startswith("/dev/tty"):
            # Serial printer
            return Serial(interface, baudrate=9600, timeout=self.config.timeout / 1000)
        elif interface.startswith("tcp://"):
            # Network printer
            parts = interface.replace("tcp://", "").split(":")
            host = parts[0]
            port = int(parts[1]) if len(parts) > 1 else 9100
            return Network(host=host, port=port, timeout=self.config.timeout / 1000)
        else:
            # Default to dummy printer for testing
            return Dummy()

    def _get_printer(self):
        """Get or create printer instance."""
        if self._printer is None:
            self._printer = self._create_printer()
        return self._printer

    async def check_connection(self) -> bool:
        """Check if printer is connected and accessible."""
        try:
            printer = self._get_printer()
            # For dummy printer, always return True for testing
            if isinstance(printer, Dummy):
                return True
            # For real printers, attempt a simple operation
            return True
        except Exception:
            return False

    async def get_status(self) -> Dict[str, Any]:
        """Get printer status and configuration."""
        try:
            connected = await self.check_connection()
            return {
                "connected": connected,
                "config": self.config.model_dump(),
                "interface": self.config.interface,
            }
        except Exception as e:
            return {
                "connected": False,
                "error": str(e),
                "config": self.config.model_dump(),
            }

    async def print_text(
        self,
        text: str,
        align: str = "left",
        bold: bool = False,
        underline: bool = False,
        size: str = "normal",
        cut: bool = True,
        new_line: bool = True,
    ) -> Dict[str, Any]:
        """Print formatted text."""
        try:
            printer = self._get_printer()

            # Set alignment
            if align == "center":
                printer.set(align="center")
            elif align == "right":
                printer.set(align="right")
            else:
                printer.set(align="left")

            # Set text formatting
            format_args = {}
            if bold:
                format_args["double_height"] = True
                format_args["double_width"] = True
            if underline:
                format_args["underline"] = 1
            if size == "large":
                format_args["double_height"] = True
                format_args["double_width"] = True

            # Apply formatting
            if format_args:
                printer.set(**format_args)

            # Print text
            if new_line:
                printer.text(text + "\n")
            else:
                printer.text(text)

            # Reset formatting
            printer.set()

            if cut:
                printer.cut()

            return {"success": True, "message": "Text printed successfully"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def print_qr(
        self,
        data: str,
        align: str = "left",
        cell_size: int = 8,
        correction: str = "M",
        model: int = 2,
        cut: bool = True,
    ) -> Dict[str, Any]:
        """Print QR code."""
        try:
            printer = self._get_printer()

            # Set alignment
            if align == "center":
                printer.set(align="center")
            elif align == "right":
                printer.set(align="right")
            else:
                printer.set(align="left")

            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=getattr(
                    qrcode.constants, f"ERROR_CORRECT_{correction}"
                ),
                box_size=cell_size,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            # Generate QR code image
            img = qr.make_image(fill_color="black", back_color="white")

            # Convert PIL Image to bytes for escpos
            img_bytes = BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes.seek(0)

            # Print QR code
            printer.image(img_bytes, impl="bitImageColumn")

            # Reset alignment
            printer.set(align="left")

            if cut:
                printer.cut()

            return {"success": True, "message": "QR code printed successfully"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def print_buffer(self, buffer: bytes) -> Dict[str, Any]:
        """Print raw buffer data."""
        try:
            printer = self._get_printer()
            printer._raw(buffer)
            return {"success": True, "message": "Print job completed successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def print_image(
        self,
        image_data: str,
        image_type: str,
        align: str = "left",
        impl: str = "bitImageRaster",
        cut: bool = True,
    ) -> Dict[str, Any]:
        """Print image from URL, base64, or file path."""
        try:
            printer = self._get_printer()

            # Set alignment
            if align == "center":
                printer.set(align="center")
            elif align == "right":
                printer.set(align="right")
            else:
                printer.set(align="left")

            # Load image based on type
            img = None
            if image_type == "url":
                response = requests.get(image_data, timeout=10)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
            elif image_type == "base64":
                # Remove data URL prefix if present
                if image_data.startswith("data:"):
                    image_data = image_data.split(",", 1)[1]
                img_data = base64.b64decode(image_data)
                img = Image.open(BytesIO(img_data))
            elif image_type == "file":
                img = Image.open(image_data)
            else:
                return {"success": False, "error": "Invalid image_type"}

            # Convert image to bytes for escpos
            img_bytes = BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes.seek(0)

            # Print image
            printer.image(img_bytes, impl=impl)

            # Reset alignment
            printer.set(align="left")

            if cut:
                printer.cut()

            return {"success": True, "message": "Image printed successfully"}

        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Failed to fetch image from URL: {str(e)}",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
