from division.models import Division

def get_division(name):
    try:
        division = Division.objects.get(name=name)
    except Exception:
        division = create_division(name)

def create_division(name):
    weapons = {
        'D': ['simple'],
        'C': ['double', 'armor'],
        'B': ['triple', 'radar'],
        'A': ['antena', 'nuclear']
    }

    division = {
        'D': {
            'go_up_points': 100,
            'go_down_points': -1,
            'plane_type': 'airborne',
            'achieve_points': 50,
        },
        'C': {
            'go_up_points': 100,
            'go_down_points': -1,
            'plane_type': 'airborne',
            'achieve_points': 50,
        },
        'B': {
            'go_up_points': 100,
            'go_down_points': -1,
            'plane_type': 'airborne',
            'achieve_points': 50,
        },
        'A': {
            'go_up_points': 100,
            'go_down_points': -1,
            'plane_type': 'airborne',
            'achieve_points': 50,
        }
    }