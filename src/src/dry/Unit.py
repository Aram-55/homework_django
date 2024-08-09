def dry_unit(unit):
    data = {}
    if unit:
        data = {
            "id": unit.id,
            "code": unit.code if unit.code else "",
            "measure": unit.measure
        }
    return data
