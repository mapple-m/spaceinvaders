liste = [x for x in range (100)]

liste2 = []
for x in liste:
    if x%2 != 0:
        liste2.append(x-1)
liste = liste2
print (liste)

"""
projectile2 = []
for j in range(12):
    rectAlien = pygame.Rect((positionAlien[j]), (33, 27))

    for pro in projectile:
        collision = rectAlien.collidepoint(pro)
        if collision:
            score += 1
            positionAlien[j] = (-1, -1)
        elif pro[1] > 5:
            projectile2.append((pro[0], pro[1] - 10))

projectile = projectile2"""

for j in range(12):
    rectAlien = pygame.Rect((positionAlien[j]), (33, 27))
