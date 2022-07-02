def reward_function(params):
    #                            #
    # Method: Follow center line #
    #                            #

    # Initialize the reward with typical value 
    reward = 1

    """ Reward when getting close to centerline """
    #   Step 1: Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    #   Step 2: Calculate 3 markers that are increasingly further away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    #   Step 3: Give high reward when close to center line and vice versa
    if distance_from_center <= marker_1:
        reward += 1
    elif distance_from_center <= marker_2:
        reward += 0.5
    elif distance_from_center <= marker_3:
        reward += 0.1
    else: # likely crashed / about to off track
        reward += 1e-3  
    
    """ Reward when on track & speedy
        Penalize when going off track or when moving slowly """
    # Step 1: Read input variables
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    # Step 2: Set the speed threshold based on the action space 
    SPEED_THRESHOLD = 1.0 
    # Step 3: Assign rewards and penalties 
    if not all_wheels_on_track:
        reward += 1e-3
    elif speed < SPEED_THRESHOLD:
        reward += 0.5
    else:
        reward += 1.0

    """ Penalize on excessive steering """    
    # Step 1: Read input variable
    steering = abs(params['steering_angle']) # Direction (neg/Pos) isn't important here, thus used abs()
    # Step 2: Set the steering threshold based on the action space
    ABS_STEERING_THRESHOLD = 0.5
    # Step 3: Assign the penalty
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    """ Reward when num of steps taken to finish the track is minimized """    
    # Setp 1: Read input variable
    steps = params['steps']
    progress = params['progress']
    # Step 2: Set total num of steps to finish the lap, based on the track length
    TOTAL_NUM_STEPS = 300
    # Step 3: Reward if the car pass every 100 steps faster than expected 
    if (steps % 100) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100 :
        reward += 10.0
        
    return float(reward)
