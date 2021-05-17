class Account_m:
    def __init__(self):
        pass

    def auth(self, username, password):
        try:
            if (username == "admin" and password == "215802"):
                return (1)
            return (-1)
        except:
            return (-1)


    # info account
    # get name, status, and target
    def information(self, accountid):
        pass