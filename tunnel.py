from pyngrok import ngrok

# Open an HTTP tunnel on port 8000
public_url = ngrok.connect(8000)
print("Ngrok tunnel running at:", public_url)

input("Press ENTER to keep it alive...")
