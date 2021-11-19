import asyncio

import quotequail
import requests
from aiohttp import web
from imap_tools import *
from email_data import *

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

    while False:
        await asyncio.sleep(timeout)
        await stuff()


async def check_mailbox():
    global imap_client

    imap_client = MailBox('imap.gmail.com')
    imap_client.login(EMAIL, PASSWORD, initial_folder='INBOX')
    subjects = [msg.html for msg in imap_client.fetch(AND(all=True, seen=False), mark_seen=False)]

    subjects = list(map(lambda x: (quotequail.unwrap_html(x) or {}).get("html_top") or x, subjects))
    print("fetched" + str(subjects))
    imap_client.logout()


async def create_instance() -> str:
    response = requests.post(
        bpmn_url + "model/ticketing.bpmn/instance",
        timeout=5,
    )
    id = dict(response.json()).get("id")
    print(id)
    return id


async def call_receive_mail_task(instance_id: str, email_data: EmailData):
    data = email_data.__dict__
    response = requests.post(
        bpmn_url + f"instance/{instance_id}/task/primi_mail/receive",
        timeout=5,
        json=data

    )
    print("sent")


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
    web.run_app(app, port=8087)
