class QuoteDB:
    def __init__(self):
        # Load DB here
        self.quotes = ["test quote 1", "test quote 2", "test quote 3"]

    def get_quotes(self) -> list:
        return self.quotes

    def add_quote(self, quote) -> None:
        self.quotes.append(quote)

    def remove_quote(self, quote) -> None:
        self.quotes.remove(quote)

    def random_quote(self, quote) -> None:
        # Put randomisation logic here, simplest way is just random.choice
        raise NotImplementedError
