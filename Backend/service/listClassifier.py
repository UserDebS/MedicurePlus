def listClassifier(data : list[dict[str, int | float | str]]) -> list[dict]:
    if(len(data) == 0):
        return []
    
    output = []
    classifier = {
        'id' : data[0]['id'],
        'total' : data[0]['cost'] * data[0]['quantity'],
        'placed' : data[0]['placed_at'],
        'orders' : [{
            'name' : data[0]['name'],
            'cost' : data[0]['cost'],
            'quantity' : data[0]['quantity']
        }]
    }

    for i in range(1, len(data)):
        if(data[i]['id'] == classifier['id']):
            classifier['total'] += data[i]['cost'] * data[i]['quantity']
            classifier['orders'].append({
                'name' : data[i]['name'],
                'cost' : data[i]['cost'],
                'quantity' : data[i]['quantity']
            })

        else:
            classifier.pop('id')
            output.append(classifier)
            classifier = {
                'id' : data[i]['id'],
                'total' : data[i]['cost'] * data[i]['quantity'],
                'placed' : data[i]['placed_at'],
                'orders' : [{
                    'name' : data[i]['name'],
                    'cost' : data[i]['cost'],
                    'quantity' : data[i]['quantity']
                } ]
            }
    classifier.pop('id')
    output.append(classifier)
    return output


if __name__ == '__main__':
    data = [
        {
            "id": 17,
            "name": "Naproxen",
            "cost": 68.97,
            "quantity": 20,
            "placed_at": "2024-11-12"
        },
        {
            "id": 17,
            "name": "Celecoxib",
            "cost": 99.92,
            "quantity": 10,
            "placed_at": "2024-11-12"
        },
        {
            "id": 16,
            "name": "Aspirin",
            "cost": 83.01,
            "quantity": 10,
            "placed_at": "2024-11-12"
        },
        {
            "id": 16,
            "name": "Acyclovir",
            "cost": 34.29,
            "quantity": 50,
            "placed_at": "2024-11-12"
        }
    ]
    print(listClassifier(data=data))