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
        if building.lat < upperLatBound and building.lat > lowerLatBound and building.lng > leftLngBound and building.lng < rightLngBound:
            buildingsInRange.append(building)

    return buildingsInRange