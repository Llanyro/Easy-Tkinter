import aiohttp
import asyncio
from requests import get
from re import findall
from rx.core import Observer
from extralib import UrlCntroller
from rx import *


def p():
    print("p")


class UrlObserver(core.Observer):
    __list: list = []

    def on_next(self, v):
        self.__list.append(v)
        print(f'Recibido: {v}')

    def on_completed(self):
        print('Terminado')

    def get(self):
        return self.__list


def getUrls(url: str):
    dom, root = UrlCntroller.urlRootDom(url)
    r = get(url)
    urllist: list = findall("src=\"(.+?)\"", r.text)
    i: int = 0
    while i < urllist.__len__():
        if urllist[i].__contains__(".jpg") is False and urllist[i].__contains__(".png") is False:
            del urllist[i]
        else:
            i += 1
    return urllist, dom, root


async def test(url: str, u: str, root: str):
    async def func(o, s):
        print("Ha entrado")
        result = None
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    result = resp.content
        except:
            url2 = UrlCntroller.prepararUrl(url, u)
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url2) as resp:
                        result = resp.content
            except:
                url2 = UrlCntroller.prepararUrl(url, root)
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url2) as resp:
                            result = resp.content
                except:
                    pass
        o.on_next(result)
    create(await func).subscribe(urlob)


async def getAsync(u: str):
    urllist, dom, root = getUrls(u)
    for url in urllist:
        await test(url, u, root).subscribe(on_next=lambda t: p(), on_error=lambda e: print(e))


#print(getAsync("https://www3.animeflv.net/"))
urlob = UrlObserver()
loop = asyncio.get_event_loop()
loop.run_until_complete(getAsync("https://www3.animeflv.net/"))
print(urlob.get())


"""class UrlObserver(core.Observer):
    __list: list = []

    def on_next(self, v):
        self.__list.append(v)
        print(f'Recibido: {v}')

    def on_completed(self):
        print('Terminado')

    def get(self):
        return self.__list


def wtf(url: str, u: str, root: str, urlob: Observer):
    async def func(o, s):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    return resp.content
        except:
            url2 = UrlCntroller.prepararUrl(url, u)
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url2) as resp:
                        return resp.content
            except:
                url2 = UrlCntroller.prepararUrl(url, root)
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url2) as resp:
                            return resp.content
                except:
                    pass
    return create(func).subscribe(urlob)


async def getAsync(u: str, urlob: Observer):
    dom, root = UrlCntroller.urlRootDom(u)
    r = get(u)
    urllist: list = findall("src=\"(.+?)\"", r.text)
    i: int = 0
    while i < urllist.__len__():
        if urllist[i].__contains__(".jpg") is False and urllist[i].__contains__(".png") is False:
            del urllist[i]
        else:
            i += 1
    return await asyncio.gather(*(func(url, u, root, urlob) for url in urllist))


obs = UrlObserver()
loop = asyncio.get_event_loop()
print(loop.run_until_complete(getAsync("https://www3.animeflv.net/", obs)))
"""
"""
from bs4 import BeautifulSoup
html_page = get("https://www3.animeflv.net/").content
soup = BeautifulSoup(html_page, 'lxml')
images = []
for img in soup.findAll('img'):
    images.append(img.get('src'))
print(images)
"""
"""async def foo():
    await asyncio.sleep(1)
    return 42


def intervalRead(rate, fun) -> rx.Observable:
    loop = asyncio.get_event_loop()
    return rx.interval(rate).pipe(ops.map(lambda i: rx.from_future(loop.create_task(fun()))), ops.merge_all())


async def main(loop):
    obs = intervalRead(5, foo)
    obs.subscribe(on_next=lambda item: print(item), scheduler=AsyncIOScheduler(loop))

loop = asyncio.get_event_loop()
loop.create_task(main(loop))
loop.run_forever()
"""

