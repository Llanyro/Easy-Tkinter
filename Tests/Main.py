from guiclass import GeneralVentana, GeneralDivTab, GeneralButton, GeneralLabel, GeneralEntradaTexto, GeneralPhoto, \
    GeneralProgressBar, GeneralListBox, messagebox
from extralib import UrlCntroller
from requests import get
from re import findall
from rx.core import Observer
from rx import from_list
from aiohttp import ClientSession
from asyncio import run, create_task, gather


def getUrls(u: str) -> list:
    web = UrlCntroller.getOrUrl(u)
    r = get(u)
    urllist: list = []
    urllist += (findall("src=\"(.+?)\"", r.text))

    i: int = 0
    while i < urllist.__len__():
        if urllist[i].__contains__(".jpg") is False and urllist[i].__contains__(".png") is False:
            del urllist[i]
        else:
            urllist[i] = UrlCntroller.prepararUrl2(urllist[i], web)
            i += 1
    return urllist


async def func(url: str, urlob: Observer) -> None:
    async with ClientSession() as session:
        async with session.get(url) as resp:
            result = await resp.content.read()
            if result is not None:
                from_list([(url, result)]).subscribe(urlob)


async def getAsync(urls: list, urlob: Observer) -> None:
    tasks = []
    for url in urls:
        task = create_task(func(url, urlob))
        tasks.append(task)
    await gather(*tasks)


class DivSuperior(GeneralDivTab):
    def __init__(self, parent, row: int = 0, col: int = 0):
        super().__init__("DivSuperior", parent, row=row, col=col)
        GeneralLabel("Label", self, "URL a procesar: ", 0, 0)
        GeneralEntradaTexto("url", self, 0, 1)
        GeneralButton("Buscar!", self, 0, 2, command=self.getURLContent)

    def getURLContent(self):
        url = self.get("url")
        if url is None:
            messagebox.showinfo("Aviso", "No se ha introducido URL")
        else:
            otherdiv = self.parent.get("DivMedio")
            if otherdiv is not None:
                obs = otherdiv.obs
                if obs is not None:
                    urls = getUrls(url.getText())
                    # print(urls)
                    otherdiv.addNumImages(urls.__len__())
                    run(getAsync(urls, obs))
                else:
                    messagebox.showerror("Error", "Obs no encontrado")
            else:
                messagebox.showerror("Error", "Div no encontrado")


class DivMedio(GeneralDivTab):
    __images: dict
    __obs = None
    __maxNumEnlaces: float

    def __init__(self, parent, row: int = 0, col: int = 0):
        super().__init__("DivMedio", parent, row=row, col=col)
        GeneralListBox("box", self, 0, 0, command=self.onclick)
        GeneralProgressBar("bar", self, 3, 1)

        self.__images = {}
        self.__obs = ImageController(self)
        self.__maxNumEnlaces = 0

        #self.addImage("caram", open("../CarameloRaro.png", 'rb').read())
        #self.addImage("wat", open("../MlsPy.png", 'rb').read())

    def clearImages(self):
        for i in self.__object_list:
            if i.name == "img":
                del i

    def addImage(self, name: str, content: bytes):
        # lo guardo en el diccionario
        self.__images.update({name: content})
        # lo guardo en la lista de imagenes a mostrar
        self.get("box").addElement(name)
        self.addNewImageValue()

    def onclick(self, event):
        selection = event.widget.curselection()
        if selection:
            imageName = event.widget.get(selection[0])
            print(imageName)

            # Eliminamos la imagen anterior si existe
            self.deleteItem("img")

            # Obtenemos el contenido de la imagen
            content: bytes = self.__images.get(imageName)

            # Creamos la imagen
            GeneralPhoto("img", self, content, 0, 1, columnspan=3, rowspan=3, width=200, height=200)
        else:
            messagebox.showerror("Error", "Algo ha pasado al seleccionar imagen")

    def addNumImages(self, num: int):
        oldValue = self.__maxNumEnlaces
        self.__maxNumEnlaces += num

        bar = self.get("bar")
        oldProgress: float = bar.getProgress()
        if oldProgress != 0:
            bar.setProgress((oldProgress * oldValue) / self.__maxNumEnlaces)

        print("Values", oldValue, self.__maxNumEnlaces)

    def addNewImageValue(self):
        val = 100 / self.__maxNumEnlaces
        if self.get("bar").getProgress() + val < 100:
            self.get("bar").addProgress(val)
        else:
            self.get("bar").setProgress(99.99)
        print("Add value", val, self.get("bar").getProgress())

    def setProgress(self, progress: int):
        bar = self.get("bar")
        if bar is not None:
            bar.setProgress(progress)

    @property
    def obs(self):
        return self.__obs


class ImageController(Observer):
    __parent: DivMedio

    def __init__(self, parent: DivMedio):
        super().__init__()
        self.__parent = parent

    def on_next(self, result):
        #print(result)
        #print("Recibido:", result[0], result[1])
        self.__parent.addImage(result[0], result[1])

    def on_error(self, error: Exception) -> None:
        print(error)

    def on_completed(self):
        print(f'Terminado!')


class MainVentana(GeneralVentana):
    def __init__(self, titulo: str):
        super().__init__(titulo)
        self.nucleo.geometry("400x600")
        DivSuperior(self, 0, 0)
        DivMedio(self, 1, 0)

    def closeWindow(self):
        self.nucleo.destroy()


if __name__ == '__main__':
    v = MainVentana("Practica 1")
    v.start()
