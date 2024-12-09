import random
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import time

bot_token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(bot_token)

group_game_status = {}
correct_answer = None  # تعريف متغير الرقم السري بشكل عام
game_board = [["👊", "👊", "👊", "👊", "👊", "👊"]]
numbers_board = [["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]]
original_game_board = [["👊", "👊", "👊", "👊", "👊", "👊"]]
points = {}

def format_board(game_board, numbers_board):
    """تنسيق الجدول للعرض بشكل مناسب"""
    formatted_board = ""
    formatted_board += " ".join(numbers_board[0]) + "\n"
    formatted_board += " ".join(game_board[0]) + "\n"
    return formatted_board

def reset_game(chat_id):
    """إعادة تعيين حالة اللعبة بعد انتهائها"""
    global game_board, correct_answer, group_game_status
    game_board = [row[:] for row in original_game_board]
    correct_answer = None
    group_game_status[chat_id]['is_game_started2'] = False
    group_game_status[chat_id]['joker_player'] = None
@bot.message_handler(func=lambda message: message.text == 'محيبس')
def strt(message):
    global correct_answer
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("ابدأ اللعبة", callback_data="startGame"))

    username = message.from_user.username or "unknown"
    bot.send_video(
        message.chat.id,
        "t.me/VIPABH/1210",  
        caption=f"أهلاً [{message.from_user.first_name}](https://t.me/{username})! حياك الله. اضغط على الزر لبدء اللعبة.",
        parse_mode="Markdown",
        reply_markup=markup
    )

    chat_id = message.chat.id
    if chat_id not in group_game_status:
        group_game_status[chat_id] = {'is_game_started2': False, 'joker_player': None}

@bot.callback_query_handler(func=lambda call: call.data == "startGame")
def handle_start_game(call):
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    chat_id = call.message.chat.id
    user_id = call.from_user.id 

    if chat_id not in group_game_status:
        group_game_status[chat_id] = {'is_game_started2': False, 'joker_player': None}

    if not group_game_status[chat_id]['is_game_started2']:
        group_game_status[chat_id]['is_game_started2'] = True
        group_game_status[chat_id]['joker_player'] = user_id  
        correct_answer = random.randint(1, 6) 
        group_game_status[chat_id]['correct_answer'] = correct_answer
        bot.send_message(chat_id, f"تم تسجيلك في لعبة محيبس \n ملاحظة : لفتح العضمة ارسل طك ورقم العضمة لأخذ المحبس أرسل جيب ورقم العضمة.")


@bot.message_handler(regexp=r'\جيب (\d+)')
def handle_guess(message):
    global group_game_status, correct_answer, game_board, points

    chat_id = message.chat.id
    if chat_id in group_game_status and group_game_status[chat_id]['is_game_started2']:
        try:
            guess = int(message.text.split()[1])
            if 1 <= guess <= 6:
                if guess == correct_answer:
                    winner_id = message.from_user.id
                    points[winner_id] = points.get(winner_id, 0) + 1
                    sender_first_name = message.from_user.first_name
                    game_board = [["💍" if i == correct_answer - 1 else "🖐️" for i in range(6)]]
                    bot.reply_to(chat_id, f'🎉 الف مبروك! اللاعب ({sender_first_name}) وجد المحبس 💍!\n{format_board(game_board, numbers_board)}')
                    reset_game(chat_id)
                else:
                    sender_first_name = message.from_user.first_name
                    game_board = [["❌" if i == guess - 1 else "🖐️" for i in range(6)]]
                    bot.reply_to(message, f"ضاع البات ماضن بعد تلگونة ☹️ \n{format_board(game_board, numbers_board)}")
                    reset_game(chat_id)
            else:
                bot.reply_to(message, "❗ يرجى إدخال رقم صحيح بين 1 و 6.")
        except (IndexError, ValueError):
            bot.reply_to(message, "❗ يرجى إدخال رقم صحيح بين 1 و 6.")

@bot.message_handler(regexp=r'\طك (\d+)')
def handle_strike(message):
    global game_board, correct_answer, group_game_status

    chat_id = message.chat.id
    if chat_id in group_game_status and group_game_status[chat_id]['is_game_started2']:
        try:
            strike_position = int(message.text.split()[1])
            if strike_position == correct_answer:
                game_board = [["💍" if i == correct_answer - 1 else "🖐️" for i in range(6)]]
                
                bot.reply_to(message, f"خسرت شبيك مستعجل وجه الچوب 😒 \n{format_board(game_board, numbers_board)}")
                reset_game(chat_id) 
            else:
                abh = [
    "تلعب وخوش تلعب 👏🏻",
    "لك عاش يابطل استمر 💪🏻",
    "على كيفك ركزززز انتَ كدها 🤨",
    "لك وعلي ذيييب 😍"]
                
                iuABH = random.choice(abh)

                game_board[0][strike_position - 1] = '🖐️'
                bot.reply_to(message, f" {iuABH} \n{format_board(game_board, numbers_board)}")
        except (IndexError, ValueError):
            bot.reply_to(message, "يرجى إدخال رقم صحيح بين 1 و 6.")
            if __name__ == "__main__":
                bot.polling(none_stop=True)


banned_users = [74659206340, 60489018900]  

def is_user_banned(user_id):
    return user_id in banned_users

@bot.message_handler(func=lambda message: message.text in ['ضوجه', 'ضوجة', 'ضايج', 'ضايجه'])
def abh(message):
    if is_user_banned(message.from_user.id):
        bot.reply_to(message, "أنت محظور من التفاعل مع البوت.")
    else:
        bot.reply_to(
            message, 
            "جربت الألعاب؟ اكتب `المزيد` لمعرفة الخدمات المتوفرة", 
            parse_mode='Markdown'
        )
        bot.reply_to(message, "🤨")

@bot.message_handler(func=lambda message: message.text == 'المزيد')
def more(message):
    if is_user_banned(message.from_user.id):
        bot.reply_to(message, "أنت محظور من التفاعل مع البوت.")
    else:
        bot.reply_to(message, """
        ~ الالعاب المتوفرة ~
        \n •الكت تويت والأمر الخاص بيها `كتويت`
        \n •الأرقام ، احزر الرقم المطلوب والأمر الخاص بيها /num 
        \n •امر الميمز ، `ميم` او `ميمز` يرسلك صورة ميم 
        \n\n استمتع ❤️
        """, parse_mode='Markdown')

game_active = False
number = None
max_attempts = 3
attempts = 0
active_player_id = None  



@bot.message_handler(commands=['start'])
def handle_start(message):
    # تحقق إذا كان المستخدم محظورًا
    if message.from_user.id in banned_users:
        bot.reply_to(message, "عذرا , انت محظور من استخدام البوت.")
        bot.reply_to(message, "☝️")
        return

    bot.reply_to(
        message,
        "أهلاً حياك الله! \n"
        "• أرسل `كتويت` لبدء أسئلة الكت تويت. \n"
        "• أرسل `/ارقام` أو /num لبدء لعبة الأرقام.\n"
        "• أرسل `ميم` او `ميمز` للميمز. \n\n"
        " استمتع! 🎉",
        parse_mode='Markdown'
    )
@bot.message_handler(commands=['ارقام', 'num'])
def start(message):
    if message.from_user.id in banned_users:
        bot.reply_to(message, "عذرا , انت محظور من استخدام البوت.")
        bot.reply_to(message, "☝️")
        return

    global game_active, attempts, active_player_id
    game_active = False
    attempts = 0
    active_player_id = None

    username = message.from_user.username if message.from_user.username else "لا يوجد اسم مستخدم"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("ابدأ اللعبة", callback_data="start_game"))
    bot.send_video(
        message.chat.id,
        "t.me/VIPABH/1204",
        caption=f"اهلا [{message.from_user.first_name}](t.me/{username}) حياك الله! اضغط على الزر لبدء اللعبة.",
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "start_game")
def start_game(call):
    if call.from_user.id in banned_users:
        bot.reply_to(call.message, "عذرا , انت محظور من استخدام البوت.")
        bot.reply_to(call.message, "☝️")
        return

    global game_active, number, attempts, active_player_id
    if not game_active:
        number = random.randint(1, 10)
        active_player_id = call.from_user.id
        username = call.from_user.username if call.from_user.username else "لا يوجد اسم مستخدم"

        # إزالة زر Inline بعد بدء اللعبة
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None
        )
        bot.send_message(call.message.chat.id, f'عزيزي  [{call.from_user.first_name}](t.me/@{username}) اختر أي رقم من 1 إلى 10 🌚',  parse_mode="Markdown")
        game_active = True
        attempts = 0
    else:
        bot.reply_to(call.message.chat.id, 'اللعبة قيد التشغيل، يرجى انتهاء الجولة الحالية أولاً.')

