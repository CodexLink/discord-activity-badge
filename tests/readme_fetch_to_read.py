import aiohttp
import asyncio
import os
from dotenv import find_dotenv, load_dotenv
async def main():

	load_dotenv(
		find_dotenv(
				filename="../.env",
				raise_error_if_not_found=True,
		)
	)

	session = aiohttp.ClientSession()
	base_auth = await session.get('https://api.github.com/', **{"auth": aiohttp.BasicAuth("CodexLink", os.environ["INPUT_WORKFLOW_TOKEN"])})

	print("%s Left to Rate Limited." % base_auth.headers["X-RateLimit-Remaining"])
	print(f"%s of Requests Max." % base_auth.headers["X-RateLimit-Limit"], end="\n\n")

	print(base_auth)

	# Once we got login. Get the repository README.
	# Display, make changes and then push it.

	# # GET README — Importing to Runtime to Modify.
	while True:
		try:
			repo_container = await session.get('https://api.github.com/repos/CodexLink/CodexLink/readme', headers={"accept": "application/vnd.github.v3.text"}, **{"auth": aiohttp.BasicAuth("CodexLink", os.environ["INPUT_WORKFLOW_TOKEN"])})

			from ast import literal_eval
			from base64 import b64decode

			print(repo_container)

			readme_file = repo_container.content.read_nowait()
			print(readme_file)

			data_decoded = literal_eval(readme_file.decode("utf-8"))
			print(data_decoded)

			data_sterilized = data_decoded["content"].replace("\n", "")
			break
		except Exception as Err:
			print("Error: %s" % Err)

	# For local testing only.
	with open("base64_output.md", "w", errors="ignore") as f:
		a = b64decode(data_sterilized)
		f.write(a.decode("ascii", errors='replace'))


	# # Make Changes by Identifying `identifier in the badge`
	# ! Keep note that, we can only modify atleast one of the badge if ever this is one existing. First Come, First Serve.
	# from re import compile, MULTILINE
	# from src.elements.constants import BADGE_REGEX_STRUCT_IDENTIFIER

	# compiled_regex = compile(BADGE_REGEX_STRUCT_IDENTIFIER) # Match() will be used to get only the beginning. We wouldn't want to match it per line. Single Occurence only.

	# with open("base64_output.md", "r") as _:
	# 	__ = _.read()
	# 	print("Open Output > ", __)
	# 	pattern_matched = compiled_regex.search(__, MULTILINE)
	# 	print("Regex Pattern > ", pattern_matched)

	# await session.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())