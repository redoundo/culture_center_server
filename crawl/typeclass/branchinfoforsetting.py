class BranchInfoForSetting:
    branchId: int
    branchName: str
    centerIdOfBranch: int
    centerUrl: str
    centerName: str

    def __init__(self, branch_id: int, branch_name: str, center_name: str, center_id: int, url: str):
        self.branchId = branch_id
        self.centerName = center_name
        self.centerUrl = url
        self.centerIdOfBranch = center_id
        self.branchName = branch_name
        return

