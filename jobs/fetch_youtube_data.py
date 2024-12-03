import argparse
import requests
import json
import re
from datetime import datetime

def fetch_video_list(api_key, channel_id, max_results=50):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "channelId": channel_id,
        "order": "viewCount",
        "type": "video",
        "maxResults": max_results,
        "key": api_key,
    }
    response = requests.get(url, params=params)
    data = response.json()
    video_details = []
    if "items" in data:
        for item in data["items"]:
            title = item["snippet"]["title"]
            cleaned_title = re.sub(r"[^\w\s]", "", title).strip()  # 특수문자 제거
            if cleaned_title:
                video_details.append({
                    "videoId": item["id"]["videoId"],
                    "title": cleaned_title,
                })
    return video_details

def fetch_video_statistics(api_key, video_details):
    video_ids = [video['videoId'] for video in video_details]
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "statistics",
        "id": ",".join(video_ids),
        "key": api_key,
    }
    response = requests.get(url, params=params)
    data = response.json()
    video_stats = []
    if "items" in data:
        for i, item in enumerate(data["items"]):
            stats = item["statistics"]
            video_stats.append({
                "videoId": item["id"],
                "title": video_details[i]["title"],
                "viewCount": stats.get("viewCount", "0"),
                "likeCount": stats.get("likeCount", "0"),
                "commentCount": stats.get("commentCount", "0"),
            })
    return video_stats

def save_to_file(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_key", required=True, help="YouTube API key")
    parser.add_argument("--channel_id", required=True, help="YouTube Channel ID")
    parser.add_argument("--output_path", required=True, help="Output file path")
    args = parser.parse_args()

    video_list = fetch_video_list(args.api_key, args.channel_id, max_results=5)
    video_stats = fetch_video_statistics(args.api_key, video_list)
    save_to_file(video_stats, args.output_path)
