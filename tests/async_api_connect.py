import aiohttp
import asyncio
from typing import Coroutine

async def fetch(session, url):
	print("Getting {}...".format(url))

	resp = await session.get(url)
	text = await resp.text()
	return "{}: Got {} bytes".format(url, len(text))

async def main():
	session = aiohttp.ClientSession()

	endpoints = ["https://github.com", "https://badgen.net", "https://google.com", "https://facebook.com"]
	tasks: list[Coroutine] = []

	for each_endpoints in endpoints:
		print("Pushed %s" % each_endpoints)
		tasks.append(fetch(session, each_endpoints))

	print(f"Tasks should contain the following: {tasks}")

	for task in asyncio.as_completed(tasks):
		print("Result > " +  await task)

	await session.close()

	return "Done."

loop = asyncio.get_event_loop()
main_loop = loop.run_until_complete(main())