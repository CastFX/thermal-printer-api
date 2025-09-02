const { printBuffer, printText, printQR, getPrinterStatus, savePrinterConfig } = require('../scripts/printer');

async function printerRoutes(fastify, options) {
    // Swagger documentation
    const printTextSchema = {
        description: 'Print text to thermal printer',
        tags: ['printer'],
        body: {
            type: 'object',
            required: ['text'],
            properties: {
                text: { type: 'string', description: 'Text to print' },
                align: { type: 'string', enum: ['left', 'center', 'right'], default: 'left' },
                bold: { type: 'boolean', default: false },
                underline: { type: 'boolean', default: false },
                size: { type: 'string', enum: ['normal', 'large'], default: 'normal' },
                cut: { type: 'boolean', default: false },
                newLine: { type: 'boolean', default: true }
            }
        },
        response: {
            200: {
                type: 'object',
                properties: {
                    success: { type: 'boolean' },
                    message: { type: 'string' }
                }
            }
        }
    };

    const printQRSchema = {
        description: 'Print QR code to thermal printer',
        tags: ['printer'],
        body: {
            type: 'object',
            required: ['data'],
            properties: {
                data: { type: 'string', description: 'Data to encode in QR code' },
                align: { type: 'string', enum: ['left', 'center', 'right'], default: 'left' },
                cellSize: { type: 'integer', minimum: 1, maximum: 10, default: 3 },
                correction: { type: 'string', enum: ['L', 'M', 'Q', 'H'], default: 'M' },
                model: { type: 'integer', enum: [1, 2], default: 2 },
                cut: { type: 'boolean', default: false }
            }
        },
        response: {
            200: {
                type: 'object',
                properties: {
                    success: { type: 'boolean' },
                    message: { type: 'string' }
                }
            }
        }
    };

    // Print text endpoint
    fastify.post('/print/text', { schema: printTextSchema }, async (request, reply) => {
        try {
            const result = await printText(request.body.text, request.body);
            return result;
        } catch (error) {
            reply.status(500);
            return { success: false, error: error.message };
        }
    });

    // Print QR code endpoint
    fastify.post('/print/qr', { schema: printQRSchema }, async (request, reply) => {
        try {
            const result = await printQR(request.body.data, request.body);
            return result;
        } catch (error) {
            reply.status(500);
            return { success: false, error: error.message };
        }
    });

    // Print raw buffer endpoint
    fastify.post('/print/buffer', {
        description: 'Print raw buffer to thermal printer',
        tags: ['printer'],
        body: {
            type: 'object',
            required: ['buffer'],
            properties: {
                buffer: { 
                    type: 'array',
                    items: { type: 'integer' },
                    description: 'Raw buffer bytes as array of integers'
                }
            }
        }
    }, async (request, reply) => {
        try {
            const buffer = Buffer.from(request.body.buffer);
            const result = await printBuffer(buffer);
            return result;
        } catch (error) {
            reply.status(500);
            return { success: false, error: error.message };
        }
    });

    // Get printer status
    fastify.get('/printer/status', {
        description: 'Get printer connection status and configuration',
        tags: ['printer'],
        response: {
            200: {
                type: 'object',
                properties: {
                    connected: { type: 'boolean' },
                    config: { type: 'object' },
                    interface: { type: 'string' },
                    error: { type: 'string' }
                }
            }
        }
    }, async (request, reply) => {
        const status = await getPrinterStatus();
        return status;
    });

    // Update printer configuration
    fastify.put('/printer/config', {
        description: 'Update printer configuration',
        tags: ['printer'],
        body: {
            type: 'object',
            properties: {
                type: { type: 'string', enum: ['EPSON', 'STAR'], default: 'EPSON' },
                interface: { type: 'string', default: '/dev/usb/lp0' },
                width: { type: 'integer', minimum: 20, maximum: 80, default: 60 },
                timeout: { type: 'integer', minimum: 1000, maximum: 30000, default: 5000 }
            }
        }
    }, async (request, reply) => {
        try {
            const saved = savePrinterConfig(request.body);
            if (saved) {
                return { success: true, message: 'Configuration updated successfully' };
            } else {
                reply.status(500);
                return { success: false, error: 'Failed to save configuration' };
            }
        } catch (error) {
            reply.status(500);
            return { success: false, error: error.message };
        }
    });

    // Test print endpoint
    fastify.post('/printer/test', {
        description: 'Print a test page',
        tags: ['printer']
    }, async (request, reply) => {
        try {
            const testText = `Thermal Printer API Test\n${new Date().toISOString()}\n\nPrinter is working correctly!`;
            const result = await printText(testText, { align: 'center', cut: true });
            return result;
        } catch (error) {
            reply.status(500);
            return { success: false, error: error.message };
        }
    });
}

module.exports = printerRoutes;