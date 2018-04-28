from .constants import Couleur, Direction
from .outils import Outils


class PositionsDamier:
    """
    Cette classe a la responsabilité de gérer la position des cases sur un damier
    """

    colonnes = 5
    lignes = 10
    """ nombre initial des lignes de pions, par couleur """
    numeroInitialLignesPionsParCouleur = 4

    @staticmethod
    def getNombrePositions():
        """Obtient le nombre de positions sur le damier """
        return PositionsDamier.lignes * PositionsDamier.colonnes

    @staticmethod
    def getPositionsInitiales(couleur):
        """
        Obtient la liste des positions initiales pour une couleur donnée
        @param couleur
                couleur de pièce (noir ou blanc)
        @return la liste des positions initiales pour une couleur donnée
        """
        # nombre initial des pions, par couleur
        nombreInitialPionsParCouleur = PositionsDamier.numeroInitialLignesPionsParCouleur * \
            PositionsDamier.colonnes

        # la première position occupée par les pions de la couleur demandée
        if (couleur == Couleur.NOIR):
            premierePositionPions = 1
        else:
            premierePositionPions = PositionsDamier.getNombrePositions() - \
                nombreInitialPionsParCouleur + 1

        # le tableau des positions occupées par les pièces noires
        positionsInitiales = []
        for i in range(nombreInitialPionsParCouleur):
            positionsInitiales.append(i + premierePositionPions)
        return positionsInitiales

    @staticmethod
    def getPositionVoisine(position, direction):
        """
        Obtient une position voisine
            @param position
                la position sur le damier
            @param direction
                direction de mouvement en diagonale sur le damier vers: Haut à
                Gauche, Haut à Droite, Bas à Gauche, Bas à Droite
            @return
                la position voisine ou -1 si on est en bordure du damier
        """
        # si le numéro de ligne est pair
        result = {
            Direction.HAUT_GAUCHE: position - PositionsDamier.colonnes,
            Direction.HAUT_DROITE: position - PositionsDamier.colonnes + 1,
            Direction.BAS_GAUCHE: position + PositionsDamier.colonnes,
            Direction.BAS_DROITE: position + PositionsDamier.colonnes + 1,
        }[direction]

        # si le numéro de ligne est impair, une correction est necessaire
        numeroLigne = PositionsDamier.getNumeroLigne(position)
        if (Outils.estImpair(numeroLigne)):
            result = result - 1

        # si la position est en déhors du damier, retourner -1
        if (PositionsDamier.estPositionInvalide(result)):
            return -1

        # calculer le numéro de la ligne voisine
        numeroLigneVoisine = PositionsDamier.getNumeroLigne(result)
        offsetLigne = numeroLigneVoisine - numeroLigne

        # la ligne de la position voisine valide se trouve une ligne
        # plus haut (offsetLigne = -1)
        # ou plus bas (offsetLigne = 1)
        # en bordure du damier (offsetLigne = +/- 2)
        if ((offsetLigne != 1) and (offsetLigne != -1)):
            result = -1
        return result

    @staticmethod
    def estPositionValide(position):
        return (position >= 1) and (position <= PositionsDamier.getNombrePositions())

    @staticmethod
    def estPositionInvalide(position):
        """
        Vérifie si la position est invalide
            @param position
                position en notation Manoury
            @return true si la position est invalide
        """
        return not PositionsDamier.estPositionValide(position)

    @staticmethod
    def estLigneDeFond(position, couleur):
        """
         Vérifie si une ligne est une ligne de fond
            @param position
                la position sur le damier
            @param couleur
                couleur d'une pièce (noir ou blanc)
            @return true si est une ligne de fond
        """
        # le blanc avance vers le haut, le noir vers le bas
        if couleur == Couleur.BLANC:
            directions = Direction.haut
        else:
            directions = Direction.bas

        for direction in directions:
            if (PositionsDamier.getPositionVoisine(position, direction) > 0):
                return False
        return True

    @staticmethod
    def getNumeroLigne(position):
        """
        Calcule le numéro de la ligne (la numérotation commence à zéro)
            @param position
                la position sur le damier en notation Manoury (entier qui demarre à 1
            @return
                numéro de ligne ou -1 si la position est en déhors du damier
        """
        # une position est valide si >= 1 et <= nombre de positions
        if (PositionsDamier.estPositionInvalide(position)):
            return -1

        positionAbsolue = position - 1
        result = positionAbsolue // PositionsDamier.colonnes
        return result

    @staticmethod
    def getNumeroColonne(position):
        """
        Calcule le numéro de colonne (la numérotation commence à zéro)
            @param position
                la position sur le damier en notation Manoury (entier qui demarre à 1
            @return
                numéro colonne ou -1 si la position est en déhors du damier
        """
        # une position est valide si >= 1 et <= nombre de positions
        if (PositionsDamier.estPositionInvalide(position)):
            return -1
        positionAbsolue = position - 1
        result = (positionAbsolue % PositionsDamier.colonnes) * \
            2 + (PositionsDamier.getNumeroLigne(position) + 1) % 2
        return result
    @staticmethod
    def getPositionManoury(ligne, colonne):
        if(ligne + colonne) % 2 == 0:
            return -1
        return ligne * PositionsDamier.colonnes + colonne // 2 + 1
    
    @staticmethod
    def getCoords(position):
        ligne = PositionsDamier.getNumeroLigne(position)
        if ligne < 0 :
            return None
        colonne = PositionsDamier.getNumeroColonne(position)
        return (ligne, colonne)
