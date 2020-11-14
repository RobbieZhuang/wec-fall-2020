from copy import deepcopy

#one at a time
# only one robot will be away from base and active at a given point in time
# we will try sending each robot on a "trip" which will be an out and back, cleaning along the way
# at each point, we will choose to keep the trip that results in the best score

def one_at_a_time_strat(trip_strat, game_state):
    while True:
        best_game_state = game_state
        for i in range(len(game_state.robots)):
            new_game_state = trip_strat(i, deepcopy(game_state))

            if new_game_state.get_stranded() > 0:
                print('Warning: robots stranded after trip completed')
            
            max_score = best_game_state.get_score(count_stranding=True)
            new_score = new_game_state.get_score(count_stranding=True)
    
            if new_score > max_score:
                best_game_state = new_game_state

        if best_game_state == game_state:
            break
        
        game_state = best_game_state

    return game_state
