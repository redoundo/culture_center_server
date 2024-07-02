class PublicLibrary:

    __address: dict[str, str]
    __link: str
    __libraryName: str
    __type: str
    __region: str
    __branch: str
    __toEnroll: str | None

    def __init__(self, address: dict[str, str], url: str, region: str, to_enroll: str | None,
                 branch: str, library_name: str, library_type="도서관"):
        self.__address = address
        self.__libraryName = library_name
        self.__type = library_type
        self.__branch = branch
        self.__region = region
        self.__link = url
        self.__toEnroll = to_enroll
        return

    def __getstate__(self) -> dict:
        return {
            "address": self.__address,
            "library_name": self.__libraryName,
            "branch": self.__branch,
            "region": self.__region,
            "link": self.__link,
            "type": self.__type,
            "to_enroll": self.__toEnroll
        }

    def __setstate__(self, state: dict):
        self.__toEnroll = state.get("to_enroll")
        self.__libraryName = state.get("library_name")
        self.__type = state.get("type")
        self.__address = state.get("address")
        self.__region = state.get("region")
        self.__branch = state.get("branch")
        self.__link = state.get("link")
        return

    def get_link(self) -> str:
        return self.__link

    def get_type(self) -> str:
        return self.__type

    def get_region(self) -> str:
        return self.__region

    def get_branch(self) -> str:
        return self.__branch

    def get_library_name(self) -> str:
        return self.__libraryName

    def get_addresses(self) -> dict[str, str]:
        return self.__address

    def get_to_enroll(self) -> str | None:
        return self.__toEnroll

