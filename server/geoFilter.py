# Finds all buildings in list whose coordinates match those given
def getBuildingsInRange(allBuildings, userLat, userLng):

    # Set to a more realistic value like 0.001 to only find objects close to your coordinates. Please make sure that there are objects in the database which
    # are near you.    
    geoDistance = 1

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