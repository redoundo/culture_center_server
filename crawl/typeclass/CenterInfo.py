class CenterInfo:
    __region: str
    __branch: str
    __centerName: str
    __address: str

    def __init__(self, region: str, address: str, branch: str, name: str):
        self.__region = region
        self.__address = address
        self.__branch = branch
        self.__centerName = name
        return

    def get_region(self):
        return self.__region

    def get_address(self) -> str:
        return self.__address

    def get_branch(self):
        return self.__branch

    def get_center_name(self):
        return self.__centerName

    def __getstate__(self) -> dict:
        return {
            "region": self.__region,
            "address": self.__address,
            "branch": self.__branch,
            "center_name": self.__centerName
        }

    def __setstate__(self, state: dict):
        self.__region = state.get("region")
        self.__branch = state.get("branch")
        self.__address = state.get("address")
        self.__centerName = state.get("center_name")
        return


class CenterInfoWithLink(CenterInfo):
    __category: str
    __link: str
    __target: str

    def __init__(self, region: str, address: str, branch: str, category: str, link: str, target: str, name: str) -> None:
        super().__init__(region=region, address=address, branch=branch, name=name)
        self.__category = category
        self.__target = target
        self.__link = link
        self.__target = target
        return

    def get_category(self):
        return self.__category

    def get_target(self):
        return self.__target

    def get_link(self):
        return self.__link

    def get_center_info(self) -> tuple:
        return (self.__region, self.__address, self.__branch, self.__category,
                self.__link, self.__target)

    def __getstate__(self) -> dict:
        return {
            "region": self.__region,
            "address": self.__address,
            "branch": self.__branch,
            "category": self.__category,
            "link": self.__link,
            "target": self.__target,
            "center_name": self.__centerName
        }

    def __setstate__(self, state):
        self.__region = state.get("region")
        self.__branch = state.get("branch")
        self.__address = state.get("address")
        self.__crawlerIndex = state.get("crawler_index")
        self.__category = state.get("category")
        self.__link = state.get("link")
        self.__target = state.get("target")
        self.__centerName = state.get("center_name")
        return
