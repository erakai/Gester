from gester import sounds, Game, Entity


class SoundTest(Entity):
    def __init__(self, *args):
        super().__init__()
        sounds.create_sound("slots", "games/assets/slot-machine.wav")
        self.playing = False

    def think(self):
        if not self.playing:
            sounds.play_sound("slots")
            self.playing = True

    def render(self, surface):
        pass

    def start(self):
        pass


game = Game()
game.add_ent(SoundTest())
game.init(1280, 720, True)
