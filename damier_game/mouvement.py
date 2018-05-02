from .constants import Couleur
from .mouvement_unitaire import MouvementUnitaire
from .damier_exception import DamierException
from .position_damier import PositionsDamier
class Mouvement:
    """
    La classe Mouvement représente un mouvement complet demandé par un joueur. Il
    est constitué d’un enchaînement des mouvements unitaires.
    """

    def __init__(self, damier, mouvementManoury):
        self.mouvementManoury = mouvementManoury
        try:
            positionsDeplacements = Mouvement.getPositions(mouvementManoury)
        except:
            positionsDeplacements = []

        self.damier = damier
        self.mouvementsUnitaires = Mouvement.creerSegments(
            positionsDeplacements)

    def valider(self):
        """
        Vérifie la validité du mouvement et détermine les causes d’invalidité
        """
        self.verifierSyntaxe()
        self.verifierPiece()
        self.verifierPositionsValides()
        self.verifierDestinationsLibres()

        mouvementsPossibles = self.getMouvementsPossibles()
        self.verifierMouvementPossible(mouvementsPossibles)
        self.verifierPriseMax()

    def execute(self):
        """
        Exécute le mouvement (si valide) en déplaçant la pièce puis retirer les
        captures
        """
        p = self.piece
        for i in range(len(self.mouvementsUnitaires)):
            mu = self.mouvementsUnitaires[i]
            p.deplacer(mu.positionDestination)

        for mu in self.mouvementsUnitaires:
            if mu.estCapture:
                self.damier.retirer(mu.positionCapturee)
        prochainCouleur = Couleur.autre(p.couleur)
        self.damier.prochainMouvement = prochainCouleur

    def verifierPriseMax(self):
        """
        Vérifie si la prise est maximale
        @param mouvementsPossibles
        liste des mouvements unitaires possibles
        @throws DamierException
        declanche une exception si la prise n'est pas maximale
        """
        # on obtient les mouvements avec prise maximale
        mouvementsPossibles = self.damier.analyse()
        maxCaptures = MouvementUnitaire.getMaxCaptures(mouvementsPossibles)

        # si le nombre de captures max du mouvement < nombre de captures
        # maximales pour un autre mouvement
        # on va proposer à l'utilisateur les variantes de coup maximal
        if maxCaptures > self.getCaptures():
            # on transforme l'arbre des mouvements unitaires possibles dans une
            # liste de mouvements Manoury
            variantesPossibles = MouvementUnitaire.getVariantes(
                mouvementsPossibles)
            # si une seule variante
            if len(variantesPossibles) == 1:
                variantes = variantesPossibles[0]
            else:
                # si plusieurs variantes, on les affichent concaténées
                variantes = ", ".join(variantesPossibles)
            errorMsg = "Vous devez prendre le coup maximal de pièces: {}".format(
                variantes)
            raise DamierException(errorMsg)

    def getCaptures(self):
        """
        Obtient le nombre des pièces capturée
        """
        result = 0
        for mu in self.mouvementsUnitaires:
            if mu.estCapture:
                result = result + 1
        return result

    def verifierMouvementPossible(self, mouvementsPossibles):
        """
        Vérifie si le mouvement est possible
        @param mouvementsPossibles
        liste des mouvements possibles
        declanche une exception si le mouvement est invalide
        """
        for mu in self.mouvementsUnitaires:
            # au départ on n'a pas d'erreur
            erreur = ""
            if mouvementsPossibles is None:
                erreur = "Le mouvement {:d} -> {:d} est invalide".format(
                    mu.positionDepart, mu.positionDestination)
            else:
                leMouvementEstPossible = False
                for mouvementPossible in mouvementsPossibles:
                    if mouvementPossible.positionDepart == mu.positionDepart and mouvementPossible.positionDestination == mu.positionDestination:
                        leMouvementEstPossible = True
                        # on recupère la position de la pièce capturée
                        mu.positionCapturee = mouvementPossible.positionCapturee
                        # on cherche recursivement le segment suivant
                        mouvementsPossibles = mouvementPossible.mouvementsSuivants
                        break
                if not leMouvementEstPossible:
                    erreur = "Le mouvement {:d} -> {:d} est invalide".format(mu.positionDepart, mu.positionDestination)
            # si on a une erreur, on déclanche une exception qui arrête
            # l'execution de la méthode
            if erreur != "":
                raise DamierException(erreur)

    def getMouvementsPossibles(self):
        """
        Obtient la liste des mouvements possibles
        @return les mouvements possibles
        """
        p = self.piece
        # true dans le cas de prise maximale, false pour toutes les mouvements
        # possibles sans prise max
        return p.analyse(False)

    def verifierPositionsValides(self):
        positions = []
        for mu in self.mouvementsUnitaires:
            positions.append(mu.positionDepart)
        if len(self.mouvementsUnitaires) > 0:
            mu = self.mouvementsUnitaires[-1]
            positions.append(mu.positionDestination)

        for i in range(len(positions) - 1, -1, -1):
            position = positions[i]
            if PositionsDamier.estPositionValide(position):
                positions.remove(position)
        nombrePositionsInvalides = len(positions)
        if nombrePositionsInvalides == 0:
            return
        elif nombrePositionsInvalides == 1:
            raise DamierException(
                "La position {:d} est invalide".format(positions[0]))
        else:
            raise DamierException(
                "Les positions {} est invalide".format(", ".join(positions)))

    def verifierDestinationsLibres(self):
        """
        Vérifie si les positions nécessaires au mouvement sont libres. 
        @throws DamierException
        déclanche une exception si la position est ocuppée
        """
        positions = []
        for mu in self.mouvementsUnitaires:
            if not self.damier.estPositionLibre(mu.positionDestination):
                positions.append(mu.positionDestination)

        nombrePositionsInvalides = len(positions)
        if nombrePositionsInvalides == 0:
            return
        elif nombrePositionsInvalides == 1:
            raise DamierException(
                "La position {:d} est occupée".format(positions[0]))
        else:
            raise DamierException(
                "Les positions {} sont occupées".format(", ".join(positions)))

    def verifierPiece(self):
        piece = self.piece
        if piece is None:
            raise DamierException("La case de départ n'est pas occupée")
        if piece.couleur != self.damier.prochainMouvement:
            raise DamierException(
                "Vous essayez de jouer une pièce de votre adversaire")

    @property
    def piece(self):
        start = self.mouvementsUnitaires[0]
        piece = self.damier.getPiece(start.positionDepart)
        return piece

    def verifierSyntaxe(self):
        """
        Vérifie la syntaxe de la chaîne introduite par l’utilisateur

        @throws DamierException
        déclanche une exception si la syntaxe d'un coup est
        incorrecte
        """
        if len(self.mouvementsUnitaires) == 0:
            raise DamierException(
                "Syntaxe incorrecte pour la notation d'un coup: " + self.mouvementManoury)

    def toString(self):
        result = ""
        for mu in self.mouvementsUnitaires:
            if mu.estCapture:
                sep = "x"
            else:
                sep = "-"
            result = result + mu.positionDepart + sep
        if len(self.mouvementsUnitaires) > 0:
            mu = self.mouvementsUnitaires[-1]
            result = result + mu.positionDestination
        return result

    @staticmethod
    def getPositions(mouvementManoury):
        """
        Obtient les positions à partir du mouvement Manoury donné sous forme de
        string
        
        @param mouvementManoury
        representation sous forme d'un string d'un mouvement
        @return les positions d'un mouvement Manoury
        """

        positionsStr = mouvementManoury.replace("x", "-").split("-")
        result = []
        for positionStr in positionsStr:
            result.append(int(positionStr))
        return result

    @staticmethod
    def creerSegments(positions):
        """
        Crée des mouvements unitaires à partir d'une liste de positions données
        
        @param positions
        @return mouvements unitaires
        """
        mouvementsUnitaires = []
        for i in range(len(positions)-1):
            positionDepart = positions[i]
            positionDestination = positions[i + 1]
            # la position capturée n'est pas conue ici, nous allons l'initialiser avec -1==sans capture
            mu = MouvementUnitaire(positionDepart, positionDestination, -1)
            mouvementsUnitaires.append(mu)
        return mouvementsUnitaires
