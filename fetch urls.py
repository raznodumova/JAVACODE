import aiohttp
import asyncio
import json


async def fetch_url(session, url, semaphore):
    async with semaphore:
        try:
            async with session.get(url, timeout=10) as response:
                return url, response.status
        except Exception:
            return url, 0


async def fetch_urls(urls):
    semaphore = asyncio.Semaphore(5)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url, semaphore) for url in urls]
        results = await asyncio.gather(*tasks)

        # Форматируем результаты в словарь
        result_dict = {url: status for url, status in results}

        # Сохраняем результаты в файл
        with open('results.json', 'w') as f:
            for url, status in result_dict.items():
                json.dump({"url": url, "status_code": status}, f)
                f.write('\n')  # Для новой строки в файле


# Пример использования
if __name__ == "__main__":
    urls_to_fetch = [
        "https://example.com",
        "https://httpbin.org/status/404",
        "https://nonexistent.url",
        "https://httpbin.org/status/500",
        "https://httpbin.org/delay/5",  # Можно добавить задержку
    ]
    asyncio.run(fetch_urls(urls_to_fetch))
