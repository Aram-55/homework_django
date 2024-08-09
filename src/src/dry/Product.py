from .Unit import dry_unit
from .Brand import dry_brand


def dry_product(product):
    data = {
        "unit": dry_unit(product.unit),
        "brand": dry_brand(product.brand),
        "code": product.code if product.code else "",
        "name": product.name,
        "weight": product.weight if product.weight else "",
        "buy_date": product.buy_date if product.buy_date else "",
        "type": product.type,
        "comment": product.comment if product.comment else ""
    }
    return data
