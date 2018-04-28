class Outils:
    @staticmethod
    def estImpair(n):
        return n % 2 == 1

    @staticmethod
    def estPair(n):
        return n % 2 == 0

    @staticmethod
    def getIndent(indent):
        if indent < 1:
            return ""
        else:
            return ("{:>"+"{:d}".format(indent)+"}").format(" ")
