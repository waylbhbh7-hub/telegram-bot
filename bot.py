import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# التوكن بتاع البوت بتاعك
TOKEN = "9224322400:AAFEC8SzVeC-3k-sfKA_7tz0o7J8483f5wc"

# القائمة الكاملة للكلمات الممنوعة (استدراج للخاص + ألفاظ جنسية وشتايم)
BAD_WORDS = [
    # الاستدراج للخاص
    "خاص", "private", "pm", "dm", "inbox",
    "تعالي", "تعالى", "تعالى خاص", "تعالي خاص", "يلا خاص", "ادخلي خاص", "افتحي خاص",
    
    # كلمات التدليع والجنس
    "ادلعك", "أدلعك", "هدلعك", "هنيكك", "أنيكك", "نيك", "نيكك", 
    "زبي", "زب", "كسك", "كس", "طيزك", "طيز", 
    "شرموطة", "قحبة", "متناكه", "متناك",
    
    # كلمات شائعة في نفس السياق
    "سكسي", "سكس", "نودز", "صور", "فيديو", 
    "تعالي نلعب", "عايزاك", "عایزك", "هات رقمك", "واتساب", "تليجرام"
]

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # التأكد إن الرسالة جاية من جروب وليست رسالة خاصة
    if update.message and update.message.chat.type in ["group", "supergroup"]:
        message_text = update.message.text or update.message.caption
        if message_text:
            text_lower = message_text.lower()
            
            # فحص إذا كانت الرسالة تحتوي على أي كلمة من القائمة الممنوعة
            for word in BAD_WORDS:
                # بنتاكد إن الكلمة موجودة جوه النص
                if word in text_lower:
                    try:
                        # حذف الرسالة المسيئة فوراً
                        await update.message.delete()
                        
                        # (اختياري) إرسال تنبيه خفيف للي كتبها
                        user_name = update.message.from_user.first_name
                        warning = await context.bot.send_message(
                            chat_id=update.message.chat_id,
                            text=f"عذراً يا {user_name}، الرسالة دي ممنوعة في الجروب! 🚫"
                        )
                        
                        # حذف رسالة التنبيه بعد 4 ثواني عشان الجروب ميتحرقش بالرسائل
                        await context.job_queue.run_once(
                            lambda ctx: warning.delete(), 
                            when=4, 
                            chat_id=update.message.chat_id
                        )
                        break
                    except Exception as e:
                        print(f"خطأ أثناء حذف الرسالة: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    # مراقبة النصوص والكابشنز في الصور
    app.add_handler(MessageHandler(filters.TEXT | filters.CAPTION, check_message))
    
    print("البوت يعمل الآن ويراقب الشتايم ومخالفات الخاص بنجاح...")
    app.run_polling()
