from supabase import create_client, Client

url = "https://lvawgzthxcougqtqfhzb.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx2YXdnenRoeGNvdWdxdHFmaHpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI4OTE4NzgsImV4cCI6MjA2ODQ2Nzg3OH0.wm2IbN88xYpAKDfShRE6_I8ke_xEicQvxSqhte4AYyw"
supabase: Client = create_client(url, key)

dummy_posts = [
    {
        "title": "마시멜로우 재배 꿀팁 공유해요!",
        "content": "작년에 처음 재배해봤는데, 물 주는 시기와 양이 정말 중요하더라고요. 혹시 다른 분들은 어떤 비법이 있으신가요?",
        "nickname": "초보농부",
        "email": "farmer1@example.com",
        "ip_address": "192.168.1.101",
        "is_notice": False,
        "likes": 5,
        "views": 42
    },
    {
        "title": "마시멜로우 꽃이 피었어요!",
        "content": "드디어 저희 밭에도 마시멜로우 꽃이 피었습니다. 사진은 첨부 못하지만 정말 예뻐요. 다들 풍년 되세요~",
        "nickname": "행복한농장",
        "email": "happyfarm@example.com",
        "ip_address": "192.168.1.102",
        "is_notice": False,
        "likes": 8,
        "views": 67
    },
    {
        "title": "비 오는 날 관리법 질문",
        "content": "이번 주 내내 비가 온다는데, 마시멜로우가 습기에 약하다고 들었어요. 다들 어떻게 관리하시나요?",
        "nickname": "궁금이",
        "email": "asker@example.com",
        "ip_address": "192.168.1.103",
        "is_notice": False,
        "likes": 2,
        "views": 31
    },
    {
        "title": "마시멜로우 수확량 늘리는 방법?",
        "content": "작년보다 수확량이 줄어서 고민입니다. 비료나 토양 관리에 팁 있으신 분 계신가요?",
        "nickname": "수확왕",
        "email": "harvestking@example.com",
        "ip_address": "192.168.1.104",
        "is_notice": False,
        "likes": 3,
        "views": 28
    },
    {
        "title": "마시멜로우로 만든 디저트 추천",
        "content": "직접 재배한 마시멜로우로 디저트 만들어봤어요! 구워 먹으니 정말 맛있네요. 다른 레시피도 공유해주시면 감사하겠습니다.",
        "nickname": "디저트러버",
        "email": "dessertlover@example.com",
        "ip_address": "192.168.1.105",
        "is_notice": False,
        "likes": 7,
        "views": 54
    },
    {
        "title": "초보자를 위한 재배 가이드",
        "content": "마시멜로우 재배 처음이신 분들께: 햇빛, 물, 통풍만 잘 챙기면 생각보다 어렵지 않아요! 모두 화이팅입니다.",
        "nickname": "응원맨",
        "email": "cheerup@example.com",
        "ip_address": "192.168.1.106",
        "is_notice": False,
        "likes": 4,
        "views": 39
    },
    {
        "title": "마시멜로우 병충해 방지법",
        "content": "올해는 벌레가 많아서 걱정이네요. 친환경 방제법 아시는 분 있으면 공유 부탁드려요.",
        "nickname": "걱정많은농부",
        "email": "worryfarmer@example.com",
        "ip_address": "192.168.1.107",
        "is_notice": False,
        "likes": 1,
        "views": 22
    },
    {
        "title": "마시멜로우 재배 인증샷",
        "content": "드디어 첫 수확! 가족들과 함께 기뻐했어요. 모두들 풍성한 수확 하시길 바랍니다.",
        "nickname": "행복가득",
        "email": "joyful@example.com",
        "ip_address": "192.168.1.108",
        "is_notice": False,
        "likes": 6,
        "views": 48
    },
    {
        "title": "마시멜로우 재배 중 실수담",
        "content": "물을 너무 많이 줘서 뿌리가 썩을 뻔 했어요. 초보분들 참고하세요! 적당히가 제일 중요합니다.",
        "nickname": "실수쟁이",
        "email": "mistaker@example.com",
        "ip_address": "192.168.1.109",
        "is_notice": False,
        "likes": 2,
        "views": 35
    },
    {
        "title": "마시멜로우 재배 동호회 모집",
        "content": "함께 정보도 나누고, 오프라인 모임도 하고 싶어요! 관심 있으신 분 댓글 남겨주세요~",
        "nickname": "동호회장",
        "email": "clubmaster@example.com",
        "ip_address": "192.168.1.110",
        "is_notice": False,
        "likes": 9,
        "views": 73
    }
]

result = supabase.table("board_posts").insert(dummy_posts).execute()
print("추가 결과:", result)