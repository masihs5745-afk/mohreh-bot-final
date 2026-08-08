from aiogram import Bot


async def check_membership(
    bot: Bot,
    user_id: int,
    channel: str,
) -> bool:
    try:
        member = await bot.get_chat_member(
            chat_id=channel,
            user_id=user_id,
        )

        return member.status in {
            "member",
            "administrator",
            "creator",
        }

    except Exception:
        return False
