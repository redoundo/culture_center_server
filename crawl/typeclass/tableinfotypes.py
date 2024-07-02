class BranchesTableInfo:

    branchId: int
    branchName: str
    centerIdOfBranch: int
    branchAddress: str
    branchState: str
    branchCity: str
    branchTown: str
    longitude: int
    latitude: int

    def __init__(self, name: str, center_id: int, address: str, state: str, city: str, town: str,
                 long: int, lat: int, branch_id: int = None):
        self.branchCity = city
        self.branchTown = town
        self.branchState = state
        self.branchName = name
        self.branchId = branch_id
        self.branchAddress = address
        self.centerIdOfBranch = center_id
        self.longitude = long
        self.latitude = lat
        return


