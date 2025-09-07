# Try these simple fixes one by one

# Fix 1: Use HTTP proxy instead of SOCKS5
import asyncio
from telethon import TelegramClient
import aiohttp

api_id = 1111111
api_hash = ""

# Method 1: Try with HTTP proxy (if your proxy supports it)
async def try_http_proxy():
    try:
        connector = aiohttp.ProxyConnector.from_url('http://142.171.138.233:8989')
        client = TelegramClient(
            "http_session", 
            api_id, 
            api_hash,
            proxy=connector
        )
        await client.start()
        me = await client.get_me()
        print(f"✅ HTTP proxy works: {me.username}")
        await client.disconnect()
        return True
    except Exception as e:
        print(f"❌ HTTP proxy failed: {e}")
        return False

# Method 2: Force IPv4 and disable IPv6
import socket
socket.getaddrinfo = lambda *args: [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('127.0.0.1', 80))]

async def try_ipv4_only():
    import socks
    try:
        # Force IPv4
        original_getaddrinfo = socket.getaddrinfo
        def ipv4_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
            return original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
        socket.getaddrinfo = ipv4_getaddrinfo
        
        client = TelegramClient(
            "ipv4_session", 
            api_id, 
            api_hash,
            proxy=(socks.SOCKS5, "142.171.138.233", 8989)
        )
        await client.start()
        me = await client.get_me()
        print(f"✅ IPv4-only works: {me.username}")
        await client.disconnect()
        socket.getaddrinfo = original_getaddrinfo  # Restore
        return True
    except Exception as e:
        print(f"❌ IPv4-only failed: {e}")
        return False

# Method 3: Use environment variables for proxy
import os
async def try_env_proxy():
    import socks
    try:
        # Set environment proxy
        os.environ['HTTPS_PROXY'] = 'socks5://142.171.138.233:8989'
        os.environ['HTTP_PROXY'] = 'socks5://142.171.138.233:8989'
        
        client = TelegramClient("env_session", api_id, api_hash)
        await client.start()
        me = await client.get_me()
        print(f"✅ Env proxy works: {me.username}")
        await client.disconnect()
        return True
    except Exception as e:
        print(f"❌ Env proxy failed: {e}")
        return False

# Method 4: Try a completely different proxy library
async def try_pysocks():
    try:
        import socks
        import socket
        
        # Monkey patch socket
        socks.set_default_proxy(socks.SOCKS5, "142.171.138.233", 8989)
        socket.socket = socks.socksocket
        
        client = TelegramClient("pysocks_session", api_id, api_hash)
        await client.start()
        me = await client.get_me()
        print(f"✅ PySocks monkey patch works: {me.username}")
        await client.disconnect()
        return True
    except Exception as e:
        print(f"❌ PySocks failed: {e}")
        return False

# Method 5: Try with requests-based approach
def try_requests_session():
    try:
        import requests
        
        session = requests.Session()
        session.proxies = {
            'http': 'socks5://142.171.138.233:8989',
            'https': 'socks5://142.171.138.233:8989'
        }
        
        # Test if we can reach Telegram API
        response = session.get('https://api.telegram.org/bot', timeout=10)
        print(f"✅ Requests with proxy works: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Requests failed: {e}")
        return False

# Method 6: Minimal working example with error details
async def minimal_test():
    import socks
    try:
        print("Creating client...")
        client = TelegramClient(
            "minimal", 
            api_id, 
            api_hash,
            proxy=(socks.SOCKS5, "142.171.138.233", 8989),
            timeout=120,  # Very long timeout
            connection_retries=1  # Just one attempt
        )
        
        print("Attempting to connect...")
        await client.connect()
        print("Connected! Checking authorization...")
        
        if await client.is_user_authorized():
            me = await client.get_me()
            print(f"✅ Success: {me.username or me.first_name}")
        else:
            print("Need to authorize...")
            # Don't do full auth, just check if we got this far
            
        await client.disconnect()
        return True
        
    except Exception as e:
        print(f"❌ Minimal test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("Trying different proxy methods...\n")
    
    methods = [
        ("Requests session", try_requests_session),
        ("Minimal Telethon", minimal_test),
        ("HTTP proxy", try_http_proxy),
        ("IPv4 only", try_ipv4_only),
        ("Environment proxy", try_env_proxy),
        ("PySocks monkey patch", try_pysocks),
    ]
    
    for name, method in methods:
        print(f"\n--- {name} ---")
        try:
            if asyncio.iscoroutinefunction(method):
                success = await method()
            else:
                success = method()
            
            if success:
                print(f"🎉 {name} worked! Try adapting this method.")
                break
        except Exception as e:
            print(f"❌ {name} crashed: {e}")

if __name__ == "__main__":
    # Clean sessions
    import glob
    import os
    for f in glob.glob("*.session"):
        try:
            os.remove(f)
        except:
            pass
    
    asyncio.run(main())