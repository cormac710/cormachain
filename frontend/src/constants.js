const LOCALHOST_BASE_URI = 'http://127.0.0.1:5000/';
const BLOCKCHAIN_API = LOCALHOST_BASE_URI + 'blockchain';
const WALLET_API = LOCALHOST_BASE_URI + 'wallet/info';
const TRANSACT_API = LOCALHOST_BASE_URI + '/wallet/transact';
const KNOWN_ADDRESSES_API = LOCALHOST_BASE_URI + '/known-addresses';
const TRANSACTIONS_API = LOCALHOST_BASE_URI + '/transactions';
const BLOCKCHAIN_MINE_API = BLOCKCHAIN_API + '/mine'

export { BLOCKCHAIN_API, WALLET_API, TRANSACT_API, KNOWN_ADDRESSES_API, 
    TRANSACTIONS_API, BLOCKCHAIN_MINE_API}