from app.model import User

async def get(app, id_):
    pool = app['pool']

    async with pool.acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare('''
                select
                    id,
                    username,
                    password,
                    first_name,
                    middle_name,
                    last_name,
                    polynomial_coef,
                    roles
                from "user"
                where id = $1
            ''')
            result = await stmt.fetchrow(id_)
    return User(**dict(result.items()))


async def get_by_username(app, username):
    pool = app['pool']

    async with pool.acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare('''
                select
                    id,
                    username,
                    password,
                    first_name,
                    middle_name,
                    last_name,
                    polynomial_coef,
                    roles
                from "user"
                where username = $1
            ''')
            result = await stmt.fetchrow(username)
    return User(**dict(result.items()))


async def update(app, user):
    pool = app['pool']

    async with pool.acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare('''
                update "user" set
                  username=$2,
                  password=$3,
                  first_name=$4,
                  middle_name=$5,
                  last_name=$6,
                  polynomial_coef=$7,
                  roles=$8
                where id=$1
            ''')
            await stmt.fetch(
                user.id,
                user.username,
                user.password,
                user.first_name,
                user.middle_name,
                user.last_name,
                user.polynomial_coef,
                user.roles,
            )
    return user


async def create(app, user):
    pool = app['pool']
    async with pool.acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare('''
                insert into "user" (
                  username, password,
                  first_name, middle_name, last_name,
                  polynomial_coef, roles
                ) values (
                  $1, $2, $3, $4, $5, $6, $7
                )
            ''')
            await stmt.fetch(
                user.username,
                user.password,
                user.first_name,
                user.middle_name,
                user.last_name,
                user.polynomial_coef,
                user.roles,
            )


async def get_users_by_ids(app, ids):
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            stmt = await conn.prepare('''
                select
                    id,
                    username,
                    password,
                    first_name,
                    middle_name,
                    last_name,
                    polynomial_coef,
                    roles
                from "user"
                where id = any($1)
            ''')
            results = await stmt.fetch(ids)
    return {
        result['id']: User(**dict(result.items()))
        for result in results
    }
