# -*- coding: utf-8 -*-

MAX_THREADS_PER_DAY = 100
MAX_COMMENTS_PER_DAY = 500
MAX_VOTES_PER_DAY = 2000

MAX_USERNAME = 80
MAX_EMAIL = 200
MAX_PASSW = 200

# User status
DEAD = 0
ALIVE = 1

STATUS = {
    DEAD: 'dead',
    ALIVE: 'alive',
}

# User role
ADMIN = 2
STAFF = 1
USER = 0

ROLE = {
    ADMIN: 'admin',
    STAFF: 'staff',
    USER: 'user',
}
