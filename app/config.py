# app/config.py

# Tier 1 예시: 정적 사이트
STATIC_URL = "https://quotes.toscrape.com/"

# Tier 2 & 3 예시: 동적 사이트
DYNAMIC_URL = "https://www.youtube.com/@programmingwithmosh/videos"

# Tier 2 & 3 예시: 로그인 필요 사이트
# 실제 로그인 테스트 시, 해당 사이트의 로그인 페이지 URL로 변경해야 합니다.
LOGIN_URL = "https://example-login-site.com/login"

# 로그인 정보 (실제 값으로 대체)
# 보안을 위해 실제 프로젝트에서는 환경 변수나 다른 안전한 방법을 사용하는 것을 권장합니다.
LOGIN_CREDENTIALS = {
    'username': 'your_username',
    'password': 'your_password'
}