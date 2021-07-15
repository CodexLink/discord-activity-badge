import aiohttp
import asyncio

async def fetch(session, url):
	print("Getting {}...".format(url))

	resp = await session.get(url)
	text = await resp.text()
	print(dir(resp))
	print(resp)
	return "{}: Got {} bytes".format(url, len(text))

async def main():
	__session = aiohttp.ClientSession()

	__endpoints = ["https://github.com", "https://badgen.net", "https://google.com", "https://facebook.com"]
	tasks = []

	for each_endpoints in __endpoints:
		tasks.append(fetch(__session, each_endpoints))

	print(f"Tasks should contain the following: {tasks}")

	for task in asyncio.as_completed(tasks):
		print(await task)

	await __session.close()

	return "Done."

loop = asyncio.get_event_loop()
main_loop = loop.run_until_complete(main())