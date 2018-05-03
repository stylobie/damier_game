from .constants import Couleur
from .position_damier import PositionsDamier
from .damier import Damier
from .mouvement import Mouvement
from .damier_exception import DamierException
from .mouvement_unitaire import MouvementUnitaire


class Board:
    @property
    def boardSize(self):
        return self._boardSize

    @property
    def pieces(self):
        return self._pieces

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._trace = []
        self._start = value
        self._hints = []
        if value is None:
            """
            Nous allons chercher ici les points de depart possibles
            Pour réaliser cela on va retrouver l'arbre des mouvements possibles et on va prendre les points de départ
            """
            if not self.damier is None:
                mouvementsUnitaires = self.damier.analyse()
                for mu in mouvementsUnitaires:
                    self._hints.append(mu.positionDepart)
            self._trace = []
            self._mouvementsUnitaires = []

        else:
            """Nous allons chercher ici les positions de destination pour la piece sélectionnée"""

            mouvementsUnitaires = self._mouvementsUnitaires
            if len(mouvementsUnitaires) == 0:
                self.start = None
                return
            hints = []
            for mu in mouvementsUnitaires:
                hints.append(mu.positionDestination)
            self._hints = hints
            self._trace = [value]

    @property
    def hints(self):
        return self._hints

    @property
    def trace(self):
        return self._trace

    @property
    def damier(self):
        return self._damier

    @damier.setter
    def damier(self, value):
        self._damier = value
        self.dessiner(self.damier.pieces)
        self.initialiseMvt()

    def initialiseMvt(self):
        self.start = None
        if not self.damier is None:
            if self.damier.getEstTermine():
                msgFmt = "Les {} ont gagné"
                if self.damier.prochainMouvement == Couleur.BLANC:
                    msg = "noirs"
                else:
                    msg = "blancs"
            else :   
                msgFmt = "C'est au tour des {}"
            if self.damier.prochainMouvement == Couleur.BLANC:
                msg = "blancs"
            else:
                msg = "noirs"
            message = msgFmt.format(msg)
            
            self.dessinerMessage(message)

            self.dessiner(self.damier.pieces)

            self._boardUI.drawBoard(False)

    def __init__(self, boardUI):
        self._boardUI = boardUI
        self._boardSize = PositionsDamier.lignes
        self._pieces = None
        self._damier = None
        self.initialiseMvt()

    def dessinerMessage(self, message):
        self._boardUI.dessinerMessage(message)

    def dessiner(self, pieces):
        self._pieces = pieces
        self._boardUI.drawPieces()
    
    def click(self, ligne, colonne):
        position = PositionsDamier.getPositionManoury(ligne, colonne)
        if position < 0:
            return
        if self.start is None:
            # démarer un mvt
            p = self._damier.getPiece(position)
            if p is None:
                return
            if p.couleur != self._damier.prochainMouvement:
                return
            mouvementsUnitaires = self._damier.analyse()
            mouvementsUnitaires = MouvementUnitaire.filter(mouvementsUnitaires, position)
            if len(mouvementsUnitaires) == 0:
                return
            self._mouvementsUnitaires = mouvementsUnitaires
            self.start = p.position
        elif position == self.start:
            self.start = None
        else:
            for mu in self._mouvementsUnitaires:
                if position == mu.positionDestination:
                    self._mouvementsUnitaires = mu.mouvementsSuivants
                    self._trace.append(position)
                    if (self._mouvementsUnitaires is None) or len(self._mouvementsUnitaires) == 0:
                        self.move()
                    else:
                        hints = []
                        for mu in self._mouvementsUnitaires:
                            hints.append(mu.positionDestination)
                        self._hints = hints
        self._boardUI.drawBoard(False)

    def nouveauJeu(self):
        self.damier = Damier()
    def move(self):
        traceStr = []
        for p in self._trace:
            traceStr.append(str(p))
        mvtStr = "-".join(traceStr)
        self._start = None
        self._trace = []
        self._hints = []
        mvt = Mouvement(self._damier, mvtStr)
        try:
            mvt.valider()
            mvt.execute()
            self.initialiseMvt()
        except DamierException as e:
            self.dessinerMessage(str(e))
        
