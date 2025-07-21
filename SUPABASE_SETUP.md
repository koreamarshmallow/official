# Supabase 설정 가이드

이 가이드는 GitHub에 인증정보를 공개하지 않고 Supabase를 안전하게 사용하는 방법을 설명합니다.

## 1. Supabase 프로젝트 설정

### 1.1 Supabase 계정 생성 및 프로젝트 생성
1. [Supabase](https://supabase.com)에 가입
2. 새 프로젝트 생성
3. 프로젝트 URL과 anon public key 확인

### 1.2 데이터베이스 테이블 생성
Supabase SQL Editor에서 다음 SQL을 실행:

```sql
-- 게시판 테이블 생성
CREATE TABLE board_posts (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    nickname VARCHAR(50) NOT NULL,
    email VARCHAR(255),
    ip_address VARCHAR(45),
    is_notice BOOLEAN DEFAULT FALSE,
    likes INTEGER DEFAULT 0,
    views INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스 생성
CREATE INDEX idx_board_posts_created_at ON board_posts(created_at DESC);
CREATE INDEX idx_board_posts_likes ON board_posts(likes DESC);
CREATE INDEX idx_board_posts_is_notice ON board_posts(is_notice);

-- RLS (Row Level Security) 정책 설정
ALTER TABLE board_posts ENABLE ROW LEVEL SECURITY;

-- 모든 사용자가 게시글을 읽을 수 있도록 허용
CREATE POLICY "Anyone can read posts" ON board_posts FOR SELECT USING (true);

-- 모든 사용자가 게시글을 작성할 수 있도록 허용
CREATE POLICY "Anyone can insert posts" ON board_posts FOR INSERT WITH CHECK (true);

-- 게시글 업데이트 (추천, 조회수)
CREATE POLICY "Anyone can update post stats" ON board_posts FOR UPDATE USING (true);

-- 게시글 삭제 (필요시)
CREATE POLICY "Anyone can delete posts" ON board_posts FOR DELETE USING (true);
```

## 2. GitHub Secrets 설정

### 2.1 GitHub 저장소 설정
1. GitHub 저장소의 **Settings** 탭으로 이동
2. 왼쪽 메뉴에서 **Secrets and variables** > **Actions** 선택
3. **New repository secret** 버튼 클릭

### 2.2 필요한 Secrets 추가
다음 두 개의 secret을 추가하세요:

- **Name**: `SUPABASE_URL`
  - **Value**: 당신의 Supabase 프로젝트 URL (예: `https://your-project.supabase.co`)

- **Name**: `SUPABASE_ANON_KEY`
  - **Value**: 당신의 Supabase anon public key

## 3. 로컬 개발 환경 설정

### 3.1 환경 변수 파일 생성
프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 추가:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
```

**주의**: `.env` 파일은 `.gitignore`에 포함되어 있어 GitHub에 업로드되지 않습니다.

### 3.2 로컬 테스트
1. HTML 파일을 브라우저에서 열기
2. 개발자 도구 콘솔에서 Supabase 연결 상태 확인
3. 게시글 작성/조회 테스트

## 4. 배포

### 4.1 자동 배포
- `main` 브랜치에 푸시하면 GitHub Actions가 자동으로 실행됩니다
- GitHub Secrets의 값들이 HTML 파일에 안전하게 주입됩니다
- GitHub Pages로 자동 배포됩니다

### 4.2 수동 배포
GitHub Actions 탭에서 워크플로우를 수동으로 실행할 수 있습니다.

## 5. 보안 고려사항

### 5.1 anon public key 사용
- Supabase의 anon public key는 클라이언트에서 사용하도록 설계되었습니다
- RLS(Row Level Security) 정책으로 데이터 접근을 제어합니다

### 5.2 추가 보안 강화
더 높은 보안이 필요한 경우:
1. 서버리스 함수 사용 (Netlify Functions, Vercel Functions)
2. 별도 백엔드 API 서버 구축
3. JWT 토큰 기반 인증 구현

## 6. 문제 해결

### 6.1 Supabase 연결 실패
- 브라우저 개발자 도구에서 네트워크 탭 확인
- CORS 설정 확인
- URL과 키가 올바른지 확인

### 6.2 로컬 스토리지 폴백
- Supabase 연결이 실패하면 자동으로 로컬 스토리지를 사용합니다
- 데이터는 브라우저에만 저장되며 다른 사용자와 공유되지 않습니다

## 7. 추가 기능

### 7.1 관리자 기능
- 관리자 키를 사용한 게시글 삭제
- 공지사항 등록

### 7.2 확장 가능한 기능
- 댓글 시스템
- 파일 업로드
- 사용자 인증
- 실시간 알림