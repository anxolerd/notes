from app.model import Category

async def get(app, id_):
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare('''
                select
                    id,
                    name,
                    allowed_roles
                from "category"
                where id = $1
            ''')
            result = await stmt.fetchrow(id_)
    return Category(**dict(result.items()))


async def get_by_name(app, name):
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare('''
                select
                    id,
                    name,
                    allowed_roles
                from "category"
                where name = $1
            ''')
            result = await stmt.fetchrow(name)
    return Category(**dict(result.items()))


async def get_by_roles(app, roles):
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare('''
                select
                    id,
                    name,
                    allowed_roles
                from "category"
                where allowed_roles && $1
            ''')
            results = await stmt.fetch(roles)
    return [
        Category(**dict(result.items()))
        for result in results
    ]


async def update(app, category):
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare('''
                update "category" set
                  name=$2,
                  allowed_roles=$3
                where id=$1
            ''')
            await stmt.fetch(
                category.id,
                category.name,
                category.allowed_roles,
            )
    return category


async def create(app, category):
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare('''
                insert into category (name, allowed_roles)
                values ($1, $2)
            ''')
            await stmt.fetch(category.name, category.allowed_roles)


async def get_all(app, limit, offset):
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare('''
                select id, name, allowed_roles
                from "category"
                order by id
                limit $1 offset $2
            ''')
            results = await stmt.fetch(limit, offset)
    return [
        Category(**dict(result.items()))
        for result in results
    ]
