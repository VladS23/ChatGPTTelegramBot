from aiogram import Bot, Dispatcher, executor, types
import openai
import gptconfig

bot = Bot(gptconfig.BOTTOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет!\nЯ GPT3 бот \nОтправь мне любое сообщение, начинающееся с !, а я тебе обязательно отвечу. Начни сообщение с !code если хочешь, чтобы я написал код")


@dp.message_handler()
async def echo(message: types.Message):
    if message.text[0] == "!":
        if message.from_user.id in gptconfig.WHITELIST:
            openai.api_key = gptconfig.API_KEY2
        else:
            openai.api_key = gptconfig.API_KEY1
        completion = openai.Completion.create(model="text-davinci-003",
                                              prompt=message.text[1::],
                                              temperature=0.7,
                                              max_tokens=2048,
                                              top_p=1.0,
                                              frequency_penalty=0,
                                              presence_penalty=0.0)
        await message.answer(completion.choices[0].text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
