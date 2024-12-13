import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import rc
import os
import platform
import matplotlib.font_manager as fm

def conduct_survey():
    """설문조사를 실시하고 결과를 반환합니다."""

    questions = {
        "유다": [
            "나는 위기 상황이 닥쳤을 때, 주저하지 않고 앞장서서 해결하려는 경향이 있다.",
            "나는 어려움에 처한 사람을 보면, 기꺼이 나를 희생하여 돕고자 한다.",
        ],
        "르우벤": [
            "나는 새로운 일을 시작할 때, 쉽게 의욕이 넘치고 열정적으로 임하는 편이다.",
            "나는 과거의 잘못을 돌아보고, 그것으로부터 교훈을 얻어 성장하려 노력한다.",
        ],
        "스불론": [
            "나는 낯선 사람들과도 스스럼없이 어울리고, 그들과 함께 하는 것을 즐긴다.",
            "나는 가지고 있는 자원을 효율적으로 관리하고, 필요한 사람들과 나누는 것에 보람을 느낀다.",
        ],
        "잇사갈": [
            "나는 한 번 맡은 일은 어려움이 있더라도 끝까지 완수하는 편이다.",
            "나는 현재 내가 가진 것들에 감사하고, 주어진 상황에 만족하며 살아간다.",
        ],
        "갓": [
            "나는 힘든 상황 속에서도 나의 믿음을 굳건히 지켜나가려 애쓴다.",
            "나는 영적인 성장을 위해 꾸준히 기도하며, 어려움을 극복하려 한다.",
        ],
        "아셀": [
            "나는 다른 사람을 돕는 일에서 큰 기쁨과 보람을 느낀다.",
            "나는 나의 영적인 은사를 다른 사람들과 나누며, 그들을 격려하는 것을 좋아한다.",
        ],
        "납달리": [
            "나는 나의 생각과 의견을 상대방에게 명확하고 효과적으로 전달하는 편이다.",
            "나는 상대방과 소통할 때, 부드럽고 온화한 태도를 유지하려 노력한다.",
        ],
        "레위": [
            "나는 하나님의 말씀을 듣고, 그 가르침에 따라 살아가려고 노력한다.",
            "나는 과거에 잘못한 일이 있다면, 그것을 인정하고 바로잡으려 애쓴다.",
        ],
        "요셉": [
            "나는 주변 사람들에게 긍정적인 영향을 미치며, 그들의 삶에 좋은 본보기가 되고자 한다.",
            "나는 영적,물질적으로 도움이 필요한 사람들에게 베풀고 나누는 삶을 실천한다.",
        ],
        "베냐민": [
            "나는 사람들에게 복음을 전하는 일에 적극적으로 참여하고, 그들에게 하나님의 사랑을 알리고 싶다.",
            "나는 한 번 시작한 일은 어떤 어려움이 있어도 포기하지 않고 끝까지 해내는 끈기가 있다.",
        ],
        "시므온": [
            "나는 새로운 도전을 즐기며 받아들인다.",
            "나는 믿음을 나누는데 열정적이다.",
        ],
        "므낫세": [
            "나는 장기적인 계획을 세우고 실천한다.",
            "나는 맡은 자리에서 신실하게 섬긴다.",
        ],
    }

    scores = {tribe: 0 for tribe in questions}

    st.title("열두지파 성격 유형 설문조사")
    st.write("다음 질문에 대해 1-5점으로 답해주세요 (1: 전혀 그렇지 않다, 5: 매우 그렇다)")

    for tribe, tribe_questions in questions.items():
        st.subheader(tribe)
        for i, question in enumerate(tribe_questions):
            score = st.slider(f"{question}", 1, 5, 3, key=f"{tribe}_{i}")
            scores[tribe] += score

    return scores

