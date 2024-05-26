import React, { useState } from 'react';

function Scrape() {
    const [username, setUsername] = useState('');

    const handleScrape = async () => {
        const response = await fetch ('/scrape', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username }),
        });
        const data = await response.json();
        // response data
    };

    return (
        <div>
        <h2>Scrape User Data</h2>
        <input 
          type="text" 
          value={username} 
          onChange={(e) => setUsername(e.target.value)} 
          placeholder="Enter GitHub username"
        />
        <button onClick={handleScrape}>Scrape Now</button>
      </div>
    );
}

export default Scrape;