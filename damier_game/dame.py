from .constants import Direction, TypePiece
from .piece import Piece
from .mouvement_unitaire import MouvementUnitaire
from .position_damier import PositionsDamier

class Dame(Piece) :
    """"
    La classe Dame représente une dame. Cette classe hérite la classe « Pièce ».
    """
    @property
    def typePiece(self) :
        return TypePiece.DAME

    def __init__(self, couleur) :
        """
        Crée une dame, en initialisant sa couleur
        
        @param couleur
        couleur de la dame
        """
        super(Dame, self).__init__(couleur)

    def getDestinationsPossiblesSansCapture(self) :
        result = []
        # sans capture, une dame peut avancer/reculer d'une ou plusieurs cases
        # sur n'importe quelle diagonale
        directionsAvancement = Direction.all
        for direction in directionsAvancement :
            positionTemp = self.position
            # tant qu'une position voisine est occupée ou inexistante
            while True :
                positionVoisine = PositionsDamier.getPositionVoisine(positionTemp, direction)
                # si une position voisine existe
                if positionVoisine > 0 :
                    # et si elle est libre
                    if self.damier.estPositionLibre(positionVoisine) :
                        # on deduit un mouvement unitaire sans capture (positionCapturee = -1)
                        mu = MouvementUnitaire(self.position, positionVoisine, -1)
                        # on rajoute le mouvement unitaire de la position de départ à la positionVoisine à la liste des
                        # destinations possibles sans capture
                        result.append(mu)
                        positionTemp = positionVoisine
                        positionVoisineOccupeeOuInexistante = False
                    else :
                        positionVoisineOccupeeOuInexistante = True
                else :
                    positionVoisineOccupeeOuInexistante = True
                
                if positionVoisineOccupeeOuInexistante :
                    break
        return result

    def getDestinationsPossiblesAvecUneCapture(self, piecesCapturees) :
        result = []
        # avec capture, une dame peut avancer/reculer sur la diagonale
        # dans toutes les directions d'une ou plusieurs cases libres
        # en sautant la pièce adverse à capturer. La case destination doit se
        # trouver sur la même direction, entre la pièce à capturer et une autre case
        # occupée.
        directionsAvancement = Direction.all
        for direction in directionsAvancement :
            self.getDestinationsPossiblesAvecUneCaptureEnDirection(result, direction, piecesCapturees)
        return result

    def getDestinationsPossiblesAvecUneCaptureEnDirection(self, liste, direction, piecesCapturees) :
        """
        Obtient la liste des destinations possibles dans le cas d'un coup avec une
        capture
        
        @param liste
        liste des mouvements unitaires
        @param direction
        direction du mouvement
        @param piecesCapturees
        positions des pieces capturées
        """
        premierePieceTrouvee = self.damier.getPremierePiece(self.position, direction)
        # s'il n'y a pas de pièce proche trouvée
        # on ne fait rien
        if premierePieceTrouvee is None :
            return
        
        # si la couleur de la pièce proche trouvée n'est pas celle d'une pièce adverse
        # on ne fait rien
        if premierePieceTrouvee.couleur== self.couleur :
            return
        
        # si la pièce trouvée a déjà été sautée une fois (considérée capturée)
        # on ne fait rien
        if premierePieceTrouvee.position in piecesCapturees :
            return

        positionsLibresApresPremierePieceTrouvee = self.damier.getPositionsLibres(premierePieceTrouvee.position, direction)
        for positionLibreApresPremierePieceTrouvee in positionsLibresApresPremierePieceTrouvee :
            # on deduit un mouvement unitaire avec capture
            mu = MouvementUnitaire(self.position, positionLibreApresPremierePieceTrouvee, premierePieceTrouvee.position)
            # on rajoute le mouvement unitaire de la position de départ vers la
            # positionLibreApresPremierePieceTrouvee à la liste des
            # destinations possibles
            liste.append(mu)
