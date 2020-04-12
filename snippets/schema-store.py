import argparse
import asyncio
import json
import traceback

import aiohttp
import freddy
import jsonschema


async def iterate_store_schemas():
    json_store_url = "http://schemastore.org/api/json/catalog.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(json_store_url) as resp:
            if resp.status != 200:
                raise Exception("Could not get json store url")
            catalog = await resp.json()

        for schema in catalog["schemas"]:
            url = schema["url"]
            try:
                async with session.get(url) as resp:
                    if resp.status == 404:
                        # Not found anymore
                        continue
                    if resp.status != 200:
                        print(f"Skipping {url}: {resp.status} {resp.reason}")
                        continue
                    try:
                        content_type = resp.content_type
                        if content_type == "text/plain":
                            content = await resp.text()
                            yield json.loads(content)
                        elif content_type in (
                            "application/json",
                            "application/octet-stream",
                        ):
                            content = await resp.content.read()
                            yield json.loads(content)
                        else:
                            print(
                                f"Skipping {url}: unknown content type: {content_type}"
                            )
                            continue
                    except KeyboardInterrupt:
                        raise
                    except Exception:
                        print(f"Skipping {url}: {traceback.print_exc()}")
                        continue
            except KeyboardInterrupt:
                raise
            except Exception:
                print(f"Skipping {url}: {traceback.print_exc()}")
                continue


async def run():
    results = {"total": 0, "invalid": 0, "success": 0}
    try:
        async for schema in iterate_store_schemas():
            results["total"] += 1
            try:
                sample = freddy.jsonschema(schema)
            except KeyboardInterrupt:
                raise
            except Exception as ex:
                kls = ex.__class__.__name__
                results.setdefault(str(kls), 0)
                results[str(kls)] += 1
                continue

            try:
                jsonschema.validate(sample, schema)
            except KeyboardInterrupt:
                raise
            except Exception:
                results["invalid"] += 1
            else:
                results["success"] += 1
        print(results)

    except KeyboardInterrupt:
        print("Halted")
        print(results)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
