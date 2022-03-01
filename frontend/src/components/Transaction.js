import React from 'react';

function Transaction({ transaction }) {
    const { input, output } = transaction;
    const receivers = Object.keys(output);

    return (
        <div className="Transaction">
            <div>
                From: {input.address}
            </div>
            More Info:
            <br/>
            {
                receivers.map(receiver => (
                    <div key={receiver}>
                        To: {receiver} | Sent: {output[receiver]}
                    </div>
                ))
            }
        </div>
    )
}

export default Transaction;
