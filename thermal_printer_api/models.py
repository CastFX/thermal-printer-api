"""Pydantic models for API requests and responses."""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class PrintTextRequest(BaseModel):
    """Request model for printing text."""

    text: str = Field(..., description="Text to print")
    align: Literal["left", "center", "right"] = Field(
        default="left", description="Text alignment"
    )
    bold: bool = Field(default=False, description="Bold text")
    underline: bool = Field(default=False, description="Underlined text")
    size: Literal["normal", "large"] = Field(default="normal", description="Text size")
    cut: bool = Field(default=False, description="Cut paper after printing")
    new_line: bool = Field(default=True, description="Add new line after text")


class PrintQRRequest(BaseModel):
    """Request model for printing QR codes."""

    data: str = Field(..., description="Data to encode in QR code")
    align: Literal["left", "center", "right"] = Field(
        default="left", description="QR code alignment"
    )
    cell_size: int = Field(default=3, ge=1, le=10, description="QR code cell size")
    correction: Literal["L", "M", "Q", "H"] = Field(
        default="M", description="Error correction level"
    )
    model: Literal[1, 2] = Field(default=2, description="QR code model")
    cut: bool = Field(default=False, description="Cut paper after printing")


class PrintImageRequest(BaseModel):
    """Request model for printing images."""

    image_data: str = Field(..., description="Image data as URL, base64 string, or file path")
    image_type: Literal["url", "base64", "file"] = Field(
        ..., description="Type of image data provided"
    )
    align: Literal["left", "center", "right"] = Field(
        default="left", description="Image alignment"
    )
    impl: Literal["bitImageRaster", "bitImageColumn", "graphics"] = Field(
        default="bitImageRaster", description="Image implementation method"
    )
    cut: bool = Field(default=False, description="Cut paper after printing")


class PrintBufferRequest(BaseModel):
    """Request model for printing raw buffer."""

    buffer: List[int] = Field(..., description="Raw buffer bytes as array of integers")


class PrinterConfigRequest(BaseModel):
    """Request model for updating printer configuration."""

    type: Literal["EPSON", "STAR"] = Field(default="EPSON", description="Printer type")
    interface: str = Field(default="/dev/usb/lp0", description="Printer interface")
    width: int = Field(
        default=60, ge=20, le=80, description="Print width in characters"
    )
    timeout: int = Field(
        default=5000, ge=1000, le=30000, description="Timeout in milliseconds"
    )


class PrintResponse(BaseModel):
    """Response model for print operations."""

    success: bool
    message: Optional[str] = None
    error: Optional[str] = None


class PrinterStatusResponse(BaseModel):
    """Response model for printer status."""

    connected: bool
    config: dict
    interface: str
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str
    service: str
    version: str
    timestamp: str


class ApiOverviewResponse(BaseModel):
    """Response model for API overview."""

    service: str
    version: str
    documentation: str
    health: str
    endpoints: dict
