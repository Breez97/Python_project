import asyncio
import types
from config import token
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pyppeteer import launch
from bs4 import BeautifulSoup
import json
from program.creating_database import get_info_by_title
from aiogram.types import InputFile


bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())


class User(StatesGroup):
    restart = State()
    # diet
    choose_diet = State()
    set_diet = State()
    change_diet = State()
    change_diet_confirm = State()
    # calories
    info_calories = State()
    get_calories = State()
    set_calories = State()
    count_calories = State()
    change_answer = State()
    change_calories = State()
    # meals
    count_meals = State()
    set_meals = State()
    set_meals_fin = State()
    # info
    fin_info = State()
    info_answer = State()
    change_info = State()
    # parsing
    generation = State()
    show = State()
    choose_meal = State()
    # count_calories
    get_age = State()
    get_height = State()
    set_height = State()
    get_weight = State()
    set_weight = State()
    get_gender = State()
    set_gender = State()
    get_target = State()
    set_target = State()
    get_coefficient = State()
    set_coefficient = State()
    fin_calories = State()
    calories_answer = State()
    calculate_calories = State()
    confirm_calories = State()
    change_personal = State()
    change_age = State()
    change_height = State()
    change_weight = State()
    change_target = State()
    change_coefficient = State()
    confirm_age = State()
    confirm_height = State()
    confirm_weight = State()
    confirm_target = State()
    confirm_coefficient = State()
    confirm_regeneretaion = State()


async def show_info_dish(message: types.Message, dish):
    await message.answer(f"<b>{dish}</b>\n\n"
                         f"<i>Information on one serving:</i>\n"
                         f"· Calories: {get_info_by_title('calories', dish)}\n"
                         f"· Carbs: {get_info_by_title('carbs', dish)}\n"
                         f"· Fat: {get_info_by_title('fat', dish)}\n"
                         f"· Protein: {get_info_by_title('protein', dish)}",
                         parse_mode='HTML')
    file_url = get_info_by_title('image', dish)
    photo = InputFile.from_url(file_url)
    await bot.send_photo(chat_id=message.chat.id, photo=photo)


async def create_keyboard(buttons):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


@dp.message_handler(commands=["start"])
async def bot_start(message: types.Message):
    keyboard = await create_keyboard(["Let's try ⏩"])
    await message.answer("👋 <b>Hello, my friend! And welcome!</b>",
                         parse_mode='HTML')
    photo = InputFile.from_url("https://www.euroguidance-france.org/wp"
                               "-content/uploads/2020/03/diet-nutrition.jpg")
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.answer("🧑‍⚕️ I'm your personal nutritionist bot and I'll "
                         "help you to plan your own daily menu according"
                         "to your requests",
                         reply_markup=keyboard)
    await User.choose_diet.set()


@dp.message_handler(state=User.choose_diet)
async def choose_diet(message: types.Message):
    if message.text in ["Let's try ⏩", "Confirm ➡️"]:
        if message.text == "Confirm ➡️":
            await message.answer("Let's start from the beginning :)")
        keyboard = await create_keyboard(["Anything 🥪", "Paleo 🍖",
                                          "Vegetarian 🥦", "Vegan 🌱",
                                          "Ketogenic 🥙", "Mediterranean 🪔"])
        await message.answer("Choose the type of your diet.",
                             reply_markup=keyboard)
        await User.set_diet.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.set_diet)
async def set_diet(message: types.Message, state: FSMContext):
    if message.text in ["Anything 🥪", "Paleo 🍖", "Vegetarian 🥦", "Vegan 🌱", "Ketogenic 🥙", "Mediterranean 🪔"]:
        keyboard = await create_keyboard(["Continue ➡️"])
        await state.update_data(diet=message.text)
        await message.answer(f"Your choice: {message.text}",
                             reply_markup=keyboard)
        await User.info_calories.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.info_calories)
async def info_calories(message: types.Message):
    if message.text == "Continue ➡️":
        keyboard = await create_keyboard(["Yes ✅", "No ❌"])
        await message.answer("Do you know how many calories per day do you "
                             "need?", reply_markup=keyboard)
        await User.get_calories.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.get_calories)
async def get_calories(message: types.Message):
    if message.text in ["Yes ✅", "Change", "Change the amount of calories "
                                           "and meals"]:
        await message.answer("Input the amount of calories.",
                             reply_markup=types.ReplyKeyboardRemove())
        await User.set_calories.set()
    elif message.text == "No ❌":
        keyboard = await create_keyboard(["Count 🔢"])
        await message.answer("Let's count how many calories do you need.",
                             reply_markup=keyboard)
        await User.count_calories.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.count_calories)
async def count_calories(message: types.Message):
    if message.text == "Count 🔢":
        await message.answer("Ok. Let's count.")
        await message.answer("First of all. Input your age.",
                             reply_markup=types.ReplyKeyboardRemove())
        await User.get_age.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.get_age)
