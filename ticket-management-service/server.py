import asyncio
import datetime
import json
import uuid

import aiohttp_cors
from aiohttp import web
import db_connector

routes = web.RouteTableDef()


@routes.post("/check_ticket_closable")
async def check_ticket_closable(request):
    print("test")
    return web.json_response({"status": "OK", "can_close": True})


@routes.post("/close_ticket")
async def close_ticket(request):
    return web.json_response({"status": "OK", "closed": True})


@routes.post("/set_close_date")
async def set_close_date(request):
    return web.json_response({"status": "OK", "closed": True})


@routes.post("/reset_close_date")
async def reset_close_date(request):
    return web.json_response({"status": "OK", "closed": True})


@routes.get("/test")
async def test(request):
    db_connector.add_event(instance_id=str(uuid.uuid4()),
                           close_timestamp=datetime.datetime.now() + datetime.timedelta(days=7))
    return web.json_response({"status": "OK", "closed": True})


async def setup_app(app):
    db_connector.setup_db()


app = None


def run():
    global app

    app = web.Application()
    app.on_startup.append(setup_app)
    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods="*",
            )
        },
    )
    app.add_routes(routes)
    for route in list(app.router.routes()):
        cors.add(route)
    return app


async def serve():
    return run()


if __name__ == "__main__":
    app = run()
    web.run_app(app, port=8088)
