const fastify = require('fastify')({
    logger: true
});
const fs = require('node:fs');
const path = require('path');

// Configuration
const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || '0.0.0.0';

// Register Swagger for API documentation
fastify.register(require('@fastify/swagger'), {
    swagger: {
        info: {
            title: 'Thermal Printer API',
            description: 'Local REST API for thermal printer management',
            version: '2.0.0'
        },
        externalDocs: {
            url: 'https://swagger.io',
            description: 'Find more info here'
        },
        host: `${HOST}:${PORT}`,
        schemes: ['http'],
        consumes: ['application/json'],
        produces: ['application/json'],
        tags: [
            { name: 'printer', description: 'Printer related operations' }
        ]
    }
});

fastify.register(require('@fastify/swagger-ui'), {
    routePrefix: '/docs',
    uiConfig: {
        docExpansion: 'full',
        deepLinking: false
    },
    uiHooks: {
        onRequest: function (request, reply, next) { next(); },
        preHandler: function (request, reply, next) { next(); }
    },
    staticCSP: true,
    transformStaticCSP: (header) => header,
    transformSpecification: (swaggerObject, request, reply) => { return swaggerObject; },
    transformSpecificationClone: true
});

// Register static files for any future web interface
const publicDir = path.join(__dirname, 'public');
if (fs.existsSync(publicDir)) {
    fastify.register(require('@fastify/static'), {
        root: publicDir,
        prefix: '/public/',
    });
}

// Register form body parser
fastify.register(require('@fastify/formbody'));

// Register printer routes
fastify.register(require('./routes/printer'), { prefix: '/api' });

// Health check endpoint
fastify.get('/health', async (request, reply) => {
    return { 
        status: 'ok', 
        service: 'thermal_printer_api',
        version: '2.0.0',
        timestamp: new Date().toISOString()
    };
});

// Root endpoint
fastify.get('/', async (request, reply) => {
    return {
        service: 'Thermal Printer API',
        version: '2.0.0',
        documentation: '/docs',
        health: '/health',
        endpoints: {
            'POST /api/print/text': 'Print text',
            'POST /api/print/qr': 'Print QR code',
            'POST /api/print/buffer': 'Print raw buffer',
            'GET /api/printer/status': 'Get printer status',
            'PUT /api/printer/config': 'Update printer config',
            'POST /api/printer/test': 'Print test page'
        }
    };
});

// Error handler
fastify.setErrorHandler((error, request, reply) => {
    fastify.log.error(error);
    reply.status(500).send({ 
        success: false, 
        error: 'Internal Server Error',
        message: error.message 
    });
});

// Graceful shutdown
process.on('SIGTERM', () => {
    fastify.log.info('SIGTERM received, shutting down gracefully');
    fastify.close();
});

process.on('SIGINT', () => {
    fastify.log.info('SIGINT received, shutting down gracefully');
    fastify.close();
});

// Start the server
const start = async () => {
    try {
        await fastify.listen({ port: PORT, host: HOST });
        fastify.log.info(`Server listening on http://${HOST}:${PORT}`);
        fastify.log.info(`API documentation available at http://${HOST}:${PORT}/docs`);
    } catch (err) {
        fastify.log.error(err);
        process.exit(1);
    }
};

start();