async def set_age(message: types.Message, state: FSMContext):
    age = message.text
    if age.isdigit():
        age = int(age)
        if 0 < age < 100:
            keyboard = await create_keyboard(["Continue ➡️"])
            await state.update_data(age=age)
            await message.answer(f"Your age: {age}", reply_markup=keyboard)
            await User.get_height.set()
        else:
            await message.answer("⚠️ Incorrect answer, try again. ⚠️")
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.get_height)
async def get_height(message: types.Message):
    if message.text == "Continue ➡️":
        await message.answer("Input your height in cm.",
                             reply_markup=types.ReplyKeyboardRemove())
        await User.set_height.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.set_height)
async def set_height(message: types.Message, state: FSMContext):
    height = message.text
    if height.isdigit():
        height = int(height)
        if 130 <= height <= 250:
            keyboard = await create_keyboard(["Continue ➡️"])
            await state.update_data(height=height)
            await message.answer(f"Your height in cm: {height}",
                                 reply_markup=keyboard)
            await User.get_weight.set()
        else:
            await message.answer("⚠️ Incorrect answer, try again. ⚠️")
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.get_weight)
async def get_weight(message: types.Message):
    if message.text == "Continue ➡️":
        await message.answer("Input your weight in kg.",
                             reply_markup=types.ReplyKeyboardRemove())
        await User.set_weight.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.set_weight)
async def set_weight(message: types.Message, state: FSMContext):
    weight = message.text
    if weight.isdigit():
        weight = int(weight)
        if 40 <= weight <= 150:
            keyboard = await create_keyboard(["Continue ➡️"])
            await state.update_data(weight=weight)
            await message.answer(f"Your weight in kg: {weight}",
                                 reply_markup=keyboard)
            await User.get_gender.set()
        else:
            await message.answer("⚠️ Incorrect answer, try again ⚠️")
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.get_gender)
async def get_gender(message: types.Message):
    if message.text == "Continue ➡️":
        keyboard = await create_keyboard(["Male 👨", "Female 👩"])
        await message.answer("Choose your gender.", reply_markup=keyboard)
        await User.set_gender.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.set_gender)
async def set_gender(message: types.Message, state: FSMContext):
    if message.text in ["Male 👨", "Female 👩"]:
        await state.update_data(gender=message.text)
        keyboard = await create_keyboard(["Continue ➡️"])
        await message.answer(f"Your gender: {message.text}",
                             reply_markup=keyboard)
        await User.get_target.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.get_target)
async def get_target(message: types.Message):
    if message.text == "Continue ➡️":
        keyboard = await create_keyboard(["Weight loss 🧘‍♀️",
                                          "Maintaining weight ⏲️",
                                          "Weight gain 💪"])
        await message.answer("Choose your target.", reply_markup=keyboard)
        await User.set_target.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.set_target)
async def set_target(message: types.Message, state: FSMContext):
    if message.text in ["Weight loss 🧘‍♀️", "Maintaining weight ⏲️",
                        "Weight gain 💪"]:
        keyboard = await create_keyboard(["Continue ➡️"])
        await message.answer(f"Your choice: {message.text}",
                             reply_markup=keyboard)
        await state.update_data(target=message.text)
        await User.get_coefficient.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.get_coefficient)
async def get_coefficient(message: types.Message):
    if message.text == "Continue ➡️":
        await message.answer("<b><i>--- Now I need your activity coefficient "
                             "---</i></b>\n"
                             "\n<b>Variants:</b>"
                             "\n· Low (~1,2) - Sedentary lifestyle, lack of "
                             "sports, less than 10 thousand steps per day."
                             "\n· Small (~1,38) - Work related to "
                             "walking/standing, not very intense workouts "
                             "1-3 times a week (exercise, yoga, pilates, "
                             "etc.)."
                             "\n· Average (~1,55) - Intensive sports "
                             "consistently 1-3 times a week, active lifestyle."
                             "\n· High (~1,73) - Sports daily."
                             "\n· Very high (~2,2) - hard physical work, "
                             "sports 2 times a day.", parse_mode='HTML')
        keyboard = await create_keyboard(["Low", "Small", "Average", "High",
                                          "Very high"])
        await message.answer("Choose the most suitable variant for you.",
                             reply_markup=keyboard)
        await User.set_coefficient.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.set_coefficient)
async def set_coefficient(message: types.Message, state: FSMContext):
    if message.text in ["Low", "Small", "Average", "High", "Very high"]:
        await state.update_data(coefficient=message.text)
        keyboard = await create_keyboard(["Continue ➡️"])
        await message.answer(f"Your choice: {message.text}",
                             reply_markup=keyboard)
        await User.fin_calories.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.fin_calories)
