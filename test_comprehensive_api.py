"""
Test script for comprehensive API flow
Tests all endpoints step by step:
1. Psychology submit
2. Neuroscience submit
3. Astrology analyze
4. Comprehensive analyze from results
"""

import httpx
import json
import asyncio
from datetime import datetime


BASE_URL = "http://localhost:8000"


async def test_psychology_api():
    """Test 1: Psychology Assessment"""
    print("\n" + "="*60)
    print("🧠 Test 1: Psychology Assessment API")
    print("="*60)
    
    # Submit answers
    payload = {
        "answers": [1, 2, 3, 1, 2, 1, 3]  # 7 answers, each 1-3
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/psychology/submit",
            json=payload,
            timeout=10.0
        )
    
    print(f"\n📤 Request to: POST /psychology/submit")
    print(f"📦 Payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
    print(f"\n✅ Status: {response.status_code}")
    
    result = response.json()
    print(f"\n📥 Response:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    return result


async def test_neuroscience_api():
    """Test 2: Neuroscience Assessment"""
    print("\n" + "="*60)
    print("🧬 Test 2: Neuroscience Assessment API")
    print("="*60)
    
    # Submit answers
    payload = {
        "answers": ["A", "B", "A", "C", "A", "B", "D", "A", "B"]  # 9 answers
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/neuroscience/submit",
            json=payload,
            timeout=10.0
        )
    
    print(f"\n📤 Request to: POST /neuroscience/submit")
    print(f"📦 Payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
    print(f"\n✅ Status: {response.status_code}")
    
    result = response.json()
    print(f"\n📥 Response:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    return result


async def test_astrology_api():
    """Test 3: Astrology Analysis"""
    print("\n" + "="*60)
    print("⭐ Test 3: Astrology Analysis API")
    print("="*60)
    
    # Analyze astrology
    payload = {
        "name": "أحمد",
        "birth_date": "1995-03-21",
        "day_type": "today",
        "birth_time": "14:30",
        "birth_location": "القاهرة",
        "latitude": 30.0444,
        "longitude": 31.2357
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/astrology/analyze",
            json=payload,
            timeout=30.0  # Longer timeout for API calls
        )
    
    print(f"\n📤 Request to: POST /astrology/analyze")
    print(f"📦 Payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
    print(f"\n✅ Status: {response.status_code}")
    
    result = response.json()
    print(f"\n📥 Response:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    return result


async def test_comprehensive_api(psychology_result, neuroscience_result, astrology_result):
    """Test 4: Comprehensive Analysis from Results (NEW!)"""
    print("\n" + "="*60)
    print("🎯 Test 4: Comprehensive Analysis API (NEW ENDPOINT!)")
    print("="*60)
    
    # Send all results to get comprehensive analysis
    payload = {
        "name": "أحمد",
        "psychology_result": psychology_result,
        "neuroscience_result": neuroscience_result,
        "astrology_result": astrology_result
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/comprehensive/analyze-from-results",
            json=payload,
            timeout=60.0  # Longer timeout for AI generation
        )
    
    print(f"\n📤 Request to: POST /comprehensive/analyze-from-results")
    print(f"📦 Payload Structure:")
    print(f"   - name: {payload['name']}")
    print(f"   - psychology_result: ✅ (score: {psychology_result.get('score')})")
    print(f"   - neuroscience_result: ✅ (dominant: {neuroscience_result.get('dominant')})")
    print(f"   - astrology_result: ✅ (sun_sign: {astrology_result.get('sun_sign')})")
    
    print(f"\n✅ Status: {response.status_code}")
    
    result = response.json()
    print(f"\n📥 Response:")
    print(f"   - name: {result.get('name')}")
    print(f"   - type: {result.get('type')}")
    print(f"   - status: {result.get('status')}")
    print(f"   - message: {result.get('message')}")
    print(f"\n📊 Comprehensive Report (first 500 chars):")
    print("-" * 60)
    report = result.get('report', '')
    print(report[:500] + "..." if len(report) > 500 else report)
    print("-" * 60)
    
    # Save full report to file
    with open("comprehensive_report.txt", "w", encoding="utf-8") as f:
        f.write(f"تقرير شامل للمستخدم: {result.get('name')}\n")
        f.write(f"التاريخ: {datetime.now()}\n")
        f.write("=" * 80 + "\n\n")
        f.write(result.get('report', ''))
    
    print(f"\n💾 Full report saved to: comprehensive_report.txt")
    
    return result


async def main():
    """Run all tests in sequence"""
    print("\n" + "🚀" * 30)
    print("بدء اختبار الـ API الشامل")
    print("🚀" * 30)
    
    try:
        # Test 1: Psychology
        psychology_result = await test_psychology_api()
        await asyncio.sleep(1)
        
        # Test 2: Neuroscience
        neuroscience_result = await test_neuroscience_api()
        await asyncio.sleep(1)
        
        # Test 3: Astrology
        astrology_result = await test_astrology_api()
        await asyncio.sleep(1)
        
        # Test 4: Comprehensive (NEW!)
        comprehensive_result = await test_comprehensive_api(
            psychology_result,
            neuroscience_result,
            astrology_result
        )
        
        print("\n" + "✅" * 30)
        print("اكتمل الاختبار بنجاح!")
        print("✅" * 30)
        print("\n📝 Summary:")
        print(f"   1. Psychology: ✅ Score = {psychology_result.get('score')}")
        print(f"   2. Neuroscience: ✅ Dominant = {neuroscience_result.get('dominant')}")
        print(f"   3. Astrology: ✅ Sun Sign = {astrology_result.get('sun_sign')}")
        print(f"   4. Comprehensive: ✅ Report generated successfully!")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
