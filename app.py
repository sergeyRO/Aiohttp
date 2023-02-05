from aiohttp import web
from database import engine, Base
from views import AdsView

from flask import Flask, jsonify
from views import AdsView


async def context_orm(app: web.Application):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    yield
    await engine.dispose()


routes = web.RouteTableDef
app = web.Application()
app.cleanup_ctx.append(context_orm)
app.add_routes(
    [
        web.get('/ads/{id:\d+}/', AdsView),
        web.post('/ads/', AdsView),
        web.patch('/ads/{id:\d+}/', AdsView),
        web.delete('/ads/{id:\d+}/', AdsView)
    ]
)

if __name__ == '__main__':
    web.run_app(app)
# app.add_url_rule('/ads/<int:id>', view_func=AdsView.as_view('ads'), methods={'GET', 'PATCH', 'DELETE'})
# app.add_url_rule('/ads/', view_func=AdsView.as_view('ads_create'), methods={'POST'})