async def fin_calories(message: types.Message, state: FSMContext):
    if message.text in ["Continue ➡️", "Confirm ➡️"]:
        data = await state.get_data()
        await message.answer(f"<b><i>--- Information about you --- </i></b>\n\n"
                             f"· <b>Your age:</b> {data['age']}\n\n"
                             f"· <b>Your height in cm:</b> {data['height']}\n\n"
                             f"· <b>Your weight in kg:</b> {data['weight']}\n\n"
                             f"· <b>Your target:</b> {data['target']}\n\n"
                             f"· <b>Your activity coefficient:</b> "
                             f"{data['coefficient']}", parse_mode='HTML')
        keyboard = await create_keyboard(["Yes ✅", "No ❌"])
        await message.answer("Is the information correct? 🤔",
                             reply_markup=keyboard)
        await User.calories_answer.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.calories_answer)
async def calories_answer(message: types.Message):
    if message.text == "Yes ✅":
        keyboard = await create_keyboard(["Calculate 🖥"])
        await message.answer("Ok, fine. Let me calculate the suitable amount "
                             "of calories for you.", reply_markup=keyboard)
        await User.calculate_calories.set()
    elif message.text == "No ❌":
        keyboard = await create_keyboard(["Age", "Height", "Weight", "Target",
                                          "Activity coefficient"])
        await message.answer("What do you want to change?",
                             reply_markup=keyboard)
        await User.change_personal.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.change_personal)
async def change_personal(message: types.Message, state: FSMContext):
    keyboard = await create_keyboard(["Change"])
    if message.text == "Age":
        await message.answer("Let's change your age.", reply_markup=keyboard)
        await User.change_age.set()
    elif message.text == "Height":
        await message.answer("Let's change your height.",
                             reply_markup=keyboard)
        await User.change_height.set()
    elif message.text == "Weight":
        await message.answer("Let's change your weight.",
                             reply_markup=keyboard)
        await User.change_weight.set()
    elif message.text == "Target":
        await message.answer("Let's change your target.",
                             reply_markup=keyboard)
        await User.change_target.set()
    elif message.text == "Activity coefficient":
        await message.answer("Let's change your activity coefficient.",
                             reply_markup=keyboard)
        await User.change_coefficient.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.change_age)
async def change_age(message: types.Message):
    if message.text == "Change":
        await message.answer("Input your age",
                             reply_markup=types.ReplyKeyboardRemove())
        await User.confirm_age.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.confirm_age)
async def confirm_age(message: types.Message, state: FSMContext):
    age = message.text
    if age.isdigit():
        age = int(age)
        if 0 < age < 100:
            keyboard = await create_keyboard(["Confirm ➡️"])
            await state.update_data(age=age)
            await message.answer(f"Your changed age: {age}",
                                 reply_markup=keyboard)
            await User.fin_calories.set()
        else:
            await message.answer("⚠️ Incorrect answer, try again. ⚠️")
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.change_height)
async def change_age(message: types.Message):
    if message.text == "Change":
        await message.answer("Input your height",
                             reply_markup=types.ReplyKeyboardRemove())
        await User.confirm_height.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.confirm_height)
async def confirm_age(message: types.Message, state: FSMContext):
    height = message.text
    if height.isdigit():
        height = int(height)
        if 130 < height < 250:
            keyboard = await create_keyboard(["Confirm ➡️"])
            await state.update_data(height=height)
            await message.answer(f"Your changed height: {height}",
                                 reply_markup=keyboard)
            await User.fin_calories.set()
        else:
            await message.answer("⚠️ Incorrect answer, try again. ⚠️")
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.change_weight)
async def change_age(message: types.Message):
    if message.text == "Change":
        await message.answer("Input your height",
                             reply_markup=types.ReplyKeyboardRemove())
        await User.confirm_weight.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.confirm_weight)
async def confirm_age(message: types.Message, state: FSMContext):
    weight = message.text
    if weight.isdigit():
        weight = int(weight)
        if 40 < weight < 150:
            keyboard = await create_keyboard(["Confirm ➡️"])
            await state.update_data(weight=weight)
            await message.answer(f"Your changed weight: {weight}",
                                 reply_markup=keyboard)
            await User.fin_calories.set()
        else:
            await message.answer("⚠️ Incorrect answer, try again. ⚠️")
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.change_target)
async def change_target(message: types.Message):
    if message.text == "Change":
        keyboard = await create_keyboard(["Weight loss 🧘‍♀️",
                                          "Maintaining weight ⏲️",
                                          "Weight gain 💪"])
        await message.answer("Choose your target.",
                             reply_markup=keyboard)
        await User.confirm_target.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.confirm_target)
