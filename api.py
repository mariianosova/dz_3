import requests
from datetime import datetime, timedelta


def task_1():
    types = set()
    for _ in range(10):
        data = requests.get("https://official-joke-api.appspot.com/jokes/ten").json()
        for joke in data:
            types.add(joke["type"])
    for type in types:
        print(f'10 Jokes of type "{type}":')
        for joke in requests.get(
            f"https://official-joke-api.appspot.com/jokes/{type}/ten"
        ).json():
            print(joke["setup"], joke["punchline"])
        print()


def task_2(from_currency, amount, to_currency):
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    rates = requests.get("https://open.er-api.com/v6/latest/USD").json()["rates"]
    return amount / rates[from_currency] * rates[to_currency]


def task_3():
    data = requests.get("https://api.publicapis.org/entries").json()["entries"]
    count_by_auth = {}
    count_on_github = 0
    count_by_category = {}
    for api in data:
        auth = api["Auth"]
        category = api["Category"]
        if auth not in count_by_auth:
            count_by_auth[auth] = 0
        if category not in count_by_category:
            count_by_category[category] = 0
        count_by_auth[auth] += 1
        count_by_category[category] += 1
        if "github" in api["Link"].lower():
            count_on_github += 1
    count_by_auth["None"] = count_by_auth[""]
    del count_by_auth[""]
    print("Percentage by auth:")
    for auth, count in count_by_auth.items():
        print(f"{auth}: {count * 100 / len(data)}")
    print()
    print("Deployed to github:", count_on_github)
    print()
    print("Count by category:")
    for category, count in count_by_category.items():
        print(f"{category}: {count}")


def task_4():
    sites = [
        site[1] for site in requests.get("https://kontests.net/api/v1/sites").json()
    ]
    contests = []
    for site in sites:
        if site == "toph":  # https://kontests.net/api/v1/toph error here
            continue
        contests += requests.get(f"https://kontests.net/api/v1/{site}").json()
    upper_date = datetime.now() + timedelta(days=15)
    print("Available contests in next 15 days:")
    for contest in contests:
        date = datetime.strptime(contest["start_time"][:10], "%Y-%m-%d")
        if date <= upper_date:
            print(contest["name"])


# workers_data = [{'name': "Ivan Ivanov", "currency": "RUB", "rate": 100}]
def task_5(workers):
    working_hours = 0
    for month in [3, 4, 5]:
        response = requests.get(
            f"https://isdayoff.ru/api/getdata?year=2022&month={month}"
        )
        if response.status_code != 200:
            raise ValueError("Non-200 response code")
        data = list(map(int, list(response.text)))
        for day_status in data:
            if day_status in [0, 4]:
                working_hours += 8
            elif day_status == 2:
                working_hours += 6
    for worker in workers:
        hourly_pay_in_rub = task_2(worker["currency"], worker["rate"], "RUB")
        print(f"{worker['name']} earned {hourly_pay_in_rub * working_hours} RUB")

task_1()
print("100 USD =>", task_2("USD", 100, "RUB"), "RUB")
print("100 RUB =>", task_2("RUB", 100, "EUR"), "EUR")
print("100 EUR =>", task_2("EUR", 100, "USD"), "USD")
task_3()
task_4()
task_5(
    [
        {"name": "Ivan Ivanov", "rate": 1000, "currency": "USD"},
        {"name": "Alex Random", "rate": 1000, "currency": "EUR"},
        {"name": "Athur Smith", "rate": 1000, "currency": "RUB"},
    ]
)
