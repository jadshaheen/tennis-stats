TEST TEST TEST
Practicing making a basic python web application.

The end goal is to have a basic website UI that will allow users to enter years, names of players, or names of tournaments and get relevant Grand Slam information for the provided entity. There should be a backend which reads and processes this data from espn.com, and a frontend which makes an API request to the backend to retrieve the data associated with the user input and then displays it on the webpage.

STEP 1: Cretae a python module that can read data from espn.com/tennis/rankings and espn.com/tennis/history.
Planned ETA: 8/31/22
COMPLETED as of 9/1 12:11 AM PDT

STEP 2: Create a flask app with the ability to serve HTTP requests getting the various player, tournament, and year data.
Planned ETA: 9/1
COMPLETED as of 9/1 1:05 AM PDT

STEP 3: Convert flask app output to json data like the response of a typical modern industry API.
Planned ETA: 9/1
COMPLETED as of 9/1 1:52 AM

STEP 4: Build skeleton frontend (react?) which is capable of sending HTTP requests to the flask app.
Planned ETA: 9/3
COMPLETED s of 9/6 12:25 PM

STEP 4.5: Switch to a more object-oriented approach. Have Player objects storing relevant player information, instead of constructing ungodly maps of maps of maps.
STEP 4.25 create a types.py to house the structs that will power the above.

STEP 5: Prettify frontend to have input field and look decent.
Planned ETA: 9/5

player output should look like following:

	PLAYER NAME is currently (ranked x in the world / not ranked)
	GRAND SLAM STATS
	grand slam | finals appearances | wins | losses
	wimbledon  | value              | value| value
	australian | value              | value| value
	french open| value              | value| value
	us open    | value              | value| value


STEP 6: Productionize flask app and add frontend as a page on jadshaheen.com.
Planned ETA: 9/7

ADD TO THIS FILE UPON COMPLETION OF EACH STEP, WITH COMPLETION DATE AND DESCRIPTION OF THE NEXT STEP

LIVE! at jadshaheen.com/tennis as of Wednesday, September 21 2022 at 3:30 PM PST
