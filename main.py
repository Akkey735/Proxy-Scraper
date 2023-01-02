import os
import sys
import time
import httpx # pip install httpx
import colorama # pip install colorama
import pyfiglet # pip install pyfiglet
import threading
from bs4 import BeautifulSoup # pip install beautifulsoup

colorama.init(convert=True)

raw_proxy_link = [
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http',
    'https://openproxylist.xyz/http.txt',
    'https://proxyspace.pro/http.txt',
    'https://proxyspace.pro/https.txt',
    'https://raw.githubusercontent.com/almroot/proxylist/master/list.txt',
    'https://raw.githubusercontent.com/andigwandi/free-proxy/main/proxy_list.txt',
    'https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt',
    'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
    'https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/http.txt',
    'https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/https.txt',
    'https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt', 
    'https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt',
    'https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt',
    'https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt',
    'https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt',
    'https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt',
    'https://raw.githubusercontent.com/proxylist-to/proxy-list/main/http.txt',
    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt',
    'https://raw.githubusercontent.com/rx443/proxy-list/main/online/http.txt',
    'https://raw.githubusercontent.com/rx443/proxy-list/main/online/https.txt',
    'https://raw.githubusercontent.com/saisuiu/uiu/main/free.txt',
    'https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt',
    'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxy-list/data.txt',
    'https://api.openproxy.space/lists/http'
]

normal_proxy_link = [
    "https://free-proxy-list.net/"
]

scraped_proxies = []
title_thread = True

class ScrapeNormalProxies():
    def __init__(self):
        pass

    def free_proxy_list_net_parse(self, html_src):
        soup = BeautifulSoup(html_src, "html.parser")
        return soup.find(class_="form-control").text.split("\n")

    def scrape_normal_proxies(self):
        for proxy_link in normal_proxy_link:
            response = None
            try:
                response = httpx.get(proxy_link)
            except:
                print(colorama.Fore.RED + "Error: " + proxy_link + colorama.Fore.RESET)
                continue
            if proxy_link == "https://free-proxy-list.net/":
                proxies = self.free_proxy_list_net_parse(response.content)
                for proxy in proxies:
                    if proxy in scraped_proxies:
                        continue
                    elif proxy == "" or proxy == " ":
                        continue
                    elif not proxy.replace("\n", "").replace("\r", "").replace(":", "").replace(".", "").isnumeric():
                        continue
                    scraped_proxies.append(proxy.replace("\n", "").replace("\r", ""))
            else:
                pass

def scrape_raw_proxies():
    global scraped_proxies
    proxies = []
    for proxy_link in raw_proxy_link:
        response = None
        try:
            response = httpx.get(proxy_link)
        except:
            print(colorama.Fore.RED + "Error: " + proxy_link + colorama.Fore.RESET)
            continue
        if response.status_code != 200:
            print(colorama.Fore.RED + "Error: " + proxy_link + colorama.Fore.RESET)
            continue
        proxies = response.text.split("\n")
        if "api.openproxy.space" in proxy_link:
            proxies = []
            for data_obj in  response.json()["data"]:
                for proxy in data_obj["items"]:
                    proxies.append(proxy)
        for proxy in proxies:
            if proxy in scraped_proxies:
                continue
            elif proxy == "" or proxy == " ":
                continue
            elif not proxy.replace("\n", "").replace("\r", "").replace(":", "").replace(".", "").isnumeric():
                continue
            scraped_proxies.append(proxy.replace("\n", "").replace("\r", ""))

def update_title():
    while title_thread:
        os.system(f"title Proxy Scraper / Scraped: {len(scraped_proxies)}")
    return

def main():
    global title_thread
    os.system("title Proxy Scraper")
    print(colorama.Fore.CYAN + pyfiglet.figlet_format("Scraper") + colorama.Fore.RESET)
    time.sleep(5)
    threading.Thread(target=update_title).start()
    time.sleep(1)
    print(colorama.Fore.GREEN + "Scraping..." + colorama.Fore.RESET)
    scrape_raw_proxies()
    normal_proxy_scraper = ScrapeNormalProxies()
    normal_proxy_scraper.scrape_normal_proxies()
    with open("proxies.txt", "w", encoding="utf-8") as file:
        file.write("{0}".format("\n".join(scraped_proxies)))
    print(colorama.Fore.GREEN + "Scraped: " + colorama.Fore.YELLOW + str(len(scraped_proxies)) + colorama.Fore.RESET)
    title_thread = False
    time.sleep(5)

if __name__ == "__main__": # Determine if it is not called as a library
    main()
    sys.exit()
else:
    print("It cannot be called and used as an external file.")
    sys.exit()