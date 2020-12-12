from django.contrib import admin

from auctions.models import User, auction_listing, bids, comments, watchlist, wonitems

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "password")
    list_editable = ("username", "email", "password")

class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "poster", "poster_id", "name", "desc", "price", "image_url", "category", "closed")
    list_editable = ("name", "desc", "price", "image_url", "category", "closed")
    list_display_links = ("id", "poster", "poster_id")

class BidsAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "username_id", "starting", "price")
    list_editable = ("starting", "price")
    list_display_links = ("id", "username", "username_id", "username_id")

class CommentsAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "listing_item", "listing_item_id", "user_comment")
    list_editable = ("username", "user_comment")
    list_display_links = ("id", "listing_item", "listing_item_id")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "user_id", "item_name", "item_id")
    list_display_links = ("user", "user_id", "item_id")

class WonitemsAdmin(admin.ModelAdmin):
    list_display = ("id", "won_username", "won_username_id", "item_name", "won_items_price")
    list_display_links = ("won_username", "won_username_id", "item_name")

# Register your models here.
admin.register(User),
admin.register(auction_listing),
admin.register(bids),
admin.register(comments),
admin.register(watchlist),
admin.register(wonitems)

admin.site.register(auction_listing, AuctionAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(bids, BidsAdmin)
admin.site.register(comments, CommentsAdmin)
admin.site.register(watchlist, WatchlistAdmin)
admin.site.register(wonitems, WonitemsAdmin)