import faust

from time import sleep

print("sleeping...", flush=True)
sleep(20)
print("woke up.")

app = faust.App("views_counter", broker="kafka://kafka:9092")

topic = app.topic("views", value_type=str, value_serializer="raw")


@app.agent(topic)
async def processor(stream):
    async for message in stream:
        print(f"Received : {message}", flush=True)
