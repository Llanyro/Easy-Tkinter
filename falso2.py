from guiclass import GeneralVentana, GeneralDivTab, GeneralButton, GeneralLabel, GeneralEntradaTexto, messagebox, GeneralMenu, GeneralMenuBar
import webbrowser


class MainMenuHelp(GeneralMenu):
    def __init__(self, parent: GeneralMenuBar):
        super().__init__("Help", parent)
        self.nucleo.add_command(label="Help", command=self.__help)
        self.nucleo.add_command(label="Not help", command=self.__openNever)
        self.nucleo.add_separator()
        self.nucleo.add_command(label="Acerca de...", command=self.__opengit)

    def __help(self):
        if messagebox.askyesno("Help", "¿Necesitas ayuda?"):
            messagebox.showinfo("Help", "Entonces busca en google")

    def __openNever(self):
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstleyVEVO", new=2)

    def __opengit(self):
        if messagebox.askyesno("Acerca de ..", "Seguro que quiere abrir el enlace?"):
            webbrowser.open("https://github.com/Llanyro", new=2)


class MainMenu(GeneralMenuBar):
    def __init__(self, parent: GeneralVentana):
        super().__init__("Main menu", parent)
        MainMenuHelp(self)


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
            messagebox.showinfo("Aviso", url.getText())


class MainVentana(GeneralVentana):
    def __init__(self, titulo: str):
        super().__init__(titulo)
        self.nucleo.geometry("400x600")
        DivSuperior(self, 0, 0)
        MainMenu(self)

    def closeWindow(self):
        self.nucleo.destroy()


if __name__ == '__main__':
    v = MainVentana("Test 2")
    v.start()
