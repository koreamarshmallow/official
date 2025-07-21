#!/usr/bin/env python3
import psycopg2
import sys

def list_database_tables():
    try:
        # Supabase PostgreSQL 연결 (SSL 포함)
        conn_string = "postgresql://postgres:Goldstar1019!!@db.lvawgzthxcougqtqfhzb.supabase.co:5432/postgres?sslmode=require"
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        
        print("🗄️  Supabase 데이터베이스 테이블 목록")
        print("=" * 60)
        
        # 1. 모든 스키마 조회
        cur.execute("""
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name NOT IN ('information_schema', 'pg_catalog', 'pg_toast', 'pg_temp_1', 'pg_toast_temp_1')
            ORDER BY schema_name;
        """)
        
        schemas = cur.fetchall()
        print("\n📁 사용 가능한 스키마:")
        for schema in schemas:
            print(f"   - {schema[0]}")
        
        # 2. public 스키마의 테이블 목록
        cur.execute("""
            SELECT 
                table_name, 
                table_type,
                CASE 
                    WHEN table_type = 'BASE TABLE' THEN '📋'
                    WHEN table_type = 'VIEW' THEN '👁️'
                    ELSE '❓'
                END as icon
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        
        tables = cur.fetchall()
        
        print(f"\n📋 public 스키마의 테이블 목록 ({len(tables)}개):")
        print("-" * 50)
        
        if tables:
            for table_name, table_type, icon in tables:
                print(f"{icon} {table_name} ({table_type})")
        else:
            print("❌ public 스키마에 테이블이 없습니다.")
        
        # 3. board_posts 테이블 상세 정보
        if any(table[0] == 'board_posts' for table in tables):
            print(f"\n📊 board_posts 테이블 상세 정보:")
            print("-" * 40)
            
            # 컬럼 정보
            cur.execute("""
                SELECT 
                    column_name,
                    data_type,
                    is_nullable,
                    column_default
                FROM information_schema.columns 
                WHERE table_schema = 'public' 
                AND table_name = 'board_posts'
                ORDER BY ordinal_position;
            """)
            
            columns = cur.fetchall()
            print("컬럼 구조:")
            for col_name, data_type, nullable, default in columns:
                nullable_str = "NULL" if nullable == "YES" else "NOT NULL"
                default_str = f" DEFAULT {default}" if default else ""
                print(f"  • {col_name}: {data_type} {nullable_str}{default_str}")
            
            # 레코드 수
            cur.execute("SELECT COUNT(*) FROM board_posts;")
            count = cur.fetchone()[0]
            print(f"\n총 레코드 수: {count}개")
            
            # 최근 게시글
            cur.execute("""
                SELECT title, nickname, created_at 
                FROM board_posts 
                ORDER BY created_at DESC 
                LIMIT 3;
            """)
            recent_posts = cur.fetchall()
            print("\n최근 게시글 3개:")
            for title, nickname, created_at in recent_posts:
                print(f"  • {title} - {nickname} ({created_at})")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ 데이터베이스 연결 실패: {e}")
        return False
    
    return True

if __name__ == "__main__":
    list_database_tables()