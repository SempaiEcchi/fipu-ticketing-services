import asyncio

from aiohttp import web
from imap_tools import *

from env import *

routes = web.RouteTableDef()


@routes.get("/test")
async def test(request):
    print("test")
    return web.json_response({"status": "OK"})


def handle_new_mail(email_listener, msg_dict):
    print(msg_dict.values())
    return web.json_response({"status": "OK"})


app = None
imap_client = None


async def periodic(timeout, stuff):
    await stuff()
    while True:
        await asyncio.sleep(timeout)
        await stuff()


async def check_mailbox():
    global imap_client

    imap_client = MailBox('imap.gmail.com')
    imap_client.login(EMAIL, PASSWORD, initial_folder='INBOX')
    subjects = [msg.html for msg in imap_client.fetch(AND(all=True, seen=False), mark_seen=False)]
    print("fetched" + str(subjects))
    imap_client.logout()


async def mail_listener(app):
    asyncio.create_task(periodic(5, check_mailbox))


async def close_imap(app):
    print("closing imap")
    global imap_client
    if isinstance(imap_client, MailBox):
        try:
            imap_client.logout()
        except (ValueError, Exception):
            print("error")


def run():
    global app

    app = web.Application()
    app.on_startup.append(mail_listener)
    app.on_shutdown.append(close_imap)
    app.add_routes(routes)

    return app


async def serve():
    return run()


if __name__ == "__main__":
    app = run()
    web.run_app(app, port=8081)
