import urllib.request
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
req = urllib.request.Request('https://www.rotowire.com/baseball/daily-lineups.php', headers=headers)
with urllib.request.urlopen(req) as response:
   print(response.getcode())
   print(response.read()[:500].decode('utf-8'))
