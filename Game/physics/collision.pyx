import cython
from Game.graphic.cartesian cimport CartesianPlane, Vector2d
from Game.physics.body cimport object_body, FREE
from Game.math.util cimport LSI as line_segment_intersect
from Game.math.core cimport point2d

@cython.optimize.unpack_method_calls(False)
cdef class collision:

    def __cinit__(self, *args, **kwargs):
        pass

    def __init__(self, CartesianPlane plane) -> None:
        self.plane = plane

    cpdef void check(self, object_body b1, object_body b2):
        self.diagonal_intersect(b1, b2)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.cdivision(True)
    @cython.initializedcheck(False)
    cdef void diagonal_intersect(self, object_body body1, object_body body2):
        cdef object_body b1 = body1
        cdef object_body b2 = body2
        cdef int i, j, k
        cdef double dx = 0, dy = 0, val
        cdef (double, double) l1s
        cdef (double, double) l1e
        cdef (double, double) l2s
        cdef (double, double) l2e
        for k in range(2):
            if k == 1:
                if body2.type == FREE:
                    break
                else:
                    b1 = body2
                    b2 = body1
            dx = 0
            dy = 0
            l1s = self.plane.to_xy(b1.shape.plane.get_CENTER())
            for i in range(b1.shape.vertex_count):
                # check for every vertex of first shape against ...
                l1e = self.plane.to_xy((<Vector2d>b1.shape.vertices[i]).get_HEAD())
                l2s = self.plane.to_xy((<Vector2d>b2.shape.vertices[0]).get_HEAD())
                for j in range(b2.shape.vertex_count):
                    # ... every edge of second shape
                    if j > 0:
                        l2s = l2e
                    l2e = self.plane.to_xy((<Vector2d>b2.shape.vertices[(j+1)%b2.shape.vertex_count]).get_HEAD())
                    # check these two line segments are intersecting or not
                    val = line_segment_intersect(l1s[0], l1s[1], l1e[0], l1e[1], l2s[0], l2s[1], l2e[0], l2e[1])
                    if val != 0:
                        dx += (l1e[0] - l1s[0]) * (1 - val)
                        dy += (l1e[1] - l1s[1]) * (1 - val)
                        if b1.type == FREE:
                            b1.USR_resolve_collision_point((l1e[0] - l1s[0]) * val, (l1e[1] - l1s[1]) * val)
            if dx != 0 or dy != 0:
                b1.USR_resolve_collision(b2, (dx, dy))