async def set_target(message: types.Message, state: FSMContext):
    if message.text in ["Weight loss 🧘‍♀️", "Maintaining weight ⏲️",
                        "Weight gain 💪"]:
        keyboard = await create_keyboard(["Confirm ➡️"])
        await message.answer(f"Your changed target: {message.text}",
                             reply_markup=keyboard)
        await state.update_data(target=message.text)
        await User.fin_calories.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.change_coefficient)
async def get_coefficient(message: types.Message):
    if message.text == "Change":
        await message.answer("<b>Variants:</b>"
                             "\n· Low (~1,2) - Sedentary lifestyle, lack of "
                             "sports, less than 10 thousand steps per day."
                             "\n· Small (~1,38) - Work related to "
                             "walking/standing, not very intense workouts "
                             "1-3 times a week (exercise, yoga, pilates, "
                             "etc.)."
                             "\n· Average (~1,55) - Intensive sports "
                             "consistently 1-3 times a week, active lifestyle."
                             "\n· High (~1,73) - Sports daily."
                             "\n· Very high (~2,2) - hard physical work, "
                             "sports 2 times a day.", parse_mode='HTML')
        keyboard = await create_keyboard(["Low", "Small", "Average", "High",
                                          "Very high"])
        await message.answer("Choose the most suitable variant for you.",
                             reply_markup=keyboard)
        await User.confirm_coefficient.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.confirm_coefficient)
async def set_coefficient(message: types.Message, state: FSMContext):
    if message.text in ["Low", "Small", "Average", "High", "Very high"]:
        await state.update_data(coefficient=message.text)
        keyboard = await create_keyboard(["Confirm ➡️"])
        await message.answer(f"Your changed coefficient: {message.text}",
                             reply_markup=keyboard)
        await User.fin_calories.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.calculate_calories)