@bot.message_handler(func=lambda message: game_active and message.from_user.id == active_player_id)
def handle_guess(message):
    # تحقق إذا كان المستخدم محظورًا
    if message.from_user.id in banned_users:
          bot.reply_to(message, "عذرا , انت محظور من استخدام البوت.")
          bot.reply_to(message, "☝️")
    global game_active, number, attempts
    try:
        guess = int(message.text)
        if guess < 1 or guess > 10:
            bot.reply_to(message, "يرجى اختيار رقم بين 1 و 10 فقط!")
            return

        attempts += 1

        if guess == number:
            bot.reply_to(message, "مُبارك فزتها بفخر 🥳")
            won = "t.me/VIPABH/2"
            bot.send_voice(message.chat.id, won)
            bot.reply_to(message,  "🥳")
            game_active = False
        elif attempts >= max_attempts:
            bot.reply_to(message, f"للأسف، لقد نفدت محاولاتك. الرقم الصحيح هو {number}.🌚")
            lose = "t.me/VIPABH/23"
            bot.send_voice(message.chat.id, lose)
            game_active = False
        else:
            bot.reply_to(message, "جرب مرة لخ، الرقم غلط💔")
    except ValueError:
        bot.reply_to(message, "يرجى إدخال رقم صحيح")

@bot.message_handler(func=lambda message: message.text in ['ميم'] or message.text in ['ميمز'])
def send_random_file(message):
    rl = random.randint(2, 222)
    url = f"t.me/iuabh/{rl}"
    bot.send_photo(message.chat.id, url, caption="😎يسعد مسائك", reply_to_message_id=message.message_id)
    
    if __name__ == "__main__":
        bot.polling(none_stop=True)


