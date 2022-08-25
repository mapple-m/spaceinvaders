import pygame
import random

pygame.init()
pygame.mixer.init()

fenetre = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Space Invader Mariam")

arial = pygame.font.SysFont('arial', 15)
arialG = pygame.font.SysFont('arial', 60, True)

sonTir = pygame.mixer.Sound('tir.mp3')
sonExplosion = pygame.mixer.Sound('explosion.mp3')

imageVaisseau = pygame.image.load("vaisseau.png")
imageVaisseau = pygame.transform.scale(imageVaisseau, (64, 64))
positionVaisseau = (268, 525)

imageAlien = pygame.image.load("alien.png")
positionAlien = [(5, 10), (55, 10), (105, 10), (155, 10), (205, 10), (255, 10), (305, 10), (355, 10), (405, 10),
                 (455, 10), (505, 10), (555, 10)]
directionAlien = [True] * 12  # gauche

projectile = []
score = 0
nb_projectiles = 30
vie = 3

stars = [(random.randrange(0, 600), random.randrange(0, 600)) for i in range(50)]

positionBombe = positionAlien[random.randrange(0, 12)]
positionBonus = (random.randrange(10, 590), 10)


def dessiner():
    global imageAlien, imageVaisseau, fenetre, projectile, arial, score, stars, positionAlien, positionVaisseau, positionBombe, positionBonus
    fenetre.fill((0, 0, 0))

    for star in stars:
        pygame.draw.circle(fenetre, (255, 255, 255), star, 1)

    for alien in positionAlien:
        fenetre.blit(imageAlien, alien)

    for pro in projectile:
        pygame.draw.circle(fenetre, (255, 255, 255), pro, 5)

    fenetre.blit(imageVaisseau, positionVaisseau)

    pygame.draw.circle(fenetre, (255, 0, 0), positionBombe, 6)
    pygame.draw.circle(fenetre, (0, 255, 255), positionBonus, 8)

    affiche_score = arial.render('score : ' + str(score), True, pygame.Color(255, 255, 255))
    affiche_pro = arial.render('projectiles : ' + str(nb_projectiles), True, pygame.Color(255, 255, 255))
    affiche_vie = arial.render('vies : ' + str(vie), True, pygame.Color(255, 255, 255))
    fenetre.blit(affiche_score, (10, 10))
    fenetre.blit(affiche_pro, (10, 30))
    fenetre.blit(affiche_vie, (10, 50))

    pygame.display.flip()


def gererClavierEtSouris():
    global continuer, positionVaisseau, projectile, nb_projectiles
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = 0

    touchesPressees = pygame.key.get_pressed()
    if touchesPressees[pygame.K_SPACE]:
        if nb_projectiles > 0:
            sonTir.play()
            projectile.append((positionVaisseau[0] + 33.5, positionVaisseau[1]))
            nb_projectiles -= 1
    if touchesPressees[pygame.K_RIGHT]:
        if positionVaisseau[0] <= 535:
            positionVaisseau = (positionVaisseau[0] + 10, positionVaisseau[1])
    if touchesPressees[pygame.K_LEFT]:
        if positionVaisseau[0] >= 0:
            positionVaisseau = (positionVaisseau[0] - 10, positionVaisseau[1])


def fin():
    global arialG, continuer, score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = 0
    fenetre.fill((0, 0, 0))
    affiche_fin = arialG.render('GAME OVER', True, pygame.Color(255, 255, 255))
    affiche_score = arial.render('score : ' + str(score), True, pygame.Color(255, 255, 255))
    fenetre.blit(affiche_fin, (120, 250))
    fenetre.blit(affiche_score, (120, 350))
    pygame.display.flip()


clock = pygame.time.Clock()

continuer = 1
while continuer == 1:
    clock.tick(50)

    lost = False
    for alien in positionAlien:
        if alien[1] >= 500:
            lost = True

    if vie > 0 and nb_projectiles > 0 and not lost:
        dessiner()
        gererClavierEtSouris()
    else:
        fin()

    projectile2 = []
    for pro in projectile:
        if pro[1] > 5:
            projectile2.append((pro[0], pro[1] - 10))
    projectile = projectile2

    projectile2 = []
    for i in range(12):
        rectAlien = pygame.Rect((positionAlien[i]), (33, 27))
        for pro in projectile:
            collision = rectAlien.collidepoint(pro)
            if collision:
                sonExplosion.play()
                score += 1
                positionAlien[i] = (-30, 10)
                directionAlien[i] = False
                projectile2.append(pro)

    for pro in list(set(projectile2)):
        projectile.remove(pro)

    for i in range(12):
        if directionAlien[i]:
            positionAlien[i] = (positionAlien[i][0] - 2, positionAlien[i][1])
            if positionAlien[i][0] <= 0:
                directionAlien[i] = False
                positionAlien[i] = (positionAlien[i][0], positionAlien[i][1] + 30)
        else:
            positionAlien[i] = (positionAlien[i][0] + 2, positionAlien[i][1])
            if positionAlien[i][0] >= 567:
                directionAlien[i] = True
                positionAlien[i] = (positionAlien[i][0], positionAlien[i][1] + 30)

    for i in range(len(stars)):
        if stars[i][1] < 600:
            stars[i] = (stars[i][0], stars[i][1] + 1)
        else:
            stars[i] = (stars[i][0], 0)

    rectVaisseau = pygame.Rect((positionVaisseau), (64, 64))

    positionBombe = (positionBombe[0], positionBombe[1] + 10)
    if positionBombe[1] >= 600:
        positionBombe = positionAlien[random.randrange(0, 12)]
        positionBombe = (positionBombe[0] + (33 / 2), positionBombe[1] + 27)
    if rectVaisseau.collidepoint(positionBombe):
        positionBombe = (positionBombe[0], 600)
        vie -= 1

    positionBonus = (positionBonus[0], positionBonus[1] + 10)
    if positionBonus[1] >= 2000:
        positionBonus = (random.randrange(10, 590), 10)
    if rectVaisseau.collidepoint(positionBonus):
        positionBonus = (positionBonus[0], 600)
        nb_projectiles += 10

pygame.quit()
