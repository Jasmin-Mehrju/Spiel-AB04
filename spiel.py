import os
import pygame


class Settings:
    WINDOW = pygame.rect.Rect(0, 0, 1080, 780)
    FPS = 60
    FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    IMAGE_PATH = os.path.join(FILE_PATH, "images")


class Defender(pygame.sprite.Sprite):
    def __init__(self, image_file, size, pos):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, image_file)).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


class Attacker(pygame.sprite.Sprite):
    def __init__(self, image_file, size, pos, speedx, speedy):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, image_file)).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.speedx = speedx
        self.speedy = speedy

    def update(self):
        self.rect = self.rect.move(self.speedx, self.speedy)
        if self.rect.left < 0 or self.rect.right > Settings.WINDOW.width:
            self.speedx *= -1
        if self.rect.top < 0 or self.rect.bottom > Settings.WINDOW.height:
            self.speedy *= -1


class Game():
    def __init__(self):
        os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 50"
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption("Eigenes Spiel")
        self.clock = pygame.time.Clock()

        self.defenders = pygame.sprite.Group()
        self.disciple = Defender("disciple.png", (70, 80), (Settings.WINDOW.width // 2, Settings.WINDOW.height // 2))
        self.defenders.add(self.disciple)

        self.gnu = Defender("gnu.png", (120, 120), (40, Settings.WINDOW.height - 100))
        self.defenders.add(self.gnu)

        self.shadow = Defender("shadow.png", (90, 80), (Settings.WINDOW.width - 90, Settings.WINDOW.height - 80))
        self.defenders.add(self.shadow)

        self.minion = Defender("minion.png", (70, 80), (Settings.WINDOW.width // 2 - 35, 0))
        self.defenders.add(self.minion)

        self.mage = Defender("mage.png", (90, 80), (Settings.WINDOW.width - 90, 100))
        self.defenders.add(self.mage)


        self.attackers = pygame.sprite.Group()
        self.fire = Attacker("fire.png", (40, 40), (10, 80), 5, 1)
        self.attackers.add(self.fire)

        self.dragon =  Attacker("dragon.png", (90, 80), (10, 80), -3, 3)
        self.attackers.add(self.dragon)

        self.androma = Attacker("androma.png", (80, 90), (10, 80), 4, -1)
        self.attackers.add(self.androma)

        self.image_background = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "background.png")).convert()
        self.image_background = pygame.transform.scale(self.image_background, Settings.WINDOW.size)

        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.watch_for_events()
            self.update()
            self.draw()

            self.clock.tick(Settings.FPS)
        pygame.quit()


    def draw(self):
        self.screen.blit(self.image_background, (0, 0))
        self.defenders.draw(self.screen)
        self.attackers.draw(self.screen)
        pygame.display.flip()


    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


    def update(self):
        self.defenders.update()
        self.attackers.update()

        collisions = pygame.sprite.groupcollide(self.attackers, self.defenders, False, True)

        for attacker, defenders in collisions.items():
            attacker.speedx *= -1
            attacker.speedy *= -1

        attacker_collisions = pygame.sprite.groupcollide(self.attackers, self.attackers, False, False)
        for attacker1, attackers2 in attacker_collisions.items():
            for attacker2 in attackers2:
                if attacker1 != attacker2:
                    if attacker1.rect.colliderect(attacker2.rect):
                        attacker1.speedx *= -1
                        attacker1.speedy *= -1
                        attacker2.speedx *= -1
                        attacker2.speedy *= -1


def main():
        game = Game()
        game.run()
    

if __name__ == "__main__":
    main()

