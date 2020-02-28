import pygame as pg
import WorldToScreen
import GetWorld
import math

pg.init()

SIZE = (600, 600)
SPEED = 0.3
ROTSPEED = 2.5

screen = pg.display.set_mode(SIZE)
gameON = True

w2S = WorldToScreen.WorldToScreen(SIZE)
gW = GetWorld.GetWorld()

objectsW = gW.readWorld()
objectsW = gW.generateWorld(objectsW[0])
OBJECTSW = objectsW

playerPos = [0, 0, 0]
playerRot = [0, 0, 0]

pg.mouse.set_visible(False)
pg.event.set_grab(True)

while gameON:
    objectsW = OBJECTSW

    # EVENT LOOP COMMENCE
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameON = False
            break

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                gameON = False
                break

        if event.type == pg.MOUSEMOTION:
            x, y = pg.mouse.get_rel()

            k = 1
            if x == y == 0:
                k = 0
            else:
                k = math.sqrt(ROTSPEED ** 2 / (x ** 2 + y ** 2))
            a, b = x * k, y * k

            if -90 <= playerRot[1] + b <= 90:
                playerRot = [playerRot[0] + a, playerRot[1] + b, 0]

    # EVENT LOOP TERMINATE

    movement = [0, 0, 0]

    if pg.key.get_pressed()[pg.K_a]:  movement[0] -= SPEED
    if pg.key.get_pressed()[pg.K_d]:  movement[0] += SPEED
    if pg.key.get_pressed()[pg.K_w]:  movement[2] += SPEED
    if pg.key.get_pressed()[pg.K_s]:  movement[2] -= SPEED
    if pg.key.get_pressed()[pg.K_LSHIFT]:  movement[1] += SPEED
    if pg.key.get_pressed()[pg.K_SPACE]:  movement[1] -= SPEED

    mv = w2S.rotate_screen_point(movement[0::2], [-playerRot[0], playerRot[1]])
    playerPos = [c+m for c, m in zip(playerPos, [mv[0],movement[1],mv[1]])]

    objectsW = w2S.move_world(objectsW, playerPos)
    objectsW = w2S.rotate_world(objectsW, (playerRot[0], -playerRot[1], playerRot[2]))

    objectsW = w2S.sort_world(objectsW)

    pointsS = w2S.screenate_world(objectsW)
    pointsS = w2S.normalizeScreen(pointsS)

    screen.fill(pg.Color(0, 0, 0))

    i = 0
    for pAll in pointsS:
        r, g, b = pAll[-1]
        p = pAll[:-1]

        pg.draw.polygon(screen, pg.Color(r, g, b), p)

        i += 1
        i %= len(pAll[-1])

    pg.display.update()

pg.quit()
quit()
