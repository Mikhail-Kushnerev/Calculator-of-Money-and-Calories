import datetime as dt

FORMAT = '%d.%m.%Y'


class Calculator:
    """Ведение расчётов."""

    def __init__(self, limit):
        self.records = []
        self.limit = limit

    def add_record(self, record):
        """Новая запись (число: кол-во калорий или деньги)"""

        self.records.append(record)

    def get_today_stats(self):
        """Суточная трата."""

        today = (dt.datetime.now()).date()
        today_amount = sum(record.amount for record in self.records
                           if record.date == today)
        return today_amount

    def get_week_stats(self):
        """Траты за неделю."""

        today = (dt.datetime.now()).date()
        end_week = today - dt.timedelta(days=7)
        week_amount = sum(record.amount for record in self.records
                          if end_week <= record.date <= today)
        return week_amount


class CashCalculator(Calculator):
    """Калькулятор денег."""

    USD_RATE = 60.0
    EURO_RATE = 70.0

    def get_today_cash_remained(self, currency):
        """Подчсёт деняг в валюте."""

        money = {
            'rub': ('руб', 1.0),
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE)
        }
        coin, rate = money[currency]
        remained = self.limit - self.get_today_stats()
        cash = abs(round(remained / rate, 2))
        if currency not in money:
            return 'Некорректное значение'
        if self.get_today_stats() == self.limit:
            return 'Денег нет, держись'
        if self.get_today_stats() < self.limit:
            return f'На сегодня осталось {cash} {coin}'
        return f'Денег нет, держись: твой долг - {cash} {coin}'


class CaloriesCalculator(Calculator):
    """Калькулятор калорий."""

    def get_calories_remained(self):
        """Остаток калорий"""

        remained = self.limit - self.get_today_stats()
        if self.get_today_stats() < self.limit:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {remained} '
                    'кКал')
        return 'Хватит есть!'


class Record:
    """Создание записей."""

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = date
        if date is not None:
            self.date = (dt.datetime.strptime(date, FORMAT)).date()
        else:
            self.date = (dt.datetime.now()).date()
