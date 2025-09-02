const { ThermalPrinter, PrinterTypes } = require('node-thermal-printer');
const fs = require('node:fs');
const path = require('path');

// Configuration paths
const PRINTER_CONFIG_PATH = path.join(__dirname, '../printer-config.json');

// Default printer configuration
const DEFAULT_CONFIG = {
    type: 'EPSON',
    interface: '/dev/usb/lp0',
    width: 60,
    timeout: 5000
};

// Load printer configuration
function loadPrinterConfig() {
    try {
        if (fs.existsSync(PRINTER_CONFIG_PATH)) {
            const configData = fs.readFileSync(PRINTER_CONFIG_PATH, 'utf8');
            return { ...DEFAULT_CONFIG, ...JSON.parse(configData) };
        }
    } catch (error) {
        console.warn('Error loading printer config, using defaults:', error.message);
    }
    return DEFAULT_CONFIG;
}

// Save printer configuration
function savePrinterConfig(config) {
    try {
        const configToSave = { ...DEFAULT_CONFIG, ...config };
        fs.writeFileSync(PRINTER_CONFIG_PATH, JSON.stringify(configToSave, null, 2));
        return true;
    } catch (error) {
        console.error('Error saving printer config:', error);
        return false;
    }
}

// Create printer instance
function createPrinter(config = null) {
    const printerConfig = config || loadPrinterConfig();
    
    return new ThermalPrinter({
        type: PrinterTypes[printerConfig.type] || PrinterTypes.EPSON,
        interface: printerConfig.interface,
        options: {
            timeout: printerConfig.timeout
        },
        width: printerConfig.width
    });
}

// Print raw buffer
async function printBuffer(buffer, config = null) {
    return new Promise((resolve, reject) => {
        let printer;
        try {
            printer = createPrinter(config);
        } catch (error) {
            reject(new Error(`Failed to create printer: ${error.message}`));
            return;
        }

        printer.isPrinterConnected()
            .then(isConnected => {
                if (!isConnected) {
                    throw new Error('Printer is not connected');
                }
                return printer.raw(buffer);
            })
            .then(() => {
                resolve({ success: true, message: 'Print job completed successfully' });
            })
            .catch(error => {
                reject(new Error(`Print failed: ${error.message}`));
            });
    });
}

// Print text with formatting options
async function printText(text, options = {}) {
    return new Promise((resolve, reject) => {
        let printer;
        try {
            printer = createPrinter();
        } catch (error) {
            reject(new Error(`Failed to create printer: ${error.message}`));
            return;
        }

        printer.isPrinterConnected()
            .then(isConnected => {
                if (!isConnected) {
                    throw new Error('Printer is not connected');
                }

                // Apply formatting options
                if (options.align === 'center') printer.alignCenter();
                else if (options.align === 'right') printer.alignRight();
                else printer.alignLeft();

                if (options.bold) printer.bold(true);
                if (options.underline) printer.underline(true);
                if (options.size === 'large') printer.setTextSize(1, 1);

                // Print text
                if (options.newLine !== false) {
                    printer.println(text);
                } else {
                    printer.print(text);
                }

                // Reset formatting
                printer.bold(false);
                printer.underline(false);
                printer.setTextNormal();
                printer.alignLeft();

                if (options.cut) printer.cut();

                return printer.execute();
            })
            .then(() => {
                resolve({ success: true, message: 'Text printed successfully' });
            })
            .catch(error => {
                reject(new Error(`Print failed: ${error.message}`));
            });
    });
}

// Print QR code
async function printQR(data, options = {}) {
    return new Promise((resolve, reject) => {
        let printer;
        try {
            printer = createPrinter();
        } catch (error) {
            reject(new Error(`Failed to create printer: ${error.message}`));
            return;
        }

        printer.isPrinterConnected()
            .then(isConnected => {
                if (!isConnected) {
                    throw new Error('Printer is not connected');
                }

                if (options.align === 'center') printer.alignCenter();
                else if (options.align === 'right') printer.alignRight();

                printer.printQR(data, {
                    cellSize: options.cellSize || 3,
                    correction: options.correction || 'M',
                    model: options.model || 2
                });

                printer.alignLeft();
                if (options.cut) printer.cut();

                return printer.execute();
            })
            .then(() => {
                resolve({ success: true, message: 'QR code printed successfully' });
            })
            .catch(error => {
                reject(new Error(`Print failed: ${error.message}`));
            });
    });
}

// Check printer status
async function getPrinterStatus() {
    try {
        const printer = createPrinter();
        const isConnected = await printer.isPrinterConnected();
        const config = loadPrinterConfig();
        
        return {
            connected: isConnected,
            config: config,
            interface: config.interface
        };
    } catch (error) {
        return {
            connected: false,
            error: error.message,
            config: loadPrinterConfig()
        };
    }
}

module.exports = {
    createPrinter,
    printBuffer,
    printText,
    printQR,
    getPrinterStatus,
    loadPrinterConfig,
    savePrinterConfig
};