async def calculate_calories(message: types.Message, state: FSMContext):
    if message.text == "Calculate 🖥":
        await message.answer("Calculating... 🖥",
                             reply_markup=types.ReplyKeyboardRemove())
        data = await state.get_data()
        browser = await launch({"headless": True})
        page = await browser.newPage()
        await page.goto("https://menu-4u.ru/",
                        {"waitUntil": "domcontentloaded"})
        await page.click("#go_to_calc")
        await page.waitForSelector("#button_calc_rasch")
        await page.type(
            "#calculator > div:nth-child(3) > div > div > div.calc_wrap > "
            "div:nth-child(1) > div.calc_item.calc_item_now.calc_item_now_h "
            "> div:nth-child(2) > label > input[type=text]", str(data['weight']))
        await page.type(
            "#calculator > div:nth-child(3) > div > div > div.calc_wrap > "
            "div:nth-child(1) > div.calc_item.calc_item_now.calc_item_now_h "
            "> div:nth-child(3) > label > input[type=text]",
            str(data['height']))
        await page.type(
            "#calculator > div:nth-child(3) > div > div > div.calc_wrap > "
            "div:nth-child(1) > div.calc_item.calc_item_now.calc_item_now_h "
            "> div:nth-child(4) > label > input[type=text]",
            str(data['age']))
        await asyncio.sleep(1)
        if data['gender'] == "Male 👨":
            await page.click(
                "#calculator > div:nth-child(3) > div > div > div.calc_wrap "
                "> div:nth-child(1) > div.calc_item.calc_item_sex > "
                "div:nth-child(2) > label > input[type=radio]")
        if data['gender'] == "Female 👩":
            await page.click(
                "#calculator > div:nth-child(3) > div > div > div.calc_wrap "
                "> div:nth-child(1) > div.calc_item.calc_item_sex > "
                "div:nth-child(3) > label > input[type=radio]")
        await asyncio.sleep(1)
        if data['target'] == "Weight loss 🧘‍♀️":
            await page.click(
                "#calculator > div:nth-child(3) > div > div > div.calc_wrap "
                "> div:nth-child(1) > div.calc_item.calc_item_goal > "
                "div:nth-child(2) > label > input[type=radio]")
        if data['target'] == "Maintaining weight ⏲️":
            await page.click(
                "#calculator > div:nth-child(3) > div > div > div.calc_wrap "
                "> div:nth-child(1) > div.calc_item.calc_item_goal > "
                "div:nth-child(3) > label > input[type=radio]")
        if data['target'] == "Weight gain 💪":
            await page.click(
                "#calculator > div:nth-child(3) > div > div > div.calc_wrap "
                "> div:nth-child(1) > div.calc_item.calc_item_goal > "
                "div:nth-child(4) > label > input[type=radio]")
        await asyncio.sleep(1)
        if data['coefficient'] == "Low":
            await page.click(
                "#calculator > div:nth-child(3) > div > div > div.calc_wrap "
                "> div:nth-child(2) > div > div:nth-child(2) > label > "
                "input[type=radio]")
        if data['coefficient'] == "Small":
            await page.click(
                "#calculator > div:nth-child(3) > div > div > div.calc_wrap "
                "> div:nth-child(2) > div > div:nth-child(3) > label > "
                "input[type=radio]")
        if data['coefficient'] == "Average":
            await page.click(
                "#calculator > div:nth-child(3) > div > div > div.calc_wrap "
                "> div:nth-child(2) > div > div:nth-child(4) > label > "
                "input[type=radio]")
        if data['coefficient'] == "High":
            await page.click(
                "#calculator > div:nth-child(3) > div > div > div.calc_wrap "
                "> div:nth-child(2) > div > div:nth-child(5) > label > "
                "input[type=radio]")
        if data['coefficient'] == "Very high":
            await page.click(
                "#calculator > div:nth-child(3) > div > div > div.calc_wrap "
                "> div:nth-child(2) > div > div:nth-child(6) > label > "
                "input[type=radio]")
        await page.click("#button_calc_rasch")
        await page.waitForSelector("#btn_udalit_recepti")

        element_calories = await page.querySelector("#go_to_result > span")
        calories = await page.evaluate("(element_calories) => "
                                       "element_calories.textContent",
                                       element_calories)

        element_protein_from = await page.querySelector("#calc_result > "
                                                        "div:nth-child(2) > "
                                                        "span:nth-child(1)")
        protein_from = await page.evaluate("(element_calories) => "
                                           "element_calories.textContent",
                                               element_protein_from)

        element_protein_to = await page.querySelector("#calc_result > "
                                                      "div:nth-child(2) > "
                                                      "span:nth-child(2)")
        protein_to = await page.evaluate("(element_calories) => "
                                         "element_calories.textContent",
                                         element_protein_to)

        element_fat_from = await page.querySelector("#calc_result > "
                                                    "div:nth-child(3) > "
                                                    "span:nth-child(1)")
        fat_from = await page.evaluate("(element_calories) => "
                                       "element_calories.textContent",
                                       element_fat_from)

        element_fat_to = await page.querySelector("#calc_result > "
                                                  "div:nth-child(3) > "
                                                  "span:nth-child(2)")
        fat_to = await page.evaluate("(element_calories) => "
                                     "element_calories.textContent",
                                     element_fat_to)

        element_carbs_from = await page.querySelector("#calc_result > "
                                                      "div:nth-child(4) > "
                                                      "span:nth-child(1)")
        carbs_from = await page.evaluate("(element_calories) => "
                                         "element_calories.textContent",
                                         element_carbs_from)

        element_carbs_to = await page.querySelector("#calc_result > "
                                                    "div:nth-child(4) > "
                                                    "span:nth-child(2)")
        carbs_to = await page.evaluate("(element_calories) => "
                                       "element_calories.textContent",
                                       element_carbs_to)

        keyboard = await create_keyboard(["Leave this amount ✅",
                                          "Set my own value ❌"])
        await state.update_data(calories=int(calories))
        await message.answer(f"<b><i>--- My requirements ---</i></b>\n\n"
                             f"· The required number of calories: "
                             f"{calories}\n\n"
                             f"· The required amount of proteins: from "
                             f"{protein_from} to {protein_to} g\n\n"
                             f"· The required amount of fat: from "
                             f"{fat_from} to {fat_to}\n\n"
                             f"· The required amount of carbohydrates: from "
                             f"{carbs_from} to {carbs_to} g", parse_mode='HTML')
        await message.answer("Do you want this amount of calories or you "
                             "want to input your own value according to my "
                             "calculations?", reply_markup=keyboard)
        await browser.close()
        await User.confirm_calories.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.confirm_calories)
async def confirm_calories(message: types.Message):
    if message.text == "Leave this amount ✅":
        keyboard = await create_keyboard(["Continue ➡️"])
        await message.answer("Ok, fine. I get it.", reply_markup=keyboard)
        await User.count_meals.set()
    elif message.text == "Set my own value ❌":
        await message.answer("Input the amount of calories.",
                             reply_markup=types.ReplyKeyboardRemove())
        await User.set_calories.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.set_calories)
async def set_calories(message: types.Message, state: FSMContext):
    answer = message.text
    if answer.isdigit():
        amount_of_calories = int(answer)
        if 200 <= amount_of_calories <= 16000:
            keyboard = await create_keyboard(["Continue ➡️"])
            await message.answer(f"Your amount of calories: "
                                 f"{amount_of_calories}",
                                 reply_markup=keyboard)
            await state.update_data(calories=amount_of_calories)
            await User.count_meals.set()
        elif amount_of_calories < 200:
            await message.answer("Input more calories. 📈")
        else:
            await message.answer("Input less calories. 📉")
    else:
        await message.answer("⚠️ Input should be a number, try again. ⚠️")


