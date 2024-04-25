# gitcomp

Gitcomp is a Python program that takes user input while connected to a MongoDB server to scrape and store data from GitHub pages for comparison. The goal was to make this app scalable so that more functionalities could easily be added to it. This tool uses the Beautifulsoup package to scrape the repository names and contributions in the last year.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Installation
### necessary packages
```bash
mognod -version
```
### install files
```bash
git clone https://github.com/Ajmccrory/gitcomp.git
cd gitcomp
pip3 install requirements.txt
```
## Operation
### Start MongoDB server
```bash
sudo systemctl start mongod
sudo systemctl status mongod
# do this to verify server is running
```
### In a new window in the program directory
```bash
mongosh # to connect to mongodb server on port 27010
python3 gitcomp.py
```

## Contributing
If you want others to contribute to your project, provide guidelines for how they can do so. This might include:

1. Fork the repository
2. Create a new branch (git checkout -b feature)
3. Make your changes
4. Commit your changes (git commit -am 'Add new feature')
5. Push to the branch (git push origin feature)
6. Create a new Pull Request



