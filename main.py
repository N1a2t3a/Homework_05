import aiohttp
import asyncio
import argparse
import datetime
import json

# Функція для отримання обмінного курсу на певну дату та валюту
async def fetch_exchange_rate(date, currency):
    async with aiohttp.ClientSession() as session:
        url = f'https://api.privatbank.ua/p24api/exchangerates/exchangerates?json&date={date}'
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Error: Unable to fetch data for date {date}. Status code: {response.status}")
                return None
            
            data = await response.json()
            return data[currency]

# Основна функція програми
async def main(days, save_to_file=False):
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days)

    results = []

    # Отримання обмінного курсу для кожного дня у заданому діапазоні
    while start_date <= end_date:
        date_str = start_date.strftime('%d.%m.%Y')
        exchange_rates = {
            date_str: {
                'EUR': await fetch_exchange_rate(date_str, 'EUR'),
                'USD': await fetch_exchange_rate(date_str, 'USD')
            }
        }
        results.append(exchange_rates)
        start_date += datetime.timedelta(days=1)

    # Збереження результатів у JSON-файл 
    if save_to_file:
        with open('exchange_rates.json', 'w') as file:
            json.dump(results, file, indent=2)
        print("Exchange rates saved to 'exchange_rates.json'")

    print(results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get exchange rates for EUR and USD from PrivatBank API")
    parser.add_argument("days", type=int, help="Number of days to retrieve exchange rates for (up to 10 days)")
    parser.add_argument("--save", action="store_true", help="Save results to a JSON file")
    args = parser.parse_args()

    # Перевірка, чи не перевищено ліміт в 10 днів і виклик основної функції
    if args.days > 10:
        print("Error: You can only retrieve exchange rates for up to 10 days.")
    else:
        asyncio.run(main(args.days, args.save))



