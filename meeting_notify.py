from notion_client import Client
from datetime import datetime
from dateutil import parser
import pytz
import os

tz = pytz.timezone("Asia/Taipei")

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
MEETING_DB_ID = "cd784a100f784e15b401155bc3313a1f"
USERID_DB_ID = "21bd8d0b09f180908e1df38429153325"
notion = Client(auth=NOTION_TOKEN)

def get_staff_name_by_dc_id(dc_id: int):
    filter_cond = {
        "property": "DC ID",
        "number": {
            "equals": dc_id
        }
    }
    results = notion.databases.query(
        database_id=USERID_DB_ID,
        filter=filter_cond
    ).get("results", [])

    if not results:
        return None

    name = results[0]["properties"]["Name"]["title"][0]["text"]["content"]
    return name

def get_today_meetings_for_user(user_name: str):
    now = datetime.now(tz)
    today_str = now.date().isoformat()
    today_display = now.strftime("%Y/%m/%d")

    filter_conditions = {
        "and": [
            {
                "property": "日期",
                "date": {
                    "on_or_after": today_str,
                    "on_or_before": today_str
                }
            },
            {
                "property": "類別",
                "select": {
                    "equals": "會議"
                }
            }
        ]
    }

    meeting_pages = notion.databases.query(
        database_id=MEETING_DB_ID,
        filter=filter_conditions
    ).get("results", [])

    meetings_for_user = []

    for page in meeting_pages:
        props = page["properties"]
        persons = props.get("相關人員", {}).get("people", [])

        if not any(user_name == p.get("name", "") for p in persons):
            continue

        title = props["Name"]["title"][0]["text"]["content"] if props["Name"]["title"] else "未命名會議"
        datetime_str = props["日期"]["date"]["start"]
        dt_obj = parser.isoparse(datetime_str).astimezone(tz)

        if dt_obj.date() != now.date():
            continue

        date_time = dt_obj.strftime("%Y/%m/%d %H:%M")

        location = "未填寫"
        location_prop = props.get("地點")
        if location_prop and location_prop.get("select"):
            location = location_prop["select"]["name"]

        meetings_for_user.append({
            "title": title,
            "datetime": date_time,
            "location": location
        })

    if not meetings_for_user:
        return f"{today_display} 今天沒有會議喔！"

    lines = [f"{today_display} 會議提醒"]
    for idx, m in enumerate(meetings_for_user, start=1):
        lines.append(f"{idx}. {m['title']}")
        lines.append(f"－ 時間：{m['datetime']}")
        lines.append(f"－ 地點：{m['location']}")
        lines.append("")

    return "\n".join(lines).strip()

def get_meeting_notification_by_dc_id(dc_id: int) -> str:
    """主函式，傳入 Discord user id (數字)，回傳會議訊息字串"""
    user_name = get_staff_name_by_dc_id(dc_id)
    if not user_name:
        return "❌ 找不到你的員編資料，請聯絡管理員登記"

    return get_today_meetings_for_user(user_name)
