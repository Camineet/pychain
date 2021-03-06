Thanks for taking a look at my blockchain project from my recent coursework. This app is from a [course](https://www.udemy.com/course/python-js-react-blockchain/) I took by David Katz after doing a Python bootcamp. I took this course and have linked the project on my CV to show that I can learn new tech stacks and also to show that if given new opportunities to do so, I will enthusiastically dive in and gain competency with which to serve.

As with many projects that are built in Udemy courses, this app is just a code-along where you build it component by component along with the instructor through the videos in the course. It certainly isn't my engineering design. David Katz is a highly skilled Silicon Valley developer, and there's a big difference in what he and I can create. But with a lot of effort, I did understand everything in the many modules as I built them. 

As simplistic as it looks, this app is actually a working blockchain and cryptocurrency with the usual functionalities of:

 - Block Mining with Proof of Work
 - Difficulty Adjustment
 - Transactions
 - Transaction Validation
 - Block Validation
 - Chain Validation

**Block Mining with Proof of Work**

Here is the ```mine_block()``` function inside of the ```block.py``` module found in ```backend/blockchain``` which performs proof of work and mines a block.

![](screenshots/mine_block().PNG)

You can see in the call to the ```crypto_hash()``` function that the usual data is used to create the hash for the newly mined block, including a timestamp, the previous block's hash, the current difficulty, a nonce, and the data (a transaction pool) to be recorded in the block. The ```mine_block()``` function calls the ```crypto_hash()``` function until a hash is created which has a count of leading zeroes matching the current difficulty level.

The ```crypto_hash()``` function utilizes the Python hashlib module's ```sha256()``` function to cryptographically derive a hash from the given inputs as seen here.

![](screenshots/crypto_hash().PNG)

More code walkthrough coming soon!

**Activate the virtual environment**

```
source blockchain-env/Scripts/activate
```
**Install all packages**

```
pip install -r requirements.txt     
```
**Run the tests**

Make sure to activate the virtual environment

```
python -m pytest backend/tests    
```
**Run the application and API**

Make sure to activate the virtual environment

```
python -m backend.app    
```

**Run a peer instance**

Make sure to activate the virtual environment

```
export PEER=True && python -m backend.app    
```

**Run the frontend**

In the frontend directory:
```
npm run start    
```

**Seed the backend with data**

Make sure to activate the virtual environment


```
export SEED_DATA=True && python -m backend.app    
```
