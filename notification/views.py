from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from notification.models import Notification
#from profile.models import Friend
#
#def accept_friend(recipient, sender):
#    friend, created = Friend.objects.get_or_create(user=recipient.user)
#    friend.friends.add(sender)
#    friend.save()
#    friend, created = Friend.objects.get_or_create(user=sender.user)
#    friend.friends.add(recipient)
#    friend.save()
#
#def un_friend(recipient, sender):
#    friend = Friend.objects.get(user=recipient.user)
#    friend.friends.remove(sender)
#    friend.save()
#    friend = Friend.objects.get(user=sender.user)
#    friend.friends.remove(recipient)
#    friend.save()
#


@csrf_exempt
def seen_notification(request, notification_id):
    notification = Notification.objects.get(pk=notification_id)
    notification.seen = True
    notification.save()
    return HttpResponse('ok')