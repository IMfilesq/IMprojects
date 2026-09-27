from examples.price_aso import price_aso
from examples.price_put import price_put
from examples.area_spread_fig import generate_aso_fig
from examples.put_fig import generate_put_fig

def main() -> None:
    price_aso()
    price_put()
    generate_aso_fig()
    generate_put_fig()

if __name__ == "__main__":
    main()