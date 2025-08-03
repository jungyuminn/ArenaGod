def get_korean_initials(text):
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    result = ""
    for char in text:
        if '가' <= char <= '힣':
            char_code = ord(char) - ord('가')
            chosung_index = char_code // 588
            result += CHOSUNG_LIST[chosung_index]
        else:
            result += char
    return result

def match_text(search_text, target_text):
    """
    검색어와 대상 텍스트를 비교하여 일치 여부를 반환합니다.
    일반 텍스트 검색과 초성 검색을 모두 지원합니다.
    
    Args:
        search_text (str): 검색어
        target_text (str): 검색 대상 텍스트
        
    Returns:
        bool: 검색어가 대상 텍스트와 일치하는지 여부
    """
    if not search_text:
        return True
        
    search_text = search_text.lower().replace(" ", "")
    target_text = target_text.lower().replace(" ", "")
    
    is_initial_search = all(char in ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'] for char in search_text)
    
    if is_initial_search:
        target_initials = get_korean_initials(target_text)
        return search_text in target_initials.lower()
    else:
        return search_text in target_text 