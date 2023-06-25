import asyncio
import aiohttp

API_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date="


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


async def get_exchange_rates(date):
    url = API_URL + date
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, url)
        return response['exchangeRate']


async def main():

    dates = ['10.06.2023', '09.06.2023', '08.06.2023', '07.06.2023', '06.06.2023',
             '05.06.2023', '04.06.2023', '03.06.2023', '02.06.2023', '01.06.2023']

    tasks = []
    for date in dates:
        tasks.append(get_exchange_rates(date))

    results = await asyncio.gather(*tasks)

    formatted_results = []
    for i, result in enumerate(results):
        formatted_result = {dates[i]: {'EUR': {'sale': None, 'purchase': None},
                                       'USD': {'sale': None, 'purchase': None}}}

        for rate in result:
            if rate['currency'] == 'EUR':
                formatted_result[dates[i]]['EUR']['sale'] = rate['saleRate']
                formatted_result[dates[i]
                                 ]['EUR']['purchase'] = rate['purchaseRate']
            elif rate['currency'] == 'USD':
                formatted_result[dates[i]]['USD']['sale'] = rate['saleRate']
                formatted_result[dates[i]
                                 ]['USD']['purchase'] = rate['purchaseRate']

        formatted_results.append(formatted_result)

    print(formatted_results)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
