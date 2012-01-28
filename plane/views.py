from django.http import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from account.models import UserProfile
from battle.models import Battle
from plane.models import Plane, Coordinates, Positioning

@csrf_exempt
def position_coordinates(request, type):
    if request.method == 'POST':
        if type == 'plane1' or type == 'plane2' or type == 'plane3':
            #get POST variable
            owner = UserProfile.objects.get(user=request.user)
            #TODO: check if battle exists
            battle = Battle.objects.get(pk=request.POST.get('battleID'))
            x = request.POST.get('x')
            y = request.POST.get('y')

            #get or create the plane
            plane, created = Plane.objects.get_or_create(owner=owner, battle=battle, type=type)

            #make coordinates
            coordinates = Coordinates.objects.create(x=x, y=y)

            #TODO: check if coordinates haven't already taken by this plane
            Positioning.objects.create(plane=plane, coordinates=coordinates)

            return HttpResponse(simplejson.dumps({'message': 'success'}))

        return HttpResponse(simplejson.dumps({'error': 'Wrong type!'}))
    else:
        return HttpResponse('N0t here!')

def check_hit(plane, x, y):
    position = plane.positioning_set.all()
    k = True
    for positioning in position:
        if int(x) == int(positioning.coordinates.x) and int(y) == int(positioning.coordinates.y):
            if k:
                return 'head'
            return 'hit'
        k = False
    return False