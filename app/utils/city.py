import aiohttp

from app.utils.generator import generate_random_email, generate_user_agent


async def get_city_name_from_coords(lat: float, lon: float) -> str | None:
    url = (
        f"https://nominatim.openstreetmap.org/reverse"
        f"?lat={lat}&lon={lon}&format=json&addressdetails=1"
    )
    headers = {
        "User-Agent": generate_user_agent(),
        "Referer": generate_random_email(),
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                print(f"Nominatim error: {resp.status}")
                return None

            data = await resp.json()
            address = data.get("address", {})

            for key in ["city", "town", "village", "municipality", "county"]:
                if key in address:
                    return address[key]

            return None
