from guiclass import GeneralVentana, GeneralDivTab, GeneralButton, GeneralLabel, GeneralEntradaTexto, GeneralPhoto, \
    GeneralProgressBar, GeneralListBox, messagebox
from extralib import UrlCntroller
import aiohttp
import asyncio


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
            messagebox.showinfo("Aviso", "No implementado")


class DivMedio(GeneralDivTab):
    def __init__(self, parent, row: int = 0, col: int = 0):
        super().__init__("DivMedio", parent, row=row, col=col)
        GeneralListBox("box", self, 0, 0)
        GeneralProgressBar("bar", self, 1, 1)

    def clearImages(self):
        for i in self.__object_list:
            if i.name == "img":
                del i

    def addImage(self, content: bytes):
        GeneralPhoto("img", self, content, 0, 0, columnspan=3, rowspan=3, width=200, height=200)

    def setProgress(self, progress: int):
        bar = self.get("bar")
        if bar is not None:
            bar.setProgress(progress)


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
