
import urllib.request as urlrq
import certifi
import ssl

resp = urlrq.urlopen("https://www.calendar.auckland.ac.nz/en.html", context=ssl.create_default_context(cafile=certifi.where()))


html_bytes = resp.read()
a = str(html_bytes)
print(a)
