class CenterInfoNoLink:
    __region: str
    __branch: str
    __address: str
    __regionIndex: int
    __branchIndex: int
    __crawlerIndex: str
    __centerName: str

    def __init__(self, region: str, branch: str, address: str, region_index: int,
                 branch_index: int, index: str, name: str) -> None:
        self.__region = region
        self.__branch = branch
        self.__address = address
        self.__regionIndex = region_index
        self.__branchIndex = branch_index
        self.__crawlerIndex = index
        self.__centerName = name
        return

    def get_branch(self) -> str:
        return self.__branch

    def get_region(self) -> str:
        return self.__region

    def get_region_index(self) -> int:
        return self.__regionIndex

    def get_branch_index(self) -> int:
        return self.__branchIndex

    def get_crawler_index(self) -> str:
        return self.__crawlerIndex

    def get_address(self) -> str:
        return self.__address

    def get_center_name(self) -> str:
        return self.__centerName

    def get_center_info(self) -> tuple:
        return self.__branch, self.__address, self.__region, self.__regionIndex, self.__branchIndex, self.__crawlerIndex

    def __getstate__(self) -> dict:
        return {
            "address": self.__address,
            "crawler_index": self.__crawlerIndex,
            "branch_index": self.__branchIndex,
            "region_index": self.__regionIndex,
            "region": self.__region,
            "name": self.__centerName,
            "branch": self.__branch
        }

    def __setstate__(self, state):
        self.__address = state.get("address")
        self.__centerName = state.get("name")
        self.__crawlerIndex = state.get("crawler_index")
        self.__branch = state.get("branch")
        self.__region = state.get("region")
        self.__regionIndex = state.get("region_index")
        self.__branchIndex = state.get("branch_index")
        return

