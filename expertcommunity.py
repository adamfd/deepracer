def reward_function(params):
    all_wheels_on_track = params['all_wheels_on_track']
    x = params['x']
    y = params['y']
    distance_from_center = params['distance_from_center']
    heading = params['heading']
    steering = params['steering']
    track_width = params['track_width']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    all_wheels_on_track = params['all_wheels_on_track']
    is_left_of_center = params['is_left_of_center']

    reward = 1e-3

    wp_coord = [0, 0]
    next_coord = [0, 0]

    # Reward when car is pointed to the next waypoint

    # Find next nearest waypoint coordinates
    wp_coord = [waypoints[closest_waypoints+1][0], waypoints[closest_waypoints+1][1]]

    # Calculate the hypotenuse of the triangle - i.e. the radius of the circle drawn from current location to next
    radius = math.hypot(x - wp_coord[0], y - wp_coord[1])

    # work out where you would go based on the current car direction measured -180 to 180 on x measured from a left direction on the map
    if heading <= 90 and heading >= 0:
        car_orientation_off_axis = heading
        next_coord[0] = x + (radius * math.cos(car_orientation_off_axis))
        next_coord[1] = y + (radius * math.sin(car_orientation_off_axis))
    elif heading >90 
        car_orientation_off_axis =  = 180 - heading
        next_coord[0] = x + (radius * math.cos(car_orientation_off_axis))
        next_coord[1] = y + (radius * math.sin(car_orientation_off_axis))
    elif heading >=-90 and heading <0:
        car_orientation_off_axis = 
        next_coord[0] = x + (radius * math.cos(car_orientation_off_axis))
        next_coord[1] = y + (radius * math.sin(car_orientation_off_axis))
    elsif heading <-90:
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
    center_variance = distance_from_center / track_width
    


    # Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 30

    # Penalize reward if the car is steering too much - additional re-enforcement for being too far off
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.5

    # penalize reward for the car taking slow actions
    # speed is in m/s
    # the below assumes your action space has a maximum speed of 5 m/s and speed granularity of 3
    # we penalize as a ratio of how much slower than the threshold
    SPEED_THRESHOLD = 4.5
    if speed < SPEED_THRESHOLD:
        reward *= (speed / SPEED_THRESHOLD)

    return reward
