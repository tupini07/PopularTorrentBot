# PopularTorrentBot

Documentation can be seen here: [https://tupini07.github.io/PopularTorrentBot](https://tupini07.github.io/PopularTorrentBot)

PopularTorrentBot is a simple telegram bot that tells you which are the most popular torrents for a given date. 
It will give you information on a series of categories of torrents. These are:

- movies
- TV-series
- software
- ebooks
- music
- games
- all

This bot was created as the final project for the course 
of [Introduction to Service Design and Engineering](https://sites.google.com/unitn.it/introsde2018-19) course at UNITN.

If the categorie is either movie or TV-series then the bot will also fetch the relevant 
information from IMBD (by using the excelent [OMDb API](http://www.omdbapi.com/) service), and shows it to you.

As mentioned above, OMDb API is used to fetch movie/tv-series information. For the torrent information we 
use the [torrentapi](https://torrentapi.org/apidocs_v2.txt) service. And for saving informaiton we use a mix of a 
local database in SQLite and [Pastebin](http://pastebin.com/). In Pastebin we store the bulk of the data 
and in the database we just store key value pairs, where the key is composed of the date + category, and the value 
is a pastebin URL. In this way, when we get asked for information on a category for a specific date we can just pull 
the data from Pastebin.

You can use the bot by adding [@ptorrentsbot](https://telegram.me/ptorrentsbot) as a contect in Telegram.


## How to run the bot

This repository contains 3 different projects:

- The database service
- The torrent service
- The telegram bot

These are executed as standalone applications, and can communicate freely between themselves. 

To run them you'll first of all need to install the dependencies by running from the root of the reporsitory:

```
pip install -r requirements.txt
```

Then you'll need to get the appropiate keys for each of the services and add them to the `keys example.py` file. Then rename 
this file to just `keys.py`. 

Then you just need to run each of the applications. 

#### For the torrent service 

```
cd torrent_service
python t_main.py
```

#### For the database service

```
cd database_service
python db_main.py
```

#### For the telegram bot

```
cd bot_interface
python bot_main.py
```





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
