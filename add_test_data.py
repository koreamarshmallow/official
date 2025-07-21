#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def add_test_posts():
    # Supabase 설정
    SUPABASE_URL = "https://lvawgzthxcougqtqfhzb.supabase.co"
    SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx2YXdnenRoeGNvdWdxdHFmaHpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI4OTE4NzgsImV4cCI6MjA2ODQ2Nzg3OH0.wm2IbN88xYpAKDfShRE6_I8ke_xEicQvxSqhte4AYyw"
    
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    # 테스트 게시글 데이터
    test_posts = [
        {
            "title": "🎉 한국마시멜로우협회 게시판 오픈!",
            "content": "안녕하세요! 한국마시멜로우협회 공식 게시판이 오픈되었습니다.\n\n마시멜로우에 관한 모든 이야기를 자유롭게 나누어보세요!\n- 재배 경험 공유\n- 레시피 교환\n- 질문과 답변\n- 협회 소식\n\n많은 참여 부탁드립니다! 🍭",
            "nickname": "관리자",
            "email": "admin@marshmallow.or.kr",
            "ip_address": "127.0.0.1",
            "is_notice": True,
            "likes": 15,
            "views": 89
        },
        {
            "title": "마시멜로우 재배 첫 도전 후기",
            "content": "올해 처음으로 마시멜로우 재배에 도전해봤습니다!\n\n처음에는 정말 어려웠는데, 협회에서 제공해주신 가이드라인을 따라하니 점점 요령이 생기더라구요.\n\n특히 온도와 습도 관리가 정말 중요한 것 같아요. 초보자분들께 도움이 될까 해서 몇 가지 팁을 공유합니다:\n\n1. 온도는 18-22도 유지\n2. 습도는 60-70% 유지\n3. 직사광선 피하기\n4. 통풍 잘 되는 곳에 배치\n\n다음 시즌에는 더 좋은 결과를 얻을 수 있을 것 같습니다! 💪",
            "nickname": "농부김씨",
            "email": "farmer@example.com",
            "ip_address": "192.168.1.100",
            "is_notice": False,
            "likes": 23,
            "views": 156
        },
        {
            "title": "마시멜로우 요리 레시피 공유",
            "content": "집에서 만든 마시멜로우로 간단한 디저트를 만들어봤어요!\n\n🍫 마시멜로우 초콜릿 바\n재료:\n- 마시멜로우 200g\n- 다크초콜릿 150g\n- 견과류 50g\n\n만드는 법:\n1. 초콜릿을 중탕으로 녹입니다\n2. 마시멜로우를 작게 자릅니다\n3. 녹인 초콜릿에 마시멜로우와 견과류를 넣고 섞습니다\n4. 틀에 부어 냉장고에서 2시간 굳힙니다\n\n정말 맛있어요! 다른 분들도 한번 시도해보세요 😋",
            "nickname": "디저트러버",
            "email": "dessert@example.com",
            "ip_address": "10.0.0.50",
            "is_notice": False,
            "likes": 31,
            "views": 203
        },
        {
            "title": "마시멜로우 품질 인증 기준 안내",
            "content": "한국마시멜로우협회에서 시행하는 품질 인증 기준에 대해 안내드립니다.\n\n📋 인증 기준:\n1. 원료의 순도 (95% 이상)\n2. 당도 측정 (Brix 75-80)\n3. 수분 함량 (18-22%)\n4. 미생물 검사 통과\n5. 중금속 검사 통과\n\n🏆 인증 혜택:\n- 협회 공식 인증마크 사용 권한\n- 마케팅 지원\n- 유통업체 연결 서비스\n- 기술 컨설팅 제공\n\n자세한 문의는 협회 사무국으로 연락주세요.\n📞 02-1234-5678",
            "nickname": "품질관리팀",
            "email": "quality@marshmallow.or.kr",
            "ip_address": "203.241.185.10",
            "is_notice": True,
            "likes": 8,
            "views": 67
        },
        {
            "title": "마시멜로우 시장 동향 분석",
            "content": "2024년 마시멜로우 시장 동향을 분석해봤습니다.\n\n📈 주요 트렌드:\n- 프리미엄 마시멜로우 수요 증가 (전년 대비 35% 상승)\n- 유기농 제품 선호도 상승\n- 온라인 직판 채널 확대\n- 해외 수출 증가 (일본, 동남아시아)\n\n💡 시사점:\n품질 향상과 브랜딩이 더욱 중요해지고 있습니다. 협회에서도 회원사들의 경쟁력 강화를 위한 다양한 지원 프로그램을 준비하고 있으니 많은 관심 부탁드립니다.\n\n자세한 보고서는 협회 홈페이지에서 다운로드 받으실 수 있습니다.",
            "nickname": "시장분석팀",
            "email": "research@marshmallow.or.kr",
            "ip_address": "211.106.114.186",
            "is_notice": False,
            "likes": 12,
            "views": 94
        }
    ]
    
    try:
        print("🚀 테스트 게시글 추가 중...")
        
        for i, post in enumerate(test_posts, 1):
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/board_posts",
                headers=headers,
                json=post
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ 게시글 {i} 추가 성공: {post['title'][:30]}...")
            else:
                print(f"❌ 게시글 {i} 추가 실패: {response.status_code}")
                print(f"   응답: {response.text}")
        
        print(f"\n🎉 총 {len(test_posts)}개의 테스트 게시글 추가 완료!")
        print("이제 board.html을 열어서 게시판을 확인해보세요!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    add_test_posts()