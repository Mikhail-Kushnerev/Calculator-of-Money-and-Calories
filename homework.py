import datetime as dt

FORMAT = '%d.%m.%Y'


class Calculator:
    """Ведение расчётов."""

    def __init__(self, limit):
        self.records = []
        self.limit = limit

    def add_record(self, record):
        """Новая запись (число: кол-во калорий или денег)"""

        self.records.append(record)

    def get_today_stats(self):
        """Суточная трата."""

        today = dt.datetime.today()
        today_amount = sum(record.amount for record in self.records
                           if record.date == today.date())
        return today_amount

    def get_week_stats(self):
        """Траты за неделю."""

        today = dt.datetime.today()
        end_week = today - dt.timedelta(days=7)
        week_amount = sum(record.amount for record in self.records
                          if end_week.date() <= record.date <= today.date())
        return week_amount

    def remained(self):
        """Остаток."""

        return self.limit - self.get_today_stats()


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
        if currency not in money:
            return 'Некорректное значение'
        if self.get_today_stats() == self.limit:
            return 'Денег нет, держись'
        remained = self.remained()
        coin, rate = money[currency]
        cash = abs(round(remained / rate, 2))
        if self.get_today_stats() < self.limit:
            return f'На сегодня осталось {cash} {coin}'
        return f'Денег нет, держись: твой долг - {cash} {coin}'


class CaloriesCalculator(Calculator):
    """Калькулятор калорий."""

    def get_calories_remained(self):
        """Остаток калорий"""

        remained = self.remained()
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
            self.date = dt.datetime.strptime(date, FORMAT).date()
        else:
            self.date = dt.datetime.now().date()
