import asyncio
import random
import ssl
import json
import time
import uuid
from loguru import logger
from websockets_proxy import Proxy, proxy_connect
from fake_useragent import UserAgent

# Set up log files
logger.add("errors.log", level="ERROR")
logger.add("connections.log", level="INFO")

# Generate random headers
def generate_headers():
    user_agent = UserAgent(os='windows', platforms='pc', browsers='chrome')
    return {
        "User-Agent": user_agent.random,
    }

# Connect to WebSocket server using proxy and user_id
async def connect_to_wss(socks5_proxy, user_id, semaphore):
    async with semaphore:  # Limit simultaneous connections
        device_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, socks5_proxy))
        logger.info(f"Device ID for user {user_id}: {device_id}")
        
        while True:
            try:
                await asyncio.sleep(random.uniform(0.1, 1.0))  # Random delay for connection
                
                # Set up headers and SSL context
                custom_headers = generate_headers()
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                ssl_context.timeout = 10  # SSL timeout

                # Choose random WebSocket URI
                urilist = ["wss://proxy.wynd.network:4444/", "wss://proxy.wynd.network:4650/"]
                uri = random.choice(urilist)
                server_hostname = "proxy.wynd.network"
                proxy = Proxy.from_url(socks5_proxy)

                # Connect with proxy to WebSocket
                async with proxy_connect(uri, proxy=proxy, ssl=ssl_context, server_hostname=server_hostname,
                                         extra_headers=custom_headers) as websocket:

                    # Send periodic PING messages
                    async def send_ping():
                        while True:
                            send_message = json.dumps(
                                {"id": str(uuid.uuid4()), "version": "1.0.0", "action": "PING", "data": {}}
                            )
                            logger.debug(send_message)
                            await websocket.send(send_message)
                            await asyncio.sleep(5)  # Ping every 5 seconds

                    # Start PING task
                    await asyncio.sleep(1)
                    asyncio.create_task(send_ping())

                    # Handle WebSocket messages
                    while True:
                        try:
                            response = await asyncio.wait_for(websocket.recv(), timeout=30)
                            message = json.loads(response)
                            logger.info(message)

                            if message.get("action") == "AUTH":
                                auth_response = {
                                    "id": message["id"],
                                    "origin_action": "AUTH",
                                    "result": {
                                        "browser_id": device_id,
                                        "user_id": user_id,
                                        "user_agent": custom_headers['User-Agent'],
                                        "timestamp": int(time.time()),
                                        "device_type": "desktop",
                                        "version": "4.28.1",
                                    }
                                }
                                logger.debug(auth_response)
                                await websocket.send(json.dumps(auth_response))

                            elif message.get("action") == "PONG":
                                pong_response = {"id": message["id"], "origin_action": "PONG"}
                                logger.debug(pong_response)
                                await websocket.send(json.dumps(pong_response))

                        except asyncio.TimeoutError:
                            logger.warning("Connection timed out. Retrying...")
                            break  # Reconnect on timeout

            except Exception as e:
                logger.error(e)
                logger.error(f"Proxy: {socks5_proxy}")
                await asyncio.sleep(random.uniform(5, 15))  # Random delay before reconnect

# Main function to initialize tasks and proxies
async def main():
    semaphore = asyncio.Semaphore(10)  # Limit simultaneous connections
    with open('user_id.txt', 'r') as user_file:
        user_ids = user_file.read().splitlines()
    
    with open('local_proxies.txt', 'r') as proxy_file:
        local_proxies = proxy_file.read().splitlines()
    
    tasks = []
    proxies_per_user = 10  # Number of proxies per account

    for i, user_id in enumerate(user_ids):
        proxies_for_user = local_proxies[i * proxies_per_user:(i + 1) * proxies_per_user]
        for proxy in proxies_for_user:
            tasks.append(asyncio.ensure_future(connect_to_wss(proxy, user_id, semaphore)))
    
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