questions = [
    "شلون تعمل هالشي؟",
    "شلون تقضي وقتك بالفراغ؟",
    "شلون تتحكم بالضغط؟",
    "شلون تكون صبور؟",
    "شلون تحافظ على التركيز؟",
    "شلون تكون قوي نفسياً؟",
    "شلون تسيطر على الغضب؟",
    "شلون تدير وقتك بشكل فعال؟",
    "شلون تكون ناجح في حياتك المهنية؟",
    "شلون تطور مهاراتك الشخصية؟",
    "شلون تدير الضغوطات في العمل؟",
    "شلون تدير الامور المالية؟",
    "شلون تتعلم لغة جديدة؟",
    "شلون تكون مبدع في عملك؟",
    "شلون تطور علاقاتك الاجتماعية؟",
    "شلون تتغلب على التحديات؟",
    "شلون تنظم حياتك بشكل منظم؟",
    "شلون تحافظ على صحتك؟",
    "شلون تحمي نفسك من الإجهاد؟",
    "شلون تعتني بنفسك بشكل جيد؟",
    "شلون تكون متفائل في الحياة؟",
    "شلون تدير الوقت بين العمل والحياة الشخصية؟",
    "شلون تتعامل مع الشكوك والتوتر؟",
    "شلون تعطي قيمة لوقتك؟",
    "شلون تدير التوتر في العلاقات العائلية؟",
    "شلون تتعلم من الاخطاء؟",
    "شلون تدير الصعوبات في الحياة؟",
    "شلون تكون منظم في حياتك اليومية؟",
    "شلون تحسن من تركيزك وانتباهك؟",
    "شلون تطور مهاراتك الشخصية والاجتماعية؟",
    "شلون تدير العمل في فريق؟",
    "شلون تحسن من قدراتك التواصلية؟",
    "شلون تكون منظم في الدراسة؟",
    "شلون تكون فعال في استخدام التكنولوجيا؟",
    "شلون تحافظ على توازنك بين العمل والحياة الشخصية؟",
    "شلون تتعلم مهارات جديدة بسرعة؟",
    "شلون تكون ملهماً للآخرين؟",
    "شلون تدير الخلافات في العمل؟",
    "شلون تكون مؤثراً في العروض التقديمية؟",
    "شلون تحسن من قدراتك التفكير الإبداعي؟",
    "شلون تطور قدراتك القيادية؟",
    "شلون تكون متفائل في ظروف صعبة؟",
    "شلون تدير التحولات في الحياة؟",
    "شلون تتعلم من النجاحات والإخفاقات؟",
    "شلون تكون مستعداً للتغيير؟",
    "شلون تستمتع بالحياة؟",
    "شلون تكون إنساناً محبوباً ومحترماً؟",
    "شلون تتعلم من خبرات الآخرين؟",
    "شلون تطور مهاراتك في التعلم الذاتي؟",
    "شلون تحسن من قدراتك على اتخاذ القرارات؟",
    "شلون تكون مبادراً في العمل؟",
    "شلون تطور مهاراتك في حل المشكلات؟",
    "شلون تستفيد من النقد البناء؟",
    "شلون تطور ثقتك بالنفس؟",
    "شلون تتعامل مع التغييرات في العمل؟",
    "شلون تطور مهاراتك في التعاون والعمل الجماعي؟",
    "شلون تتعامل مع الضغوطات في الحياة؟",
    "شلونك؟",
    "شنو اسمك؟",
    "شنو جنسيتك؟",
    "شنو عمرك؟",
    "شنو لونك المفضل؟",
    "شنو طبخة تحبها اكثر؟",
    "شنو هوايتك المفضلة؟",
    "شنو مكان سفرة اللي تحلم تروحله؟",
    "شنو نوع السيارة اللي تفضلها؟",
    "شنو نوع الموسيقى اللي تحب تستمع لها؟",
    "شنو تحب تسوي في وقت الفراغ؟",
    "شنو اكلتك المفضلة في الفطور؟",
    "شنو اكلتك المفضلة في الغدا؟",
    "شنو اكلتك المفضلة في العشا؟",
    "شنو نوع الشاي اللي تحب تشربه؟",
    "شنو نوع القهوة اللي تحب تشربها؟",
    "شنو اكثر شيء مميز في ثقافة العراق؟",
    "شنو نوع الافلام اللي تحب تشوفها؟",
    "شنو البلدة العربية اللي تفضل تزورها؟",
    "شنو نوع الهدية اللي تحب تتلقاها؟",
    "شنو اهم شيء بالنسبة إليك في الصداقة؟",
    "شنو الشيء اللي تشوفه عند العراقيين بشكل خاص؟",
    "شنو الاكلة العراقية المفضلة عندك؟",
    "شنو نوع الرياضة اللي تحب تمارسها؟",
    "شنو مكان العراقي اللي تحب تزوره في العراق؟",
    "شنو اكثر شيء تحبه في الطبيعة؟",
    "شنو اللون اللي يحبه العراقيين كثير؟",
    "شنو الشيء اللي يستفزك بسرعة؟",
    "شنو الشيء اللي يخليك تفرح؟",
    "شنو الشيء اللي تحس إنه اكثر شيء يعبر عن الهوية العراقية؟",
    "شنو نوع الهاتف اللي تستخدمه؟",
    "شنو الشيء اللي تحس فيه إنه مفقود في المجتمع العراقي؟",
    "شنو اكثر مكان تحب تزوره في العراق؟",
    "شنو النصيحة اللي تحب تعطيها لشخص صغير؟",
    "شنو الشيء اللي يخليك تشعر بالراحة والهدوء؟",
    "شنو الشيء اللي تحب تسويه بالعطلة؟",
    "شنو الحيوان اللي تحبه اكثر؟",
    "شنو الشيء اللي تحب تهديه لشخص عزيز عليك؟",
    "شنو الشيء اللي تحس بإنجاز كبير إذا قمت به؟",
    "شنو اكثر موقع التواصل الاجتماعي اللي تستخدمه؟",
    "شنو الشيء اللي يحبه العراقيين في الاعياد والمناسبات؟",
    "شنو الشيء اللي تحب تشوفه في العراق مطور ومتطور؟",
    "شنو الشيء اللي تحب تشاركه مع الآخرين بشكل كبير؟",
    "شنو اكثر موسم تحبه في العراق؟",
    "شنو الشيء اللي تتمنى تغيره في العراق؟",
    "شنو الشيء اللي تحب تستثمر فيه وقتك وجهدك؟",
    "شنو الشيء اللي يميز العراق والعراقيين برايك؟",
    "شنو نوع الفن اللي تحب تستمتع به؟",
    "شنو الشيء اللي تحب تتعلمه في المستقبل؟",
    "شنو اكثر شيء تحبه في الشتاء؟",
    "شنو الشيء اللي يرفع معنوياتك بشكل سريع؟",
    "شنو الشيء اللي تحب تهديه لنفسك؟",
    "شنو الشيء اللي تتمنى تحققه في حياتك؟",
     "منو افضل صديق عندك؟",
    "منو شخصيتك المفضلة في الافلام؟",
    "منو الشخص اللي تحب تسافر معه؟",
    "منو الشخص اللي بتستشيره في قراراتك؟",
    "منو اكثر شخص تحب تشوفه كل يوم؟",
    "منو اكثر شخص غريب بتعرفه؟",
    "منو الشخص اللي تحب تحجي معه لساعات؟",
    "منو اكثر شخص قدوة بحياتك؟",
    "منو الشخص اللي تثق فيه بشكل كامل؟",
    "منو اكثر شخص ملهم في حياتك؟",
    "منو الشخص اللي تتمنى تشوفه اليوم؟",
    "منو الشخص اللي تحب تكون جارك؟",
    "منو الشخص اللي بتتحدث معه كل يوم؟",
    "منو الشخص اللي بتشتاقله كثير؟",
    "منو الشخص اللي بتعتمد عليه في الصعوبات؟",
    "منو الشخص اللي تحب تشاركه اسرارك؟",
    "منو الشخص اللي بتقدر قيمته في حياتك؟",
    "منو الشخص اللي تحب تطلب منه المشورة؟",
    "منو الشخص اللي تحب تكون معه في المشاكل؟",
    "منو الشخص اللي بتحسه اكثر شخص يفهمك؟",
    "منو الشخص اللي تحب تحتفل معه في الاعياد؟",
    "منو الشخص اللي تتوقعه اكثر شخص بيرحل عنك؟",
    "منو الشخص اللي تحب تشترك معه في الهوايات؟",
    "منو الشخص اللي تحب تشوفه بعد غياب طويل؟",
    "منو الشخص اللي تتمنى تقدمله هدية مميزة؟",
    "منو الشخص اللي تحب تذهب معه في رحلة استكشافية؟",
    "منو الشخص اللي تحب تحجي معه عن مشاكلك العاطفية؟",
    "منو الشخص اللي تتمنى تكون له نفس قدراتك ومهاراتك؟",
    "منو الشخص اللي تحب تقابله وتشتغل معه في المستقبل؟",
    "منو الشخص اللي تحب تحتفل معه بنجاحك وإنجازاتك؟",
    "منو الشخص اللي بتتذكره بكل سعادة عندما تراجع صورك القديمة؟",
    "منو الشخص اللي تحب تشاركه تجاربك ومغامراتك في الحياة؟",
    "منو الشخص اللي تحب تسمع نصائحه وتطبقها في حياتك؟",
    "منو الشخص اللي تحب تشوفه ضحكته بين الفينة والاخرى؟",
    "منو الشخص اللي تعتبره اكثر شخص يدعمك ويحفزك على تحقيق اهدافك؟",
    "منو الشخص اللي تحب تشوفه محقق نجاحاته ومستقبله المشرق؟",
    "منو الشخص اللي تحب تشكره على وجوده في حياتك ودعمه المستمر؟",
    "منو الشخص اللي تحب تقدمله هدية تذكارية لتخليك تذكره للابد؟",
    "منو الشخص اللي تحب تشكره على دعمه الكبير لك في مشوارك الدراسي؟",
    "منو الشخص اللي تتمنى تعرفه في المستقبل وتصير صداقتكم مميزة؟",
    "منو الشخص اللي تحب تشاركه لحظات الفرح والسعادة في حياتك؟",
    "منو الشخص اللي تعتبره اكثر شخص يستحق منك كل الحب والاحترام؟",
    "منو الشخص اللي تحب تشاركه اسرارك وتحجي له كل شيء بدون تردد؟",
    "منو الشخص اللي تتمنى تحضر معه حفلة موسيقية لفرقتك المفضلة؟",
    "منو الشخص اللي تحب تتنافس معه في لعبة او رياضة تحبها؟",
    "منو الشخص اللي تحب تشوفه مبتسماً ومتفائلاً في الحياة؟",

    "شوكت تفتح المحل؟",
    "شوكت بتروح على العمل؟",
    "شوكت تكون مستعد للمقابلة؟",
    "شوكت بتنوم بالليل؟",
    "شوكت بتصحى بالصبح؟",
    "شوكت بتسافر؟",
    "شوكت بتعود من العمل؟",
    "شوكت بتعمل رياضة؟",
    "شوكت بتذاكر للامتحان؟",
    "شوكت بتنظف البيت؟",
    "شوكت بتقرا الكتاب؟",
    "شوكت تكون فاضي للتسوق؟",
    "شوكت بتنطر الباص؟",
    "شوكت بتعود من السفر؟",
    "شوكت بتشتري الهدية؟",
    "شوكت بتتقابل مع صديقك؟",
    "شوكت بتحضر الحفلة؟",
    "شوكت بتتعشى؟",
    "شوكت بتتناول الفطور؟",
    "شوكت بتسافر في العطلة؟",
    "شوكت بترجع للمنزل؟",
    "شوكت تخلص المشروع؟",
    "شوكت بتتخرج من الجامعة؟",
    "شوكت بتبدا العمل؟",
    "شوكت بتفتح المحل؟",
    "شوكت تنتهي الدورة التدريبية؟",
    "شوكت بتتزوج؟",
    "شوكت بترتب الغرفة؟",
    "شوكت تتعلم الموسيقى؟",
    "شوكت بترتب الوثائق؟",
    "شوكت بتسجل في النادي الرياضي؟",
    "شوكت تستلم الطلبية؟",
    "شوكت بتشوف الطبيب؟",
    "شوكت بتتناول الغداء؟",
    "شوكت تكون مستعد للسفر؟",
    "شوكت بتكمل المشروع؟",
    "شوكت تخلص الواجب؟",
    "شوكت تحصل على النتيجة؟",
    "شوكت تتعلم اللغة الجديدة؟",
    "شوكت بتحضر المؤتمر؟",
    "شوكت بتنهي الكتاب؟",
    "شوكت بتفتح المطعم؟",
    "شوكت بتسافر في الإجازة؟",
    "شوكت بتبدا التدريب؟",
    "شوكت تخلص المشروع الفني؟",
    "شوكت تنتهي الجلسة؟",
    "شوكت تتعلم الطبخ؟",
    "شوكت تستلم الشهادة؟",
    "شوكت بتبدا الرحلة؟",
    "شوكت بتنهي الاعمال المنزلية؟",
    "شوكت تكون فاضي للقراءة؟",
    "شوكت تستلم السيارة الجديدة؟",
    "شوكت بتتناول العشاء؟",
    "وين رايح؟",
    "وين تسكن؟",
    "وين بتشتغل؟",
    "وين بتروح في ايام العطلة؟",
    "وين تحب تسافر في العطلات؟",
    "وين تحب تروح مع الاصدقاء؟",
    "وين تكون في الساعة الثامنة صباحاً؟",
    "وين تكون في الساعة العاشرة مساءً؟",
    "وين تحب تتناول الإفطار؟",
    "وين تحب تتسوق؟",
    "وين تحب تتناول العشاء؟",
    "وين تكون في الساعة الثانية ظهراً؟",
    "وين تحب تمضي امسياتك؟",
    "وين تحب تقضي ايام العطلة؟",
    "وين تحب تزور المعالم السياحية؟",
    "وين تحب تشتري الهدايا؟",
    "وين تحب تتمرن وتمارس الرياضة؟",
    "وين تحب تذهب للتسوق؟",
    "وين تحب تقضي وقتك مع العائلة؟",
    "وين تكون في الساعة الخامسة مساءً؟"
]

