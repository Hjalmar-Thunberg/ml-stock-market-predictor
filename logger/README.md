# Logger Component
### Description
The logger is a component that will attach to any other component manipulating data or handling event. It's primary objective is to log these manipulations, events, and potentially anything else of importance. This is necessary for debugging more complex systems as it allows the user to navigate readable logs where they design the message, urgency, etc.
### Requirements
1. The logger needs to store the log files separately for each component to make traceability and readability more available to the user.
2. The log files themselves should be named after the component they are attached to. For example, a component that scrapes web data (aptly named Scraper), should have it's log files stored in some variation of "logs_scraper.db".
3. The log files will be stored in a SQLite database, where the read and writes are handled by the sqlite3 library.
4. These log files shall be stored in a central location such as a "logs" folder in the repository/project root directory.
5. The logger shall provide the user with a variety of urgencies to log their messages with such as None, Mild, Severe.
### How to use
1. Import the Logger into the desired component.
2. Create the Logger instance
```python
logger = Logger('logs_myComponentName.db')
```
3. On methods where data is being manipulated, or exceptions are expected, add the following line:
```python
logger.log(
    message="My message to be logged",
    urgency=logger.urgency.NONE|LOW|MODERATE|HIGH|SEVERE # This parameter defaults to logger.urgency.NONE
    )
```
4. When the logger is done, to preserve resources call:
```python
logger.close()
```
