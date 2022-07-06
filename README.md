# Trip Planner Project
Hello examiners! This is our final project for our cs-degree.
Do you ever want to just go abroad and have a fun time, but then are suddenly reminded that you need to meticulously plan the entire thing, everything from hotels to stay in to attraction to visit and up until forms of transportation and flights?
Well, we have got you covered!
Our project's goal is to ease the process of trip planning for the user by automating it in its entirety!
All the user has to do is enter which airport he wants to depart from, where does he want to fly to and how long for. We will do the rest!
Optionally, the user can enter additional criteria to specialize the trip in his own way, such as wether or not he is on a budget, and so on.
We believe this can tremendously help spontaneous people who can't be bothered to plan their entire vacation, but would rather just go right ahead and experience it instead.
## The Code
Our code is seperated into two segments:
The front end and the backend + algo itself.
The front end is written in react, while the backend is written in flask.
The backend also has all the api calls to the external api from which we obtain the information used for our trips.
The backend also accesses our mongodb database for user login information as well as for saved trips information.
The algorithm itself was written in python.
### The Backend Code
* The backend has a few classes all in place to do different things.
* The Flights class is in charge of getting flights by locations.
* The transportFunctions class is in charge of gettings the public transport information to move from point A to point B.
* The hotelFunctions class is responsible for getting the attractions as well as the hotels required for the algo.
* In addition, we have the classes we use to store the information regarding the trip itself in the classes file which contains the placeOfStay class, the Transport class, the Attraction class, the day class and the Trip class.
* Lastly, in the tripAlgo file we use all of this classes to get a trip given the user inputs.
* Additionally, it implements a mechanism to adjust the transportation for the case where the attractions are moved around.
### The Frontend Code
* The frontend has a file for each of the pages the user is able to access.
* There are many pages the user can access and they are categorized.
* I guess that is about it.
#### Link to our project video:
* https://drive.google.com/file/d/1UDJD9EDs37DCoIYAK_4gPGTa8Nn3HTMs/view?usp=sharing
#### Link to our promotional video:
* https://drive.google.com/file/d/1EeEb7B4zlM9Syy5RR3nWLZrX7FGMu4ay/view?usp=sharing
#### Link to our jira:
* https://biubarilan.atlassian.net/jira/software/projects/TEAM/boards/1