@bot.message_handler(func=lambda message: message.text in ['كتويت'])
def send_random_question(message):
    random_question = random.choice(questions)
    bot.reply_to(message, random_question)



if __name__ == "__main__":
    bot.polling(none_stop=True)


# def create_keyboard():
#     markup = InlineKeyboardMarkup(row_width=3)
#     buttons = [
#         InlineKeyboardButton("باسميات", callback_data="باسم"),
#         InlineKeyboardButton("حيدر البياتي", callback_data="حيدر"),
#         InlineKeyboardButton("الخاقاني", callback_data="فاقد"),
#         InlineKeyboardButton("مسلم الوائلي", callback_data="مسلم"),
#         InlineKeyboardButton("منوع", callback_data="منوع"),
#         InlineKeyboardButton("نزلة", callback_data="نزلة"),
#         InlineKeyboardButton("مصطفى السوداني", callback_data="مصطفى"),
#         InlineKeyboardButton("افراح", callback_data="افراح"),
#         InlineKeyboardButton("عشوائي", callback_data="عشوائي")
#     ]
#     markup.add(*buttons)
#     return markup

# start_time = time.time()

# # Handle message and send the inline keyboard
# @bot.message_handler(func=lambda message: message.text in ['لطميه', 'لطمية'])
# def handle_message(message):
#     try:
#         if message.date >= start_time:
#             markup = create_keyboard()
#         bot.send_message(message.chat.id, "اختر لطمية 🫀", reply_markup=markup)
#     except Exception as e:
#         print(f"Error in handle_message: {e}")