@dp.message_handler(state=User.count_meals)
async def count_meals(message: types.Message, state: FSMContext):
    if message.text == "Continue ➡️" or message.text == "Change the amount " \
                                                        "of meals":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        data = await state.get_data()
        buttons = []
        if 200 <= data['calories'] <= 4000:
            buttons.append("1")
        if 200 <= data['calories'] <= 8000:
            buttons.append("2")
        if 300 <= data['calories'] <= 12000:
            buttons.append("3")
        if 400 <= data['calories'] <= 16000:
            buttons.append("4")
        keyboard.row(*buttons)
        await message.answer("How many meals per day do you want?",
                             reply_markup=keyboard)
        await User.set_meals.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.set_meals)
async def set_meals(message: types.Message, state: FSMContext):
    if message.text in ["1", "2", "3", "4"]:
        await state.update_data(meals=int(message.text))
        keyboard = await create_keyboard(["No ❌", "Yes ✅"])
        await message.answer("If you want less or more meals change the "
                             "amount of calories.")
        await message.answer("Do you want to change the amount of calories?",
                             reply_markup=keyboard)
        await User.set_meals_fin.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again ⚠️")


@dp.message_handler(state=User.set_meals_fin)
async def set_meals_fin(message: types.Message, state: FSMContext):
    if message.text == "Yes ✅":
        keyboard = await create_keyboard(["Change"])
        await message.answer("Change your calories.", reply_markup=keyboard)
        await User.get_calories.set()
    elif message.text == "No ❌" or "Continue ➡️":
        data = await state.get_data()
        keyboard = await create_keyboard(["Continue ➡️"])
        await message.answer(f"Your choice: {data['meals']} meals",
                             reply_markup=keyboard)
        await User.fin_info.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.fin_info)
async def fin_info(message: types.Message, state: FSMContext):
    if message.text == "Continue ➡️":
        data = await state.get_data()
        await message.answer(f"<b><i>--- Information about your choices --- "
                             f"</i></b>\n\n"
                             f"<b>· The type of your diet:</b> {data['diet']}"
                             f"\n\n"
                             f"<b>· The amount of your calories:</b> "
                             f"{data['calories']} calories\n\n"
                             f"<b>· The amount of your meals:</b> "
                             f"{data['meals']} meals", parse_mode='HTML')
        keyboard = await create_keyboard(["Yes ✅", "No ❌"])
        await message.answer("Is the information correct? 🤔",
                             reply_markup=keyboard)
        await User.info_answer.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.info_answer)
async def info_answer(message: types.Message):
    if message.text == "Yes ✅":
        keyboard = await create_keyboard(["Generate my meal plan for day"])
        await message.answer("Great! Let's generate your plan.",
                             reply_markup=keyboard)
        await User.generation.set()
    elif message.text == "No ❌":
        keyboard = await create_keyboard(["The type of my diet",
                                          "The amount of calories and meals",
                                          "The amount of meals"])
        await message.answer("What do you want to change?",
                             reply_markup=keyboard)
        await User.change_info.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.change_info)
async def change_info(message: types.Message):
    if message.text == "The type of my diet":
        keyboard = await create_keyboard(["Change the type of my diet"])
        await message.answer("Let's change it.", reply_markup=keyboard)
        await User.change_diet.set()
    elif message.text == "The amount of calories and meals":
        keyboard = await create_keyboard(["Change the amount of calories and "
                                          "meals"])
        await message.answer("Let's change it.", reply_markup=keyboard)
        await User.get_calories.set()
    elif message.text == "The amount of meals":
        button = "Change the amount of meals"
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(button)
        keyboard = await create_keyboard(["Change the amount of meals"])
        await message.answer("Let's change it.", reply_markup=keyboard)
        await User.count_meals.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.change_diet)
async def change_diet(message: types.Message):
    if message.text == "Change the type of my diet":
        keyboard = await create_keyboard(["Anything 🥪", "Paleo 🍖",
                                          "Vegetarian 🥦", "Vegan 🌱",
                                          "Ketogenic 🥙", "Mediterranean 🪔"])
        await message.answer("Choose the type of your diet.",
                             reply_markup=keyboard)
        await User.change_diet_confirm.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again ⚠️")


@dp.message_handler(state=User.change_diet_confirm)
async def change_diet_confirm(message: types.Message, state: FSMContext):
    if message.text in ["Anything 🥪", "Paleo 🍖", "Vegetarian 🥦",
                        "Vegan 🌱", "Ketogenic 🥙", "Mediterranean 🪔"]:
        keyboard = await create_keyboard(["Continue ➡️"])
        await state.update_data(diet=message.text)
        await message.answer(f"Your choice: {message.text}",
                             reply_markup=keyboard)
        await User.fin_info.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.generation)
