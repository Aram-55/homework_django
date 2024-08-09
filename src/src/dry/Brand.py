def dry_brand(brand):
    data = {}
    if brand:
        data = {
            "id": brand.id,
            "name": brand.name
        }
    return data
