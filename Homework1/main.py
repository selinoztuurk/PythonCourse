import random


class Portfolio:
    cash = 0
    stocks = {}
    mutual_funds = {}
    log = []

    def addCash(self, amount):
        self.cash += amount
        new_log = f'Added cash: +${amount}, New cash amount: {self.cash}'
        self.log.append(new_log)

    def buyStock(self, num_shares, stock):
        if not isinstance(num_shares, int):
            new_log = f'Tried to buy stock, error due to non-integer number of shares'
            self.log.append(new_log)
            return
        self.cash -= stock.price * num_shares
        if stock.symbol in self.stocks:
            self.stocks[stock.symbol] += num_shares
        else:
            self.stocks[stock.symbol] = num_shares
        new_log = f'Bought new stock: {num_shares} {stock.symbol}, paid ${stock.price * num_shares} cash'
        self.log.append(new_log)

    def buyMutualFund(self, num_shares, mutual_fund):
        if not isinstance(num_shares, float):
            new_log = f'Tried to buy mutual fund, error due to integer number of shares'
            self.log.append(new_log)
            return
        self.cash -= num_shares
        if mutual_fund.symbol in self.stocks:
            self.mutual_funds[mutual_fund.symbol] += num_shares
        else:
            self.mutual_funds[mutual_fund.symbol] = num_shares
        new_log = f'Bought new mutual fund: {num_shares} {mutual_fund.symbol}, paid ${num_shares} cash'
        self.log.append(new_log)

    def sellStock(self, stock_symbol, num_shares):
        if not isinstance(num_shares, int):
            new_log = f'Tried to sell stock, error due to non-integer number of shares'
            self.log.append(new_log)
            return
        if stock_symbol in self.stocks:
            x = self.stocks[stock_symbol]
            if x >= num_shares:
                sell_price = random.uniform(x*0.5, x*1.5)
                self.cash += sell_price * num_shares
                new_log = f'Sold stock: {num_shares} {stock_symbol}, at price {sell_price} for each share'
                self.log.append(new_log)
            else:
                new_log = f'Tried to sell {num_shares} shares of {stock_symbol}, ' \
                          f'error due to insufficient amount of shares.'
                self.log.append(new_log)
        else:
            new_log = f'Tried to sell {num_shares} shares of {stock_symbol}, '\
                      f'error due to lack of {stock_symbol} in the portfolio.'
            self.log.append(new_log)

    def sellMutualFund(self, mutual_fund_symbol, num_shares):
        if not isinstance(num_shares, float):
            new_log = f'Tried to sell mutual fund, error due to integer number of shares'
            self.log.append(new_log)
            return
        if mutual_fund_symbol in self.mutual_funds:
            x = self.mutual_funds[mutual_fund_symbol]
            if x >= num_shares:
                sell_price = random.uniform(0.9, 1.2)
                self.cash += sell_price * num_shares
                new_log = f'Sold mutual fund: {num_shares} {mutual_fund_symbol}, at price {sell_price} for each share'
                self.log.append(new_log)
            else:
                new_log = f'Tried to sell {num_shares} shares of {mutual_fund_symbol},'\
                          f'error due to insufficient amount of shares.'
                self.log.append(new_log)
        else:
            new_log = f'Tried to sell {num_shares} "shares of {mutual_fund_symbol},'\
                      f'error due to lack of {mutual_fund_symbol} in the portfolio.'
            self.log.append(new_log)

    def withdrawCash(self, amount):
        if self.cash >= amount:
            self.cash -= amount
            new_log = f'Withdrew cash: -${amount}, New cash amount: {self.cash}'
            self.log.append(new_log)
        else:
            new_log = f'Tried to withdraw ${amount}, error due to lack of cash.'
            self.log.append(new_log)

    def __str__(self):
        nicely_formatted_stocks = ""
        for stock in self.stocks:
            new_line = f'\n{self.stocks[stock]} {stock}'
            nicely_formatted_stocks += str(new_line)
        nicely_formatted_mfs = ""
        for mf in self.mutual_funds:
            new_line = f'\n{self.mutual_funds[mf]} {mf}'
            nicely_formatted_mfs += str(new_line)
        return f'\nCurrent Portfolio: \nCash: ${self.cash} \nStock: {nicely_formatted_stocks} \nMutual funds: {nicely_formatted_mfs}'

    def history(self):
        print("\nTransaction History:")
        for log in self.log:
            print(log)


class Investment:

    def __init__(self, symbol):
        self.symbol = symbol


class Stock(Investment):

    def __init__(self, price, symbol):
        super().__init__(symbol)
        self.price = price


class MutualFund(Investment):

    pass


portfolio = Portfolio()
portfolio.addCash(300.50)
s = Stock(20, "HFH")
portfolio.buyStock(5, s)
mf1 = MutualFund("BRT")
mf2 = MutualFund("GHT")
portfolio.buyMutualFund(10.3, mf1)
portfolio.buyMutualFund(2, mf2)
print(portfolio)
portfolio.sellMutualFund("BRT", 3)
portfolio.sellStock("HFH", 1)
portfolio.withdrawCash(50)
portfolio.history()

# additional test cases

portfolio.withdrawCash(150)  # error
portfolio.addCash(500)

portfolio.buyStock(10.5, "HFH")  # error
portfolio.sellStock(10.5, "HFH")  # error
portfolio.buyMutualFund(10, "BRT")  # error
portfolio.sellMutualFund(10, "BRT")  # error

print(portfolio)
portfolio.history()


# bonus

class Bond(Investment):

    pass


