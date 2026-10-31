import pygame, time
pygame.mixer.init()                        # once, at the top
pygame.mixer.music.load("sounds_swaras/1_Sa.mp3")
pygame.mixer.music.play()
time.sleep(2)
pygame.mixer.music.load("sounds_swaras/2_Re.mp3")
pygame.mixer.music.play()
time.sleep(2)
pygame.mixer.music.load("sounds_swaras/3_Ga.mp3")
pygame.mixer.music.play()
time.sleep(2) 