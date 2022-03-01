import React, { useEffect, useState} from 'react';
import { Link } from 'react-router-dom';
import {Button} from "react-bootstrap";
import {BLOCKCHAIN_API} from '../constants'
import Block from "./Block";

const PAGE_RANGE = 3;

function Cormachain() {
    const [cormachain, setCormachain] = useState([]);
    const [cormachainLength, setCormachainLength] = useState(0);

    const fetchPage = ({ start, end }) => {
    fetch(`${BLOCKCHAIN_API}/range?start=${start}&end=${end}` )
        .then(response => response.json())
        .then(json => setCormachain(json))
    };

    useEffect(() => {
        fetchPage({start: 0, end: PAGE_RANGE});

        fetch(`${BLOCKCHAIN_API}/length`)
        .then(response => response.json())
        .then(cormachainJson => setCormachainLength(cormachainJson));
    }, []);

    const buttonNumbers = [];

    for (let i=0; i < Math.ceil(cormachainLength / PAGE_RANGE); i++) {
        buttonNumbers.push(i)
    }

    return (
        <div className="Blockchain">

            <Link to="/">Home</Link>
            <hr/>

            <h3>Cormachain</h3>
            <div>
                {
                    cormachain.map((block) => <Block key={block.hash} block={block}/>)
                }
            </div>
            <div>{
                buttonNumbers.map(number => {
                    const start = number * PAGE_RANGE;
                    const end = (number + 1) * 3;
                    return (
                        <span key={number} onClick={() => fetchPage({start, end})}>
                            <Button size="sm" variant="danger">
                                {number + 1}
                            </Button>{" "}
                        </span>
                    )
                })
            }</div>
        </div>
    )
}

export default Cormachain;