# PopularTorrentBot

**NOTE: The services that are part of this project are no longer live. If you with to use them you'll have to host them yourself :smiley:**

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

You can use the bot by adding [@ptorrentsbot](https://telegram.me/ptorrentsbot) as a contact on Telegram.


## How to run the bot

This repository contains 3 different projects:

- The database service
- The torrent service
- The telegram bot

These are executed as standalone applications, and can communicate freely among themselves. 

To run them you'll first of all need to install the dependencies by running from the root of the reporsitory:

```
pip install -r requirements.txt
```

Then you'll need to get the appropiate keys for each of the services and add them to the `keys example.py` file. Then rename 
this file to just `keys.py`. Note that for Pastebin you can define multiple keys, although this is not required, only 
one key will still work fine (however, the `PASTEBIN_KEYS` variable should be left as a _List_ of _Dicts_)

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


#### To build the documentation 

*Note: it will be built in the `docs` folder, in the root of the project*

```
cd doc_sphinx
make html
```
