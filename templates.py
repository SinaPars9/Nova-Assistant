import random
from translations import text_reshape_farsi
RESPONSE_TEMPLATES = {
    "weather": [
        "🌤️ دمای {city} الان {temp} درجه‌ست.",
        "🌡️ هوا در {city} {temp} درجه هست.",
        "☀️ امروز در {city} {temp} درجه است.",
        "⛅ {city}: {temp} درجه.",
        "در {city} الان {temp} درجه است.",
    ],
    "gold": [
        "💰 موجودی طلا: {gold}.",
        "✨ طلاهایت: {gold}.",
        "🗿 {gold} طلا داری.",
        "طلا: {gold}.",
        "موجودی: {gold} طلا.",
    ],
    "time": [
        "🕐 ساعت {hour}:{minute} هست.",
        "⏰ الان {hour} و {minute} دقیقه‌ست.",
        "ساعت {hour}:{minute}.",
        "وقت: {hour}:{minute}.",
        "الان {hour}:{minute} هست.",
    ],
    "date": [
        "📅 امروز {year}/{month}/{day} است.",
        "🗓️ تاریخ امروز: {year}/{month}/{day}.",
        "امروز {year} / {month} / {day}.",
        "{year} {month} {day}",
    ],
    "hello": [
        "👋 سلام {user}! چطوری؟",
        "😊 سلام {user}! خوش اومدی!",
        "🎈 درود بر {user}!",
        "سلام {user}، چطور می‌تونم کمک کنم؟",
    ],
    "help": [
        "📋 دستورات موجود:\n{commands}",
        "🔍 لیست دستورات:\n{commands}",
        "🛠️ این دستورات رو امتحان کن:\n{commands}",
    ],
    "about": [
        "🤖 Nova - نسخه {version}\n👨‍💻 ساخته شده توسط {creator}",
        "🧠 Nova v{version}\n✍️ توسعه‌دهنده: {creator}",
        "✨ Nova {version}\n👤 سازنده: {creator}",
    ],
    "city": [
        "📍 شهر شما: {city}.",
        "🏙️ شهرت: {city}.",
        "شهر: {city}.",
        "شهر شما {city} هست.",
    ],
    "language": [
        "🌐 زبان: {lang}.",
        "زبان فعلی: {lang}.",
        "🗣️ زبان شما: {lang}.",
        "نوا به زبان {lang} صحبت می‌کند.",
    ],
    "settings": [
        "⚙️ تنظیمات:\nزبان: {language}\nشهر: {city}",
        "🛠️ تنظیمات:\n🌐 زبان: {language}\n📍 شهر: {city}",
        "تنظیمات فعلی:\nزبان: {language}\nشهر: {city}",
    ],
    "stats": [
        "📊 وضعیت:\nنام: {name}\nطلا: {gold}\nتعداد دستورات: {commands}",
        "📈 آمار:\n👤 نام: {name}\n💰 طلا: {gold}\n📝 دستورات: {commands}",
        "وضعیت شما:\nنام: {name}\nطلا: {gold}\nدستورات: {commands}",
    ],
    "fact": [
        "🧠 حقیقت: {fact}",
        "📖 آیا می‌دانستی؟ {fact}",
        "💡 جالب است: {fact}",
        "🔍 دانستی که: {fact}",
    ],
    "joke": [
        "😂 {joke}",
        "😆 {joke}",
        "🤣 {joke}",
        "😁 {joke}",
    ],
    "todo_added": [
        "✅ کار '{name}' با توضیح '{description}' اضافه شد.",
        "📝 '{name}' به لیست کارها اضافه شد.",
        "✔️ کار جدید: {name} - {description}",
    ],
    "todo_removed": [
        "🗑️ کار '{name}' حذف شد.",
        "❌ '{name}' از لیست کارها حذف شد.",
        "✅ کار '{name}' پاک شد.",
    ],
    "todo_toggled": [
        "🔄 وضعیت '{name}' به '{status}' تغییر کرد.",
        "✅ '{name}' اکنون {status} است.",
        "📌 '{name}': {status}",
    ],
    "reminder_added": [
        "⏰ یادآوری '{name}' برای {deadline} تنظیم شد.",
        "📅 یادآوری: {name} - {deadline}",
        "🔔 یادآوری '{name}' ثبت شد.",
    ],
    "reminder_removed": [
        "🗑️ یادآوری '{name}' حذف شد.",
        "❌ یادآوری {name} پاک شد.",
        "✅ '{name}' از یادآوری‌ها حذف شد.",
    ],
    "reminder_toggled": [
        "🔄 وضعیت یادآوری '{name}' به '{status}' تغییر کرد.",
        "✅ یادآوری '{name}' اکنون {status} است.",
    ],
    "overdue_reminders": [
        "⏰ یادآوری‌های سررسید شده:\n{reminders}",
        "📢 این یادآوری‌ها وقتش رسیده:\n{reminders}",
        "⚠️ موارد سررسید شده:\n{reminders}",
    ],
    "no_overdue": [
        "✅ هیچ یادآوری سررسید شده‌ای نیست.",
        "🎉 همه‌ی یادآوری‌ها به موقع هستن.",
        "🌟 هیچ مورد سررسید شده‌ای وجود نداره.",
    ],
    "search": [
        "🔍 {result}",
        "نتایج جستجو: {result}",
        "{result}",
    ],
}

def get_response(template_key, data):
    templates = RESPONSE_TEMPLATES.get(template_key, [])
    if not templates:
        return str(data)
    template = random.choice(templates)
    try:
        return (template.format(**data))
    except KeyError as e:
        text = text_reshape_farsi(f"⚠️ متغیر {e} توی قالب پیدا نشد!")
        print (text)
        return str(data)