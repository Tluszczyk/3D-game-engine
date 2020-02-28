class GetWorld:
    def __init__(self):
        self.world = []

        self.worldRF = open("Objects").readlines()
        self.worldF = open("Objects")

    def readWorld(self):
        for line in self.worldRF:
            if line[0] == '@':
                self.world.append([])

            elif line[0] == '#':
                self.world[-1].append([])

            elif line[0] != '@' and line[0] != 'c':
                a = [int(coord) for coord in line.split(" ")]
                self.world[-1][-1].append((a[0], a[1], a[2]))

            elif line[0] == 'c':
                a = [int(coord) for coord in line[2:].split(" ")]
                self.world[-1][-1].append((a[0], a[1], a[2]))

        return self.world

    def generateWorld(self, obj):
        worldRF = open("Labirynth").readlines()
        world = []

        for line, y in zip(worldRF, range(len(worldRF))):
            for cube, x in zip(line, range(len(line))):
                if cube == '#':
                    world.append([])
                    for sideAll in obj:
                        side = sideAll[:-1]
                        world[-1].append([])
                        for point in side:
                            (xC, yC, zC) = point
                            cubeTmp = (xC+2*x, yC+2*y, zC)
                            world[-1][-1].append(cubeTmp)
                        world[-1][-1].append(sideAll[-1])

        return world