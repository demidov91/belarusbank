from belarusbank.utils import get_bb_cards_balance


def run():
    print(tuple(get_bb_cards_balance()))

if __name__ == '__main__':
    run()
