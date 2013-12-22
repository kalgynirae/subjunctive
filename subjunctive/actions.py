class Action:
    def do_it(self):
        raise NotImplemented

class StayAction(Action):
    def do_it(self):
        pass

class MoveAction(Action):
    pass

class ConsumeAction(Action):
    pass

class VanishAction(Action):
    pass
