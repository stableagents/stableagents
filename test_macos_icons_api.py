#!/usr/bin/env python3
"""
Test script for macOS Icons API integration
"""

import requests
import json

class macOSIconsAPITest:
    def __init__(self):
        self.base_url = "https://macosicons.com/api"
    
    def test_search(self, query="calculator"):
        """Test the search functionality"""
        print(f"🔍 Testing search for: '{query}'")
        try:
            url = f"{self.base_url}/search"
            params = {"q": query, "size": "512"}
            
            print(f"📡 Making request to: {url}")
            response = requests.get(url, params=params)
            
            print(f"📊 Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Search successful!")
                print(f"📋 Response keys: {list(data.keys())}")
                
                if "icons" in data:
                    icons = data["icons"]
                    print(f"🎨 Found {len(icons)} icons")
                    
                    if icons:
                        first_icon = icons[0]
                        print(f"📝 First icon: {first_icon.get('name', 'Unknown')}")
                        print(f"🆔 Icon ID: {first_icon.get('id', 'Unknown')}")
                        print(f"📄 Description: {first_icon.get('description', 'No description')}")
                        
                        return True, data
                    else:
                        print("❌ No icons found in response")
                        return False, data
                else:
                    print("❌ No 'icons' key in response")
                    return False, data
            else:
                print(f"❌ Request failed with status {response.status_code}")
                print(f"📄 Response text: {response.text[:200]}...")
                return False, None
                
        except Exception as e:
            print(f"❌ Error during search: {str(e)}")
            return False, None
    
    def test_icon_download(self, icon_id):
        """Test icon download functionality"""
        print(f"⬇️ Testing icon download for ID: {icon_id}")
        try:
            url = f"{self.base_url}/icon/{icon_id}"
            params = {"size": "512"}
            
            print(f"📡 Making request to: {url}")
            response = requests.get(url, params=params)
            
            print(f"📊 Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Icon info retrieved!")
                print(f"📋 Response keys: {list(data.keys())}")
                
                if "url" in data:
                    icon_url = data["url"]
                    print(f"🔗 Icon URL: {icon_url}")
                    
                    # Test downloading the icon
                    print("⬇️ Testing icon download...")
                    icon_response = requests.get(icon_url)
                    
                    if icon_response.status_code == 200:
                        print(f"✅ Icon downloaded successfully!")
                        print(f"📏 Icon size: {len(icon_response.content)} bytes")
                        
                        # Save the icon
                        filename = f"test_icon_{icon_id}.png"
                        with open(filename, 'wb') as f:
                            f.write(icon_response.content)
                        print(f"💾 Icon saved as: {filename}")
                        
                        return True, data
                    else:
                        print(f"❌ Icon download failed: {icon_response.status_code}")
                        return False, data
                else:
                    print("❌ No 'url' key in response")
                    return False, data
            else:
                print(f"❌ Request failed with status {response.status_code}")
                return False, None
                
        except Exception as e:
            print(f"❌ Error during icon download: {str(e)}")
            return False, None

def main():
    print("🚀 macOS Icons API Test")
    print("=" * 50)
    
    api_test = macOSIconsAPITest()
    
    # Test search functionality
    print("\n1️⃣ Testing Search Functionality")
    print("-" * 30)
    success, data = api_test.test_search("calculator")
    
    if success and data and "icons" in data and data["icons"]:
        # Test icon download
        print("\n2️⃣ Testing Icon Download")
        print("-" * 30)
        first_icon = data["icons"][0]
        icon_id = first_icon.get("id")
        
        if icon_id:
            api_test.test_icon_download(icon_id)
        else:
            print("❌ No icon ID found in response")
    else:
        print("\n⚠️ Skipping icon download test due to search failure")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")

if __name__ == "__main__":
    main() 