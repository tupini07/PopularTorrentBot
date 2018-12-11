# PopularTorrentBot

Telegram bot that gives you information on the most "shared" torrents by country

External services used:
- Torrent Information: 
  - https://iknowwhatyoudownload.com/assets/docs/ContentAPI.html
  - https://github.com/Yuuyuuei/Torapi
- Access to IMDB data: http://www.omdbapi.com/
- Pastebin to publish results: https://pastebin.com/api

https://python-telegram-bot.org/


## Notes:

Remember to implement database as a separate service. Could use the following structure. 

- bot
- server
- database

Hosting can be done like this:

- telegram bot on raspberry pi
- database on pythonanywhere
- server (all the rest) of heroku


## Questions:

- Output of project, besides the live version, should we also provide a VM/docker (which)?
- What should the report contain?


## Idea for structure

### For main part:

- If the :mediatype is either `movie` or `tv show` then it's information will be obtained from IMDB

`/locations`

    supported countries 

`/locations/:country`

    Top items of all media types for the specified country

`/locations/global`

    Top items of all media types globally. We treat global as a special country

`/locations/:location/types`

    List of media type of which we have information for the specified location. This is actually
    hardcoded depending on the different API suppert (country || global)

`/locations/:country/types/:mediatype`

    Top items of :mediatype for the specified country.
    If :mediatype is movie or tv show then here we fetch information from IMDB

`/locations/global/types/:mediatype`

    Top itemos of :mediatype globally
    If :mediatype is movie or tv show then here we fetch information from IMDB


### For database:

Note that database only saves references (to save space). Actual data is stored in pastebin.com . Also note that 
actual number of pastebin keys needs to be calculated. We want to enforce the 10 posts per day limit directly
in the service.

`/records`

    returns all the dates of which we have a record. Note that records are only saved on the days in which a user
    makes a request. 

`/records/:date/categories`

    returns all the categories that we have in record for the specified date. 
    The :date is the specific day we're talking about. it is given in yyyy-mm-dd format

    404 if :date doesn't exist

`/records/:date/categories/:category`

    Returns the information we have about :category for the specified :date
    Need to handle:
        - unexisting date
        - unexisting category

`POST /record/:date/categories`

    {type: :category, content: :content} 

    creates a new entry in the database for the {:type} category for the specified :date
    If :date does not exist then it is created. 


### For documentation:

Just add to `gh-pages` . Separate documentation for each service (in separate pages).
Also include documentation for *non-API* stuff.