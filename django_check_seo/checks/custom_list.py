class CustomList:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name")
        self.settings = kwargs.get("settings")
        self.found = kwargs.get("found")
        self.searched_in = kwargs.get("searched_in", [])
        self.description = kwargs.get("description")
