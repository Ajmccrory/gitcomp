import React, { useState } from 'react';
import { compareUsers, displayComparison } from '../api';

const CompareUsers = () => {
    const [usernames, setUsernames] = useState(['', '', '', '']);
    const [error, setError] = useState('');
    const [comparisonImage, setComparisonImage] = useState('');

    const handleChange = (index, value) => {
        const newUsernames = [...usernames];
        newUsernames[index] = value;
        setUsernames(newUsernames);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const validUsernames = usernames.filter(username => username);

        if (validUsernames.length < 2 || validUsernames.length > 4) {
            setError('Please provide 2 to 4 usernames.');
            return;
        }

        try {
            const response = await compareUsers(validUsernames);
            const plotId = response.data.plot_id;
            const imageResponse = await displayComparison(plotId);
            setComparisonImage(`data:image/png;base64,${imageResponse.data.plot_data}`);
        } catch (err) {
            setError(err.response ? err.response.data.error : 'An error occurred.');
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                {usernames.map((username, index) => (
                    <input
                        key={index}
                        type="text"
                        value={username}
                        onChange={(e) => handleChange(index, e.target.value)}
                        placeholder={`Username ${index + 1}`}
                    />
                ))}
                <button type="submit">Compare</button>
            </form>
            {error && <p>{error}</p>}
            {comparisonImage && <img src={comparisonImage} alt="User Comparison" />}
        </div>
    );
};

export default CompareUsers;
