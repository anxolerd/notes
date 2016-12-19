from app.model import Note


async def get(app, id_):
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare('''
                select
                  id,
                  author_id,
                  category_id,
                  title,
                  text
                from "note"
                where id = $1
            ''')
            result = await stmt.fetchrow(id_)
    return Note(**dict(result.items()))


async def get_by_author_id(app, author_id):
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare('''
                select
                  id,
                  author_id,
                  category_id,
                  title,
                  text
                from "note"
                where author_id = $1
            ''')
            results = await stmt.fetch(author_id)
    return [
        Note(**dict(result.items()))
        for result in results
    ]


async def get_by_category_id(app, category_id):
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare('''
                select
                  id,
                  author_id,
                  category_id,
                  title,
                  text
                from "note"
                where category_id = $1
            ''')
            results = await stmt.fetch(category_id)
    return [
        Note(**dict(result.items()))
        for result in results
    ]

async def update(app, note):
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare('''
                update "note" set
                  author_id=$2,
                  category_id=$3,
                  title=$4,
                  text=$5
                where id=$1
            ''')
            await stmt.fetch(
                note.id,
                note.author_id,
                note.category_id,
                note.title,
                note.text,
            )
    return note


async def create(app, note):
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare('''
                insert into "note" (
                  author_id, category_id,
                  title, text
                ) values ($1, $2, $3, $4)
            ''')
            await stmt.fetch(
                note.author_id,
                note.category_id,
                note.title,
                note.text,
            )
