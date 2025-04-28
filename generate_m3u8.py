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

    # Add default stream(s) here
    default_streams = '''
#EXTINF:-1 tvg-logo=" https://www.fancode.com/skillup-uploads/fc-web-logo/fc_logo_white_bg.svg  " group-title="Cricket",FANCODE
#KODIPROP:inputstream.adaptive.license_type=clearkey
#KODIPROP:inputstream.adaptive.license_key=159a2b4e1d2d7f16892d35d935a2fb34:07809840dd0f511221ca78459167d1b3
https://a166aivottlinear-a.akamaihd.net/OTTB/sin-nitro/live/clients/dash/enc/gdhz5mhnyu/out/v1/fe72171ab2684ab8b9ee3e2ffcc9cff2/cenc.mpd

#EXTINF:-1 tvg-logo=" https://images.fubo.tv/channel-config-ui/station-logos/on-dark/willow_sports_stacked_logo_full_white.png?ch=width&auto=format%2Ccompress&w=0.4&h=0.4" group-title="Cricket",WILLOW SPORTS 
#KODIPROP:inputstream.adaptive.license_type=clearkey
#KODIPROP:inputstream.adaptive.license_key=1779c27b9d077a3ba0c9cc1bb9a94b9f:cc5cf3b7928fb9e0a1ee6a8b566f0a8e
https://abmyxykaaaaaaaamkyvb65fuqebyg.7a77200bf98444ac997a89ed83775793.emt.cf.ww.aiv-cdn.net/iad-nitro/live/clients/dash/enc/f60kqesunw/out/v1/a435ed7a00f947deb4369b46d8f2fb70/cenc.mpd




'''
    m3u_content += default_streams

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
