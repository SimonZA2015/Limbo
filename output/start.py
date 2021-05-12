# ����������� ���������� PyGame
import pygame

# ������������� PyGame
pygame.init()

# ���� ����: ������, �������
gameScreen = pygame.display.set_mode((400, 300))

# ������ os - ������� ����
import os
x = 100
y = 100
os.environ['Sp_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

# ��������� ����
size = [500, 500]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Test drawings")
gameScreen.fill((0,0,255))
pygame.display.flip()
runGame = True # ���� ������ �� ����� ����
while runGame:
    # ������������ �������: "������� ����"
    for event in pygame.event.get():
        if event.type == pygame.QUIT: runGame = False
# ����� �� ����: 
pygame.quit()