from .constants import Couleur, Direction
from .position_damier import PositionsDamier
from .mouvement_unitaire import MouvementUnitaire
from .outils import Outils
from .damier_exception import DamierException


class Piece():
    """
    La classe abstraite Piece représente une pièce du damier (pion ou dame). Elle
    est la classe ancêtre des classes « Pion » et « Dame ».
    """

    @property
    def damier(self):
        """
        Obtient le damier sur lequel la pièce est positionnée
            @return le damier
        """
        return self._damier

    @property
    def typePiece(self):
        """
        Obtient le type d'une pièce
        """
        pass

    @property
    def couleur(self):
        return self._couleur

    @property
    def img(self):
        return "{}_{}".format(self.typePiece, self.couleur)

    @property
    def position(self):
        """
            Position d'une pièce
            @return la position de la pièce sur le damier ou -1 si la pièce n'est pas placée
        """
        return self._position

    @property
    def coords(self):
        position = self.position
        return PositionsDamier.getCoords(position)

    def __init__(self, couleur):
        """
            Crée une pièce, en initialisant sa couleur et sa position à -1 (la pièce n'est pas placée)
                @param couleur
                    couleur de la pièce
        """
        self._couleur = couleur
        self._position = -1
        self._damier = None

    def placer(self, damierDestination, position):
        """
        Positionne une pièce sur un damier.

        @param damierDestination de type Damier
               le damier ou on va positionner la pièce
        @param position
               la position de destination sur le "damierDestination"
        """
        if damierDestination is None:
            raise DamierException("Le damier n'est pas défini")
        # si la pièce est déjà placée sur un damier
        if not self.damier is None:
            raise DamierException("La piece est déjà placée à la position {:d}".format(self.position))

        # si la position est invalide ou occupée
        if (PositionsDamier.estPositionInvalide(position) or damierDestination.estPositionOccupee(position)):
            raise DamierException("La piece ne peut pas être placée à la position {:d}".format(position))

        # si la position est libre, positionner la pièce sur le damier
        self._damier = damierDestination
        self._position = position
        # et l'ajouter à la liste des pièces du damier
        self.damier.addPiece(self)
        return None

    def retirer(self):
        """
        Retire une pièce depuis un damier
        """
        if not self._damier is None:
            self._damier.removePiece(self)
            self._damier = None
            self._position = -1

    def deplacer(self, destination):
        """
        Deplace une pièce à un position donnée
        @param destination
               position à laquelle la pièce doit être deplacée
        """
        # sans vérifier la validité du mouvement
        self._position = destination

    def analyse(self, garderPriseMaximale, piecesCapturees=[]):
        # pour un mouvement unitaire initial la liste des pièces capturées est
        # vide
        estMouvementInitial = len(piecesCapturees) == 0

        # on mémorise la position de départ
        positionDepart = self.position
        # on rajoute au resultat la liste des destinations possibles avec une
        # capture
        result = self.getDestinationsPossiblesAvecUneCapture(piecesCapturees)
        # pour chaque mouvement unitaire avec capture on rajoute de façon
        # récursive
        # les captures suivantes
        for mouvementUnitaire in result:
            # on initialise la liste des pièces capturées aux mouvementx
            # suivants avec la
            # valeur
            # du paramètre de la méthode
            piecesCaptureesSuivantes = piecesCapturees.copy()
            # aux pièces déjà capturées on rajoute la nouvelle capture
            piecesCaptureesSuivantes.append(mouvementUnitaire.positionCapturee)
            # on déplace la pièce sur la nouvelle position
            self._position = mouvementUnitaire.positionDestination
            # on continue l'analyse pour trouver les mouvements unitaires
            # suivants
            mouvementUnitaire.mouvementsSuivants = self.analyse(
                garderPriseMaximale, piecesCaptureesSuivantes)
            # on remet la pièce sur la position de départ
            self._position = positionDepart

        # si on n'a pas pu capturer des pièces, on va rechercher des mouvements sans capture
        if estMouvementInitial and (len(result) == 0 or not garderPriseMaximale):
            result = result + self.getDestinationsPossiblesSansCapture()

        if garderPriseMaximale:
            MouvementUnitaire.removeNonMaximal(result)

        return result

    def getDestinationsPossiblesSansCapture(self):
        pass

    def getDestinationsPossiblesAvecUneCapture(self, piecesCapturees):
        pass
