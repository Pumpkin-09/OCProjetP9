from django.contrib import admin

from book_reviews.models import Ticket, Review, UserFollows
from authentication.models import User

admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)
admin.site.register(User)
