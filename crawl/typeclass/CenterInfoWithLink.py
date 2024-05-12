class CenterInfoWithLink:
    __region: str
    __address: str
    __branch: str
    __category: str
    __link: str
    __target: str
    __crawlerIndex: str
    __centerName: str

    def __init__(self, region: str, address: str, branch: str, category: str,
                 link: str, target: str, index: str, name: str) -> None:
        self.__region = region
        self.__address = address
        self.__branch = branch
        self.__category = category
        self.__target = target
        self.__link = link
        self.__target = target
        self.__crawlerIndex = index
        self.__centerName = name
        return

    def get_region(self):
        return self.__region

    def get_address(self):
        return self.__address

    def get_branch(self):
        return self.__branch

    def get_category(self):
        return self.__category

    def get_target(self):
        return self.__target

    def get_crawler_index(self) -> str:
        return self.__crawlerIndex

    def get_link(self):
        return self.__link

    def get_center_name(self):
        return self.__centerName

    def get_center_info(self) -> tuple:
        return (self.__region, self.__address, self.__branch, self.__category,
                self.__link, self.__target, self.__crawlerIndex)

    def __getstate__(self) -> dict:
        return {
            "region": self.__region,
            "address": self.__address,
            "branch": self.__branch,
            "category": self.__category,
            "link": self.__link,
            "target": self.__target,
            "center_name": self.__centerName,
            "crawler_index": self.__crawlerIndex
        }

    def __setstate__(self, state):
        self.__region = state.get("region")
        self.__centerName = state.get("center_name")
        self.__branch = state.get("branch")
        self.__address = state.get("address")
        self.__crawlerIndex = state.get("crawler_index")
        self.__category = state.get("category")
        self.__link = state.get("link")
        self.__target = state.get("target")
        return
