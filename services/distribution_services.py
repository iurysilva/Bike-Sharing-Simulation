def get_percentage(total, value):
    return (value * 100)/total


def get_amount_of_resources(resource_amount, list_of_stations, popularity):
    total = 0
    for station in list_of_stations:
        total += list_of_stations[station].from_station_number
    percentage = (get_percentage(total, popularity))/100
    amount = resource_amount * percentage
    return amount
