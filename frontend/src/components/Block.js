import React, { useState } from 'react';
import { Button } from "react-bootstrap";
import Transaction from "./Transaction";

import { MILLISEC_PY } from '../config'

function ToggleTransactionDisplay({ block }) {
    const [displayTransaction, setDisplayTransaction] = useState(false);
    const { data } = block;

    const toggleDisplayTransaction = () => {
        console.log(displayTransaction);
        setDisplayTransaction(!displayTransaction);
    };

    if (displayTransaction) {
        return(
            <div>
                {
                    data.map(transaction => (
                        <div key={transaction.id}>
                            <hr/>
                            <Transaction transaction={transaction} />
                        </div>
                    ))
                }
                <br/>
                <Button variant="danger" size="sm" onClick={toggleDisplayTransaction}>
                    Show Less
                </Button>
            </div>
        )
    }

    return (
        <div>
            <br/>
            <Button variant="danger" size="sm" onClick={toggleDisplayTransaction}>
                Show More
            </Button>
        </div>
    )

}

function Block({ block }) {
    const {timestamp, block_hash } = block;
    const hashDisplay = `${block_hash.substring(0, 15)}...`;
    const timestampDisplay = new Date(timestamp / MILLISEC_PY).toLocaleString();

    return(
        <div className="Block" key={block.id}>
            <div>
                Hash: {hashDisplay}
            </div>
            <div>
                Time: {timestampDisplay}
            </div>
            <ToggleTransactionDisplay block={block}/>
            {/*<div>*/}
            {/*    {*/}
            {/*        data.map(transaction => (*/}
            {/*            <div key={transaction.id}>*/}
            {/*                <hr/>*/}
            {/*                <Transaction transaction={transaction} />*/}
            {/*            </div>*/}
            {/*        ))*/}
            {/*    }*/}
            {/*    <br/>*/}
            {/*</div>*/}
            <br/>
        </div>
    )
}

export default Block;
