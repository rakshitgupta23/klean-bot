import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pywa import WhatsApp, types

load_dotenv()

app = FastAPI()

wa = WhatsApp(
    phone_id=os.getenv("PHONE_ID"),
    token=os.getenv("ACCESS_TOKEN"),
    server=app,
    verify_token=os.getenv("VERIFY_TOKEN"),
    callback_url="https://3dcb29e68890.ngrok-free.app",  # <== Replace with your actual pyngrok URL
    app_id=os.getenv("APP_ID"),          
    app_secret=os.getenv("APP_SECRET")  
)

# In-memory store for known users (for demo only)
known_users = set()

@wa.on_message()
def handle_message(_: WhatsApp, msg: types.Message):
    print(f"[📥 Incoming] Name: {msg.from_user.name} | WA_ID: {msg.from_user.wa_id} | Text: {msg.text}")

    user_id = msg.from_user.wa_id
    name = msg.from_user.name

    if user_id not in known_users:
        known_users.add(user_id)
        send_welcome_message(user_id, name)
    else:
        backend_response = fake_backend(msg.text)
        msg.reply_text(backend_response)


def send_welcome_message(user_id, name):
    wa.send_message(
        to=user_id,
        text=f"👋 Hi {name}, welcome to Klean!\n\nChoose an option to get started:",
        buttons=[
            types.Button(title="About Klean", callback_data="ABOUT_KLEAN"),
            types.Button(title="How to use Klean", callback_data="HOW_USE_KLEAN"),
        ]
    )

@wa.on_callback_button()
def handle_buttons(_: WhatsApp, clb: types.CallbackButton):
    if clb.data == "ABOUT_KLEAN":
        clb.reply_text("📢 Klean helps uncover the truth about ingredients in food, cosmetics, and more.")
    elif clb.data == "HOW_USE_KLEAN":
        clb.reply_text("🔍 Just type the name of a product or ingredient and we’ll tell you what’s really inside.")

def fake_backend(message: str) -> str:
    print(f"[Dummy Backend] Received user message: {message}")
    return "I'm Backend"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("SERVER_HOST", "0.0.0.0"), port=int(os.getenv("SERVER_PORT", 8000)))
