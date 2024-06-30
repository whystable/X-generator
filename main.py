import config
import requests
import json
import re
import hashlib
import hmac
import secrets

def generate_key(length):
    secret_key = secrets.token_bytes(16)
    random_message = secrets.token_bytes(32)
    hmac_hash = hmac.new(secret_key, random_message, hashlib.sha256).hexdigest()
    new_key = hmac_hash[:length]
    return new_key

token_counter = 0
url = 'https://x.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
proxy_type = config.proxy_type.lower()

if proxy_type == "socks5":
    if config.proxy_user and config.proxy_pass:
        proxy = f"socks5://{config.proxy_user}:{config.proxy_pass}@{config.proxy_ip}:{config.proxy_port}"
    else:
        proxy = f"socks5://{config.proxy_ip}:{config.proxy_port}"
elif proxy_type == "http":
    if config.proxy_user and config.proxy_pass:
        proxy = f"http://{config.proxy_user}:{config.proxy_pass}@{config.proxy_ip}:{config.proxy_port}"
    else:
        proxy = f"http://{config.proxy_ip}:{config.proxy_port}"
else:
    raise ValueError("Unsupported proxy type: " + proxy_type)

proxies = {
    "http": proxy,
    "https": proxy
}

LOGO = '''
██╗░░██╗  ████████╗░█████╗░██╗░░██╗███████╗███╗░░██╗  ░█████╗░██╗░░██╗███████╗░█████╗░██╗░░██╗███████╗██████╗░
╚██╗██╔╝  ╚══██╔══╝██╔══██╗██║░██╔╝██╔════╝████╗░██║  ██╔══██╗██║░░██║██╔════╝██╔══██╗██║░██╔╝██╔════╝██╔══██╗
░╚███╔╝░  ░░░██║░░░██║░░██║█████═╝░█████╗░░██╔██╗██║  ██║░░╚═╝███████║█████╗░░██║░░╚═╝█████═╝░█████╗░░██████╔╝
░██╔██╗░  ░░░██║░░░██║░░██║██╔═██╗░██╔══╝░░██║╚████║  ██║░░██╗██╔══██║██╔══╝░░██║░░██╗██╔═██╗░██╔══╝░░██╔══██╗
██╔╝╚██╗  ░░░██║░░░╚█████╔╝██║░╚██╗███████╗██║░╚███║  ╚█████╔╝██║░░██║███████╗╚█████╔╝██║░╚██╗███████╗██║░░██║
╚═╝░░╚═╝  ░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝  ░╚════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
                                            github.com/whystable'''
print(LOGO)

with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(f'''╭━╮╭━╮╱╭━━━┳━━━┳━━━┳━━━┳━━━┳━━━╮
╰╮╰╯╭╯╱┃╭━╮┃╭━╮┃╭━╮┃╭━╮┃╭━━┫╭━╮┃
╱╰╮╭╯╱╱┃╰━╯┃┃╱┃┃╰━╯┃╰━━┫╰━━┫╰━╯┃
╱╭╯╰┳━━┫╭━━┫╰━╯┃╭╮╭┻━━╮┃╭━━┫╭╮╭╯
╭╯╭╮╰┳━┫┃╱╱┃╭━╮┃┃┃╰┫╰━╯┃╰━━┫┃┃╰╮
╰━╯╰━╯╱╰╯╱╱╰╯╱╰┻╯╰━┻━━━┻━━━┻╯╰━╯\n''')
    f.write(f'================================\n')

token_count = int(input("How many tokens to generate: "))

while token_counter < token_count:
    cookies = {
        'auth_token': generate_key(43)
    }

    response = requests.get(url, headers=headers, cookies=cookies, proxies=proxies)
    data = response.text
    json_data = re.search(r'window\.__INITIAL_STATE__=(\{.*?\});', data, re.DOTALL)
    if json_data:
        json_str = json_data.group(1)
        initial_state = json.loads(json_str)
        users = initial_state['entities']['users']['entities']
        first_user_id = next(iter(users))
        first_user_data = users[first_user_id]
        is_blue_verified = first_user_data['is_blue_verified']
        screen_name = first_user_data['screen_name']
        name = first_user_data['name']
        normal_followers_count = first_user_data['normal_followers_count']
        token = cookies.get('auth_token')

        with open('output.txt', 'a', encoding='utf-8') as f:
            f.write(f'Token: {token}\n')
            f.write(f'Username: {screen_name}\n')
            f.write(f'Name: {name}\n')
            f.write(f'Is Verified: {is_blue_verified}\n')
            f.write(f'Followers: {normal_followers_count}\n')
            f.write('================================\n')  # Добавляем пустую строку для читаемости или разделения

        print(f'Token: {token}')
        print(f'Username: {screen_name}')
        print(f'Name: {name}')
        print(f'Is Verified: {is_blue_verified}')
        print(f'Followers: {normal_followers_count}')
        print("================================")
        token_counter += 1
    else:
        token = cookies.get('auth_token')
        print(f'Token invalid: {token}')
