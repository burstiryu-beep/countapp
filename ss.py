from pyngrok import ngrok

ngrok.set_auth_token("YOUR_TOKEN")

url = ngrok.connect(8501)
print("🌐 公開URL:", url)

input("Enterで停止")