# PopularTorrentBot

Telegram bot that gives you information on the most "shared" torrents by country

External services used:
- Torrent Information: https://iknowwhatyoudownload.com/assets/docs/ContentAPI.html
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

- If the :mediatype is either `movie` or `tv show` then it's information will be obtained from IMDB

/locations

    supported countries 

/locations/:country

    Top items of all media types for the specified country

/locations/global

    Top items of all media types globally. We treat global as a special country

/locations/:location/types

    List of media type of which we have information for the specified location

/locations/:country/types/:mediatype

    Top items of :mediatype for the specified country


/locations/global/types/:mediatype

    Top itemos of :mediatype globally
