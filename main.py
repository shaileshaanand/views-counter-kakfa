import faust

from time import sleep

print("sleeping...", flush=True)
sleep(10)
print("woke up.")

app = faust.App("views_counter", broker="kafka://kafka:9092")


class PostView(faust.Record):
    post_id: str
    user_id: str


topic = app.topic("views", value_type=PostView)
post_views = app.Table("post_views", default=int)


@app.agent(topic)
async def processor(stream):
    async for message in stream.group_by(PostView.post_id):
        print(f"Received : {message}", flush=True)
        post_views[message.post_id] += 1
