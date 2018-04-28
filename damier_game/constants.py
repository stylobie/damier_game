class Couleur:
    NOIR = "NOIR"
    BLANC = "BLANC"
    all = [NOIR, BLANC]

    @staticmethod
    def autre(couleur):
        if(couleur == Couleur.NOIR):
            return Couleur.BLANC
        return Couleur.NOIR


class Direction:
    HAUT_GAUCHE = "HAUT_GAUCHE"
    BAS_GAUCHE = "BAS_GAUCHE"
    HAUT_DROITE = "HAUT_DROITE"
    BAS_DROITE = "BAS_DROITE"
    all = [HAUT_GAUCHE, HAUT_DROITE, BAS_GAUCHE, BAS_DROITE]
    haut = [HAUT_GAUCHE, HAUT_DROITE]
    bas = [BAS_GAUCHE, BAS_DROITE]
    avancement = {
        Couleur.NOIR: [BAS_DROITE, BAS_GAUCHE],
        Couleur.BLANC: [HAUT_DROITE, HAUT_GAUCHE]
    }


class TypePiece:
    PION = "PION"
    DAME = "DAME"
    all = [PION, DAME]
