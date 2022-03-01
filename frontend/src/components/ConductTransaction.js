import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { FormGroup, FormControl, Button } from "react-bootstrap";
import { TRANSACT_API, KNOWN_ADDRESSES_API } from "../constants";
import history from "../history";

function ConductTransaction() {
    const [amount, setAmount] = useState(0);
    const [receiver, setReceiver] = useState('');
    const [knownAddresses, setKnownAddresses] = useState([])

    useEffect(() => {
        fetch(KNOWN_ADDRESSES_API)
            .then(response => response.json())
            .then(known_addresses_json => setKnownAddresses(known_addresses_json))
    }, []);

    const updateReceiver = event => {
        setReceiver(event.target.value);
    };

    const updateAmount = event => {
        setAmount(
            Number(event.target.value)
        );
    };

    const submitTransaction = () => {
        fetch(`${TRANSACT_API}`,
            {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ receiver, amount })
            })
            .then(response => response.json())
            .then(json => {
                console.log('submit transaction json', json);
                history.push('/transaction-pool');
            })
    };

    return (
        <div className="ConductTransaction">
            <Link to="/">Home</Link>
            <hr/>
            <h3>Conduct Transaction</h3>
            <br />

            <FormGroup>
                <FormControl
                    input="text"
                    placeholder="receiver"
                    value={receiver}
                    onChange={updateReceiver}
                />
            </FormGroup>

            <FormGroup>
                <FormControl
                    input="number"
                    placeholder="amount"
                    value={amount}
                    onChange={updateAmount}
                />
            </FormGroup>
            <div>
                <Button variant="danger" onClick={submitTransaction}>Submit</Button>
            </div>
            <br />
            <h4>Known Addresses</h4>
            <div>
                {
                    knownAddresses.map((knownAddress, i) => (
                        <span key={knownAddress}>
                            <u>{knownAddress}</u>{i !== knownAddresses.length - 1 ? ', ' : ''}
                        </span>
                    ))
                }
            </div>
        </div>
    )

}

export default ConductTransaction