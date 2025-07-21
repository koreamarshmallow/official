#!/usr/bin/env python3
import requests
import json

def check_supabase_tables():
    # Supabase 설정
    SUPABASE_URL = "https://lvawgzthxcougqtqfhzb.supabase.co"
    SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx2YXdnenRoeGNvdWdxdHFmaHpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI4OTE4NzgsImV4cCI6MjA2ODQ2Nzg3OH0.wm2IbN88xYpAKDfShRE6_I8ke_xEicQvxSqhte4AYyw"
    
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        print("🗄️  Supabase 데이터베이스 테이블 목록")
        print("=" * 60)
        
        # 알려진 테이블들을 확인
        known_tables = [
            'board_posts',
            'users', 
            'posts',
            'articles',
            'comments',
            'categories',
            'tags',
            'contact_inquiries',
            'news',
            'members'
        ]
        
        existing_tables = []
        
        print("\n🔍 테이블 존재 여부 확인:")
        print("-" * 40)
        
        for table in known_tables:
            try:
                response = requests.get(
                    f"{SUPABASE_URL}/rest/v1/{table}?limit=1", 
                    headers=headers, 
                    timeout=5
                )
                
                if response.status_code == 200:
                    print(f"✅ {table} - 존재함")
                    existing_tables.append(table)
                elif response.status_code == 404:
                    print(f"❌ {table} - 존재하지 않음")
                else:
                    print(f"⚠️  {table} - 상태 코드: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {table} - 오류: {str(e)[:50]}...")
        
        # 존재하는 테이블들의 상세 정보
        if existing_tables:
            print(f"\n📊 존재하는 테이블 상세 정보:")
            print("=" * 50)
            
            for table in existing_tables:
                try:
                    # 테이블의 레코드 수 확인
                    response = requests.get(
                        f"{SUPABASE_URL}/rest/v1/{table}?select=count",
                        headers={**headers, "Prefer": "count=exact"}
                    )
                    
                    if response.status_code == 200:
                        total_count = response.headers.get('Content-Range', '0').split('/')[-1]
                        print(f"\n📋 {table}")
                        print(f"   레코드 수: {total_count}개")
                        
                        # 샘플 데이터 조회 (첫 번째 레코드)
                        sample_response = requests.get(
                            f"{SUPABASE_URL}/rest/v1/{table}?limit=1",
                            headers=headers
                        )
                        
                        if sample_response.status_code == 200:
                            sample_data = sample_response.json()
                            if sample_data:
                                print("   컬럼 구조:")
                                for key, value in sample_data[0].items():
                                    value_type = type(value).__name__
                                    print(f"     • {key}: {value_type}")
                        
                except Exception as e:
                    print(f"   ❌ 상세 정보 조회 실패: {str(e)[:50]}...")
        
        # board_posts 테이블 특별 분석
        if 'board_posts' in existing_tables:
            print(f"\n🎯 board_posts 테이블 특별 분석:")
            print("-" * 40)
            
            try:
                # 최근 게시글 3개
                response = requests.get(
                    f"{SUPABASE_URL}/rest/v1/board_posts?order=created_at.desc&limit=3&select=id,title,nickname,created_at,likes,views",
                    headers=headers
                )
                
                if response.status_code == 200:
                    recent_posts = response.json()
                    print("최근 게시글 3개:")
                    for post in recent_posts:
                        print(f"   • ID {post['id']}: {post['title']}")
                        print(f"     작성자: {post['nickname']} | 추천: {post.get('likes', 0)} | 조회: {post.get('views', 0)}")
                        print(f"     작성일: {post['created_at']}")
                        print()
                
                # 공지사항 수
                notice_response = requests.get(
                    f"{SUPABASE_URL}/rest/v1/board_posts?is_notice=eq.true&select=count",
                    headers={**headers, "Prefer": "count=exact"}
                )
                
                if notice_response.status_code == 200:
                    notice_count = notice_response.headers.get('Content-Range', '0').split('/')[-1]
                    print(f"공지사항 수: {notice_count}개")
                
            except Exception as e:
                print(f"❌ board_posts 분석 실패: {str(e)[:50]}...")
        
        print(f"\n✅ 테이블 목록 조회 완료!")
        print(f"총 {len(existing_tables)}개의 테이블이 존재합니다: {', '.join(existing_tables)}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    check_supabase_tables()