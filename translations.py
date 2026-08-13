
from deep_translator import GoogleTranslator
import arabic_reshaper
from bidi.algorithm import get_display
def text_reshape_farsi(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def translate(text):
    try:
        return GoogleTranslator(source='auto',target='fa').translate(text)
    except Exception:
        return text

COMMAND_ALIASES = {
    # سلام و احوالپرسی
    "سلام": "hello",
    "hello": "hello",
    "درود": "hello",
    "hi": "hello",

    # اسم
    "اسم": "name",
    "name": "name",
    "نام": "name",

    # خروج
    "خروج": "bye",
    "bye": "bye",
    "خداحافظ": "bye",
    "goodbye": "bye",

    # طلا
    "طلا": "gold",
    "gold": "gold",
    "پول": "gold",
    "money": "gold",

    # افزودن طلا
    "افزودن طلا": "add_gold",
    "add gold": "add_gold",
    "اضافه کردن طلا": "add_gold",

    # زمان
    "زمان": "time",
    "time": "time",
    "ساعت": "time",
    "وقت": "time",

    # تاریخ
    "تاریخ": "date",
    "date": "date",
    "امروز": "date",

    # ماشین حساب
    "ماشین حساب": "calc",
    "calc": "calc",
    "محاسبه": "calc",
    "حساب": "calc",

    # وضعیت
    "وضعیت": "stats",
    "stats": "stats",
    "آمار": "stats",
    "statistics": "stats",

    # یادداشت‌ها
    "افزودن یادداشت": "add_note",
    "add note": "add_note",
    "اضافه کردن یادداشت": "add_note",
    "یادداشت جدید": "add_note",

    "نمایش یادداشت": "show_note",
    "show note": "show_note",
    "نمایش یادداشت‌ها": "show_note",
    "یادداشت‌ها": "show_note",

    "حذف یادداشت": "remove_note",
    "remove note": "remove_note",
    "پاک کردن یادداشت": "remove_note",

    # ذخیره و بارگذاری
    "ذخیره": "save",
    "save": "save",
    "ذخیره کردن": "save",
    "بارگذاری": "load",
    "load": "load",
    "لود": "load",

    # تاریخچه
    "تاریخچه": "history",
    "history": "history",
    "تاریخچه دستورات": "history",

    # شهر
    "شهر": "city",
    "city": "city",
    "شهر من": "city",

    "تغییر شهر": "change_city",
    "change city": "change_city",
    "عوض کردن شهر": "change_city",

    # راهنما
    "راهنما": "help",
    "help": "help",
    "کمک": "help",

    # آب و هوا
    "هوا": "weather",
    "آب و هوا": "weather",
    "weather": "weather",
    "پیش‌بینی": "weather",

    # جوک
    "جوک": "joke",
    "لطیفه": "joke",
    "joke": "joke",
    "طنز": "joke",

    # حقیقت
    "حقیقت": "fact",
    "fact": "fact",
    "واقعیت": "fact",

    # درباره
    "درباره": "about",
    "about": "about",
    "درباره من": "about",

    # تنظیمات
    "تنظیمات": "show_settings",
    "show settings": "show_settings",
    "نمایش تنظیمات": "show_settings",
    "settings": "show_settings",

    "تنظیم زبان": "set_language",
    "set language": "set_language",
    "زبان": "set_language",

    "نمایش زبان": "show_language",
    "show language": "show_language",

    # Todo (کارها)
    "افزودن کار": "add_todos",
    "add todo": "add_todos",
    "اضافه کردن کار": "add_todos",
    "کار جدید": "add_todos",

    "نمایش کارها": "show_todos",
    "show todos": "show_todos",
    "لیست کارها": "show_todos",
    "کارها": "show_todos",

    "حذف کار": "remove_todos",
    "remove todo": "remove_todos",
    "پاک کردن کار": "remove_todos",

    "تغییر وضعیت": "toggle_status",
    "toggle status": "toggle_status",
    "انجام شد": "toggle_status",
    "انجام نشد": "toggle_status",

    # Reminder (یادآوری‌ها)
    "افزودن یادآوری": "add_reminders",
    "add reminder": "add_reminders",
    "یادآوری جدید": "add_reminders",

    "نمایش یادآوری‌ها": "show_reminders",
    "show reminders": "show_reminders",
    "یادآوری‌ها": "show_reminders",

    "حذف یادآوری": "remove_reminders",
    "remove reminder": "remove_reminders",

    "تغییر وضعیت یادآوری": "toggle_reminders",
    "toggle reminder": "toggle_reminders",

    "بررسی یادآوری‌ها": "check_reminders",
    "check reminders": "check_reminders",
    "یادآوری‌های امروز": "check_reminders",
    "search": "search",
    "جستجو": "search",
    'smart mode' : 'toggle_smart_mode',
    'حالت هوشمند' : 'toggle_smart_mode',
    'هوشمند': 'toggle_smart_mode',
    'change mode' : 'toggle_smart_mode',
    'تغییر حالت گفتگو': 'toggle_smart_mode'
}



















