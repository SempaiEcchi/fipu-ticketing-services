import asyncio
import server
import email_data


async def test():
    print("running")
    id = await server.create_instance()
    await  server.call_receive_mail_task(id, email_data.EmailData("test text"))


if __name__ == "__main__":
    asyncio.run(test())