# # Handle the callback queries from the inline keyboard
# @bot.callback_query_handler(func=lambda call: True)
# def handle_callback(call):
#     try:
#         if call.data == "عشوائي":
#             # إرسال ملف عشوائي
#             rl = random.randint(157, 306)  # تحديد رقم عشوائي ضمن النطاق
#             url = f"t.me/sossosic/{rl}"  # إنشاء الرابط باستخدام الرقم العشوائي
#             bot.send_audio(
#                 call.message.chat.id,
#                 url,  # التأكد من أن الرابط هو رابط مباشر لملف صوتي
#                 reply_to_message_id=call.message.message_id
#             )
#             # حذف الأزرار بعد الضغط
#             bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

#         elif call.data == "باسم":
#             # إرسال ملف عشوائي
#             rl = random.randint(50, 118)  # تحديد رقم عشوائي ضمن النطاق
#             url = f"t.me/sossosic/{rl}"  # إنشاء الرابط باستخدام الرقم العشوائي
#             bot.send_audio(
#                 call.message.chat.id,
#                 url,  # التأكد من أن الرابط هو رابط مباشر لملف صوتي
#                 reply_to_message_id=call.message.message_id
#             )
#             # حذف الأزرار بعد الضغط
#             bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

#         elif call.data == "حيدر":
#             # إرسال ملف عشوائي
#             rl = random.randint(3, 5)  # تحديد رقم عشوائي ضمن النطاق
#             url = f"t.me/keemmn/{rl}"  # إنشاء الرابط باستخدام الرقم العشوائي
#             bot.send_audio(
#                 call.message.chat.id,
#                 url,  # التأكد من أن الرابط هو رابط مباشر لملف صوتي
#                 reply_to_message_id=call.message.message_id
#             )
#             bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

#         elif call.data == "فاقد":
#             # مثال آخر لإضافة محتوى مخصص
#             rl = random.randint(200, 250)
#             url = f"t.me/sossosic/{rl}"
#             bot.send_audio(
#                 call.message.chat.id,
#                 url,
#                 reply_to_message_id=call.message.message_id
#             )
#             bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

#         # إضافة المزيد من الأوامر حسب الحاجة...
#         # مثلاً، يمكنك إضافة "مسلم" و "منوع" بنفس الطريقة.
