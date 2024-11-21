import asyncio
from pyrogram import filters, Client
from config import *
from helpo.database import db 
from asyncio.exceptions import TimeoutError

from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from plugins.Data import Data
from telethon import TelegramClient
from telethon.sessions import StringSession
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid,
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError,
)

# user_forward_data = {}
St_Session = {}
handler = {}

def manager(id, value):
    global handler
    handler[id] = value
    return handler

def get_manager():
    global handler
    return handler


PHONE_NUMBER_TEXT = (
    "📞__ Now send your Phone number to Continue"
    " include Country code.__\n**Eg:** `+13124562345`\n\n"
    "Press /cancel to Cancel."
)

def set_session_in_config(id, session_string):
    from config import Lazy_session  # Import St_Session to modify it
    Lazy_session[id] = session_string

def set_api_id_in_config(id, lazy_api_id):
    from config import Lazy_api_id  # Import api id to modify it
    Lazy_api_id[id] = lazy_api_id

def set_api_hash_in_config(id, lazy_api_hash):
    from config import Lazy_api_hash  # Import api hash to modify it
    Lazy_api_hash[id] = lazy_api_hash

lazydeveloperrsession = {}

@Client.on_message(filters.private & filters.command("generate"))
async def generate_session(bot, msg):
    lzid = msg.from_user.id
    global lazydeveloperrsession
    await msg.reply(
        "sᴛᴀʀᴛɪɴG [ᴛᴇʟᴇᴛʜᴏɴ] sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛɪᴏɴ..."
    )
    user_id = msg.chat.id
    api_id_msg = await bot.ask(
        user_id, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `API_ID`", filters=filters.text
    )
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply(
            "ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ API_ID (ᴡʜɪᴄʜ ᴍᴜsᴛ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ). ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    api_hash_msg = await bot.ask(
        user_id, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `API_HASH`", filters=filters.text
    )
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(
        user_id,
        "ɴᴏᴡ ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `ᴘʜᴏɴᴇ_ɴᴜᴍʙᴇʀ` ᴀʟᴏɴɢ ᴡɪᴛʜ ᴛʜᴇ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ. \nᴇxᴀᴍᴘʟᴇ : `+19876543210`",
        filters=filters.text,
    )
    if await cancelled(api_id_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("sᴇɴᴅɪɴɢ ᴏᴛᴘ...")
    
    client = TelegramClient(StringSession(), api_id, api_hash)

    await client.connect()
    try:
        code = await client.send_code_request(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply(
            "`API_ID` ᴀɴᴅ `API_HASH` ᴄᴏᴍʙɪɴᴀᴛɪᴏɴ ɪs ɪɴᴠᴀʟɪᴅ. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply(
            "`PHONE_NUMBER` ɪs ɪɴᴠᴀʟɪᴅ. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    try:
        phone_code_msg = await bot.ask(
            user_id,
            "ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ꜰᴏʀ ᴀɴ ᴏᴛᴘ ɪɴ ᴏꜰꜰɪᴄɪᴀʟ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴄᴄᴏᴜɴᴛ. ɪꜰ ʏᴏᴜ ɢᴏᴛ ɪᴛ, sᴇɴᴅ ᴏᴛᴘ ʜᴇʀᴇ ᴀꜰᴛᴇʀ ʀᴇᴀᴅɪɴɢ ᴛʜᴇ ʙᴇʟᴏᴡ ꜰᴏʀᴍᴀᴛ. \nɪꜰ ᴏᴛᴘ ɪs `12345`, **ᴘʟᴇᴀsᴇ sᴇɴᴅ ɪᴛ ᴀs** `1 2 3 4 5`.",
            filters=filters.text,
            timeout=600,
        )
        if await cancelled(api_id_msg):
            return
    except TimeoutError:
        await msg.reply(
            "ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ᴏꜰ 10 ᴍɪɴᴜᴛᴇs. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        await client.sign_in(phone_number, phone_code, password=None)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply(
            "ᴏᴛᴘ ɪs ɪɴᴠᴀʟɪᴅ. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply(
            "ᴏᴛᴘ ɪs ᴇxᴘɪʀᴇᴅ. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(
                user_id,
                "ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ʜᴀs ᴇɴᴀʙʟᴇᴅ ᴛᴡᴏ-sᴛᴇᴘ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ. ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴘᴀssᴡᴏʀᴅ.",
                filters=filters.text,
                timeout=300,
            )
        except TimeoutError:
            await msg.reply(
                "ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ᴏꜰ 5 ᴍɪɴᴜᴛᴇs. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return
        try:
            password = two_step_msg.text
            
            await client.sign_in(password=password)
            
            if await cancelled(api_id_msg):
                return
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await two_step_msg.reply(
                "ɪɴᴠᴀʟɪᴅ ᴘᴀssᴡᴏʀᴅ ᴘʀᴏᴠɪᴅᴇᴅ. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
                quote=True,
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return

    string_session = client.session.save()
    try:
        # St_Session[msg.from_user.id] = string_session
        set_session_in_config(msg.from_user.id, string_session)
        set_api_id_in_config(msg.from_user.id, api_id)
        set_api_hash_in_config(msg.from_user.id, api_hash)
        print(f"Credentials api id and hash saved to config successfully ✅")
    except Exception as LazyDeveloperr:
        print(LazyDeveloperr)

    text = f"**ᴛᴇʟᴇᴛʜᴏɴ sᴛʀɪɴɢ sᴇssɪᴏɴ** \n\n`{string_session}`"
       
    try:
        await client.send_message("me", text)
    except KeyError:
        pass
    await client.disconnect()
    await phone_code_msg.reply(
        "sᴜᴄᴄᴇssꜰᴜʟʟʏ ɢᴇɴᴇʀᴀᴛᴇᴅ telethon sᴛʀɪɴɢ sᴇssɪᴏɴ. \n\nᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs!"
    )
    # Save session to the dictionary
    try:
        lazydeveloperrsession[lzid] = TelegramClient(StringSession(string_session), api_id, api_hash)
        await lazydeveloperrsession[lzid].start()
        print(f"Session started successfully for user {user_id} ✅")
    except Exception as e:
        print(f"Error starting session for user {user_id}: {e}")
        await msg.reply("Failed to start session. Please try again.")
        return


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply(
            "ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴘʀᴏᴄᴇss!",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    
    elif "/restart" in msg.text:
        await msg.reply(
            "ʙᴏᴛ ɪs ʀᴇsᴛᴀʀᴛᴇᴅ!",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("ᴄᴀɴᴄᴇʟʟᴇᴅ ᴛʜᴇ ɢᴇɴᴇʀᴀᴛɪᴏɴ ᴘʀᴏᴄᴇss!", quote=True)
        return True
    else:
        return False

# @Client.on_message(filters.private & filters.command("connect"))
# async def generate_str(c, m):

#     user_id = m.from_user.id

#     # Check if the user is allowed to use the bot
#     if not await verify_user(user_id):
#         return await m.reply("⛔ You are not authorized to use this bot.")
    
#     if user_id in St_Session:
#         # Check if session already exists for this user
#         return await m.reply("String session already connected! Use /rename")
    
#     try:
#         client = Client(":memory:", api_id=API_ID, api_hash=API_HASH)
#     except Exception as e:
#         return await c.send_message(m.chat.id ,f"**🛑 ERROR: 🛑** {str(e)}\nPress /login to create again.")

#     try:
#         await client.connect()
#     except ConnectionError:
#         await client.disconnect()
#         await client.connect()

#     while True:
#         get_phone_number = await c.ask(
#             chat_id=m.chat.id,
#             text=PHONE_NUMBER_TEXT
#         )
#         phone_number = get_phone_number.text
#         if await is_cancel(m, phone_number):
#             return
#         await get_phone_number.delete()
#         await get_phone_number.request.delete()

#         confirm = await c.ask(
#             chat_id=m.chat.id,
#             text=f'🤔 Is {phone_number} correct? (y/n): \n\ntype: y (If Yes)\ntype: n (If No)'
#         )
#         if await is_cancel(m, confirm.text):
#             return
#         if "y" in confirm.text.lower():
#             await confirm.delete()
#             await confirm.request.delete()
#             break
#     try:
#         code = await client.send_code(phone_number)
#         await asyncio.sleep(1)
#     except FloodWait as e:
#         return await m.reply(f"__Sorry to say you that you have floodwait of {e.x} Seconds 😞__")
#     except ApiIdInvalid:
#         return await m.reply("🕵‍♂ The API ID or API HASH is Invalid.\n\nPress /login to create again.")
#     except PhoneNumberInvalid:
#         return await m.reply("☎ Your Phone Number is Invalid.\n\nPress /login to create again.")

#     try:
#         # sent_type = {"app": "Telegram App 💌",
#         #     "sms": "SMS 💬",
#         #     "call": "Phone call 📱",
#         #     "flash_call": "phone flash call 📲"
#         # }[code.type]
#         otp = await c.ask(
#             chat_id=m.chat.id,
#             text=(f"I had sent an OTP to the number {phone_number} through\n\n"
#                   "Please enter the OTP in the format 1 2 3 4 5 __(provied white space between numbers)__\n\n"
#                   "If Bot not sending OTP then try /start the Bot.\n"
#                   "Press /cancel to Cancel."), timeout=300)
#     except TimeoutError:
#         return await m.reply("**⏰ TimeOut Error:** You reached Time limit of 5 min.\nPress /start to create again.")
#     if await is_cancel(m, otp.text):
#         return
#     otp_code = otp.text
#     await otp.delete()
#     await otp.request.delete()
#     try:
#         await client.sign_in(phone_number, code.phone_code_hash, phone_code=' '.join(str(otp_code)))
#     except PhoneCodeInvalid:
#         return await m.reply("**📵 Invalid Code**\n\nPress /start to create again.") 
#     except PhoneCodeExpired:
#         return await m.reply("**⌚ Code is Expired**\n\nPress /start to create again.")
#     except SessionPasswordNeeded:
#         try:
#             two_step_code = await c.ask(
#                 chat_id=m.chat.id, 
#                 text="🔐 This account have two-step verification code.\nPlease enter your second factor authentication code.\nPress /cancel to Cancel.",
#                 timeout=300
#             )
#         except TimeoutError:
#             return await m.reply("**⏰ TimeOut Error:** You reached Time limit of 5 min.\nPress /start to create again.")
#         if await is_cancel(m, two_step_code.text):
#             return
#         new_code = two_step_code.text
#         await two_step_code.delete()
#         await two_step_code.request.delete()
#         try:
#             await client.check_password(new_code)
#         except Exception as e:
#             return await m.reply(f"**⚠️ ERROR:** {str(e)}")
#     except Exception as e:
#         return await c.send_message(m.chat.id ,f"**⚠️ ERROR:** {str(e)}")
#     try:
#         session_string = await client.export_session_string()
#         St_Session[m.from_user.id] = session_string 
#         await client.send_message("me", f"**Your String Session 👇**\n\n{session_string}\n\nThanks For using {(await c.get_me()).mention(style='md')}")
#         text = "✅ Successfully Generated Your String Session and sent to you saved messages.\nCheck your saved messages or Click on Below Button."
#         reply_markup = InlineKeyboardMarkup(
#             [[InlineKeyboardButton(text="String Session ↗️", url=f"tg://openmessage?user_id={m.chat.id}")]]
#         )
#         await c.send_message(m.chat.id, text, reply_markup=reply_markup)
#     except Exception as e:
#         return await c.send_message(m.chat.id ,f"**⚠️ ERROR:** {str(e)}")
#     try:
#         await client.stop()
#     except:
#         pass

# @Client.on_message(filters.private & filters.command("logout"))
# async def logout_user(c, m):
#     user_id = m.from_user.id
#     # Check if the user is allowed to use the bot
#     if not await verify_user(user_id):
#         return await m.reply("⛔ You are not authorized to use this bot.")
    
#     # Check if the user has an active session @LazyDeveloperr
#     if user_id in St_Session:
#         try:

#             # Clear the user's session from St_Session @LazyDeveloperr
#             del St_Session[user_id]

#             # Send a confirmation message to the user @LazyDeveloperr
#             await c.send_message(m.chat.id, "🟢 You have been successfully logged out.")
        
#         except Exception as e:
#             # Handle any errors during logout @LazyDeveloperr
#             await c.send_message(m.chat.id, f"⚠️ Error during logout: {str(e)}")
#     else:
#         # If no active session is found, notify the user @LazyDeveloperr
#         await c.send_message(m.chat.id, "🛑 No active session found to log out.")


@Client.on_message(filters.command("rename"))
async def rename(client, message):
    user_id = message.from_user.id
    # Check if the user is allowed to use the bot
    if not await verify_user(user_id):
        return await message.reply("⛔ You are not authorized to use this bot.")
    
    if user_id not in lazydeveloperrsession:
        return await message.reply("⚠️ No session found. Please generate a session first using /generate.")

    # if not lazydeveloperrsession:
    #     print(f"lazydeveloperrsession not found")
    #     return  # Stop if ubot could not be connected

    chat_id = await client.ask(
        text="Send Channel Id From Where You Want To Forward in `-100XXXX` Format ",
        chat_id=message.chat.id
    )
    target_chat_id = int(chat_id.text)
    
    print(f'✅Set target chat => {target_chat_id}' )
    try:
        chat_info = await client.get_chat(target_chat_id)
        print(f"Got Chat info")
    except Exception as e:
        await client.send_message(message.chat.id, f"Something went wrong while accessing chat : {chat_info}")
        print(f"Error accessing chat: {e}")
    # Handle the exception appropriately

    Forward = await client.ask(
        text="Send Channel Id In Which You Want Renamed Files To Be Sent in `-100XXXX` Format ",
        chat_id=message.chat.id
    )
    Forward = int(Forward.text)
    print(f'🔥Set destination chat => {target_chat_id}' )


    await db.set_forward(message.from_user.id, Forward)

    print(f"Starting to forward files from channel {target_chat_id} to {BOT_USERNAME}.")

    # Using `ubot` to iterate through chat history in target chat
    file_count = 0
    
    lazy_userbot = lazydeveloperrsession[user_id]

    # Iterating through messages
    try:
        async for msg in lazy_userbot.iter_messages(target_chat_id, limit=20):
            print(f"Message ID: {msg.id}, Content: {msg.text or 'No text'}")
            # Forward or process the message
            if msg.media:  # Check if the message contains media
                # await lgbtq.forward_messages('@LazyDevDemo_BOT', msg.id, target_chat_id)
                await lazy_userbot.send_message(BOT_USERNAME, msg.text or "", file=msg.media)
                print(f"✅ Forwarded media with ID {msg.id}")
            else:
                print(f"Skipped non-media message with ID {msg.id}")
            asyncio.sleep(1)
            # Delete the message from the target channel
            await lazy_userbot.delete_messages(target_chat_id, msg.id)
            print(f"❌ Deleted message with ID {msg.id}")
        await message.reply("✅ Files successfully forwarded!")
    except Exception as e:
        print(f"Error occurred: {e}")
        await message.reply("❌ Failed to process messages.")


    # async for msg in lazydeveloperrsession.get_chat_history(target_chat_id):
    #     try:
    #         # Check if message has any file type (document, audio, video, etc.)
    #         if msg.document or msg.audio or msg.video:
    #             print("Found media message, copying to target...")
    #             await msg.copy(BOT_USERNAME)  # Send to target chat or bot PM
    #             await asyncio.sleep(3)  # Delay between each file sent
    #             print("Message forwarded successfully!")

    #             # Delete message after forwarding
    #             await lazydeveloperrsession.delete_messages(target_chat_id, msg.id)
    #             print(f"Message {msg.id} deleted from target channel.")
                
    #             file_count += 1  # Increment the file_count

    #             if file_count == 10:
    #                 confirm = await client.ask(
    #                     chat_id=message.chat.id,
    #                     text=f'Completed 10 tasks! Do you want to continue forwarding? (y/n):\n\n'
    #                          'Type: `y` (If Yes)\nType: `n` (If No)'
    #                 )

    #                 if "n" in confirm.text.lower():  # If user wants to stop
    #                     await confirm.delete()
    #                     file_count = 0
    #                     break  # Stop forwarding
    #                 await confirm.delete()
    #                 file_count = 0

    #     except Exception as e:
    #         print(f"Error processing message {msg.id}: {e}")
    #         continue  # Move to next message on error

    # # await ubot.stop()
    # print("Finished forwarding and deleting all files.")


# async def is_cancel(msg: Message, text: str):
#     if text.startswith("/cancel"):
#         await msg.reply("⛔ Process Cancelled.")
#         return True
#     return False

async def verify_user(user_id: int):
    return user_id in ADMIN


