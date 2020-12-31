from guiclass import GeneralVentana, GeneralDivTab, GeneralButton, GeneralLabel, GeneralEntradaTexto, GeneralPhoto, \
    GeneralProgressBar, GeneralListBox, messagebox
from extralib import UrlCntroller
import aiohttp
import asyncio
from requests import get
from re import findall
from rx.core import Observer
from rx import from_list


async def func(url: str, u: str, root: str, urlob: Observer):
    result = None
    urlfin = None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                result = resp.content
                urlfin = url
    except:
        url2 = UrlCntroller.prepararUrl(url, u)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url2) as resp:
                    result = resp.content
                    urlfin = url2
        except:
            url2 = UrlCntroller.prepararUrl(url, root)
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url2) as resp:
                        result = resp.content
                        urlfin = url2
            except:
                pass
    if result is not None:
        print(urlfin)
        from_list([(urlfin, result)]).subscribe(urlob)
    return result is not None


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
                    pass
                    loop = asyncio.get_event_loop()
                    print(loop.run_until_complete(getAsync(url.getText(), obs)))
                else:
                    messagebox.showerror("Error", "Obs no encontrado")
            else:
                messagebox.showerror("Error", "Div no encontrado")


class DivMedio(GeneralDivTab):
    __images: dict
    __obs = None

    def __init__(self, parent, row: int = 0, col: int = 0):
        super().__init__("DivMedio", parent, row=row, col=col)
        GeneralListBox("box", self, 0, 0, command=self.onclick)
        GeneralProgressBar("bar", self, 3, 1)

        self.__images = {}
        self.__obs = ImageController(self)

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
        res = yield from result[1].read()
        print(res)
        #print("Recibido:", result[0], result[1])
        #self.__parent.addImage(result[0], result[1])

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


v = MainVentana("Web Analysis GUI")
v.start()
