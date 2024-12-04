
# -*- coding: utf-8 -*-
# meta developer: @YourTelegramUsername
# meta description: Поиск сообщений по ключевым словам во всех чатах с детальной информацией.
# meta license: MIT

from .. import loader, utils
import datetime

@loader.tds
class SearchMessagesByKeywordsMod(loader.Module):
    """Модуль для поиска сообщений по ключевым словам во всех чатах с деталями."""

    strings = {"name": "SearchMessagesByKeywords"}

    async def poisksocmd(self, message):
        """
        .poiskso (@username) (ключевые слова) - Поиск сообщений по ключевым словам.
        """
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "❌ Укажите: (@username или пропустите) (ключевые слова)")
            return

        args_split = args.split(" ", 1)
        target_user = None
        keywords = ""

        # Определение пользователя и ключевых слов
        if len(args_split) == 2 and args_split[0].startswith("@"):
            target_user = args_split[0].strip("@")
            keywords = args_split[1].strip()
        else:
            keywords = args.strip()

        if not keywords:
            await utils.answer(message, "❌ Укажите ключевые слова для поиска.")
            return

        await utils.answer(message, f"🔍 Начинаю поиск по ключевым словам: '{keywords}'...")

        results = []
        async for dialog in self._client.iter_dialogs():
            chat_id = dialog.id
            chat_name = dialog.name or "Неизвестный чат"
            async for msg in self._client.iter_messages(chat_id, search=keywords, from_user=target_user):
                # Форматирование данных
                msg_time = datetime.datetime.fromtimestamp(msg.date.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
                msg_link = f"https://t.me/c/{str(chat_id).replace('-100', '')}/{msg.id}"
                msg_author = msg.sender_id or "Неизвестный ID"
                
                # Добавляем в результаты
                results.append(
                    f"🔗 [Сообщение]({msg_link})\n"
                    f"🕒 Дата: {msg_time}\n"
                    f"👤 Автор: {msg_author}\n"
                )

        if results:
            await utils.answer(
                message,
                f"✅ Найдено {len(results)} сообщений:\n\n" + "\n\n".join(results[:50]) +
                ("\n\nИ многое другое..." if len(results) > 50 else "") + "\n\n🧡"
            )
        else:
            await utils.answer(message, "❌ Сообщения с такими ключевыми словами не найдены. 🧡")
