# JPP
## Japanese Pronunciation Pro

JPP is a website host to a set of tools intended to help Japanese learners of all levels develop their Japanese pronunciation skills. The systems will include:

- a self-testing system intended to help students identify and fix inaccuracies in pronunciation, either of the syllables themselves, or the pitch accent of a word.

- generally helpful information about Japanese pronunciation (ie. 2+2 kanji rule, -3 katakana rule, etc.) that can be further expanded in the future if needed by Japanese professors with relative ease in an easily navigable format. Might open the possibility of adding pages for grammar lessons, etc. as needed.

- if time permits, a kanji recognition system for learning how to write/memorize certain kanji (Japanese characters) as a reach goal. This will essentially be a flash card-esque page where the page will provide the reading of each character, and the user must write the character. It will either flag it as correct or incorrect and notify the user as such.


## Why JPP?

The reason for wanting to design and create such a project is because pitch accent is often a neglected part of most Japanese language programs, even in large scale institutions with strong Japanese departments such as Yale. While resources that help explain the Japanese pronunciation patterns exist, they are often obfuscated and inaccessible to the average Japanese language learner. To resolve this issue, we want to create a website that has all this information readily available, and also create a framework for the professors to easily update or append information as needed. In the future, we hope the website can be a one-stop hub for all things related to learning Japanese, although the scope for this project will likely be set on solely pronunciation due to time constraints.

## Deliverables
### Sound Analysis
- [ ] Voice isolation
- [ ] Mora (syllable) breakdown
- [ ] Obtain pitch information/mora length/other information necessary for our grading algorithms
- [ ] Output a corresponding grade in respect to input data

### Website Pages
- [ ] Kanji 1+2
- [ ] Kanji 2+1
- [ ] Kanji 2+2
- [ ] Chinese-originated words
- [ ] Compound nouns
- [ ] 外来語 (Foreign loan words)
- [ ] Dictionary form
- [ ] ます form
- [ ] Negative conjugations in dictionary form
- [ ] て・た form
- [ ] Names
- [ ] Generic pitch accent tips
- [ ] Pronunciation Test

# Getting Started
Note that the following instructions are for running the project locally, specifically intended for testing during the development phase.

Pull from the repository to ensure you have the latest version of the code before proceeding!

## Initial Setup for Dependencies
### Python Setup
Create your virtual environment inside of the api folder if it doesn't already exist.
```
python3 -m venv venv
```

Always source this virtual environment before proceeding with any testing.
```
source venv/bin/activate
```

To install the dependencies into your virtual environment, run:
```
pip install -r requirements.txt
```

### React/npm Setup
From the home directory, navigate to the react-flask-app folder.
```
cd react-flask-app
```

From there, install the dependencies specified in package-lock.json.
```
npm install
```

### Installing yarn/npm
If your operating system doesn't come with yarn or npm supported, you may need to install it. 
Yarn and npm will install to your local device.
```
sudo npm install -g npm
sudo npm install -g yarn
```
Note that the npm installation requires you to have Node.js already installed!

## Running Code
### Initialize API
To start the backend, run:
```
yarn start-api
```

### Start Frontend
To start the frontend, run:
```
yarn start
```
