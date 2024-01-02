import BASE_URL from './client/url.js'
import REFRESH_TOKEN from './client/url.js'
import accessToken from './client/url.js'
import tokenExpires from './client/url.js'

async function placeMarketOrder(trade) {
    const path = trade.action === 'buy' ? '/api/v2/private/buy' : '/api/v2/private/sell';
    const params = {
        instrument_name: "BTC-PERPETUAL",
        amount: 7500,
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
