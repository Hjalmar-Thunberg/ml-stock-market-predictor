# Stock Market Predictor

ML system used to predict closing prices for specified stock.



## Developers <a name="developers"></a>

- [Kardo Marof](https://git.chalmers.se/kardo)
- [Christian O'Neill](https://git.chalmers.se/oneillc)
- [Hjalmar Thunberg](https://git.chalmers.se/hjathu)
- [Hugo Hempel](https://git.chalmers.se/hugohe)

### Group 3 --- Week 1 (7-14 Nov)
Planning week

### Group 3 --- Week 2 (14-21 Nov)
<hr />

> Delegated to: Christian
- Create GitLab templates
- Create logger component placeholder file
- Add logging methods for events to a specified database
- Add timestamps and urgency values to logged events
- Add data cleaner component placeholder file

<br />

> Delegated to: Hjalmar
- Add dynamic support to fetcher (fetch data from different sources)
- Store fetched data and update already existing data in the database
- Create fetcher component placeholder file
- Add training to testing to LSTM prediction model
- Create prediction model 

<br />

> Delegated to: Hugo
- Update component diagram to include model database
- Create data handler component placeholder file
- Update component and architectural diagram to reflect the same aspects

<br />

> Delegated to: Kardo
- Initialize a frontend UI
- Initialize the Django backend
- Create the REST api to interact with the frontend

<br />

### Group 3 --- Week 3 (21-28 Nov)
<hr />

> Delegated to: Christian
- Update logger to resolve changed current working directory errors
- Verify data format for incoming data from the dirty data database

<br />

> Delegated to: Hjalmar
- Update fetcher component to be a class that can be imported
- Add logging to the fetcher component
- Create CSV file with stock symbols to fetch

<br />

> Delegated to: Hugo
- Update documentation for the prediction model
- Update variable naming and comments in the predcition model to follow convention and be more descriptive

<br />

> Delegated to: Kardo
- 

<br />

### Group 3 --- Week 4 (29-5 Dec)
<hr />

> Delegated to: Christian
- Convert reactjs frontend into typescript to allow graph to work properly
- Create axios component to allow API calls to backend
- Configure CORS headers in frontend and backend components
- Create ROOT_DIR variable in Logger.py that allows for simpler pathing to databases and root directories
- Add initial data cleaner class

<br />

> Delegated to: Hjalmar
- Add store functionality to prediction models for
- Finish fetcher component README
- Add visual progress bar when fetching data

<br />

> Delegated to: Hugo
- Update prediction model with added metrics and accuracy calculation method.
- update parameters for LSTM model for higher accuracy

<br />

> Delegated to: Kardo
- 

<br />

### Group 3 --- Week 5 (6-12 Dec)
<hr />

> Delegated to: Christian
- Remake prediction model to a fully working trainer class
- Assist with database and data folder pathing in fetcher, cleaner, trainer components
- Update trainer to return captured values for accuracy, predictions, and real values

<br />

> Delegated to: Hjalmar
- Add fetching for one and all stored stocks to fetcher component
- Remake prediction model to a fully working trainer class
- Add cleaning for one and all stored stocks to cleaner component
- Fixed imports and structures for project to work for the pipeline
- Add readme to trainer and cleaner components
- Add getter to cleaner so trainer can get prepared data to train on

<br />

> Delegated to: Hugo
- Debbugging and general fixes added to fetcher, logger and cleaner (mainly sqlite3 threaded issue and general if/else logic)
- Update dependencies in backend to support django 4.0
- Add functionality to api calls in backend
- Update pipenv lockfile with correct and up-to-date dependencies

<br />

> Delegated to: Kardo
- 

<br />

### Group 3 --- Week 6 (13-19 Dec)
<hr />

> Delegated to: Christian
- Update trainer component to make it more flexible (not instantiate it with a number of nodes)
- Update trainer component to return model accuracy, predictions, and the actual closing values
- Add helper functions to get model data (version, accuracies, predictions, amount of nodes, etc.)
- Create UI using the django framework (due to issues with CORS), includes text-views for model data, dropdown for available models to predict with, and a graph to compare predicted vs actual close prices.
- Add file that keeps track of current version of the models in use, and ability to add/update models to that file.

<br />

> Delegated to: Hjalmar
- Update component diagram
- Fix fetcher when adding new stock
- Create presentation for fair

<br />

> Delegated to: Hugo
- Update backend to work with django UI(update api endpoints, urls, methods)
- Add file that keeps track of current version of the models in use, and ability to add/update models to that file.

<br />

> Delegated to: Kardo
- 

<br />
