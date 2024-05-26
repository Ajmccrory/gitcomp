// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import Scrape from './components/Scrape';
import Existing from './components/Existing';
import Clear from './components/Clear';
import Compare from './components/Compare';
import Similarity from './components/Similarity';
import Graph from './components/Graph';

function App() {
  return (
    <Router>
      <div className="container">
        <div className="summary text-center mb-4">
          <h2>Explore Gitcomp.py Features</h2>
          <p>Gitcomp.py offers a range of functionalities to streamline your GitHub data management:</p>
        </div>
        <div className="row">
          <Card 
            title="Scrape User Data" 
            description="Scrape repositories of a GitHub user." 
            link="/scrape" 
            icon="fas fa-download"
          />
          <Card 
            title="Check Existing User" 
            description="Check if a user exists in the database." 
            link="/existing" 
            icon="fas fa-search"
          />
          <Card 
            title="Clear Mongo Collection" 
            description="Clear MongoDB collection for a specific user." 
            link="/clear" 
            icon="fas fa-trash-alt"
          />
          <Card 
            title="Compare Users" 
            description="Compare the contributions of multiple users." 
            link="/compare" 
            icon="fas fa-users"
          />
          <Card 
            title="Repo Similarity" 
            description="Check to see whether 2-4 users have repos in common." 
            link="/similarity" 
            icon="fas fa-users"
          />
          <Card 
            title="User Graph" 
            description="Create a graph of user repositories and contributions." 
            link="/graph" 
            icon="fas fa-users"
          />
        </div>
        <Route path="/scrape" component={Scrape} />
        <Route path="/existing" component={Existing} />
        <Route path="/clear" component={Clear} />
        <Route path="/compare" component={Compare} />
        <Route path="/similarity" component={Similarity} />
        <Route path="/graph" component={Graph} />
      </div>
    </Router>
  );
}

function Card({ title, description, link, icon }) {
  return (
    <div className="col-lg-3 mb-4">
      <div className="card bg-primary text-white shadow">
        <div className="card-body">
          <i className={icon}></i> {title}
          <p className="mt-2">{description}</p>
          <Link to={link} className="btn btn-light">Go</Link>
        </div>
      </div>
    </div>
  );
}

export default App;
