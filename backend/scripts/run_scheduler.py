import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from backend.workers.tasks import billing, dunning, notifications


async def start_scheduler() -> None:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(billing.generate_billing_cycles.delay, "interval", hours=24, id="billing-cycles")
    scheduler.add_job(
        dunning.apply_dunning.delay,
        "cron",
        hour=1,
        minute=0,
        args=[1],
        id="dunning-workflow",
    )
    scheduler.add_job(
        notifications.send_notification.delay,
        "interval",
        minutes=5,
        args=["ops@dom.local", "scheduler heartbeat"],
        id="scheduler-heartbeat",
    )
    scheduler.start()
    while True:
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(start_scheduler())
