from aiohttp import web
from sqlalchemy.exc import IntegrityError

from database import Session, Ads
import json


async def get_ads(id_ads: int, session: Session):
    ads = await session.get(Ads, id_ads)
    if ads is None:
        raise web.HTTPNotFound(
            text=json.dumps({'status': 'Ads not found'}),
            content_type='application/json'
        )
    return ads


class AdsView(web.View):
    async def get(self):
        id_ads = int(self.request.match_info['id'])
        async with Session() as session:
            ads = await get_ads(id_ads, session)
            return web.json_response({
                'id': ads.id,
                'title': ads.title,
                'desc': ads.desc,
                'created_at': ads.created_at.isoformat()
            })

    async def post(self):
        ads_data = await self.request.json()
        async with Session() as session:
            new_ads = Ads(**ads_data)
            session.add(new_ads)
            try:
                await session.commit()
            except IntegrityError as er:
                raise web.HTTPConflict(
                    text=json.dumps({'status': 'error', 'desc': 'ads already exists'}),
                    content_type='application/json'
                )
            return web.json_response({
                'id_ads': new_ads.id, 'title': new_ads.title
            })

    async def patch(self):
        id_ads = int(self.request.match_info['id'])
        data_ads = await self.request.json()
        async with Session() as session:
            ads = await get_ads(id_ads, session)
            for field, value in data_ads.items():
                setattr(ads, field, value)
                session.add(ads)
                await session.commit()
            return web.json_response({'status': 'success'})

    async def delete(self):
        data_ads = int(self.request.match_info['id'])
        async with Session() as session:
            ads = await get_ads(data_ads, session)
            await session.delete(ads)
            await session.commit()
            return web.json_response({'status': 'deleted'})
