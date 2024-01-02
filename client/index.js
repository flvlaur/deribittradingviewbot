require('dotenv').config();
const axios = require('axios');
const crypto = require('crypto');

const API_KEY = process.env.DERIBIT_API_KEY;
const API_SECRET = process.env.DERIBIT_API_SECRET;
const BASE_URL = 'https://www.deribit.com';

// Function to generate a nonce
function getNonce() {
    return new Date().getTime();
}

// Function to generate a signature
function generateSignature(method, path, params, nonce) {
    const message = `${nonce}\n${method}\n${path}\n${params}\n`;
    const signature = crypto.createHmac('sha256', API_SECRET).update(message).digest('hex');
    return signature;
}

// Function to get account information
async function getAccountInfo() {
    const path = '/api/v2/private/get_account_summary';
    const params = 'currency=BTC';
    const nonce = getNonce();
    const signature = generateSignature('GET', path, params, nonce);

    try {
        const response = await axios.get(`${BASE_URL}${path}?${params}`, {
            headers: {
                'Authorization': `Bearer ${API_KEY}`,
                'x-deribit-sig': signature,
                // Add this header if required by the API for a nonce
                'x-deribit-nonce': nonce,
            },
        });

        console.log('Account Info:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error fetching account information:', error);
        return null;
    }
}

// Call the function to test
getAccountInfo();
















const fs = require('fs');
const path = require('path');

function messageInterpreter() {
    const directory = path.join(__dirname, "..", 'tradingview_alerts');
    const fileNames = fs.readdirSync(directory).filter(file => file.endsWith('.txt'));

    const tradeData = [];

    fileNames.forEach((fileName, index) => {
        const match = fileName.match(/(\d{4}-\d{2}-\d{2})-(\d{2}-\d{2}-\d{2})-(\d+)-(buy|sell)-([A-Z]+)-(\d+\.\d*)/);
        if (match) {
            let [, date, time, size, action, symbol, price] = match;
            time = time.replace(/-/g, ':');  // Format time correctly

            if (date && time && size && action && symbol && price) {
                tradeData.push({ index: index + 1, date, time, size, action, symbol, price: parseFloat(price) });
            } else {
                console.log(`Data not available for ${fileName}`);
            }
        } else {
            console.log(`Data not available for ${fileName}`);
        }
    });

    return tradeData;
}


function filterTrades({ dates = null, times = null, symbols = null, actions = null, priceRange = null } = {}) {
    const allTradeData = messageInterpreter();

    return allTradeData.filter(({ date, time, symbol, action, price }) => {
        const dateMatch = dates === null || dates.includes(date);
        const timeMatch = times === null || times.includes(time);
        const symbolMatch = symbols === null || symbols.includes(symbol);
        const actionMatch = actions === null || actions.includes(action);
        const priceMatch = priceRange === null || (price >= priceRange[0] && price <= priceRange[1]);

        return dateMatch && timeMatch && symbolMatch && actionMatch && priceMatch;
    });
}


async function placeMarketOrder(trade) {
    const path = trade.action === 'buy' ? '/api/v2/private/buy' : '/api/v2/private/sell';
    const params = {
        instrument_name: trade.symbol,
        amount: trade.size,
        type: 'market'
    };

    try {
        const response = await axios.post(`${BASE_URL}${path}`, params, {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        console.log('Order Response:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error placing market order:', error.response.data);
        return null;
    }
}

// Example usage
const filteredTrades = filterTrades({ /* filter criteria */ });
filteredTrades.forEach(trade => {
    placeMarketOrder(trade);
});
