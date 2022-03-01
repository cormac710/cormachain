import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Switch, Route } from 'react-router-dom';

import App from './components/App';

import './index.css';

import Cormachain from './components/Cormachain';
import ConductTransaction from './components/ConductTransaction';
import TransactionPool from './components/TransactionPool';
import history from './history';

ReactDOM.render(
    <Router history={history}>
        <Switch>
            <Route path='/' exact component={App} />
            <Route path='/cormachain' component={Cormachain} />
            <Route path='/conduct-transaction' component={ConductTransaction} />
            <Route path='/transaction-pool' component={TransactionPool} />
        </Switch>
    </Router>,
    document.getElementById('root')
);
