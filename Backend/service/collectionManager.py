def addDataToDict(a : dict, addKey : str | int | float, valMapFunc) -> dict:
    ret = {
        key : a[key] for key in a
    }
    ret.update({
        addKey : valMapFunc(ret['name'])
    })

    return ret

def addDataToDicts(a : list[dict], addKey : str | int | float, valMapFunc) -> list[dict]:
    ret = []
    for dct in a:
        tempDict = {
            key : dct[key] for key in dct
        }
        tempDict.update({
            addKey : valMapFunc(dct['name'])
        })
        ret.append(tempDict.copy())
        tempDict.clear()

    return ret