import multiprocessing
from multiprocessing import Pool
import time
import asyncio
import aiofiles
import requests
import os


# Settings
PATH_TO_PROXIES = "proxies_2.txt"
SITE_TO_CHECK_PROXY = "https://icanhazip.com/"
OUT_PATH = "work_proxies.txt"
TIMEOUT = 2
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}


async def write_to_file(proxy):
    async with aiofiles.open(OUT_PATH, 'a') as file:
        await file.write(proxy+'\n')


def handler(proxy):
    try: 
        proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}",
        }
        resp = requests.get(SITE_TO_CHECK_PROXY, proxies=proxies, headers=HEADERS, timeout=TIMEOUT)
        asyncio.run(write_to_file(proxy))
        print(f'[+] {proxy} -- valid')
    except:
        print(f'[-] {proxy} -- invalid')


async def get_proxy_list(path):
    async with aiofiles.open(path, 'r') as proxy:
        proxies = await proxy.readlines()
    return list(map(lambda proxy: proxy.replace('\n', ''), proxies))


def check_files(path):
    if os.path.exists(path):
        os.remove(path)


def main():
    start = time.time()

    proxies = asyncio.run(get_proxy_list(PATH_TO_PROXIES))

    check_files(OUT_PATH)

    with Pool(multiprocessing.cpu_count()*3) as pool:
        pool.map(handler, proxies)

    end = time.time()
    print(f'[?] Execution time: {end-start}')


if __name__ == "__main__":
    main()
