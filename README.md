# Whats this???
A course I do done to help learn more about blockchain and react. 

The emphasis of this course was to get into the code required to build a basic blockchain and display it using a UI.

A lot of the code and conventions here may not be production ready i.e. the flask app is all one page and UI styling is minimal, 
but these were not priorities here.

## Backend
### Run the application and API
Create and activate virtual env
Install requirements.txt

### Create virtualenv and install requirements
```
source venv/bin/activate
pip3 install -r requirements.txt
```

Using cli navigate to backend
```
cd /<path>/<to>/<project>/backend
```
Run the backend
```
python -m api.app
``` 
### Start backend with seededData
```
export SEED=True
python -m api.app
```
### set up pubsub 
You will have to signup to [pubsub](https://cloud.google.com/pubsub/docs/overview) and get you subscribe and publish keys

Export as env variables before running the app
```
export subscribe_key='<my_subscribe_key>'
export publish_key='<my_publish_key>'
```

### Run a peer instance

```
export PEER=true
python -m api.app
```

### Testing
All backend tests are in backend/tests/*
I have used unittest and pytests for different tests.
Why??? Because I felt like it and this project isnt focused on tests but they are important to catch any breaking changes
Really I started in unittest but decided to change to pytest to learn something different
Also please note, not all tests are exactly how I was test. They are based off the course material and are sufficient for this learning

## Frontend

### Start front end

Go to front end directory and run start command

```
cd <path to project>/frontend
npm install
npm run start
```

Open browser on [http://localhost:3000/](http://localhost:3000/)
