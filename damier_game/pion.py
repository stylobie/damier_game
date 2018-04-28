from .constants import Direction, TypePiece
from .piece import Piece
from .mouvement_unitaire import MouvementUnitaire
from .position_damier import PositionsDamier


class Pion(Piece):
    """
    La classe Pion représente un pion. Cette classe hérite la classe « Pièce ».
    """
    @property
    def typePiece(self):
        return TypePiece.PION

    def __init__(self, couleur):
        """
        Crée un pion, en initialisant sa couleur
        @param couleur
        couleur du pion (noir ou blanc)
        """
        super(Pion, self).__init__(couleur)

    def getDestinationsPossiblesSansCapture(self):
        result = []
        # sans capture, un pion peut avancer d'une case sur la diagonale
        # le noir avance vers le bas, le blanc vers le haut
        directionsAvancement = Direction.avancement[self.couleur]
        for direction in directionsAvancement:
            positionVoisine = PositionsDamier.getPositionVoisine(
                self.position, direction)
            # s'il y a une position voisine
            if positionVoisine > 0:
                # et si elle est libre
                if self.damier.estPositionLibre(positionVoisine):
                    # on deduit un mouvement unitaire sans capture (positionCapturee = -1)
                    mu = MouvementUnitaire(self.position, positionVoisine, -1)
                    # on rajoute le mouvement unitaire de la position de départ vers positionVoisine à la liste des
                    # destinations possibles sans capture
                    result.append(mu)
        return result

    def getDestinationsPossiblesAvecUneCapture(self, piecesCapturees):
        result = []
        # avec capture, un pion peut avancer/reculer d'une case sur la diagonale
        # dans toutes les directions
        # en sautant la pièce voisine adverse à capturer
        directionsAvancement = Direction.all
        for direction in directionsAvancement:
            positionVoisine = PositionsDamier.getPositionVoisine(
                self.position, direction)
            # si position voisine n'est pas sur le damier
            # on ne fait rien
            if positionVoisine <= 0:
                continue

            # si la pièce de la position voisine a déjà été sauté une fois (considérée
            # capturée)
            # on ne fait rien
            if positionVoisine in piecesCapturees:
                continue

            pieceVoisine = self.damier.getPiece(positionVoisine)
            # si pas de pièce voisine ou si la pièce voisine n'est pas une pièce adverse,
            # on ne fait rien
            if pieceVoisine is None or pieceVoisine.couleur == self.couleur:
                continue

            caseVoisineALaPieceVoisine = PositionsDamier.getPositionVoisine(
                positionVoisine, direction)
            # si la case voisine à la pièce voisine n'est pas sur le damier,
            # on ne fait rien
            if caseVoisineALaPieceVoisine <= 0:
                continue

            # si la case voisine à la pièce voisine est ocuppée,
            # on ne fait rien
            if self.damier.estPositionOccupee(caseVoisineALaPieceVoisine):
                continue

            # on deduit un mouvement unitaire avec capture
            mu = MouvementUnitaire(
                self.position, caseVoisineALaPieceVoisine, pieceVoisine.position)
            # on rajoute le mouvement unitaire de la position de départ vers la caseVoisineALaPieceVoisine à la liste des
            # destinations possibles
            result.append(mu)
        return result

    def deplacer(self, destination):
        super(Pion, self).deplacer(destination)
        position = self.position
        # si on est sur une ligne de fond,
        if PositionsDamier.estLigneDeFond(position, self.couleur):
            # le pion est promu en dame
            self.promotion()

    def promotion(self):
        """
        Promotion d'un pion en dame
        """
        d = self.damier
        position = self.position
        couleur = self.couleur
        # on retire le pion depuis le damier
        self.retirer()
        # on créé une dame à la place du pion, de la même couleur
        d.creerDame(position, couleur)