async def generation(message: types.Message, state: FSMContext):
    if message.text in ["Generate my meal plan for day", "Confirm ➡️"]:
        await message.answer("Generating your menu... Just wait a few "
                             "seconds ⏳",
                             reply_markup=types.ReplyKeyboardRemove())
        data = await state.get_data()
        browser = await launch({"headless": True})
        page = await browser.newPage()
        await page.goto("https://www.eatthismuch.com/",
                        {"waitUntil": "domcontentloaded"})
        await page.waitForSelector("#main_container > div > "
                                   "div.home_generator_box.container > "
                                   "div.row.generator_header_div > "
                                   "div.generator_header.col-12.col-md-10"
                                   ".offset-md-1.col-lg-8.offset-lg-2 > "
                                   "div:nth-child(6) > div > button")
        if data['diet'] == "Anything 🥪":
            await page.click(
                "#main_container > div > div.home_generator_box.container > "
                "div.row.generator_header_div > "
                "div.generator_header.col-12.col-md-10.offset-md-1.col-lg-8"
                ".offset-lg-2 > div.preset_selector_div > ul > li:nth-child("
                "1) > a > svg")
        if data['diet'] == "Paleo 🍖":
            await page.click(
                "#main_container > div > div.home_generator_box.container > "
                "div.row.generator_header_div > "
                "div.generator_header.col-12.col-md-10.offset-md-1.col-lg-8"
                ".offset-lg-2 > div.preset_selector_div > ul > li:nth-child("
                "2) > a > svg")
        if data["diet"] == "Vegetarian 🥦":
            await page.click(
                "#main_container > div > div.home_generator_box.container > "
                "div.row.generator_header_div > "
                "div.generator_header.col-12.col-md-10.offset-md-1.col-lg-8"
                ".offset-lg-2 > div.preset_selector_div > ul > li:nth-child("
                "3) > a > svg")
        if data["diet"] == "Vegan 🌱":
            await page.click(
                "#main_container > div > div.home_generator_box.container > "
                "div.row.generator_header_div > "
                "div.generator_header.col-12.col-md-10.offset-md-1.col-lg-8"
                ".offset-lg-2 > div.preset_selector_div > ul > li:nth-child("
                "4) > a > svg")
        if data["diet"] == "Ketogenic 🥙":
            await page.click(
                "#main_container > div > div.home_generator_box.container > "
                "div.row.generator_header_div > "
                "div.generator_header.col-12.col-md-10.offset-md-1.col-lg-8"
                ".offset-lg-2 > div.preset_selector_div > ul > li:nth-child("
                "5) > a > svg")
        if data["diet"] == "Mediterranean 🪔":
            await page.click(
                "#main_container > div > div.home_generator_box.container > "
                "div.row.generator_header_div > "
                "div.generator_header.col-12.col-md-10.offset-md-1.col-lg-8"
                ".offset-lg-2 > div.preset_selector_div > ul > li:nth-child("
                "6) > a > svg")

        calories = data['calories']
        await page.type("#cal_input", str(calories))

        await page.click("#num_meals_selector")
        await page.waitForSelector("#num_meals_selector")
        if data['meals'] == 1:
            await page.select("#num_meals_selector", '1')
        if data['meals'] == 2:
            await page.select("#num_meals_selector", '2')
        if data['meals'] == 3:
            await page.select("#num_meals_selector", '3')
        if data['meals'] == 4:
            await page.select("#num_meals_selector", '4')
        await page.click(
            "#main_container > div > div.home_generator_box.container > "
            "div.row.generator_header_div > "
            "div.generator_header.col-12.col-md-10.offset-md-1.col-lg-8"
            ".offset-lg-2 > div:nth-child(6) > div > button")

        await page.waitForSelector(
            "#main_container > div > "
            "div.container.day_plan_container.show_meals_as_cards > div.row "
            "> div.col-10.offset-1.col-md-8.offset-md-2.offset-lg-1.col-lg-6 "
            "> div > div.single_day_view.col-12 > div > div.workspace_area > "
            "div.workspace_stats > div > div > div",
            {"visible": True})

        html = await page.content()
        with open(f"menu_{message.from_user.id}.html", "w", encoding="UTF-8") \
                as file:
            file.write(html)

        with open(f"menu_{message.from_user.id}.html", encoding="UTF-8") \
                as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        cards = soup.find_all("div", class_="meal_box meal_container row")

        full_menu = {}

        for card in cards:
            name_card = card.find("div",
                                  class_="col-auto text-dark-gray text-large "
                                         "text-strong print_meal_title "
                                         "wrap_or_truncate pr-0").text.strip()
            count_calories = card.find("span", class_="cal_amount text-small "
                                                      "text-light-gray").text
            all_dishes = card.find_all("div", class_="food_name col-12")

            dishes = {}
            dish_id = 0

            for dish in all_dishes:
                name_dish = dish.find("div", class_="print_name").text.strip()
                dish_id += 1
                dishes[dish_id] = {
                    "Dish_name": name_dish
                }

            if count_calories[0] != "0":
                full_menu[name_card] = {
                    "Calories": count_calories,
                    "Dishes": dishes
                }

            with open(f"menu_dict_{message.from_user.id}.json", "w",
                      encoding="UTF-8") as file:
                json.dump(full_menu, file, indent=4, ensure_ascii=False)
        await message.answer("Menu is ready. 🤖")
        button = ["Show 👀"]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*button)
        await message.answer("Let me show your menu.", reply_markup=keyboard)
        await browser.close()
        await User.show.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again. ⚠️")


