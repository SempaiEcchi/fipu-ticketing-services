import asyncio

import aiohttp_cors
from aiohttp import web

from env import *

routes = web.RouteTableDef()


@routes.post("/save_ticket")
async def save_ticket(request):
    print("test")
    return web.json_response({"status": "OK"})

@routes.post("/close_ticket")
async def save_ticket(request):
    print("test")
    return web.json_response({"status": "OK"})



@routes.post("/save_conversation")
async def save_reply(request):
    print("test")
    return web.json_response({"status": "OK"})


app = None


def run():
    global app

    app = web.Application()
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
    web.run_app(app, port=8087)
