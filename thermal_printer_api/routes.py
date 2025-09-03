"""API routes for thermal printer operations."""

from datetime import datetime

from fastapi import APIRouter, HTTPException, status

from .config import PrinterConfig, save_printer_config
from .models import (
    ApiOverviewResponse,
    HealthResponse,
    PrintBufferRequest,
    PrinterConfigRequest,
    PrinterStatusResponse,
    PrintQRRequest,
    PrintResponse,
    PrintTextRequest,
)
from .printer import PrinterManager

router = APIRouter()
printer_manager = PrinterManager()


@router.post(
    "/print/text",
    response_model=PrintResponse,
    summary="Print text",
    description="Print formatted text to thermal printer",
    tags=["print"],
)
async def print_text(request: PrintTextRequest):
    """Print text to thermal printer."""
    result = await printer_manager.print_text(
        text=request.text,
        align=request.align,
        bold=request.bold,
        underline=request.underline,
        size=request.size,
        cut=request.cut,
        new_line=request.new_line,
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Print operation failed"),
        )

    return PrintResponse(**result)


@router.post(
    "/print/qr",
    response_model=PrintResponse,
    summary="Print QR code",
    description="Print QR code to thermal printer",
    tags=["print"],
)
async def print_qr(request: PrintQRRequest):
    """Print QR code to thermal printer."""
    result = await printer_manager.print_qr(
        data=request.data,
        align=request.align,
        cell_size=request.cell_size,
        correction=request.correction,
        model=request.model,
        cut=request.cut,
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Print operation failed"),
        )

    return PrintResponse(**result)


@router.post(
    "/print/buffer",
    response_model=PrintResponse,
    summary="Print raw buffer",
    description="Print raw buffer data to thermal printer",
    tags=["print"],
)
async def print_buffer(request: PrintBufferRequest):
    """Print raw buffer to thermal printer."""
    buffer_bytes = bytes(request.buffer)
    result = await printer_manager.print_buffer(buffer_bytes)

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Print operation failed"),
        )

    return PrintResponse(**result)


@router.get(
    "/printer/status",
    response_model=PrinterStatusResponse,
    summary="Get printer status",
    description="Get printer connection status and configuration",
    tags=["printer"],
)
async def get_printer_status():
    """Get printer status and configuration."""
    status = await printer_manager.get_status()
    return PrinterStatusResponse(**status)


@router.put(
    "/printer/config",
    response_model=PrintResponse,
    summary="Update printer configuration",
    description="Update printer configuration settings",
    tags=["printer"],
)
async def update_printer_config(request: PrinterConfigRequest):
    """Update printer configuration."""
    try:
        config = PrinterConfig(**request.model_dump())
        saved = save_printer_config(config)

        if saved:
            # Update the printer manager with new config
            global printer_manager
            printer_manager = PrinterManager(config)
            return PrintResponse(
                success=True, message="Configuration updated successfully"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save configuration",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post(
    "/printer/test",
    response_model=PrintResponse,
    summary="Print test page",
    description="Print a test page to verify printer functionality",
    tags=["printer"],
)
async def print_test():
    """Print a test page."""
    test_text = f"Thermal Printer API Test\n{datetime.now().isoformat()}\n\nPrinter is working correctly!"

    result = await printer_manager.print_text(text=test_text, align="center", cut=True)

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Test print failed"),
        )

    return PrintResponse(**result)


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check service health status",
    tags=["system"],
)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        service="thermal_printer_api",
        version="2.0.0",
        timestamp=datetime.now().isoformat(),
    )


@router.get(
    "/",
    response_model=ApiOverviewResponse,
    summary="API overview",
    description="Get API overview and available endpoints",
    tags=["system"],
)
async def api_overview():
    """API overview endpoint."""
    return ApiOverviewResponse(
        service="Thermal Printer API",
        version="2.0.0",
        documentation="/docs",
        health="/health",
        endpoints={
            "POST /api/print/text": "Print text",
            "POST /api/print/qr": "Print QR code",
            "POST /api/print/buffer": "Print raw buffer",
            "GET /api/printer/status": "Get printer status",
            "PUT /api/printer/config": "Update printer config",
            "POST /api/printer/test": "Print test page",
        },
    )
