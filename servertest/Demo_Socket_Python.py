#! -*- coding: utf-8 -*-
"""
Author: ZhenYuSha
Create Time: 2019-1-14
Info: Websocket 的使用示例
"""
import asyncio
import websockets
import json
import threading

from Simulation_Test import Va,Ca,Vb,Cb,time

import datetime

# async def display_date():
#     loop = asyncio.get_running_loop()
#     end_time = loop.time() + 5.0
#     while True:
#         print(datetime.datetime.now())
#         if (loop.time() + 1.0) >= end_time:
#             break
#         await asyncio.sleep(1)

# asyncio.run(display_date())

#定时任务，每十秒发送check到给客户端
# async def check_client(ws):
#     while True:
#         try:
#             print("send check...")
#             await ws.send("cmd:check@@@@@@@@")
#             await asyncio.sleep(0)
#         except:
#             print("check_client failed ...")
#             break

async def send_data(ws):
    while True:
        try:
            print("send check...")
            data_info ={}
            data = json.loads(json.dumps(data_info))

            concentration = {"va": Va,"vb":Vb}
            data['concentration'] = concentration
            va = {"name": "va", "value": Va}
            data['concentration']['va'] = va
            vb = {"name": "vb", "value": Vb}
            data['concentration']['vb'] = vb

            volume =  {"ca":Ca,"cb":Cb}
            data['volume'] = volume
            ca = {"name": "ca", "value": Ca}
            data['volume']['ca'] = ca
            cb = {"name": "cb", "value": Cb}
            data['volume']['cb'] = cb

            dataPh = json.dumps(data,ensure_ascii= False)
            await ws.send(dataPh)
        #     await ws.send("cmd:aaaa")
            await asyncio.sleep(2)
        except:
            print("check client failed")
            break

    # await websocket.send(json.dumps(dataPh))
    
        


websocket_users = set()


# 检测客户端权限，用户名密码通过才能退出循环
async def check_user_permit(websocket):
    print("new websocket_users:", websocket)
    websocket_users.add(websocket)
    print("websocket_users list:", websocket_users)
    while True:
        recv_str = await websocket.recv()
        cred_dict = recv_str.split(":")
        if cred_dict[0] == "admin" and cred_dict[1] == "123456":
            response_str = "Congratulation, you have connect with server..."
            await websocket.send(response_str)
            print("Password is ok...")
            return True
        else:
            response_str = "Sorry, please input the username or password..."
            print("Password is wrong...")
            await websocket.send(response_str)


# 接收客户端消息并处理，这里只是简单把客户端发来的返回回去
async def recv_user_msg(websocket):
    while True:
        recv_text = await websocket.recv()
        print("recv_text:", websocket.pong, recv_text)
        response_text = f"Server return: {recv_text}"
        print("response_text:", response_text)
        await websocket.send(response_text)
        

# 服务器端主逻辑
async def run(websocket, path):
    while True:
        try:
            asyncio.gather(send_data(websocket))
            # asyncio.gather(check_client(websocket))
            await check_user_permit(websocket)
            # asyncio.create_task(send_data(websocket))
            # await send_data(websocket)
            await recv_user_msg(websocket)
        except websockets.ConnectionClosed:
            print("ConnectionClosed...", path)    # 链接断开
            print("websocket_users old:", websocket_users)
            websocket_users.remove(websocket)
            print("websocket_users new:", websocket_users)
            break
        except websockets.InvalidState:
            print("InvalidState...")    # 无效状态
            break
        except Exception as e:
            print("Exception:", e)


if __name__ == '__main__':
    print("127.0.0.1:8181 websocket...")
    asyncio.get_event_loop().run_until_complete(websockets.serve(run, "127.0.0.1", 8181))
    asyncio.get_event_loop().run_forever()
