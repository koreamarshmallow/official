// Supabase 설정 파일
// GitHub에 공개되지 않는 안전한 설정 관리

// Node.js 환경에서만 사용 (브라우저에서는 사용하지 않음)
// const supabaseConfig = {
//     url: process.env.SUPABASE_URL || 'YOUR_SUPABASE_PROJECT_URL',
//     anonKey: process.env.SUPABASE_ANON_KEY || 'YOUR_SUPABASE_ANON_KEY'
// };

// 브라우저 환경에서 사용할 설정 (런타임에 주입)
window.SUPABASE_CONFIG = window.SUPABASE_CONFIG || {
    url: 'https://lvawgzthxcougqtqfhzb.supabase.co',
    anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx2YXdnenRoeGNvdWdxdHFmaHpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI4OTE4NzgsImV4cCI6MjA2ODQ2Nzg3OH0.wm2IbN88xYpAKDfShRE6_I8ke_xEicQvxSqhte4AYyw'
};

// Supabase 테이블 생성 SQL (참고용)
/*
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

-- 관리자 테이블 생성
CREATE TABLE board_admins (
    id BIGSERIAL PRIMARY KEY,
    admin_key VARCHAR(255) UNIQUE NOT NULL,
    nickname VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스 생성
CREATE INDEX idx_board_posts_created_at ON board_posts(created_at DESC);
CREATE INDEX idx_board_posts_likes ON board_posts(likes DESC);
CREATE INDEX idx_board_posts_is_notice ON board_posts(is_notice);

-- RLS (Row Level Security) 정책 설정
ALTER TABLE board_posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE board_admins ENABLE ROW LEVEL SECURITY;

-- 모든 사용자가 게시글을 읽을 수 있도록 허용
CREATE POLICY "Anyone can read posts" ON board_posts FOR SELECT USING (true);

-- 모든 사용자가 게시글을 작성할 수 있도록 허용
CREATE POLICY "Anyone can insert posts" ON board_posts FOR INSERT WITH CHECK (true);

-- 게시글 업데이트 (추천, 조회수)
CREATE POLICY "Anyone can update post stats" ON board_posts FOR UPDATE USING (true);

-- 관리자만 게시글 삭제 가능 (실제로는 클라이언트에서 관리자 확인 필요)
CREATE POLICY "Anyone can delete posts" ON board_posts FOR DELETE USING (true);
*/

// Supabase 클라이언트 초기화 함수 (브라우저 환경)
function initSupabase() {
    const config = window.SUPABASE_CONFIG || supabaseConfig;
    
    if (typeof supabase !== 'undefined' && config.url !== 'PLACEHOLDER_URL') {
        return supabase.createClient(config.url, config.anonKey);
    } else {
        console.warn('Supabase not configured or library not loaded, using localStorage fallback');
        return null;
    }
}

// 문의 양식 데이터를 Supabase에 저장하는 함수
async function submitContactForm(formData) {
    const client = initSupabase();
    if (!client) return false;

    try {
        const { data, error } = await client
            .from('contact_inquiries')
            .insert([
                {
                    name: formData.name,
                    company: formData.company,
                    email: formData.email,
                    inquiry_type: formData.inquiryType,
                    message: formData.message,
                    created_at: new Date().toISOString()
                }
            ]);

        if (error) {
            console.error('Error submitting form:', error);
            return false;
        }

        return true;
    } catch (error) {
        console.error('Error:', error);
        return false;
    }
}

// 뉴스 데이터를 Supabase에서 가져오는 함수
async function fetchNews() {
    const client = initSupabase();
    if (!client) return [];

    try {
        const { data, error } = await client
            .from('news')
            .select('*')
            .order('created_at', { ascending: false })
            .limit(6);

        if (error) {
            console.error('Error fetching news:', error);
            return [];
        }

        return data || [];
    } catch (error) {
        console.error('Error:', error);
        return [];
    }
}

