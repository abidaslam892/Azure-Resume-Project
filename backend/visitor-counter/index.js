const { TableClient } = require('@azure/data-tables');

// Initialize Table Storage client
let tableClient;

/**
 * Initialize CosmosDB Table API client
 */
async function initializeTableClient() {
    try {
        const connectionString = process.env.COSMOS_DB_CONNECTION_STRING || 
                                process.env.AzureWebJobsStorage;
        
        if (!connectionString) {
            throw new Error('No connection string found');
        }

        const tableName = 'VisitorCounter';
        tableClient = new TableClient(connectionString, tableName);
        
        // Ensure table exists
        await tableClient.createTable();
        return tableClient;
    } catch (error) {
        console.error('Failed to initialize table client:', error.message);
        throw error;
    }
}

/**
 * Get current visitor count
 */
async function getVisitorCount() {
    try {
        if (!tableClient) {
            await initializeTableClient();
        }

        const entity = await tableClient.getEntity('visitor-counter', 'count');
        return entity.Count || 0;
    } catch (error) {
        if (error.statusCode === 404) {
            return 0;
        }
        throw error;
    }
}

/**
 * Increment visitor count
 */
async function incrementVisitorCount() {
    try {
        if (!tableClient) {
            await initializeTableClient();
        }

        let currentCount = 0;
        
        try {
            const existingEntity = await tableClient.getEntity('visitor-counter', 'count');
            currentCount = existingEntity.Count || 0;
        } catch (error) {
            if (error.statusCode !== 404) {
                throw error;
            }
        }

        const newCount = currentCount + 1;
        
        const entity = {
            partitionKey: 'visitor-counter',
            rowKey: 'count',
            Count: newCount,
            LastUpdated: new Date().toISOString()
        };

        await tableClient.upsertEntity(entity, 'Replace');
        return newCount;
    } catch (error) {
        console.error('Error incrementing visitor count:', error.message);
        throw error;
    }
}

/**
 * Azure Function entry point
 */
module.exports = async function (context, req) {
    context.log(`HTTP trigger function processed a ${req.method} request.`);
    
    try {
        // Handle CORS preflight
        if (req.method === 'OPTIONS') {
            context.res = {
                status: 200,
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                body: ''
            };
            return;
        }

        let count;
        let message;

        if (req.method === 'POST') {
            count = await incrementVisitorCount();
            message = 'Visitor count incremented';
            context.log(`Count incremented to: ${count}`);
        } else {
            count = await getVisitorCount();
            message = 'Current visitor count';
            context.log(`Current count: ${count}`);
        }

        const responseData = {
            success: true,
            count: count,
            method: req.method,
            timestamp: new Date().toISOString(),
            message: message
        };

        context.res = {
            status: 200,
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Cache-Control': 'no-cache'
            },
            body: responseData
        };

    } catch (error) {
        context.log.error('Error in visitor counter:', error.message);
        
        context.res = {
            status: 500,
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            body: {
                success: false,
                error: 'Internal server error',
                message: error.message,
                timestamp: new Date().toISOString()
            }
        };
    }
};