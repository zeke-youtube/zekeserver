```markdown
# 🛡️ Security Guidelines for ZekeBot

Welcome to ZekeBot! To keep your server safe, stable, and Discord-compliant, here are some essential security practices — especially when managing your bot token.

---

## 🚨 Never Expose Your Bot Token

Your Discord bot token is **like a password**. Leaking it gives full control to anyone who sees it.

### ❌ What NOT to do:
- Never hardcode your token into `bot.py`:
  ```python
  # BAD – do NOT do this!
  client.run("your-secret-token-here")
  ```
- Never upload your token to GitHub, especially in commits or screenshots.

---

## ✅ How to Handle Tokens Safely

1. **Use a secure file:**  
   Save your token in a file like `token.txt`.

2. **Load it safely in code:**
   ```python
   with open("token.txt") as f:
       token = f.read().strip()
   client.run(token)
   ```

3. **Protect the file:**  
   Add it to your `.gitignore` file so it won't be pushed to GitHub:
   ```
   token.txt
   ```

4. **Rotate immediately if leaked:**  
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
   - Select your application → *Bot* section  
   - Click **"Regenerate"** to invalidate the old token  
   - Update your project with the new one

---

## 🧠 Bonus Tips

- Use **environment variables** for production deployments or CI/CD pipelines
- Never share your token in:
  - Code snippets
  - Discord messages
  - GitHub issues
  - Screenshots
- If using GitHub Actions or similar, store the token in **GitHub Secrets** instead of hardcoding

---

By following these steps, you help protect your bot, your server, and your community from malicious access.

Stay smart.  
Stay secure.  
Stay **Zeke-powered**. 💪🤖
