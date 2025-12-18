import asyncio

from backend.app.db import get_session


async def seed() -> None:
    async for session in get_session():
        # TODO: seed initial tenants, rooms, and meters
        print("Seeding database with demo data...")
        break


if __name__ == "__main__":
    asyncio.run(seed())
