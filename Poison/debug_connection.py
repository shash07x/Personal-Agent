"""Quick diagnostic for Gemini API connectivity."""
import json, sys, asyncio
from pathlib import Path

API_KEY_PATH = Path(__file__).parent / "config" / "api_keys.json"

def get_key():
    with open(API_KEY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["gemini_api_key"]

api_key = get_key()
print(f"[1] API Key loaded: {api_key[:8]}...{api_key[-4:]}")
print(f"    Key length: {len(api_key)}")
print(f"    Key prefix: {api_key[:3]}")
print()

# Test 1: Simple HTTP call (non-websocket)
print("[2] Testing simple text generation (HTTP, not WebSocket)...")
try:
    from google import genai
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents="Say hello in one word."
    )
    result = (response.text or "").strip()
    print(f"    ✅ HTTP API works! Response: {result}")
except Exception as e:
    print(f"    ❌ HTTP API failed: {e}")
    print(f"    This means your API key is invalid or network is blocked.")
    sys.exit(1)

print()

# Test 2: List available models with 'native-audio'
print("[3] Checking available native-audio models...")
try:
    found = []
    for m in client.models.list():
        if m.name and "native-audio" in m.name:
            found.append(m.name)
    if found:
        for name in found:
            print(f"    ✅ {name}")
    else:
        print("    ⚠️  No native-audio models found. Listing all live-capable models:")
        for m in client.models.list():
            if m.name and "flash" in m.name.lower():
                print(f"       {m.name}")
except Exception as e:
    print(f"    ❌ Model listing failed: {e}")

print()

# Test 3: WebSocket Live API connection
print("[4] Testing Live API WebSocket connection...")
LIVE_MODEL = "models/gemini-2.5-flash-native-audio-latest"

async def test_live():
    from google.genai import types
    client = genai.Client(
        api_key=api_key,
        http_options={"api_version": "v1beta"}
    )
    try:
        async with client.aio.live.connect(
            model=LIVE_MODEL,
            config=types.LiveConnectConfig(
                response_modalities=["AUDIO"],
            )
        ) as session:
            print(f"    ✅ WebSocket connected to {LIVE_MODEL}!")
            # Just connect and disconnect
    except Exception as e:
        print(f"    ❌ WebSocket failed with {LIVE_MODEL}: {e}")
        # Try alternative model names
        alt_models = [
            "models/gemini-2.5-flash-preview-native-audio-dialog",
            "models/gemini-2.0-flash-live-001",
        ]
        for alt in alt_models:
            try:
                print(f"    🔄 Trying {alt}...")
                async with client.aio.live.connect(
                    model=alt,
                    config=types.LiveConnectConfig(
                        response_modalities=["AUDIO"],
                    )
                ) as session:
                    print(f"    ✅ WebSocket connected to {alt}!")
                    return alt
            except Exception as e2:
                print(f"    ❌ {alt} also failed: {e2}")
        return None

asyncio.run(test_live())
print("\n[Done]")
