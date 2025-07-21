#!/usr/bin/env python3
import os
import asyncio
import sys

# 환경 변수 설정
os.environ['POSTGRES_CONNECTION_STRING'] = "postgresql://postgres.lvawgzthxcougqtqfhzb:Goldstar1019!!@aws-0-ap-northeast-2.pooler.supabase.com:6543/postgres?sslmode=require"

async def test_mcp_server():
    print("🔗 MCP 서버 연결 테스트")
    print("=" * 50)
    
    try:
        # MCP 서버 모듈 임포트 테스트
        print("1. MCP 서버 모듈 임포트 테스트...")
        from mcp_server_postgres import create_server
        print("   ✅ 모듈 임포트 성공")
        
        # 환경 변수 확인
        print("2. 환경 변수 확인...")
        conn_str = os.environ.get('POSTGRES_CONNECTION_STRING')
        if conn_str:
            print(f"   ✅ 연결 문자열 설정됨: {conn_str[:50]}...")
        else:
            print("   ❌ 연결 문자열 없음")
            return False
        
        # MCP 서버 생성 테스트
        print("3. MCP 서버 생성 테스트...")
        server = create_server()
        print("   ✅ MCP 서버 생성 성공")
        
        # 서버 정보 확인
        print("4. 서버 정보 확인...")
        if hasattr(server, 'name'):
            print(f"   서버 이름: {server.name}")
        if hasattr(server, 'version'):
            print(f"   서버 버전: {server.version}")
        
        print("\n🎉 MCP 서버 테스트 성공!")
        return True
        
    except ImportError as e:
        print(f"   ❌ 모듈 임포트 실패: {e}")
        return False
    except Exception as e:
        print(f"   ❌ MCP 서버 테스트 실패: {e}")
        return False

async def test_postgres_connection():
    print("\n🗄️ PostgreSQL 직접 연결 테스트")
    print("=" * 50)
    
    try:
        import psycopg2
        
        conn_str = os.environ.get('POSTGRES_CONNECTION_STRING')
        print("1. PostgreSQL 연결 시도...")
        
        conn = psycopg2.connect(conn_str, connect_timeout=10)
        print("   ✅ PostgreSQL 연결 성공")
        
        cur = conn.cursor()
        
        # 테이블 목록 조회
        print("2. 테이블 목록 조회...")
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        
        tables = cur.fetchall()
        print(f"   ✅ 테이블 {len(tables)}개 발견:")
        for table in tables:
            print(f"     - {table[0]}")
        
        # board_posts 테이블 레코드 수 확인
        if any(table[0] == 'board_posts' for table in tables):
            print("3. board_posts 테이블 확인...")
            cur.execute("SELECT COUNT(*) FROM board_posts;")
            count = cur.fetchone()[0]
            print(f"   ✅ board_posts: {count}개 레코드")
        
        cur.close()
        conn.close()
        
        print("\n🎉 PostgreSQL 연결 테스트 성공!")
        return True
        
    except Exception as e:
        print(f"   ❌ PostgreSQL 연결 실패: {e}")
        return False

async def main():
    print("🧪 MCP 및 PostgreSQL 연결 종합 테스트")
    print("=" * 60)
    
    # MCP 서버 테스트
    mcp_success = await test_mcp_server()
    
    # PostgreSQL 직접 연결 테스트
    pg_success = await test_postgres_connection()
    
    # 결과 요약
    print("\n📊 테스트 결과 요약")
    print("=" * 30)
    print(f"MCP 서버: {'✅ 성공' if mcp_success else '❌ 실패'}")
    print(f"PostgreSQL: {'✅ 성공' if pg_success else '❌ 실패'}")
    
    if mcp_success and pg_success:
        print("\n🎉 모든 테스트 통과! MCP 연결 준비 완료")
        print("이제 Kiro IDE에서 MCP 서버를 재연결해보세요.")
    else:
        print("\n⚠️ 일부 테스트 실패. 설정을 다시 확인해주세요.")

if __name__ == "__main__":
    asyncio.run(main())