from account.models import UserStats, UserDivision

class Divisions:
    def __init__(self):
        self.keys = ['D', 'C', 'B', 'A']

        weapons = {
            'D': ['simple'],
            'C': ['double', 'armor'],
            'B': ['triple', 'radar'],
            'A': ['antena', 'nuclear']
        }
        self.divisions = {
            'D': {
                'go_up_points': 10,
                'go_down_points': -1,
                'plane_type': 'airborne',
                'achieve_points': 50,
                'matches': 10,
                'weapons': weapons['D']
            },
            'C': {
                'go_up_points': 100,
                'go_down_points': 50,
                'plane_type': 'mig',
                'achieve_points': 50,
                'matches': 100,
                'weapons': weapons['C']
            },
            'B': {
                'go_up_points': 1000,
                'go_down_points': 500,
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

    def divisions_ranking(self, name):
        return self.keys.index(name) +1

    def next_division(self, name):
        my_division = self.keys.index(name)

        if not my_division:
            return self.keys[0], self.keys[1]
        else:
            if my_division == len(self.keys):
                return self.keys[my_division - 1], self.keys[my_division]
            else:
                return self.keys[my_division - 1], self.keys[my_division + 1]

    def go_up(self, win_division):
        try:
            new_division = self.keys[self.divisions_ranking(win_division.name)]
            win_division.name = new_division
            win_division.points = 0
            win_division.matches_played = 0
            win_division.save()
        except Exception as exp:
            print exp.message

    def go_down(self, loss_division):
        try:

            new_division = self.keys[self.divisions_ranking(loss_division.name) -2]
            loss_division.name = new_division
            loss_division.points = 0
            loss_division.matches_played = 0
            loss_division.save()

        except Exception as exp:
            print exp.message

    def check_division(self, win, loss):
        win = UserStats.objects.get(user=win)
        loss = UserStats.objects.get(user=loss)

        win_division = UserDivision.objects.get(user = win)
        loss_division = UserDivision.objects.get(user = loss)

        win_points = loss.lvl * self.divisions_ranking(loss_division.name) + win.lvl * self.divisions_ranking(win_division.name)
        loss_points = win_points / 2
        win_division.points += win_points



        loss_division.points -= loss_points
        if loss_division.points < 0:
            loss_division.points = 0

        loss_division.matches_played += 1
        win_division.matches_played += 1

        if win_division.points >= self.get_division_by_name(win_division.name)['go_up_points']:
            self.go_up(win_division)

        if loss_division.matches_played == self.get_division_by_name(loss_division.name)['matches']:
            self.go_down(loss_division)

        win_division.save()
        loss_division.save()
