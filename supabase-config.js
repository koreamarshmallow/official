// Supabase 설정 파일
// 실제 프로젝트에서는 환경 변수를 사용하세요

const supabaseConfig = {
    url: 'YOUR_SUPABASE_PROJECT_URL', // 예: https://your-project.supabase.co
    anonKey: 'YOUR_SUPABASE_ANON_KEY' // Supabase 프로젝트의 anon public key
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

// Supabase 클라이언트 초기화 함수
function initSupabase() {
    if (typeof supabase !== 'undefined') {
        return supabase.createClient(supabaseConfig.url, supabaseConfig.anonKey);
    } else {
        console.error('Supabase library not loaded');
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