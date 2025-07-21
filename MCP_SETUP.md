# Supabase MCP 설정 가이드

이 가이드는 Kiro IDE에서 Supabase MCP(Model Context Protocol) 서버를 설정하는 방법을 설명합니다.

## 📋 MCP란?

MCP(Model Context Protocol)는 AI 어시스턴트가 외부 도구와 데이터베이스에 안전하게 연결할 수 있게 해주는 프로토콜입니다. Supabase MCP를 통해 데이터베이스를 직접 조회하고 관리할 수 있습니다.

## 🔧 설정 방법

### 1. 필수 요구사항

#### Python 및 uv 설치
```bash
# Windows (PowerShell)
winget install astral-sh.uv

# macOS
brew install uv

# Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Supabase Service Role Key 확인
1. [Supabase Dashboard](https://supabase.com/dashboard) 접속
2. 프로젝트 선택 > Settings > API
3. **service_role** 키 복사 (anon key가 아님!)

### 2. 환경 변수 설정

`.env` 파일을 생성하고 다음 정보를 추가:

```env
# 클라이언트용
SUPABASE_URL=https://lvawgzthxcougqtqfhzb.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# MCP 서버용 (중요: service_role 키 사용)
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...[service_role_key]
POSTGRES_CONNECTION_STRING=postgresql://postgres:[password]@db.lvawgzthxcougqtqfhzb.supabase.co:5432/postgres
```

### 3. MCP 설정 확인

현재 설정된 MCP 서버:

```json
{
  "mcpServers": {
    "supabase": {
      "command": "uvx",
      "args": ["mcp-server-supabase@latest"],
      "env": {
        "SUPABASE_URL": "https://lvawgzthxcougqtqfhzb.supabase.co",
        "SUPABASE_SERVICE_ROLE_KEY": "your-service-role-key-here"
      },
      "disabled": false,
      "autoApprove": [
        "list_tables",
        "describe_table", 
        "select_data",
        "get_table_schema",
        "insert_data",
        "update_data"
      ]
    }
  }
}
```

## 🚀 사용 방법

### 1. MCP 서버 연결 확인
Kiro IDE에서:
1. 명령 팔레트 열기 (Ctrl+Shift+P)
2. "MCP" 검색
3. "MCP Server" 뷰에서 연결 상태 확인

### 2. 기본 명령어

#### 테이블 목록 조회
```
테이블 목록을 보여줘
```

#### 테이블 구조 확인
```
board_posts 테이블 구조를 알려줘
```

#### 데이터 조회
```
board_posts 테이블에서 최근 10개 게시글을 조회해줘
```

#### 데이터 삽입
```
board_posts 테이블에 새 게시글을 추가해줘:
- title: "테스트 게시글"
- content: "MCP 테스트 내용"
- nickname: "관리자"
```

## 🔒 보안 고려사항

### Service Role Key 보안
- **절대 GitHub에 업로드하지 마세요**
- `.env` 파일은 `.gitignore`에 포함되어 있습니다
- Service Role Key는 모든 데이터베이스 권한을 가지므로 주의깊게 관리하세요

### 자동 승인 설정
현재 다음 작업들이 자동 승인됩니다:
- `list_tables`: 테이블 목록 조회
- `describe_table`: 테이블 구조 조회
- `select_data`: 데이터 조회
- `get_table_schema`: 스키마 정보
- `insert_data`: 데이터 삽입
- `update_data`: 데이터 수정

위험한 작업 (DELETE, DROP 등)은 수동 승인이 필요합니다.

## 🛠 문제 해결

### 1. uvx 명령어를 찾을 수 없음
```bash
# uv 재설치
curl -LsSf https://astral.sh/uv/install.sh | sh
# 또는
pip install uv
```

### 2. MCP 서버 연결 실패
- Service Role Key가 올바른지 확인
- Supabase URL이 정확한지 확인
- 네트워크 연결 상태 확인

### 3. 권한 오류
- Service Role Key 사용 확인 (anon key 아님)
- RLS 정책 확인
- 테이블 권한 설정 확인

## 📚 추가 리소스

- [Supabase MCP Server GitHub](https://github.com/supabase/mcp-server-supabase)
- [Model Context Protocol 공식 문서](https://modelcontextprotocol.io/)
- [Supabase API 문서](https://supabase.com/docs/reference/api)

## 🎯 활용 예시

### 게시판 관리
```
최근 일주일간 작성된 게시글 통계를 보여줘
공지사항으로 등록된 게시글 목록을 조회해줘
추천수가 10개 이상인 인기 게시글을 찾아줘
```

### 데이터 분석
```
월별 게시글 작성 현황을 분석해줘
가장 활발한 사용자 TOP 10을 알려줘
게시글 카테고리별 분포를 보여줘
```

이제 Kiro IDE에서 Supabase 데이터베이스를 직접 관리하고 분석할 수 있습니다! 🚀