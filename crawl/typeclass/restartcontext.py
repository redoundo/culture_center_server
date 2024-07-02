from typeclass.CenterInfoWithLink import CenterInfoWithLink
from typeclass.CenterInfoNoLink import CenterInfoNoLink


class Context:
    centerName: str
    info: CenterInfoNoLink | CenterInfoWithLink


class InfoContext(Context):
    urls: list[str]
    currentUrl: str

    def __init__(self, center: str, urls: list[str], info: CenterInfoNoLink | CenterInfoWithLink, url: str = None):
        self.centerName = center
        self.currentUrl = url
        self.urls = urls
        self.info = info
        return

    def __getstate__(self):
        return {
            "info": self.info.__getstate__(),
            "centerName": self.centerName,
            "urls": self.urls,
            "currentUrl": self.currentUrl
        }

    def __setstate__(self, state: dict):
        self.info = state.get("info").__setstate__()
        self.centerName = state.get("centerName")
        self.urls = state.get("urls")
        self.currentUrl = state.get("currentUrl")
        return


class UrlContext(Context):

    def __init__(self, center: str, info: CenterInfoNoLink | CenterInfoWithLink):
        self.centerName = center
        self.info = info
        return

    def __getstate__(self):
        return {
            "info": self.info.__getstate__(),
            "centerName": self.centerName
        }

    def __setstate__(self, state: dict):
        self.info = state.get("info").__setstate__()
        self.centerName = state.get("centerName")
        return

