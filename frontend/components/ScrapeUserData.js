import React, { useState } from 'react';
import { scrapeUserData } from '../api';

const ScrapeUserData = () => {
    const [username, setUsername] = useState('');
    const [repos, setRepos] = useState([]);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!username) {
            setError('Please provide a username.');
            return;
        }

        try {
            const response = await showScrapedData(username);
            setRepos(response.data.repos);
        } catch (err) {
            setError(err.response ? err.response.data.error : 'An error occurred.');
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Username"
                />
                <button type="submit">Show Data</button>
            </form>
            {error && <p>{error}</p>}
            <ul>
                {repos.map((repo, index) => (
                    <li key={index}>{repo}</li>
                ))}
            </ul>
        </div>
    );
};

export default ScrapeUserData;
