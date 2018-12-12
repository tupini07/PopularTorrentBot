# PopularTorrentBot

Telegram bot that gives you information on the most "shared" torrents by country

External services used:
- Torrent Information: 
  - https://iknowwhatyoudownload.com/assets/docs/ContentAPI.html
  - https://github.com/Yuuyuuei/Torapi
- Access to IMDB data: http://www.omdbapi.com/
- Pastebin to publish results: https://pastebin.com/api

https://python-telegram-bot.org/

_____________

## Notes:

Remember to implement database as a separate service. Could use the following structure. 

- bot
- server
- database

Hosting can be done like this:

- telegram bot on raspberry pi
- database on pythonanywhere
- server (all the rest) of heroku

_____________

## Questions:

- Output of project, besides the live version, should we also provide a VM/docker (which)?
  - can do both
  - VM has no limit of space
  - If virtual machine then services should be accessible separately from localhost when they're launched inside the VM. 
    - there should also be a live version of the services online to test with postman

- Presentation is live demo
- What should the report contain?
  - explain all layers (we have data layer, business logic, process centric)
  - explain architecture (also include figure)
  - Not longer than 3 pages

_____________

## Idea for structure

### For Bot: 

Consume *main part* normally. Think about:

- adding a nice help message
- allow user to ask for data about previous dates that we have in database
  - possibly give the ability to ask for all dates for which we have data? 
- add a default `/today` command which returns best for all globally 

### For main part:

- If the :mediatype is either `movie` or `tv show` then it's information will be obtained from IMDB. 
- Note that a limit on the amount of items we get each query must be set. Possibly best 5, 10, or 15? This can also be parameterized and user can specify, by default we can leave 5


> `/locations`

    supported countries 
&nbsp;

> `/locations/:country`

    Top items of all media types for the specified country
&nbsp;

> `/locations/global`

    Top items of all media types globally. We treat global as a special country
&nbsp;

> `/locations/:location/types`

    List of media type of which we have information for the specified location. This is actually
    hardcoded depending on the different API suppert (country || global)

    remember to include `all` as a mediatype
&nbsp;

> `/locations/:country/types/:mediatype`

> `/locations/global/types/:mediatype`

    Top items of :mediatype for the (specified country || globally).
    If :mediatype is movie or tv show then here we fetch information from IMDB

    > add limit parameter, by default 5?
    > add only_name parameter, which doesn't return item description (only useful if :mediatype is `movie` or `tv show`)

### For database:

Note that database only saves references (to save space). Actual data is stored in pastebin.com . Also note that 
actual number of pastebin keys needs to be calculated. We want to enforce the 10 posts per day limit directly
in the service.

> `/records`

    returns all the dates of which we have a record. Note that records are only saved on the days in which a user
    makes a request. 
&nbsp;

> `/records/:date/categories`

    returns all the categories that we have in record for the specified date. 
    The :date is the specific day we're talking about. it is given in yyyy-mm-dd format

    404 if :date doesn't exist
&nbsp;

> `/records/:date/categories/:category`

    Returns the information we have about :category for the specified :date
    Need to handle:
        - unexisting date
        - unexisting category

    Will this return only the link to pastebin or will return everything + link to pastebin? (possibly the latter is best)
&nbsp;

> `POST /record/:date/categories`

    {type: :category, content: :content} 

    creates a new entry in the database for the {:type} category for the specified :date
    If :date does not exist then it is created. 


### For documentation:

Just add to `gh-pages` . Separate documentation for each service (in separate pages).
Also include documentation for *non-API* stuff.