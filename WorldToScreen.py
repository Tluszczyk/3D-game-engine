import math


class WorldToScreen:
    def __init__(self, SIZE):
        self.SIZE = SIZE
        self.distanceToScreen = 300

    def get_screen_coords(self, pos):
        x, y, z = pos

        if z == 0:
            return x*math.inf, y*math.inf

        if z < 0:
            x_res = self.SIZE[0] / 2 - 10*self.SIZE[0] * x * self.distanceToScreen / z
            y_res = self.SIZE[1] / 2 - 10*self.SIZE[1] * y * self.distanceToScreen / z
            return x_res, y_res

        x_res = self.SIZE[0] / 2 + x * self.distanceToScreen / z
        y_res = self.SIZE[1] / 2 + y * self.distanceToScreen / z

        return x_res, y_res

    def rotate_screen_point(self, pos, rot):
        x, y = pos
        at, bt = rot

        a, b = at * math.pi / 180, bt * math.pi / 180

        xRes = x * math.cos(a) - y * math.sin(a)
        yRes = x * math.sin(a) + y * math.cos(a)

        return xRes, yRes

    def rotate_point(self, pos, rot):
        x, y, z = pos
        at, bt, ct = rot

        a = at * math.pi / 180
        b = bt * math.pi / 180
        c = ct * math.pi / 180

        xRes = x * math.cos(a) - z * math.sin(a)
        zRes = x * math.sin(a) + z * math.cos(a)

        yRes = zRes * math.sin(b) + y * math.cos(b)
        zRes = zRes * math.cos(b) - y * math.sin(b)

        return xRes, yRes, zRes

    def rotate_world(self, world, rot):

        if rot == [0, 0, 0]: return world

        res = []

        for obj in world:
            res.append([])
            for sideAll in obj:
                side = sideAll[:-1]
                res[-1].append([])
                for point in side:
                    res[-1][-1].append(self.rotate_point(point, rot))
                res[-1][-1].append(sideAll[-1])

        return res

    def too_long_movement(self, vec):
        x, y, z = vec
        return abs(x + y) > 20

    def move_world(self, world, movement):
        res = []
        for obj in world:
            res.append([])
            for sideAll in obj:
                side = sideAll[:-1]
                res[-1].append([])
                for point in side:
                    x, y, z = point
                    res[-1][-1].append((x - movement[0], y - movement[1], z - movement[2]))
                res[-1][-1].append(sideAll[-1])

        return res

    @staticmethod
    def move_object(obj, movement):
        return [(x - movement[0], y - movement[1], z - movement[2]) for (x, y, z) in obj]

    def screenate_world(self, world):
        res = []
        for obj in world:
            for sideAll in obj:
                side = sideAll[:-1]
                res.append([])
                for point in side:
                    res[-1].append(self.get_screen_coords(point))
                res[-1].append(sideAll[-1])

        return res

    @staticmethod
    def sort_sides(sideAll):
        side = sideAll[:-1]
        center = [0, 0, 0]
        for point in side:
            for c in range(3):
                center[c] += point[c]

        return math.sqrt(center[0] ** 2 + center[1] ** 2 + center[2] ** 2)

    @staticmethod
    def sort_cubes(cube):
        center = [0, 0, 0]

        for sideAll in cube:
            side = sideAll[:-1]
            for point in side:
                for c in range(3):
                    center[c] += point[c]

        return math.sqrt(center[0] ** 2 + center[1] ** 2 + center[2] ** 2)

    def sort_world(self, world):
        res = []
        world.sort(reverse=True, key=self.sort_cubes)
        for cube in world:
            cube.sort(reverse=True, key=self.sort_sides)
            res.append(cube)
        return res

    @staticmethod
    def norm_sort(point):
        x, y = point
        return x

    @staticmethod
    def points_to_triangles(points):  # # Well ... not that nice actually
        triangles = []

        points = list(set(points))
        points.sort(key=WorldToScreen.norm_sort)

        for i1 in range(len(points)):
            for i2 in range(i1, len(points)):
                for i3 in range(i2, len(points)):
                    triangles.append([points[i1], points[i2], points[i3]])

        return triangles

    def sign(self, p1, p2, p3):
        p1x, p1y = p1
        p2x, p2y = p2
        p3x, p3y = p3
        return (p1x - p3x) * (p2y - p3y) - (p2x - p3x) * (p1y - p3y)

    def point_in_triangle(self, pt, v1, v2, v3):
        d1 = self.sign(pt, v1, v2);
        d2 = self.sign(pt, v2, v3);
        d3 = self.sign(pt, v3, v1);

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0);
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0);

        return not (has_neg and has_pos);

    def normalize_triangle(self, triangle):
        points = []

        ok = False
        for pt in triangle:
            for cd, i in zip(pt, range(2)):
                if 0 <= cd < self.SIZE[i]:
                    ok = True
        if not ok:
            return None

        for i in range(3):
            xa, ya = triangle[i]
            xb, yb = triangle[(i + 1) % 3]

            if 0 <= xa < self.SIZE[0] and 0 <= ya < self.SIZE[1]:
                points.append((xa, ya))

            if (xa - self.SIZE[0]) * (xb - self.SIZE[0]) < 0:
                y_temp = ((xa - self.SIZE[0]) * yb - (xb - self.SIZE[0]) * ya) / (
                        (xa - self.SIZE[0]) - (xb - self.SIZE[0]))
                if 0 <= y_temp < self.SIZE[1]:
                    points.append((self.SIZE[0], y_temp))

            if xa * xb < 0:
                y_temp = (xa * yb - xb * ya) / (xa - xb)

                if 0 <= y_temp < self.SIZE[1]:
                    points.append((0, y_temp))

            if (ya - self.SIZE[1]) * (yb - self.SIZE[1]) < 0:
                x_temp = (xa * (yb - self.SIZE[1]) - xb * (ya - self.SIZE[1])) / (
                        (yb - self.SIZE[1]) - (ya - self.SIZE[1]))

                if 0 <= x_temp < self.SIZE[0]:
                    points.append((x_temp, self.SIZE[1]))

            if ya * yb < 0:
                x_temp = (xa * yb - xb * ya) / (yb - ya)

                if 0 <= x_temp < self.SIZE[0]:
                    points.append((x_temp, 0))

            # if 0 <= xb < self.SIZE[0] and 0 <= yb < self.SIZE[1]:
            #     points.append((xb, yb))

        if len(points) == 0:
            return None

        # for p in points:
        #     x, y = p
        #     if x < 0:
        #         xR = 0
        #     elif x >= self.SIZE[0]:
        #         xR = self.SIZE[0]
        #     else:
        #         xR = x
        #
        #     if y < 0:
        #         yR = 0
        #     elif y >= self.SIZE[1]:
        #         yR = self.SIZE[1]
        #     else:
        #         yR = y
        #
        #     points_res.append((xR, yR))

        if self.point_in_triangle((0, 0), triangle[0], triangle[1], triangle[2]):
            points.append((0, 0))

        triangles = WorldToScreen.points_to_triangles(points)

        return triangles

    def normalizeScreen(self, world):
        res = []
        for sideAll in world:
            side = sideAll[:-1]
            norm = self.normalize_triangle(side)
            if norm is not None:
                for triangle in norm:
                    res.append(triangle)
                    res[-1].append(sideAll[-1])

        return res