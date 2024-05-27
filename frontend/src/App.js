import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import ScrapeUserData from './components/ScrapeUserData';
import CheckUserExists from './components/CheckUserExists';
import ClearMongoCollection from './components/ClearMongoCollection';
import CompareRepoSimilarity from './components/CompareRepoSimilarity';
import CheckRepoSimilarity from './components/CheckRepoSimilarity';
import DisplayGraph from './components/DisplayGraph';

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
            link="/api/scrape"  // Update the link to match your Flask endpoint
            icon="fas fa-download"
          />
          <Card 
            title="Check Existing User" 
            description="Check if a user exists in the database." 
            link="/api/existing"  // Update the link to match your Flask endpoint
            icon="fas fa-search"
          />
          <Card 
            title="Clear Mongo Collection" 
            description="Clear MongoDB collection for a specific user." 
            link="/api/clear"  // Update the link to match your Flask endpoint
            icon="fas fa-trash-alt"
          />
          <Card 
            title="Compare Users" 
            description="Compare the contributions of multiple users." 
            link="/api/compare"  // Update the link to match your Flask endpoint
            icon="fas fa-users"
          />
          <Card 
            title="Repo Similarity" 
            description="Check to see whether 2-4 users have repos in common." 
            link="/api/similarity"  // Update the link to match your Flask endpoint
            icon="fas fa-users"
          />
          <Card 
            title="User Graph" 
            description="Create a graph of user repositories and contributions." 
            link="/api/graph"  // Update the link to match your Flask endpoint
            icon="fas fa-users"
          />
        </div>
        <Route path="/api/scrape" component={ScrapeUserData} />
        <Route path="/api/existing" component={CheckUserExists} />
        <Route path="/api/clear" component={ClearMongoCollection} />
        <Route path="/api/compare" component={CompareRepoSimilarity} />
        <Route path="/api/similarity" component={CheckRepoSimilarity} />
        <Route path="/api/graph" component={DisplayGraph} />
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
