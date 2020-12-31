class UrlCntroller:
    @staticmethod
    def urlDomV2(url: str):
        # region Primera parte
        # Destripamos por partes
        flagHttp: int = 0
        if url.startswith("https://"):
            flagHttp = 1
            url = url.replace("https://", '', 1)
        elif url.startswith("http://"):
            flagHttp = 2
            url = url.replace("http://", '', 1)

        # Si aun quitando to.do aun quedan cosas lo quitamos to.do menos lo que queremos(el root)
        if url.__contains__('/'):
            url = url.split('/')[0]
        # endregion
        # region Segunda parte
        flagWww: int = 0
        if url.startswith("www."):
            url = url.replace("www.", '', 1)
            flagWww = 1
        # endregion
        # region Tercera parte
        urllist = url.split('.')
        fin = ""
        url = urllist[0]
        urlfinal = ""
        if flagHttp == 1:
            urlfinal += "https://"
        elif flagHttp == 2:
            urlfinal += "http://"
        if flagWww == 1:
            urlfinal += "www."
        if urllist.__len__() > 1:
            fin = urllist[1]
        # endregion
        return urlfinal + url, fin

    @staticmethod
    def urlRoot(url: str):
        if url[url.__len__() - 1] != '/':
            url += "/"
        return url

    @staticmethod
    def urlRootDom(url: str):
        dom, fin = UrlCntroller.urlDomV2(url)
        root = UrlCntroller.urlRoot(dom + '.' + fin)
        return dom, root

    @staticmethod
    def urlCorrectaType2(url: str):
        if url.startswith("https://"):
            resultado = True
        elif url.startswith("http://"):
            resultado = True
        else:
            resultado = False
        return resultado

    @staticmethod
    def prepararUrl(url: str, root_url: str):
        if url.startswith('//'):
            url = url[2:]
        elif url.startswith('/'):
            url = url[1:]
        return f"{root_url}{url}"
