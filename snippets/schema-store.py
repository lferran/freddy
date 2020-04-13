import asyncio
import json
import traceback

import aiohttp
import freddy
import jsonschema


async def get_schema(session, url):
    async with session.get(url) as resp:
        if resp.status == 404:
            return None

        if resp.status != 200:
            print(f"Skipping {url}: {resp.status} {resp.reason}")
            return None

        # Attempt to parse response content
        try:
            content_type = resp.content_type
            if content_type == "text/plain":
                content = await resp.text()
                return json.loads(content)

            elif content_type in ("application/json", "application/octet-stream"):
                content = await resp.content.read()
                return json.loads(content)

            else:
                print(f"Skipping {url}: unknown content type: {content_type}")
                return None

        except Exception:
            print(f"Skipping {url}: {traceback.print_exc()}")
            return None


async def iterate_store_schemas():
    json_store_url = "http://schemastore.org/api/json/catalog.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(json_store_url) as resp:
            if resp.status != 200:
                raise Exception("Could not get json store url")
            catalog = await resp.json()

        for schema_metadata in catalog["schemas"]:
            url = schema_metadata["url"]
            try:
                json_schema = await get_schema(session, url)
                if json_schema is not None:
                    yield json_schema
            except KeyboardInterrupt:
                raise
            except Exception:
                print(f"Skipping {url}: {traceback.print_exc()}")
                continue


def get_from_file():
    try:
        with open("snippets/store.json", "r") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return None
    except Exception:
        print("Error getting from file")
        return None


def store_in_file(results):
    with open("snippets/store.json", "w") as f:
        f.write(json.dumps(results))


async def load_schemas():
    all_schemas = get_from_file()
    if all_schemas is None:
        all_schemas = [s async for s in iterate_store_schemas()]
        store_in_file(all_schemas)
    return all_schemas


def check_schemas(all_schemas):
    results = {"total": 0, "invalid": [], "success": 0}
    try:
        for schema in all_schemas:
            results["total"] += 1
            # Try to generate a sample
            try:
                sample = freddy.jsonschema(schema)
            except KeyboardInterrupt:
                raise
            except Exception as ex:
                kls = ex.__class__.__name__
                results.setdefault(str(kls), [])
                results[str(kls)].append(schema)
                continue
            # Try to validate sample against schema
            try:
                jsonschema.validate(sample, schema)
            except KeyboardInterrupt:
                raise
            except Exception:
                results["invalid"].append(schema)
            else:
                results["success"] += 1
    except KeyboardInterrupt:
        print("Halted")
    finally:
        return results


async def run():
    all_schemas = await load_schemas()
    results = check_schemas(all_schemas)

    print("#" * 30)
    print(f"Total: {results.pop('total')}")
    print(f"Success: {results.pop('success')}")
    for err, v in results.items():
        print(f"{err}: {len(v)}")
    print("#" * 30)

    for sch in results["InvalidSchema"]:
        freddy.jsonschema(sch)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
