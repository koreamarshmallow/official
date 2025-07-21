#!/usr/bin/env python3
import psycopg2
import ssl
import socket

def test_supabase_connection():
    print("🔍 Supabase 연결 테스트")
    print("=" * 50)
    
    # 연결 정보
    host = "db.lvawgzthxcougqtqfhzb.supabase.co"
    port = 5432
    database = "postgres"
    user = "postgres"
    password = "Goldstar1019!!"
    
    # 1. DNS 해결 테스트
    print("1. DNS 해결 테스트...")
    try:
        ip = socket.gethostbyname(host)
        print(f"   ✅ DNS 해결 성공: {host} -> {ip}")
    except Exception as e:
        print(f"   ❌ DNS 해결 실패: {e}")
        return False
    
    # 2. 포트 연결 테스트
    print("2. 포트 연결 테스트...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"   ✅ 포트 {port} 연결 성공")
        else:
            print(f"   ❌ 포트 {port} 연결 실패")
            return False
    except Exception as e:
        print(f"   ❌ 포트 연결 테스트 실패: {e}")
        return False
    
    # 3. SSL 연결 테스트
    print("3. SSL 연결 테스트...")
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                print(f"   ✅ SSL 연결 성공: {ssock.version()}")
    except Exception as e:
        print(f"   ❌ SSL 연결 실패: {e}")
        return False
    
    # 4. PostgreSQL 연결 테스트 (SSL 없이)
    print("4. PostgreSQL 연결 테스트 (SSL 없이)...")
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            sslmode='disable',
            connect_timeout=10
        )
        conn.close()
        print("   ✅ PostgreSQL 연결 성공 (SSL 없이)")
    except Exception as e:
        print(f"   ❌ PostgreSQL 연결 실패 (SSL 없이): {e}")
    
    # 5. PostgreSQL 연결 테스트 (SSL 필수)
    print("5. PostgreSQL 연결 테스트 (SSL 필수)...")
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            sslmode='require',
            connect_timeout=10
        )
        
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        print(f"   ✅ PostgreSQL 연결 성공 (SSL): {version[:50]}...")
        
        # 테이블 확인
        cur.execute("SELECT COUNT(*) FROM board_posts;")
        count = cur.fetchone()[0]
        print(f"   ✅ board_posts 테이블: {count}개 레코드")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ❌ PostgreSQL 연결 실패 (SSL): {e}")
        return False

def test_connection_strings():
    print("\n🔗 다양한 연결 문자열 테스트")
    print("=" * 50)
    
    connection_strings = [
        "postgresql://postgres:Goldstar1019!!@db.lvawgzthxcougqtqfhzb.supabase.co:5432/postgres",
        "postgresql://postgres:Goldstar1019!!@db.lvawgzthxcougqtqfhzb.supabase.co:5432/postgres?sslmode=require",
        "postgresql://postgres:Goldstar1019!!@db.lvawgzthxcougqtqfhzb.supabase.co:5432/postgres?sslmode=prefer",
        "postgresql://postgres:Goldstar1019!!@db.lvawgzthxcougqtqfhzb.supabase.co:5432/postgres?sslmode=allow"
    ]
    
    for i, conn_str in enumerate(connection_strings, 1):
        print(f"\n{i}. 연결 문자열 테스트:")
        print(f"   {conn_str}")
        
        try:
            conn = psycopg2.connect(conn_str, connect_timeout=10)
            cur = conn.cursor()
            cur.execute("SELECT 1;")
            result = cur.fetchone()[0]
            cur.close()
            conn.close()
            print(f"   ✅ 연결 성공")
        except Exception as e:
            print(f"   ❌ 연결 실패: {e}")

if __name__ == "__main__":
    success = test_supabase_connection()
    test_connection_strings()
    
    if success:
        print(f"\n🎉 모든 테스트 통과! Supabase 연결에 문제없음")
        print(f"MCP 연결 실패는 다른 원인일 가능성이 높습니다.")
    else:
        print(f"\n❌ 연결 테스트 실패. Supabase 설정을 확인해주세요.")