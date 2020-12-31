import codecs

import aiohttp
import asyncio
from requests import get
from re import findall
from rx.core import Observer
from extralib import UrlCntroller
from rx import create, from_list


"""def p():
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
"""
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


"""async def func(url: str, u: str, root: str, urlob: Observer):
    result = None
    urlfin = None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                result = resp
                urlfin = url
    except:
        url2 = UrlCntroller.prepararUrl(url, u)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url2) as resp:
                    result = resp
                    urlfin = url2
        except:
            url2 = UrlCntroller.prepararUrl(url, root)
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url2) as resp:
                        result = resp
                        urlfin = url2
            except:
                pass
    if result is not None:
        print(result.content.read())
        #result = await result.read()
        #data = await result.read()
        #print(data)
        #from_list([(urlfin, result)]).subscribe(urlob)
    return result


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


class Printer(Observer):
    def on_next(self, result):
        res = yield from result[1].read()
        print(res)
        #print("Recibido:", result[0], result[1])
        #self.__parent.addImage(result[0], result[1])

    def on_error(self, error: Exception) -> None:
        print(error)

    def on_completed(self):
        print(f'Terminado!')


def a(l):
    #print(l)
    for i in l:
        print(i)
        x = i.read()
        print(x)


p = Printer()
loop = asyncio.get_event_loop()
l = loop.run_until_complete(getAsync("https://www3.animeflv.net/", p))
a(l)"""
"""
class Printer(Observer):
    t: int = 0

    def on_next(self, v):
        self.t += 1
        print("Recibido:", v[0], v[1].__len__())

    def on_completed(self):
        print(f'Terminado, times printed: {self.t}')


def observer_teclado(o, s):
    msg = input('Introduce algo:')
    if msg:
        o.on_next(msg)
    else:
        o.on_completed()

p = Printer()
for i in range(5):
    print("I:", i)
    create(observer_teclado).subscribe(p)
"""
"""class cla:
    __list: list

    def __init__(self):
        self.__list = []

    def addItem(self, item):
        print(f"Add: {item}")
        self.__list.append(item)


c = cla()
images: list = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]

obs = from_(images)
obs.subscribe(on_next=lambda i: c.addItem(i))


print("a2")
images.append("t")"""
"""print("a")
images: dict = {}
obs = from_(images)
obs.subscribe(
    #on_next=lambda v: on_next(v),
    on_next=lambda v: print(f"Recibido: {v}"),
    on_completed=lambda: print('Terminado'),
    on_error=lambda e: print(f'Error: {e}'))

print("a2")
images.update({"t": 7})"""
"""print("a")
images: list = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
obs = of(images)
#obs.subscribe(lambda v: print(f"Recibido: {v}"))
obs.subscribe(
    on_next = lambda i: print("Received {0}".format(i)),
    on_error = lambda e: print("Error Occurred: {0}".format(e)),
    on_completed = lambda: print("Done!"),
)

print("a2")
images.append("t")"""
"""print("a")
images: list = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
obs = from_(images)
obs.subscribe(lambda v: print(f"Recibido: {v}"))
obs.subscribe(
    on_next = lambda i: print("Received {0}".format(i)),
    on_error = lambda e: print("Error Occurred: {0}".format(e)),
    on_completed = lambda: print("Done!"),
)
print(obs)
print("a2")
images.append("t")"""

"""async def func(url: str, u: str, root: str, urlob: Observer, session):
    result = None
    urlfin = None
    try:
        async with session.get(url) as resp:
            result = resp
            urlfin = url
    except:
        url2 = UrlCntroller.prepararUrl(url, u)
        try:
            async with session.get(url2) as resp:
                result = resp
                urlfin = url2
        except:
            url2 = UrlCntroller.prepararUrl(url, root)
            try:
                async with session.get(url2) as resp:
                    result = resp
                    urlfin = url2
            except:
                pass
    if result is not None:
        print(await result.text())
        #result = await result.read()
        #data = await result.read()
        #print(data)
        #from_list([(urlfin, result)]).subscribe(urlob)


async def getAsync(u: str, urlob: Observer, session):
    dom, root = UrlCntroller.urlRootDom(u)
    r = get(u)
    urllist: list = findall("src=\"(.+?)\"", r.text)
    i: int = 0
    while i < urllist.__len__():
        if urllist[i].__contains__(".jpg") is False and urllist[i].__contains__(".png") is False:
            del urllist[i]
        else:
            i += 1
    tasks = []
    for url in range(urllist.__len__()):
        tasks.append(asyncio.create_task(func(urllist[url], u, root, urlob, session)))
    print(tasks.__len__())
    return await asyncio.gather(*tasks)


class Printer(Observer):
    def on_next(self, result):
        res = yield from result[1].read()
        print(res)
        #print("Recibido:", result[0], result[1])
        #self.__parent.addImage(result[0], result[1])

    def on_error(self, error: Exception) -> None:
        print(error)

    def on_completed(self):
        print(f'Terminado!')


async def main():
    p = Printer()
    async with aiohttp.ClientSession() as session:
        htmls = await getAsync("https://en.wikipedia.org/wiki/Set_(mathematics)/", p, session)
        print(htmls)

if __name__ == '__main__':
    asyncio.run(main())"""


def getUrls(u: str):
    dom, root = UrlCntroller.urlRootDom(u)
    r = get(u)
    urllist: list = findall("src=\"(.+?)\"", r.text)
    i: int = 0
    while i < urllist.__len__():
        if urllist[i].__contains__(".jpg") is False and urllist[i].__contains__(".png") is False:
            del urllist[i]
        else:
            i += 1
    return urllist, dom, root


async def fetch(session, url, dom, root):
    try:
        async with session.get(url) as response:
            if response.status != 200:
                response.raise_for_status()
            return await response.text()
    except:
        try:
            url2 = UrlCntroller.prepararUrl(url, dom)
            async with session.get(url2) as response:
                if response.status != 200:
                    response.raise_for_status()
                return await response.text()
        except:
            url2 = UrlCntroller.prepararUrl(url, root)
            try:
                async with session.get(url2) as response:
                    if response.status != 200:
                        response.raise_for_status()
                    return await response.text()
            except:
                return None


async def fetch_all(session, urls, dom, root):
    tasks = []
    for url in urls:
        task = asyncio.create_task(fetch(session, url, dom, root))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


async def main():
    urls, dom, root = getUrls("https://en.wikipedia.org/wiki/Set_(mathematics)/")
    async with aiohttp.ClientSession() as session:
        htmls = await fetch_all(session, urls, dom, root)
        print(htmls)

if __name__ == '__main__':
    asyncio.run(main())
