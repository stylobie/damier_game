from .outils import Outils


class MouvementUnitaire:
    """
    La classe MouvementUnitaire représente le déplacement d’une pièce d’une
    position à une autre, sans ou avec une capture. Par exemple, le mouvement
    26x37x48 est décomposé en 2 mouvements unitaires chacun avec une capture:
    26x37 et 37x48.
    """
    @staticmethod
    def removeNonMaximal(mouvements):
        maxCaptures = MouvementUnitaire.getMaxCaptures(mouvements)
        # on supprime les mouvements dont la prise n'est pas maximale
        for i in range(len(mouvements) - 1, -1, - 1):
            temp = mouvements[i]
            tempMaxCaptures = temp.getPriseMax()
            if tempMaxCaptures < maxCaptures:
                mouvements.remove(temp)
        return maxCaptures

    @staticmethod
    def filter(mouvements, startPosition):
        result = []
        if not(mouvements is None):
            for mu in mouvements:
                if mu.positionDepart == startPosition:
                    result.append(mu)
        return result

    @staticmethod
    def getVariantes(mouvementsPossibles):
        """
        Obtient la representation Manoury des variantes possibles
        @param mouvementsPossibles
        """
        variantes = []
        for mu in mouvementsPossibles:
            mu.getVariantesManoury(variantes)
        return variantes

    @property
    def positionDepart(self):
        return self._positionDepart

    @property
    def positionDestination(self):
        return self._positionDestination

    @property
    def positionCapturee(self):
        return self._positionCapturee

    @positionCapturee.setter
    def positionCapturee(self, value):
        self._positionCapturee = value

    @property
    def mouvementsSuivants(self):
        return self._mouvementsSuivants

    @mouvementsSuivants.setter
    def mouvementsSuivants(self, value):
        self._mouvementsSuivants = value

    @property
    def estCapture(self):
        return self.positionCapturee > 0

    def __init__(self, positionDepart, positionDestination, positionCapturee):
        self._positionDepart = positionDepart
        self._positionDestination = positionDestination
        self._positionCapturee = positionCapturee
        self._mouvementsSuivants = None

    def getPriseMax(self):
        """
        Obtient le nombre maximal de captures
        """
        # si pas de pièce capturée, le nombre de prises = 0
        if self.positionCapturee <= 0:
            return 0

        result = 1
        maxCapturesMouvementsSuivants = 0
        # on retrouve le nombre max de captures dans l'arbre des mouvements
        # suivants (maxCapturesMouvementsSuivants)
        if not self.mouvementsSuivants is None:
            for suivant in self.mouvementsSuivants:
                capturesSuivantes = suivant.getPriseMax()
                if capturesSuivantes > maxCapturesMouvementsSuivants:
                    maxCapturesMouvementsSuivants = capturesSuivantes
        result = result + maxCapturesMouvementsSuivants
        return result

    def getVariantesManoury(self, variantes, prefix=""):
        """
        Obtient la liste des variantes sous forme Manoury
        @param variantes
            liste à remplir avec les variantes possibles
        @param prefix
            mémorise les segments précédents concaténés en format Manoury
        """
        if self.estCapture:
            sep = "x"
        else:
            sep = "-"
        if prefix == "":
            prefix = "{:d}{}{:d}".format(
                self.positionDepart, sep, self.positionDestination)
        else:
            prefix = prefix + "{}{:d}".format(sep, self.positionDestination)

        # quand on ne peut plus descendre dans l'arbre (plus de mouvements
        # suivants, le prefix devient une variante
        if self.mouvementsSuivants is None or len(self.mouvementsSuivants) == 0:
            variantes.add(prefix)
        else:
            for ms in self.mouvementsSuivants:
                ms.getVariantesManoury(prefix, variantes)

    def toString(self, indent=0):
        """
        Obtient une representation texte de l'arbre de mouvements unitaires
            @param indent
        """

        indentStr = Outils.getIndent(indent)
        if self.positionCapturee > 0:
            capture = " ({:d})".format(self.positionCapturee)
        else:
            capture = ""

        element = "{}{:d}-{:d}{} MaxCaptures: {:d}".format(
            indentStr, self.positionDepart, self.positionDestination, capture, self.getPriseMax())
        enfants = ""
        if not self.mouvementsSuivants is None:
            element = element + "\n"
            enfantsElements = []
            for enfant in self.mouvementsSuivants:
                enfantsElements.append(enfant.toString(indent + 4))

            enfants = "\n".join(enfantsElements)
        return element + enfants

    @staticmethod
    def getMaxCaptures(mouvements):
        """
        Obtient de nombre maximal de captures pour la liste des mouvements
        unitaire (avec leurs continuations)

        @param mouvements
        """
        maxCaptures = 0
        # on calcule le nombre maximal des pièces capturées
        for temp in mouvements:
            tempMaxCaptures = temp.getPriseMax()
            if tempMaxCaptures > maxCaptures:
                maxCaptures = tempMaxCaptures
        return maxCaptures
