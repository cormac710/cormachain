import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom'
import logo from '../resources/cormachain.jpg'
import {WALLET_API} from '../constants'

function App() {
    const [walletInfo, setWalletInfo] = useState({});
    const {address, balance} = walletInfo;

    useEffect(() => {
        fetch(WALLET_API)
            .then(response => response.json())
            .then(walletJson => setWalletInfo(walletJson));
    }, []);

  return (
    <div className="App">
        <img className="logo" src={logo} alt="application-logo"/>
        <h3>Welcome to cormachain</h3>
        <Link to="/cormachain">Cormachain</Link>
        <Link to="/conduct-transaction">Conduct Transaction</Link>
        <Link to="/transaction-pool">Transaction Pool </Link>
        <br/>
        <div className="WalletInfo">
            <div>
                Address: {address}
            </div>
            <div>
                Balance: {balance}
            </div>

        </div>
    </div>
  );
}

export default App;
