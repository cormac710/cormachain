import React, { useState, useEffect } from "react";
import { Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import Transaction from './Transaction'
import { TRANSACTIONS_API, BLOCKCHAIN_MINE_API } from "../constants";
import history from "../history";

function TransactionPool() {
    const [transactions, setTransactions] = useState([]);

    const fetchTransactions = () => {
        fetch(TRANSACTIONS_API)
            .then(response => response.json())
            .then(transactions_json => {
                setTransactions(transactions_json)
            });
    }

    const mineBlock = () => {
        fetch(BLOCKCHAIN_MINE_API)
            .then(() => {
                history.push('/cormachain')
            });
    };

    useEffect(() => {
        fetchTransactions();
        const intervalId = setInterval(fetchTransactions, 3000);
        return () => clearInterval(intervalId);
    }, []);
    
    return (
        <div className="TransactionPool">
            <Link to="/">Home</Link>
            <hr/>
            <h3>Transaction Pool</h3>
            <div>
                {
                    transactions.map(transaction => (
                        <div key={transaction.id}>
                            <hr />
                            <Transaction transaction={transaction}/>
                        </div>
                    ))
                }
            </div>
            <hr/>
            <Button variant="danger" onClick={mineBlock}>
                Mine!
            </Button>
        </div>
    )
}

export default TransactionPool;
