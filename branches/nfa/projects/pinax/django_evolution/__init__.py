import django_evolution.admin

class EvolutionException(Exception):
    def __init__(self,msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)
        
class CannotSimulate(EvolutionException):
    pass
    
class SimulationFailure(EvolutionException):
    pass