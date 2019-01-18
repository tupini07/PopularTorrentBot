Torrent Service Documentation
=============================

The torrent service is quite simple. It gets information from ``http://torrentapi.org/`` 
for a specific category (or all categories at once). This returns an array of *torrents* 
which is sorted by ``seeds`` (meaning those that are being shared the most). The service gets 
the top 7 of these and processes them into a formated dictionary, see 
`GET /categories/(category) <#get--categories-(category)>`_ for an example. The service then 
returns these as a list of ``JSON`` objects to the user.

While processing the torrents, if one is encountered that has category of ``movies`` or of 
``TV-series`` then the service will automatically ask ``http://www.omdbapi.com/`` for extra 
information about them (once again, see `GET /categories/(category) <#get--categories-(category)>`_
for an example). This extra information will be added to the respective JSON object and will be 
sent with the data as part of the response.



Required Authentication
***********************

Anyone can consume the torrent service without need of authentication. However, the torrent service 
does need to authenticate with both ``http://torrentapi.org/`` and ``http://www.omdbapi.com/``.

``http://www.omdbapi.com/`` requires one to sign up and obtain an API key which we just need to send
with every request we make as part of the request parameters. 

For ``http://torrentapi.org/`` we ask for a token programatically. This token expires after a certain 
period of time so we need to monitor that it is still valid and renew it if needed. For torrentapi we 
also need to specify an application name which authenticates us with the service.



Endpoint Reference Table
************************

.. qrefflask:: t_main:app
   :undoc-static:

Endpoint Documentation
**********************

.. autoflask:: t_main:app
   :undoc-static: