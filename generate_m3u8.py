import json
import requests
from datetime import datetime


def main():
    # Your remote JSON URL
    json_url = 'https://raw.githubusercontent.com/drmlive/willow-live-events/refs/heads/main/willow.json'

    # Fetch the JSON from the URL
    response = requests.get(json_url)
    data = response.json()

    # Start the M3U file
   # Start the M3U file with a timestamp so that it always changes
    m3u_content = f"#EXTM3U\n# Updated: {datetime.utcnow().isoformat()} UTC\n\n"

    

    group_title = "Willow"  # Fixed group-title to "Willow"
 # group_title = data.get('name', 'Unknown')  # Example: "Willow"

    for match in data['matches']:
        title = match['title'].strip()
        logo = match['cover']
        urls = match['playback_data'].get('urls', [])
        keys = match['playback_data'].get('keys', [])

        if not urls:
            continue  # Skip if no URLs

        stream_url = urls[0]['url']  # Take the FIRST URL

        m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group_title}", {title}\n'

        if keys:
            license_key = keys[0]  # Take the FIRST Key
            m3u_content += f'#KODIPROP:inputstream.adaptive.license_type=clearkey\n'
            m3u_content += f'#KODIPROP:inputstream.adaptive.license_key={license_key}\n'

        m3u_content += f'{stream_url}\n\n\n'

    # Save the M3U file
    with open('playlist.m3u8', 'w', encoding='utf-8') as f:
        f.write(m3u_content)

if __name__ == "__main__":
    main()
