#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def get_board_data():
    # Supabase 설정
    SUPABASE_URL = "https://lvawgzthxcougqtqfhzb.supabase.co"
    SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx2YXdnenRoeGNvdWdxdHFmaHpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI4OTE4NzgsImV4cCI6MjA2ODQ2Nzg3OH0.wm2IbN88xYpAKDfShRE6_I8ke_xEicQvxSqhte4AYyw"
    
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        print("📋 board_posts 테이블 데이터 조회")
        print("=" * 50)
        
        # 게시글 목록 조회 (최신 10개)
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/board_posts?order=created_at.desc&limit=10",
            headers=headers
        )
        
        if response.status_code == 200:
            posts = response.json()
            
            if posts:
                print(f"✅ 총 {len(posts)}개의 게시글을 찾았습니다.\n")
                
                for i, post in enumerate(posts, 1):
                    print(f"📝 게시글 #{i}")
                    print(f"   ID: {post.get('id', 'N/A')}")
                    print(f"   제목: {post.get('title', 'N/A')}")
                    print(f"   작성자: {post.get('nickname', 'N/A')}")
                    print(f"   내용: {post.get('content', 'N/A')[:50]}...")
                    print(f"   공지: {'예' if post.get('is_notice', False) else '아니오'}")
                    print(f"   추천: {post.get('likes', 0)}")
                    print(f"   조회: {post.get('views', 0)}")
                    
                    created_at = post.get('created_at')
                    if created_at:
                        try:
                            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                            print(f"   작성일: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
                        except:
                            print(f"   작성일: {created_at}")
                    
                    print()
                    
            else:
                print("❌ 게시글이 없습니다.")
                
        else:
            print(f"❌ 데이터 조회 실패: {response.status_code}")
            print(f"   응답: {response.text}")
            
        # 테이블 통계 정보
        print("\n📊 테이블 통계")
        print("-" * 30)
        
        # 전체 게시글 수
        count_response = requests.get(
            f"{SUPABASE_URL}/rest/v1/board_posts?select=count",
            headers={**headers, "Prefer": "count=exact"}
        )
        
        if count_response.status_code == 200:
            total_count = count_response.headers.get('Content-Range', '0').split('/')[-1]
            print(f"전체 게시글 수: {total_count}")
        
        # 공지사항 수
        notice_response = requests.get(
            f"{SUPABASE_URL}/rest/v1/board_posts?is_notice=eq.true&select=count",
            headers={**headers, "Prefer": "count=exact"}
        )
        
        if notice_response.status_code == 200:
            notice_count = notice_response.headers.get('Content-Range', '0').split('/')[-1]
            print(f"공지사항 수: {notice_count}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    get_board_data()