def calculate_results(scores):
    """점수를 계산하고 결과를 출력합니다."""

    averages = {tribe: total / 2 for tribe, total in scores.items()}
    sorted_tribes = sorted(averages.items(), key=lambda item: item[1], reverse=True)

    st.subheader("설문 결과")
    st.write("최고점 및 최저점 지파 결���를 보여줍니다:")

    # 최고점 상위 2개
    top_tribes = sorted_tribes[:2]
    for tribe, average in top_tribes:
        st.write(f"**최고점 지파 - {tribe}:** 평균 {average:.2f}점")

    # 최저점 하위 2개
    bottom_tribes = sorted_tribes[-2:]
    for tribe, average in bottom_tribes:
        st.write(f"**최저점 지파 - {tribe}:** 평균 {average:.2f}점")

    st.write("각 지파별 특성과 권면")
    advice = {
        "유다": {"구절": "창 49:9", "권면": "유다는 사자와 같은 용맹과 헌신적 리더십을 발휘하여 어려움 속에서도 앞장서 나아갈 수 있습니다.", "대표인물": "다윗 (삼하 2:1), 예수 그리스도 (계 5:5)"},
        
        "르우벤": {"구절": "창 49:3", "권면": "르우벤은 열정적으로 새로운 일에 도전하며 회복을 통해 선한 영향력을 끼칠 수 있습니다.", "대표인물": "다단과 아비람 (민 16:1-35)"},
        
        "스불론": {"구절": "창 49:13", "권면": "스불론은 사교적이며 자원을 효율적으로 활용하여 다른 사람을 돕는 데 기여할 수 있습니다.", "대표인물": "입다의 사사 엘론 (삿 12:11)"},
        
        "잇사갈": {"구절": "창 49:14", "권면": "잇사갈은 성실함과 안정감으로 하나님께 감사하며 맡은 일을 끝까지 완수합니다.", "대표인물": "바락 (삿 4:6-10)"},
        
        "갓": {"구절": "창 49:19", "권면": "갓은 어려움 속에서도 하나님을 의지하며 영적 전쟁에서 승리합니다.", "대표인물": "엘리야 선지자 (왕상 17:1)"},
        
        "아셀": {"구절": "창 49:20", "권면": "아셀은 섬김과 영적 풍성함으로 다른 사람에게 기쁨과 평안을 제공합니다.", "대표인물": "안나 여선지자 (눅 2:36-38)"},
        
        "납달리": {"구절": "창 49:21", "권면": "납달리는 온화하고 명확한 소통으로 복음을 효과적으로 전달할 수 있습니다.", "대표인물": "바락 (삿 4:6-10)"},
        
        "레위": {"구절": "창 49:7", "권면": "레위는 말씀에 대한 순종과 회개를 통해 신앙의 본을 보일 수 있습니다.", "대표인물": "모세와 아론 (출 6:20)"},
        
        "요셉": {"구절": "창 49:22", "권면": "요셉은 긍정적 영향력과 나눔을 통해 다른 이들에게 물질적 도움을 줍니다.", "대표인물": "여호수아 (수 1:1-9), 드보라 (삿 4:4)"},
        
        "베냐민": {"구절": "창 49:27", "권면": "베냐민은 끈기와 열정을 가지고 복음을 전하며 끝까지 사명을 완수합니다.", "대표인물": "사도 바울 (행 9:1-31)"},
        
        "시므온": {"구절": "창 49:7", "권면": "시므온은 열정적인 성격으로 적극적으로 복음을 전하고 하나님의 말씀을 따르는 삶을 살아갑니다.", "대표인물": "시므온 (눅 2:25-35)"},
        
        "므낫세": {"구절": "창 48:19", "권면": "므낫세는 충성과 안정감을 바탕으로 선교 사역에 헌신하며 하나님께 영광을 돌립니다.", "대표인물": "기드온 (삿 6:11-16), 야일 (삿 10:3-5)"}
    }

    for tribe, data in advice.items():
        st.write(f"**{tribe}:** (성경구절: {data['구절']}, 대표인물: {data['대표인물']}) {data['권면']}")

    # 그래픽 출력
    st.subheader("그래프로 보는 설문 결과")
    tribes = list(averages.keys())
    scores = list(averages.values())

    # 한글 폰트 설정
    if platform.system() == 'Darwin':  # macOS
        plt.rcParams['font.family'] = 'AppleGothic'
    elif platform.system() == 'Windows':
        plt.rcParams['font.family'] = 'Malgun Gothic'
    else:  # Linux 또는 기타 환경
        # NanumGothic 폰트 파일 직접 지정
        font_dirs = ['/usr/share/fonts/truetype/nanum/', '.']  # 현재 디렉토리도 검색
        font_files = fm.findSystemFonts(fontpaths=font_dirs)
        
        for font_file in font_files:
            if 'NanumGothic' in font_file:
                font_path = font_file
                break
        else:
            # 폰트 파일이 없는 경우 다운로드
            import urllib.request
            import os
            
            font_url = "https://github.com/googlefonts/nanum-gothic/blob/main/fonts/NanumGothic-Regular.ttf?raw=true"
            font_path = "NanumGothic.ttf"
            
            if not os.path.exists(font_path):
                urllib.request.urlretrieve(font_url, font_path)
        
        font_prop = fm.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = 'NanumGothic'
        fm.fontManager.addfont(font_path)

    plt.rcParams['axes.unicode_minus'] = False

    fig, ax = plt.subplots()
    ax.bar(tribes, scores, color='skyblue')
    ax.set_xlabel('지파')
    ax.set_ylabel('평균 점수')
    ax.set_title('지파별 평균 점수')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    # 그래프 출력 이후에 추가
    st.subheader("💪 강점 및 🔍 보완점")
    
    # 상위 2개 지파 기반 강점 분석
    st.write("**💪 당신의 강점:**")
    strengths = []
    for tribe, score in top_tribes:
        if tribe in ["유다", "갓", "베냐민"]:
            strengths.append("리더십과 용기")
        elif tribe in ["르우벤", "시므온", "납달리"]:
            strengths.append("열정과 소통능력")
        elif tribe in ["스불론", "아셀", "요셉"]:
            strengths.append("나눔과 섬김")
        elif tribe in ["잇사갈", "레위", "므낫세"]:
            strengths.append("성실함과 신실함")
    
    st.write(", ".join(set(strengths[:2])) + "이(가) 돋보입니다.")
    
    # 하위 2개 지파 기반 보완점 제시
    st.write("**🔍 보완이 필요한 영역:**")
    improvements = []
    for tribe, score in bottom_tribes:
        if tribe in ["유다", "갓", "베냐민"]:
            improvements.append("결단력과 책임감")
        elif tribe in ["르우벤", "시므온", "납달리"]:
            improvements.append("의사소통과 관계형성")
        elif tribe in ["스불론", "아셀", "요셉"]:
            improvements.append("나눔과 섬김의 자세")
        elif tribe in ["잇사갈", "레위", "므낫세"]:
            improvements.append("인내심과 충성")
    
    st.write(", ".join(set(improvements[:2])) + "을(를) 더욱 발전시키면 좋겠습니다.")

if __name__ == "__main__":
    scores = conduct_survey()
    if st.button("결과 확인"):
        calculate_results(scores)
