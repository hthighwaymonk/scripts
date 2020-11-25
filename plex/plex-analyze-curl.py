# Plex analayze all files that are missing analyzation info using CURL calls
# OS: Ubunti 16.04 ( in case of other OS's make sure to change paths )
# Replace xxx with your plex token, you can get it by:
# grep -E -o "PlexOnlineToken=.{0,22}" /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Preferences.xml

#!/usr/bin/env python3
import sys
import requests
import sqlite3

folder=sys.argv[1]
conn = sqlite3.connect('/opt/plex/Library/Application Support/Plex Media Server/Plug-in Support/Databases/com.plexapp.plugins.library.db')

c = conn.cursor()
c.execute('select media_items.metadata_item_id from media_items Inner Join media_parts On media_parts.media_item_id=media_items.id where media_itemsbitrate is null AND media_parts.file LIKE '%folder%'')
items = c.fetchall()
conn.close()

print("To analyze: " + str( len(items) ))
for row in items:
        requests.put(url='http://127.0.0.1:32400/library/metadata/' + str(row[0]) + '/analyze?X-Plex-Token=xxx')
        requests.get(url='http://127.0.0.1:32400/library/metadata/' + str(row[0]) + '/refresh?X-Plex-Token=xxx')
        print(str(row[0]))
