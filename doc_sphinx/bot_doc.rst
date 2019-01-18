Telegram Bot Documentation
==========================

The telegram bot creates the interface that the user will interact with and is also in 
charge of integrating the different services (as can be seen in the :ref:`ApplicationStructure` section.

When asked for the most popular torrents of a category, on a specific date, this application will
first of all ask the database service to see if we have a record, if yes then we just fetch it and
return that to the user. If no record exists then the data is fetched from the Torrent service 
(only if the requested date it *today*, if not an error message is displayed to the user), after
obtaining this data it is sent over to the database service so that it can be saved. Finally it is 
displayed to the user.


Required Authentication
***********************

The bot module needs to authenticate with the Telegram API by using an API key, which 
is provided when signing up as Telegram developer. 



Bot Functions Documentation
****************************

.. automodule:: bot_helper
    :members: 
    :undoc-members:
    :show-inheritance:

