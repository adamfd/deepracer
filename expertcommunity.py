def reward_function(params):
    all_wheels_on_track = params['all_wheels_on_track']
    x = params['x']
    y = params['y']
    distance_from_center = params['distance_from_center']
    heading = params['heading']
    steering_angle = params['steering_angle']
    track_width = params['track_width']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    all_wheels_on_track = params['all_wheels_on_track']
    is_left_of_center = params['is_left_of_center']
    speed = params['speed']
    

    import math
    
    reward = 1e-3

    wp_coord = [0, 0]
    next_coord = [0, 0]

    # Reward when car is pointed to the next waypoint

    # Find next nearest waypoint coordinates
    wp_coord = [(waypoints[closest_waypoints[1]])[0], (waypoints[closest_waypoints[1]])[1]]

    # Calculate the hypotenuse of the triangle - i.e. the radius of the circle drawn from current location to next
    radius = math.hypot(x - wp_coord[0], y - wp_coord[1])

    # work out where you would go based on the current car direction measured -180 to 180 on x measured from a left direction on the map
    if heading <= 90 and heading >= 0:
        car_orientation_off_axis = heading
        next_coord[0] = x + (radius * math.cos(car_orientation_off_axis))
        next_coord[1] = y + (radius * math.sin(car_orientation_off_axis))
    elif heading > 90:
        car_orientation_off_axis = 180 - heading
        next_coord[0] = x + (radius * math.cos(car_orientation_off_axis))
        next_coord[1] = y + (radius * math.sin(car_orientation_off_axis))
    elif heading >= -90 and heading < 0:
        car_orientation_off_axis = heading
        next_coord[0] = x + (radius * math.cos(car_orientation_off_axis))
        next_coord[1] = y + (radius * math.sin(car_orientation_off_axis))
    elif heading < -90:
        car_orientation_off_axis = -(180 + heading)
        next_coord[0] = x + (radius * math.cos(car_orientation_off_axis))
        next_coord[1] = y + (radius * math.sin(car_orientation_off_axis))

    # Calculate the delta of where we are going from the next way point
    coord_delta = math.hypot(next_coord[0] - wp_coord[0], next_coord[1] - wp_coord[1])

    # Max delta should be the radius * 2 - i.e. we're facing 180 in the wrong direction
    # Min distance means we are aimed to the next waypoint exactly

    if coord_delta == 0:
        reward += 10
    else:
        # up to change of 0 if facing the wrong way
        reward += 10 * (1 - (coord_delta / (radius * 2)))

    # Increase reward when the next way point is going in to the corner on the racing line    
    #Based on next waypoint, is car turning left or right
    center_variance = distance_from_center / track_width

    #required heading
    req_headingr = math.atan2(x - wp_coord[0], y - wp_coord[1])
    req_heading = math.degrees(req_headingr)

    #if the heading is 1-5 degrees reward move towards the outside of the track
    #if the heading is >15 reward moving to cut in to the corner
    

    ### make reward more granular - it goes out too quickly in the corner - need to have a more gradual move from inside the corner to outside...
    ### the reward diff can be too small between great and bad progress sometimes I think as well...

    if wp_coord[0] > x and wp_coord[1] > y:
        #car is turning left
        if abs(req_heading) > 5:
            if is_left_of_center == False:
                #near the start of a corner, enter from the far side of the rack
                if abs(req_heading) > 1 and abs(req_heading) < 5:
                    if center_variance > 0.8:
                        reward *= 1.5 
            else:
                #deeper in a corner take the side of the corner
                if abs(req_heading) >15:
                    if center_variance > 0.8:
                        reward *= 1.5                
    elif wp_coord[0] > x and wp_coord[1] < y:    
        #car is turning right
        if abs(req_heading) > 5:
            if is_left_of_center == True:
                #near the start of a corner, enter from the far side of the rack
                if abs(req_heading) > 1 and abs(req_heading) < 5:
                    if center_variance > 0.8:
                        reward *= 1.5
            else:
                #deeper in a corner take the side of the corner
                if abs(req_heading) >15:
                    if center_variance > 0.8:
                        reward *= 1.5   
    elif wp_coord[0] < x and wp_coord[1] < y:
        #car is turning left
        if abs(req_heading) > 5:
            if is_left_of_center == False:
                #near the start of a corner, enter from the far side of the rack
                if abs(req_heading) > 1 and abs(req_heading) < 5:
                    if center_variance > 0.8:
                        reward *= 1.5 
            else:
                #deeper in a corner take the side of the corner
                if abs(req_heading) >15:
                    if center_variance > 0.8:
                        reward *= 1.5    
    elif wp_coord[0] <x and wp_coord[1] > y:
        #car is turning right
        if abs(req_heading) > 5:
            if is_left_of_center == True:
                #near the start of a corner, enter from the far side of the rack
                if abs(req_heading) > 1 and abs(req_heading) < 5:
                    if center_variance > 0.8:
                        reward *= 1.5 
            else:
                #deeper in a corner take the side of the corner
                if abs(req_heading) >15:
                    if center_variance > 0.8:
                        reward *= 1.5   

    # Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 25

    # Penalize reward if the car is steering too much - additional re-enforcement for being too far off
    if steering_angle > ABS_STEERING_THRESHOLD:
        reward *= 0.5

    # penalize reward for the car taking slow actions
    # speed is in m/s
    # the below assumes your action space has a maximum speed of 5 m/s and speed granularity of 3
    # we penalize as a ratio of how much slower than the threshold
    SPEED_THRESHOLD = 3.5
    if speed < SPEED_THRESHOLD:
        reward *= (speed / SPEED_THRESHOLD)

    return reward