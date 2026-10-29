import os
import xml.etree.ElementTree as ET
import requests

# LG Channels EPG endpoint for Great Britain (GB)
# Note: Adjust the URL if your specific playlist source endpoint differs
API_URL = "https://its-newid.net/api/lg/gb"  # Or standard LG EPG endpoint provider URL
OUTPUT_FILENAME = "LG_Channels_GB.xml"


def fetch_lg_channels_gb():
  print("Fetching LG Channels GB data...")
  try:
    # If using a direct XML source or API endpoint
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()
    return response.content
  except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    return None


def save_xml_file(xml_content):
  # Ensure it writes directly to the main directory
  main_directory = os.path.dirname(os.path.abspath(__file__))
  output_path = os.path.join(main_directory, OUTPUT_FILENAME)

  if xml_content:
    try:
      # Parse and pretty-print/validate XML before saving
      root = ET.fromstring(xml_content)
      tree = ET.ElementTree(root)

      # Write out with UTF-8 encoding matching standard XMLTV format
      tree.write(output_path, encoding="utf-8", xml_declaration=True)
      print(f"Successfully saved {OUTPUT_FILENAME} to main directory: {output_path}")
    except ET.ParseError as pe:
      print(f"Failed to parse XML content: {pe}")
      # Fallback to writing raw bytes if XML parsing strictness fails
      with open(output_path, "wb") as f:
        f.write(xml_content)
      print(f"Saved raw content to {output_path}")


if __name__ == "__main__":
  content = fetch_lg_channels_gb()
  if content:
    save_xml_file(content)
  else:
    print("No content retrieved. Exiting.")
