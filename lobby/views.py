from lobby.models import WaitingUser
from account.models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from battle.views import create as create_battle
from django.http import HttpResponse
from django.utils import simplejson
from nodejs_server.views import connect_to_nodejs, send_message

@csrf_exempt
def join_lobby(request):

#    if request.method == 'POST':

        user = UserProfile.objects.get(user=request.user)
        waitingUsers = WaitingUser.objects.all()

        same = False

        for waitingUser in waitingUsers:
            checkResult = check_matching(user, waitingUser.user)

            if checkResult == "ok":
                battle = create_battle(user, waitingUser.user)
                message = '"firstUser":"' + str(user.user.id) + '", "secondUser":"' + str(waitingUser.user.id) + '", "battleId":"' + str(battle.id) + '"'
                send_message("new-battle", message)

                waitingUser.delete()
                return HttpResponse(simplejson.dumps({'battle': battle.id}))
            else:
                if checkResult == "same":
                    same = True

        if not same:
            waitingUser = WaitingUser.objects.create(user=user)
            waitingUser.save()

        return HttpResponse(simplejson.dumps({'not': 'waiting'}))

#    return HttpResponse('Not here!')

#checking the matching battle posibility
def check_matching(firstUser, secondUser):
    if firstUser == secondUser:
        return "same"
    return "ok"