@dp.message_handler(state=User.show)
async def show(message: types.Message):
    if message.text in ["Show 👀", "Back ⬅️", "Confirm ➡️"]:
        buttons = []
        line = ""
        with open(f"menu_dict_{message.from_user.id}.json",
                  encoding="UTF-8") as file:
            data = json.load(file)
        if "Breakfast" in data:
            buttons.append("Breakfast 🍳")
            line += "\n\nBreakfast 🍳"
        if "Lunch" in data:
            buttons.append("Lunch 🍲")
            line += "\n\nLunch 🍲"
        if "Dinner" in data:
            buttons.append("Dinner 🍽️")
            line += "\n\nDinner 🍽️"
        if "Snack" in data:
            buttons.append("Snack 🍩")
            line += "\n\nSnack 🍩"
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons.append("Regenerate my menu. 🔄")
        buttons.append("Restart ❗")
        keyboard.add(*buttons)
        await message.answer(f"<b>Choose category:</b>{line}",
                             reply_markup=keyboard, parse_mode='HTML')
        await User.choose_meal.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again ⚠️")


@dp.message_handler(state=User.choose_meal)
async def choose_diet(message: types.Message):
    keyboard = await create_keyboard(["Back ⬅️"])
    with open(f"menu_dict_{message.from_user.id}.json",
              encoding="UTF-8") as file:
        data = json.load(file)
    if message.text == "Breakfast 🍳":
        await message.answer(f"Your breakfast 🍳:")
        await message.answer(f"· Calories: {data['Breakfast']['Calories']}")

        for i, dish in data['Breakfast']['Dishes'].items():
            dish = dish['Dish_name']
            await show_info_dish(message, dish)
        await message.answer("Click back if you want to come back to main "
                             "menu", reply_markup=keyboard)
        await User.show.set()
    elif message.text == "Lunch 🍲":
        await message.answer(f"Your lunch 🍲:")
        await message.answer(f"· Calories: {data['Lunch']['Calories']}")

        for i, dish in data['Lunch']['Dishes'].items():
            dish = dish['Dish_name']
            await show_info_dish(message, dish)
        await message.answer("Click back if you want to come back to main "
                             "menu", reply_markup=keyboard)
        await User.show.set()
    elif message.text == "Dinner 🍽️":
        await message.answer(f"Your dinner 🍽️:")
        await message.answer(f"· Calories: {data['Dinner']['Calories']}")

        for i, dish in data['Dinner']['Dishes'].items():
            dish = dish['Dish_name']
            await show_info_dish(message, dish)
        await message.answer("Click back if you want to come back to main "
                             "menu", reply_markup=keyboard)
        await User.show.set()
    elif message.text == "Snack 🍩":
        await message.answer(f"Your snack 🍩:")
        await message.answer(f"· Calories: {data['Snack']['Calories']}")

        for i, dish in data['Snack']['Dishes'].items():
            dish = dish['Dish_name']
            await show_info_dish(message, dish)
        await message.answer("Click back if you want to come back to main "
                             "menu", reply_markup=keyboard)
        await User.show.set()
    elif message.text == "Regenerate my menu. 🔄":
        keyboard = await create_keyboard(["Yes ✅", "No ❌"])
        await message.answer("Do you really want to regenerate your daily "
                             "menu?", reply_markup=keyboard)
        await User.confirm_regeneretaion.set()
    elif message.text == "Restart ❗":
        keyboard = await create_keyboard(["Confirm ➡️"])
        await message.answer("Confirm your choice.", reply_markup=keyboard)
        await User.choose_diet.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again ⚠️")


@dp.message_handler(state=User.confirm_regeneretaion)
async def confirm_regeneretaion(message: types.Message):
    keyboard = await create_keyboard(["Confirm ➡️"])
    await message.answer("Confirm your choice.", reply_markup=keyboard)
    if message.text == "Yes ✅":
        await User.generation.set()
    elif message.text == "No ❌":
        await User.show.set()
    else:
        await message.answer("⚠️ Incorrect answer, try again ⚠️")


if __name__ == '__main__':
    executor.start_polling(dp)
