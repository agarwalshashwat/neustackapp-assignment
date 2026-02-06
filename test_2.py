# Write a function shouldAllowRequest(userId) that allows a maximum of 3 requests per 10 seconds per user.
from datetime import datetime, timedelta, timezone
import time
import uuid

requests = []
def shouldAllowRequest(userId):
    print("----Requests---", requests)
    current_time = int(time.time())
    last_third_request = requests[-3] if len(requests) >= 3 else {}

    if not last_third_request:
        requests.append({"request_id":uuid.uuid4(), "user_id": userId, "created_at": current_time})
        return print("pass")
    
    n = current_time - last_third_request.get("created_at")
    if n < 10:
        return f"You're rate limited please try after {n} seconds"
    else:
        requests.append({"request_id":uuid.uuid4(), "user_id": userId, "created_at": current_time})
        print("pass")


if __name__ == "__main__":
    shouldAllowRequest(1)
    time.sleep(1)
    shouldAllowRequest(1)
    time.sleep(1)
    shouldAllowRequest(1)
    time.sleep(1)
    shouldAllowRequest(1)
    time.sleep(1)
    shouldAllowRequest(1)
    shouldAllowRequest(1)
    time.sleep(1)
    shouldAllowRequest(1)
    time.sleep(1)
    shouldAllowRequest(1)