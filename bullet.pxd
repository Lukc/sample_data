
cdef class SampleBullet(Bullet):
    cdef public target
    cdef public grazed
    cdef public double speed

    cdef custom_update
    cdef public custom_attributes

