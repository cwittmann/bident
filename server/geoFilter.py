def getBuildingsInRange(allBuildings, userLat, userLng):

    #geoDistance = 0.001
    geoDistance = 10

    userLatFloat = float(userLat)
    userLngFloat = float(userLng)    

    upperLatBound = userLatFloat + geoDistance
    lowerLatBound = userLatFloat - geoDistance
    leftLngBound = userLngFloat - geoDistance
    rightLngBound = userLngFloat + geoDistance
    
    buildingsInRange = []

    for building in allBuildings:
        if float(building.lat) < upperLatBound and float(building.lat) > lowerLatBound and float(building.lng) > leftLngBound and float(building.lng) < rightLngBound:
            buildingsInRange.append(building)

    return buildingsInRange