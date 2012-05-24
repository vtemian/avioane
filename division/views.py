class Divisions:
    def __init__(self):
        weapons = {
            'D': ['simple'],
            'C': ['double', 'armor'],
            'B': ['triple', 'radar'],
            'A': ['antena', 'nuclear']
        }
        self.divisions = {
            'D': {
                'go_up_points': 100,
                'go_down_points': -1,
                'plane_type': 'airborne',
                'achieve_points': 50,
                'matches': 10,
                'weapons': weapons['D']
            },
            'C': {
                'go_up_points': 100,
                'go_down_points': -1,
                'plane_type': 'mig',
                'achieve_points': 50,
                'matches': 100,
                'weapons': weapons['C']
            },
            'B': {
                'go_up_points': 100,
                'go_down_points': -1,
                'plane_type': 'mig',
                'achieve_points': 50,
                'matches': 500,
                'weapons': weapons['B']
            },
            'A': {
                'go_up_points': 100,
                'go_down_points': -1,
                'plane_type': 'mig',
                'achieve_points': 50,
                'matches': 1000,
                'weapons': weapons['A']
            }
        }

    def get_division_by_name(self, name):
        return self.divisions[name]

    def next_division(self, name):
        keys = ['D', 'C', 'B', 'A']

        my_division = keys.index(name)

        if not my_division:
            return keys[0], keys[1]
        else:
            if my_division == len(keys):
                return keys[my_division - 1], keys[my_division]
            else:
                return keys[my_division - 1], keys[my_division + 1]