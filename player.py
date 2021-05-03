import pygame, time

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Pygame Keyboard Test')
pygame.mouse.set_visible(0)

key_sound = {
    pygame.K_SPACE: pygame.mixer.Sound("samples/bass.wav"),
    pygame.K_RSHIFT: pygame.mixer.Sound("samples/hat.wav"),
    pygame.K_LALT: pygame.mixer.Sound("samples/snare.wav"),
}

def loop():
    print("Spacebar= Bass")
    print("Right Shift = HiHat")
    print("Right Control = Snare")
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                key_sound[event.key].play()
            elif (event.type == pygame.QUIT):
                return

loop()