# https://api.antitor.com/content/downloads?day=2018-10-20&key=54ac65d28c8f4c179d409967f4dbf052
import rarbgapi

a = rarbgapi.RarbgAPI()

# r = a.list(sort="seeders", format_="json_extended")
             
r = a.list(sort="seeders", format_="json_extended", category=a.CATEGORY_MOVIES_ALL)             
# r = a.list(sort="seeders",format_="json_extended")
# [print(x.filename + " " + x.category + " " + str(x.seeders) + ) for x in r] 
[print(x) for x in r]


# r[0]._raw

{'title': 'Replicas.2018.1080p.HC.WEBRip.x264.AAC2.0-STUTTERSHIT',
 'category': 'Movies/x264/1080',
 'download': 'magnet:?xt=urn:btih:25e895a70849dbba683e6e8b97a9aa72567b32bf&dn=Replicas.2018.1080p.HC.WEBRip.x264.AAC2.0-STUTTERSHIT&tr=http%3A%2F%2Ftracker.trackerfix.com%3A80%2Fannounce&tr=udp%3A%2F%2F9.rarbg.me%3A2710&tr=udp%3A%2F%2F9.rarbg.to%3A2710&tr=udp%3A%2F%2Fopen.demonii.com%3A1337%2Fannounce',
 'seeders': 4163,
 'leechers': 684,
 'size': 2862888589,
 'pubdate': '2018-12-22 17:50:21 +0000',
 'episode_info': {'imdb': 'tt4154916',
                  'tvrage': None,
                  'tvdb': None,
                  'themoviedb': '300681'},
 'ranked': 1,
 'info_page': 'https://torrentapi.org/redirect_to_info.php?token=yszx8qnwkm&p=1_7_2_1_2_7_1__25e895a708'}
