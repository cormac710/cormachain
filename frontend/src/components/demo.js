import React, { useState } from 'react';
import CryptoPrice from './CryptoPrice';

function Demo() {
  const [userQuery, setUserQuery] = useState('');

  const updateUserQuery = (event) => {
    setUserQuery(event.target.value);
    console.log('userQuery', userQuery);
  };

  const searchQuery = () => {
    window.open(`https://google.com/search?q=${userQuery}`);
  };

  const userKeyPress = (event) => {
    if (event.key === 'Enter') {
      searchQuery();
    }
  };

  return (
    <div className="App">
      <input value={userQuery} onChange={updateUserQuery} onKeyPress={userKeyPress}/>
      <button onClick={searchQuery}>Search</button>
        <div>{userQuery}</div>
      <hr />

      <CryptoPrice />

    </div>
  );
}

export default App;
