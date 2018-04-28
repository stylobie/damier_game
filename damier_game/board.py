from .dessinateur import Dessinateur
from .position_damier import PositionsDamier
from .damier import Damier
from .mouvement import Mouvement
from .damier_exception import DamierException
from .mouvement_unitaire import MouvementUnitaire


class Board(Dessinateur):
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
        if value is None:
            self._hints = []
        else:
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

    def __init__(self, boardUI):
        self._boardUI = boardUI
        self._boardSize = PositionsDamier.lignes
        self._pieces = None
        self._start = None
        self._hints = []
        self._trace = []
        self._damier = None
        self._mouvementsUnitaires = []

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
        except DamierException as e:
            self._boardUI.dessinerMessage(str(e))
        