// 회원가입 함수
async function registerMember(memberData) {
    const client = initSupabase();
    if (!client) return false;

    try {
        const { data, error } = await client
            .from('members')
            .insert([
                {
                    name: memberData.name,
                    company: memberData.company,
                    email: memberData.email,
                    phone: memberData.phone,
                    business_type: memberData.businessType,
                    created_at: new Date().toISOString()
                }
            ]);

        if (error) {
            console.error('Error registering member:', error);
            return false;
        }

        return true;
    } catch (error) {
        console.error('Error:', error);
        return false;
    }
}
// ========== 게시판 관련 함수들 ==========

// 게시글 목록 가져오기
async function fetchBoardPosts(sortBy = 'latest', limit = 20, offset = 0) {
    const client = initSupabase();
    if (!client) return { posts: [], total: 0 };

    try {
        let query = client.from('board_posts').select('*', { count: 'exact' });
        
        // 정렬 적용
        switch (sortBy) {
            case 'latest':
                query = query.order('created_at', { ascending: false });
                break;
            case 'likes':
                query = query.order('likes', { ascending: false });
                break;
            case 'oldest':
                query = query.order('created_at', { ascending: true });
                break;
            default:
                query = query.order('created_at', { ascending: false });
        }
        
        const { data, error, count } = await query.range(offset, offset + limit - 1);

        if (error) {
            console.error('Error fetching posts:', error);
            return { posts: [], total: 0 };
        }

        return { posts: data || [], total: count || 0 };
    } catch (error) {
        console.error('Error:', error);
        return { posts: [], total: 0 };
    }
}

// 게시글 작성
async function createBoardPost(postData) {
    const client = initSupabase();
    if (!client) return false;

    try {
        const { data, error } = await client
            .from('board_posts')
            .insert([
                {
                    title: postData.title,
                    content: postData.content,
                    nickname: postData.nickname,
                    email: postData.email || null,
                    ip_address: postData.ip_address || 'unknown',
                    is_notice: postData.is_notice || false
                }
            ])
            .select();

        if (error) {
            console.error('Error creating post:', error);
            return false;
        }

        return data && data.length > 0 ? data[0] : false;
    } catch (error) {
        console.error('Error:', error);
        return false;
    }
}

// 게시글 상세 조회 (조회수 증가)
async function getBoardPost(postId) {
    const client = initSupabase();
    if (!client) return null;

    try {
        // 조회수 증가
        await client
            .from('board_posts')
            .update({ views: client.raw('views + 1') })
            .eq('id', postId);

        // 게시글 조회
        const { data, error } = await client
            .from('board_posts')
            .select('*')
            .eq('id', postId)
            .single();

        if (error) {
            console.error('Error fetching post:', error);
            return null;
        }

        return data;
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

// 게시글 추천
async function likeBoardPost(postId) {
    const client = initSupabase();
    if (!client) return false;

    try {
        const { data, error } = await client
            .from('board_posts')
            .update({ likes: client.raw('likes + 1') })
            .eq('id', postId)
            .select();

        if (error) {
            console.error('Error liking post:', error);
            return false;
        }

        return data && data.length > 0 ? data[0] : false;
    } catch (error) {
        console.error('Error:', error);
        return false;
    }
}

// 게시글 삭제 (관리자 기능)
async function deleteBoardPost(postId, adminKey) {
    const client = initSupabase();
    if (!client) return false;

    try {
        // 관리자 확인 (실제 구현에서는 더 안전한 방법 사용)
        if (!adminKey || adminKey !== 'admin123') {
            console.error('Invalid admin key');
            return false;
        }

        const { error } = await client
            .from('board_posts')
            .delete()
            .eq('id', postId);

        if (error) {
            console.error('Error deleting post:', error);
            return false;
        }

        return true;
    } catch (error) {
        console.error('Error:', error);
        return false;
    }
}