def get_percentage(total, value):
    return (value * 100)/total


def get_amount_of_resources(resource_amount, list_of_values, value):
    total = 0
    for i in list_of_values:
        total += i
    percentage = (get_percentage(total, value))/100
    amount = resource_amount * percentage
    return amount
