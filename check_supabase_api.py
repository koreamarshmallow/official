#!/usr/bin/env python3
import requests
import json

def check_supabase_connection():
    # Supabase 설정
    SUPABASE_URL = "https://lvawgzthxcougqtqfhzb.supabase.co"
    SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx2YXdnenRoeGNvdWdxdHFmaHpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI4OTE4NzgsImV4cCI6MjA2ODQ2Nzg3OH0.wm2IbN88xYpAKDfShRE6_I8ke_xEicQvxSqhte4AYyw"
    
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # Supabase REST API로 연결 테스트
        print("🔗 Supabase 연결 테스트 중...")
        
        # 기본 연결 확인
        response = requests.get(f"{SUPABASE_URL}/rest/v1/", headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Supabase REST API 연결 성공!")
            
            # 사용 가능한 테이블 확인 (OpenAPI 스키마)
            schema_response = requests.get(f"{SUPABASE_URL}/rest/v1/", headers=headers)
            
            if schema_response.status_code == 200:
                print("\n📋 Supabase 연결 정보:")
                print(f"   - URL: {SUPABASE_URL}")
                print(f"   - 상태: 연결됨")
                
                # 실제 테이블이 있는지 확인해보기 위해 몇 가지 일반적인 테이블명으로 시도
                test_tables = ['board_posts', 'users', 'posts', 'articles']
                
                print("\n🔍 테이블 존재 여부 확인:")
                for table in test_tables:
                    try:
                        table_response = requests.get(
                            f"{SUPABASE_URL}/rest/v1/{table}?limit=1", 
                            headers=headers, 
                            timeout=5
                        )
                        if table_response.status_code == 200:
                            print(f"   ✅ {table} - 존재함")
                        elif table_response.status_code == 404:
                            print(f"   ❌ {table} - 존재하지 않음")
                        else:
                            print(f"   ⚠️  {table} - 상태 코드: {table_response.status_code}")
                    except Exception as e:
                        print(f"   ❌ {table} - 오류: {str(e)[:50]}...")
                        
            else:
                print(f"❌ 스키마 조회 실패: {schema_response.status_code}")
                
        else:
            print(f"❌ Supabase 연결 실패: {response.status_code}")
            print(f"   응답: {response.text[:200]}...")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 네트워크 오류: {e}")
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")

if __name__ == "__main__":
    check_supabase_connection()