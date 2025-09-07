import socket
import socks

proxy_host = "142.171.138.233"
proxy_port = 8989

# Try connecting to Telegram DC via proxy
try:
    s = socks.socksocket()
    s.set_proxy(socks.SOCKS5, proxy_host, proxy_port)
    s.settimeout(10)
    s.connect(("149.154.167.50", 443))  # Telegram DC IP
    print("✅ SOCKS5 proxy works with Telegram")
except Exception as e:
    print("❌ Proxy failed with Telegram:", e)
finally:
    s.close()
