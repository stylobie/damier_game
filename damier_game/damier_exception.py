class DamierException(Exception):
    def __init__(self, message):
        """
        Affiche à l'utilisateur un message d'erreur

        @param message
        message d'erreur
        """
        Exception.__init__(self, message)
