def get_division(name):
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
            'weapons': weapons['D'],
        },
        'C': {
            'go_up_points': 100,
            'go_down_points': -1,
            'plane_type': 'airborne',
            'achieve_points': 50,
            'weapons': weapons['C'],
        },
        'B': {
            'go_up_points': 100,
            'go_down_points': -1,
            'plane_type': 'airborne',
            'achieve_points': 50,
            'weapons': weapons['B'],
        },
        'A': {
            'go_up_points': 100,
            'go_down_points': -1,
            'plane_type': 'airborne',
            'achieve_points': 50,
            'weapons': weapons['A'],
        }
    }

    return division[name]

def next_division(name):
    division = get_division(name)

    print division