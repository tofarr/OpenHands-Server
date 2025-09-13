

from uuid import UUID

DEFAULT_USER_ID = UUID('00000000-0000-0000-0000-000000000000')

# TODO: Replace this with an actual user id from authentication - this is a dummy

async def get_user_id() -> UUID:
    return DEFAULT_USER_ID
