def getBuildingsInRange(allBuildings, userLat, userLng):

    userLatFloat = float(userLat)
    userLngFloat = float(userLng)

    # upperLatBound = userLatFloat + 0.001
    # lowerLatBound = userLatFloat - 0.001
    # leftLngBound = userLngFloat - 0.001
    # rightLngBound = userLngFloat + 0.001

    upperLatBound = userLatFloat + 1
    lowerLatBound = userLatFloat - 1
    leftLngBound = userLngFloat - 1
    rightLngBound = userLngFloat + 1
    
    buildingsInRange = []

    for building in allBuildings:
        if float(building.lat) < upperLatBound and float(building.lat) > lowerLatBound and float(building.lng) > leftLngBound and float(building.lng) < rightLngBound:
            buildingsInRange.append(building)

    return buildingsInRange