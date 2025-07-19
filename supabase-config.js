// Supabase 설정 파일
// 실제 프로젝트에서는 환경 변수를 사용하세요

const supabaseConfig = {
    url: 'YOUR_SUPABASE_PROJECT_URL', // 예: https://your-project.supabase.co
    anonKey: 'YOUR_SUPABASE_ANON_KEY' // Supabase 프로젝트의 anon public key
};

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