# 한국마시멜로협회 공식 홈페이지

한국마시멜로협회의 공식 웹사이트입니다. 

## 🍭 프로젝트 소개

한국마시멜로협회는 국내 마시멜로 산업의 발전과 품질 향상을 위해 설립된 전문 기관입니다. 이 웹사이트는 협회의 주요 서비스와 정보를 제공합니다.

## 🛠 기술 스택

- **Frontend**: HTML5, CSS3, JavaScript
- **CSS Framework**: Tailwind CSS
- **Database**: Supabase (PostgreSQL)
- **Hosting**: GitHub Pages
- **CI/CD**: GitHub Actions
- **Icons**: Font Awesome

## 🚀 주요 기능

- 반응형 웹 디자인
- 협회 소개 및 서비스 안내
- 최신 뉴스 및 공지사항
- 실시간 게시판 시스템
- 문의 양식
- 모바일 친화적 UI/UX
- 안전한 데이터베이스 연동

## 📱 반응형 디자인

모든 디바이스(데스크톱, 태블릿, 모바일)에서 최적화된 사용자 경험을 제공합니다.

## 🎨 디자인 특징

- 마시멜로를 연상시키는 부드러운 핑크 컬러 팔레트
- 깔끔하고 현대적인 레이아웃
- 직관적인 네비게이션
- 시각적으로 매력적인 그라디언트 효과

## ⚙️ 설정 가이드

### Supabase 데이터베이스 설정
게시판 기능을 사용하려면 Supabase 설정이 필요합니다.
자세한 설정 방법은 [SUPABASE_SETUP.md](SUPABASE_SETUP.md)를 참고하세요.

### GitHub Secrets 설정
1. GitHub 저장소 Settings > Secrets and variables > Actions
2. 다음 secrets 추가:
   - `SUPABASE_URL`: Supabase 프로젝트 URL
   - `SUPABASE_ANON_KEY`: Supabase anon public key

### 로컬 개발
```bash
# .env 파일 생성 (.env.example 참고)
cp .env.example .env

# 실제 Supabase 정보로 수정
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_ANON_KEY=your-anon-key
```

## 📞 연락처

- **주소**: 서울특별시 강남구 테헤란로 123 마시멜로타워 15층
- **전화**: 02-1234-5678
- **이메일**: info@marshmallow.or.kr

## 📄 라이선스

© 2024 한국마시멜로협회. All rights reserved.