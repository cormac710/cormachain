import React, { useEffect, useState } from 'react';

// Supposed to be dogs but API needed auth so quickly switched to an easier one for this example
const API = 'https://api.coinbase.com/v2/exchange-rates?currency=BTC';

function CryptoPrice() {
    const [crypto, setCrypto] = useState({});

    useEffect(() => {
        fetch(API)
            .then(response => response.json())
            .then(json => {
                setCrypto({currency: json['data']['currency'], aed: json['data']['rates']['AED']});
            });

        console.log('fetching data');

    //    [] is telling not to rerun between renders
    }, []);

    const {currency, aed} = crypto;

    return (
        <div>
            <h3>Crypto</h3>
            <p>{currency} is {aed}</p>
        </div>
    )
}

export default CryptoPrice
