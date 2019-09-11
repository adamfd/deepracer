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
    center_variance = distance_from_center / (track_width/2)

    #required heading
    req_headingr = math.atan2(x - wp_coord[0], y - wp_coord[1])
    req_heading = math.degrees(req_headingr)

    #if the heading is 1-5 degrees reward move towards the outside of the track
    #if the heading is >15 reward moving to cut in to the corner
    #Where no bend reward being on the centre

    if wp_coord[0] > x and wp_coord[1] > y:
    #car is turning left
        if is_left_of_center == False:
            #near the start of a corner, reward being on the outside for racing line
            if abs(req_heading) > 1 and abs(req_heading) < 5:
                if center_variance > 0.5:
                    reward *= 1.1 
                else:
                    reward *= 1.0   #no change if on the correct side of the rack
        else:
            #deeper in a corner take the side of the corner
            if abs(req_heading) >15:
                if center_variance > 0.5:
                    reward *= 1.1        
                else:
                    reward *= 1.0   #no change if on the right side of the rack     
            #punish being on the inside of the corner when a gentle curve
            if abs(req_heading) > 1 and abs(req_heading) < 5:
                if center_variance > 0.5:
                    reward *= 1.0

    elif wp_coord[0] > x and wp_coord[1] < y:    
    #car is turning right
        if is_left_of_center == True:
            #near the start of a corner, reward being on the outside for racing line
            if abs(req_heading) > 1 and abs(req_heading) < 5:
                if center_variance > 0.5:
                    reward *= 1.1
                else:
                    reward *=1.0    #no change if on the correct side of the rack
        else:
            #deeper in a corner take the inside 
            if abs(req_heading) >15:
                if center_variance > 0.5:
                    reward *= 1.1 
                else:
                    reward *=1.0    #no change if on the correct side of the rack                    
            #punish being on the inside of the corner when a gentle curve
            if abs(req_heading) > 1 and abs(req_heading) < 5:
                if center_variance > 0.5:
                    reward *= 1.0

    elif wp_coord[0] < x and wp_coord[1] < y:
    #car is turning left
        if is_left_of_center == False:
            #near the start of a corner, reward being on the outside for racing line
            if abs(req_heading) > 1 and abs(req_heading) < 5:
                if center_variance > 0.5:
                    reward *= 1.1 
                else:
                    reward *=1.0    #no change if on the correct side of the rack
        else:
            #deeper in a corner take the out side of the corner
            if abs(req_heading) >15:
                if center_variance > 0.5:
                    reward *= 1.1    
                else:
                    reward *=1.0    #no change if on the correct side of the rack
            #punish being on the inside of the corner when a gentle curve
            if abs(req_heading) > 1 and abs(req_heading) < 5:
                if center_variance > 0.5:
                    reward *= 1.0

    elif wp_coord[0] <x and wp_coord[1] > y:
    #car is turning right
        if is_left_of_center == True:
            #near the start of a corner, reward being on the outside for racing line
            if abs(req_heading) > 1 and abs(req_heading) < 5:
                if center_variance > 0.5:
                    reward *= 1.1 
                else:
                    reward *=1.0     #no change if on the correct side of the rack
        else:
            #deeper in a corner take the side of the corner
            if abs(req_heading) >15:
                if center_variance > 0.5:
                    reward *= 1.1  
                else:
                    reward *=1.0     #no change if on the correct side of the rack
            #punish being on thze outside of the corner when a gentle curve
            if abs(req_heading) > 1 and abs(req_heading) < 5:
                if center_variance > 0.5:
                    reward *= 1

    #check if only x or y coord changes - hence going in a straight line
    elif wp_coord[0] == x or wp_coord[1] == y:
    #car is on a straight line
                if center_variance == 0:
                    reward *= 1.1 #reward being on the centreline
                elif centre_variance > 0.2:
                    reward *= 1.0 #punish being too far off centre

    # Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 25

    # Penalize reward if the car is steering too much - additional re-enforcement for being too far off
    if steering_angle > ABS_STEERING_THRESHOLD:
        reward *= 0.5

    # penalize reward for the car taking slow actions
    # speed is in m/s
    # updated for current space of 8ms and 3 granularity
    # we penalize as a ratio of how much slower than the threshold
    if speed == 8  and abs(steering_angle) == 0:
        reward *= 1.1
    elif speed >5 and abs(steering_angle) == 10:
        reward *= 1.1
    elif speed <6 and abs(steering_angle) == 20:
        reward *= 1.1
    elif speed <5 and abs(steering_angle) == 30:
        reward *= 1.5

    if all_wheels_on_track:
        # Reward for staying on the track
        reward *=  1.05
        
    if center_variance > 1.0:
        # Penalize for being too far off centre
        reward = 1e-3
        
    return reward