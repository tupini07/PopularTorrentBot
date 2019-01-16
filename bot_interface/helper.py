import requests
import sys

sys.path.insert(0, '..')
import config

# The torrent service shouldn't talk with the database service. 
# The bot is the one that consumes both services and is the one that should integrate them