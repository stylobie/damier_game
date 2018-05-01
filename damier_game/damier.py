from .piece import Piece
from .pion import Pion
from .dame import Dame
from .constants import Couleur, Direction
from .position_damier import PositionsDamier
from .mouvement_unitaire import MouvementUnitaire


class Damier:
    """
    Jeu du Damier
    La classe Damier est la classe principale, elle représente le jeu de dames.
    """

    @property
    def prochainMouvement(self):
        """
        @return la couleur de la pièce à qui est le tour de jouer
        """
        return self._prochainMouvement

    @prochainMouvement.setter
    def prochainMouvement(self, couleur):
        self._prochainMouvement = couleur
        msgFmt = "C'est au tour des {}"
        if couleur == Couleur.BLANC:
            msg = "blancs"
        else :
            msg = "noirs"
        
        self._dessinateur.dessinerMessage(msgFmt.format(msg))

    @property
    def pieces(self):
        """
        Obtient la liste des pièces
        @return la liste des pièces
        """
        return self._pieces

    def __init__(self, dessinateur, tableVide = False, prochainMouvement = Couleur.BLANC):
        self._dessinateur = dessinateur
        self._prochainMouvement = prochainMouvement
        self._pieces = []
        if not tableVide:
            self.nouveauJeu()

    def nouveauJeu(self):
        """
        Initialise le damier pour un nouveau jeu
        """
        self._pieces = []
        # le blanc commence le jeu
        self._prochainMouvement = Couleur.BLANC
        positionsInitialesPionsNoirs = PositionsDamier.getPositionsInitiales(
            Couleur.NOIR)
        positionsInitialesPionsBlancs = PositionsDamier.getPositionsInitiales(
            Couleur.BLANC)
        # la méthode "creerPions" pour un nouveau jeu ne peut pas retourner une
        # erreur
        self.creerPionsParCouleur(
            positionsInitialesPionsNoirs, positionsInitialesPionsBlancs)
        self.dessiner("nouveau jeu")

    def getEstTermine(self):
        """
        Verifie si une partie est terminée (une partie est considérée terminée s'il
        n'y a plus de mouvements possibles)

        @return true si la partie est terminée
        """
        prochainsMouvements = self.analyse()
        if len(prochainsMouvements) == 0:
            return True

        return False

    def estPositionLibre(self, position):
        """
        Vérifie si la position est libre
        @param position
        position en notation Manoury
        @return true si la position est libre
        """
        p = self.getPiece(position)
        return (p is None)

    def estPositionOccupee(self, position):
        """
        Vérifie si la position est occupée

        @param position
        position en notation Manoury
        @return true si la position est occupée
        """
        return not self.estPositionLibre(position)

    def getPieces(self, couleur):
        """
        Obtient la liste des pièces pour une couleur donnée

        @param couleur
        (noir, ou blanc)
        @return la liste des pièces pour la couleur donnée
        """
        piecesParCouleur = []
        for p in self.pieces:
            if p.couleur == couleur:
                piecesParCouleur.append(p)
        return piecesParCouleur

    def getPiece(self, position):
        """
        Obtient une pièce pour une position donnée

        @param position
        la position sur le damier
        @return None si pas de pièce trouvée sur la position donnée ou la pièce
        retrouvée
        """
        if PositionsDamier.estPositionInvalide(position):
            return None

        # on cherche parmis les pièces s'il y a une qui ocupe la position
        # donnée
        for piece in self.pieces:
            if piece.position == position:
                return piece
        return None

    def addPiece(self, piece):
        self._pieces.append(piece)

    def removePiece(self, piece):
        self._pieces.remove(piece)

    def getPositionsLibres(self, position, direction):
        """
        Obtient la liste des positions libres, par rapport à une position et une
        direction données

        @param position
        la position sur le damier
        @param direction
        direction de mouvement en diagonale sur le damier vers: Haut à
        Gauche, Haut à Droite, Bas à Gauche, Bas à Droite
        @return liste des positions libres
        """
        result = []
        # tant qu'il y a des positions libres sur le damier on les rajoute à la liste de résultat
        while True:
            # on obtient la position voisine à un position et direction données
            positionVoisine = PositionsDamier.getPositionVoisine(
                position, direction)
            # si elle est valide et libre
            if PositionsDamier.estPositionValide(positionVoisine) and self.estPositionLibre(positionVoisine):
                # on la rajoute à la liste des positions libres
                result.append(positionVoisine)
                # on redefinit la position par la valeur de la positionVoisine
                position = positionVoisine
            else:
                return result

    def getPremierePiece(self, position, direction):
        """
        Obtient la pièce la plus proche par rapport à une position et direction
        données

        @param position
        la position sur le damier
        @param direction
        direction de mouvement en diagonale sur le damier vers: Haut à
        Gauche, Haut à Droite, Bas à Gauche, Bas à Droite
        @return la position de la première pièce la plus proche par rapport à une
        position et direction données
        """
        positionsLibres = self.getPositionsLibres(position, direction)
        # s'il n'y a pas de position libre par rapport à une position et direction
        # données, on obtient la position de la pièce voisine. C'est cette
        # pièce voisine qui est la pièce la plus proche recherchée.
        if len(positionsLibres) == 0:
            positionPremierePiece = PositionsDamier.getPositionVoisine(
                position, direction)
            # s'il y a des positions libres par rapport à une position et direction
            # données, on trouve la pièce voisine à la dernière position libre. C'est cette
            # pièce voisine qui est la pièce la plus proche recherchée.
        else:
            dernierePositionLibre = positionsLibres[-1]
            positionPremierePiece = PositionsDamier.getPositionVoisine(
                dernierePositionLibre, direction)
        return self.getPiece(positionPremierePiece)

    def analyse(self):
        """
        Analyse une situation de jeu pour déterminer la liste des mouvements
        possibles

        @return liste de mouvements unitaires possibles
        """
        mouvements = []

        # on obtient la liste des pièces qu'on peut déplacer au prochain mouvement
        pieces = self.getPieces(self.prochainMouvement)
        for piece in pieces:
            mouvementsPiece = piece.analyse(True)
            mouvements = mouvements + mouvementsPiece

        # on enlève les mouvements qui n'ont pas de prise maximale
        MouvementUnitaire.removeNonMaximal(mouvements)
        return mouvements

    def retirer(self, positionCapturee):
        """
        Retire une pièce depuis une position donnée

        @param positionCapturee
        position de la pièce capturée
        """
        piece = self.getPiece(positionCapturee)
        if not piece is None:
            self._pieces.remove(piece)

    def dessiner(self, message):
        """
        Dessine le damier à l'aide du dessinateur précisé dans le constructeur
        """
        if self._dessinateur is None:
            return
        if message != "":
            self._dessinateur.dessinerMessage(message)
        # dessine les pièces sur le damier
        self._dessinateur.dessiner(self.pieces)

    def creerPion(self, position, couleur):
        """
        Crée un pion

        @param position
        position du pion sur le damier
        @param couleur
        couleur du pion (noir ou blanc)
        """
        pion = Pion(couleur)
        pion.placer(self, position)

    def creerDame(self, position, couleur):
        """
        Crée une dame

        @param position
        position de la damme sur le damier
        @param couleur
        couleur de la damme (noir ou blanc)
        @return "null" si la dame a été créée ou le message d'erreur
        """
        dame = Dame(couleur)
        dame.placer(self, position)

    def creerPieces(self, pieces):
        """
        Ajoute sur le damier des pièces données

        @param pieces
        position des pions noirs, pions blancs, dames noires, dames
        blanches
        """
        if self.pieces is None:
            return

        pionsNoirs = pieces[0]
        pionsBlancs = pieces[1]
        damesNoires = pieces[2]
        damesBlanches = pieces[3]

        self.creerPionsParCouleur(pionsNoirs, pionsBlancs)
        self.creerDamesParCouleur(damesNoires, damesBlanches)
        self.dessiner("reprise jeu")

    def creerPionsParCouleur(self, positionsNoires, positionsBlanches):
        """
        Crée des pions noirs et blancs

        @param positionsNoires
        liste des positions des pions noirs
        @param positionsBlanches
        liste des positions des pions blancs
        """
        self.creerPionsParPositionEtCouleur(positionsNoires, Couleur.NOIR)
        self.creerPionsParPositionEtCouleur(positionsBlanches, Couleur.BLANC)

    def creerPionsParPositionEtCouleur(self, positions, couleur):
        """
        Crée des pions d'une seule couleur

        @param positions
        liste des positions
        @param couleur
        couleur des pions
        """
        for position in positions:
            self.creerPion(position, couleur)

    def creerDamesParCouleur(self, positionsNoires, positionsBlanches):
        """
        Crée des dames noires et blanches

        @param positionsNoires
        liste des positions des dames noires
        @param positionsBlanches
        liste des positions des dames blanches
        @return "null" ou le message d'erreur
        """
        # TODO erreurs = new ArrayList<String>()
        # String erreur =
        self.creerDamesParPositionEtCouleur(positionsNoires, Couleur.NOIR)
        # if (erreur != null)
        #    erreurs.add(erreur)

        # erreur =
        self.creerDamesParPositionEtCouleur(positionsBlanches, Couleur.BLANC)
        # if (erreur != null)
        #     erreurs.add(erreur)

        # return erreurs.size() > 0 ? String.join("\n", erreurs) : null

    def creerDamesParPositionEtCouleur(self, positions, couleur):
        """
        Crée des dames d'une seule couleur

        @param positions
        liste des positions
        @param couleur
        couleur des dames
        @return "null" si la création est réussie ou le message d'erreur
        """
        # TODO ArrayList<String> erreurs = new ArrayList<String>()
        for position in positions:
            # String erreur =
            self.creerDame(position, couleur)
            # if (erreur != null)
            #     erreurs.add(erreur)
            # return erreurs.size() > 0 ? String.join("\n", erreurs) : null
