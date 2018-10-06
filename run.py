from settings import BB_USERNAME, BB_PASSWORD
from belarusbank.utils import get_bb_cards_balance


def run():
    print(tuple(get_bb_cards_balance(BB_USERNAME, BB_PASSWORD)))


if __name__ == '__main__':
    run()
