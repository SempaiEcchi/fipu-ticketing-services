import json

import aiohttp_cors
from aiohttp import web

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
    web.run_app(app, port=8088)
