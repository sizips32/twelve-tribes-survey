import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def display_sidebar_traits():
    """사이드바에 각 지파의 이름, 특성, 성경구절, 대표인물을 표시합니다."""
    traits = {
    "유다": {
        "특성": "리더십과 용기",
        "약점": "타락과 탐욕 (창 38장 - 다말과의 부적절한 관계)",
        "성경구절": "창 49:9",
        "대표인물": "다윗, 예수 그리스도"
    },
    "르우벤": {
        "특성": "열정과 회복",
        "약점": "충동적 행동과 불안정성 (창 49:4 - 빌하와의 관계로 인해 맏아들의 권리를 상실함)",
        "성경구절": "창 49:3",
        "대표인물": "르우벤"
    },
    "스불론": {
        "특성": "사교성과 나눔",
        "약점": "세속적 유혹에 취약 (이방 문화에 쉽게 동화될 가능성)",
        "성경구절": "창 49:13",
        "대표인물": "사사 엘론"
    },
    "잇사갈": {
        "특성": "성실함과 감사",
        "약점": "지나친 타협과 안일함 (창 49:15 - 편안함을 위해 종이 되는 선택)",
        "성경구절": "창 49:14",
        "대표인물": "바락"
    },
    "갓": {
        "특성": "믿음과 영적 전쟁",
        "약점": "끊임없는 갈등 (전쟁의 삶으로 인해 평화가 부족함)",
        "성경구절": "창 49:19",
        "대표인물": "엘리야"
    },
    "아셀": {
        "특성": "섬김과 기쁨",
        "약점": "나태함과 안락함 추구 (창 49:20 - 물질적 풍요에 지나치게 의존할 가능성)",
        "성경구절": "창 49:20",
        "대표인물": "안나 여선지자"
    },
    "납달리": {
        "특성": "소통과 온화함",
        "약점": "우유부단함 (결정 상황에서 흔들릴 가능성)",
        "성경구절": "창 49:21",
        "대표인물": "바락"
    },
    "레위": {
        "특성": "신앙과 순종",
        "약점": "잔혹함과 과도한 열정 (창 49:5-7 - 세겜 사건에서의 폭력적인 복수)",
        "성경구절": "창 49:7",
        "대표인물": "모세, 아론"
    },
    "요셉": {
        "특성": "긍정적 영향과 나눔",
        "약점": "과도한 이상주의 (현실적 문제를 간과할 가능성)",
        "성경구절": "창 49:22",
        "대표인물": "여호수아, 드보라"
    },
    "베냐민": {
        "특성": "끈기와 열정",
        "약점": "파괴적 열정 (창 49:27 - 전투와 경쟁심이 지나칠 가능성)",
        "성경구절": "창 49:27",
        "대표인물": "사도 바울"
    },
    "시므온": {
        "특성": "열정적 복음 전파",
        "약점": "폭력적 성향 (창 49:5 - 세겜 사건에서의 과도한 복수)",
        "성경구절": "창 49:7",
        "대표인물": "시므온"
    },
    "므낫세": {
        "특성": "장기 계획과 충성",
        "약점": "강한 독립심으로 인한 분열 가능성 (공동체 조화를 깨뜨릴 위험)",
        "성경구절": "창 48:19",
        "대표인물": "기드온, 야일"
    },
}

    st.sidebar.title("지파별 특성")
    for tribe, data in traits.items():
        st.sidebar.write(f"### {tribe}")
        st.sidebar.write(f"- 특성: {data['특성']}")
        st.sidebar.write(f"- 성경구절: {data['성경구절']}")
        st.sidebar.write(f"- 대표인물: {data['대표인물']}")


def plot_survey_results(scores):
    """설문조사 결과를 막대그래프로 시각화합니다."""
    fig, ax = plt.subplots(figsize=(10, 6))
    tribes = list(scores.keys())
    values = list(scores.values())

    ax.bar(tribes, values, color="skyblue")
    ax.set_title("설문조사 결과", fontsize=16)
    ax.set_xlabel("지파", fontsize=12)
    ax.set_ylabel("점수 합계", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)


def display_swot_analysis_graph(top_tribes, bottom_tribes):
    """SWOT 분석을 사분면 그래프로 시각화하며 지정된 문구를 다음 행에 배치합니다."""
    strengths_map = {
        "유다": "리더십과 용기", "갓": "믿음과 영적 전쟁", "베냐민": "끈기와 열정",
        "르우벤": "열정과 회복", "시므온": "열정적 복음 전파", "납달리": "소통과 온화함",
        "스불론": "사교성과 나눔", "아셀": "섬김과 기쁨", "요셉": "긍정적 영향과 나눔",
        "잇사갈": "성실함과 감사", "레위": "신앙과 순종", "므낫세": "장기 계획과 충성"
    }
    
    swot_data = {
        "강점 (Strengths)": f"{top_tribes[0][0]}: {strengths_map[top_tribes[0][0]]}\n이(가) 빛납니다.",
        "기회 (Opportunities)": f"{top_tribes[1][0]}: {strengths_map[top_tribes[1][0]]}\n이(가) 돋보입니다.",
        "약점 (Weaknesses)": f"{bottom_tribes[0][0]}: {strengths_map[bottom_tribes[0][0]]}\n을(를) 더욱 발전시키면 좋겠습니다.",
        "위협 (Threats)": f"{bottom_tribes[1][0]}: {strengths_map[bottom_tribes[1][0]]}\n이(가) 많이 부족합니다.",
    }

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.add_patch(Rectangle((0, 0.5), 0.5, 0.5, edgecolor='black', facecolor='lightgreen', lw=2))
    ax.add_patch(Rectangle((0.5, 0.5), 0.5, 0.5, edgecolor='black', facecolor='lightcoral', lw=2))
    ax.add_patch(Rectangle((0, 0), 0.5, 0.5, edgecolor='black', facecolor='lightskyblue', lw=2))
    ax.add_patch(Rectangle((0.5, 0), 0.5, 0.5, edgecolor='black', facecolor='lightyellow', lw=2))

    ax.text(0.25, 0.75, f"강점\n{swot_data['강점 (Strengths)']}", ha='center', va='center', fontsize=10)
    ax.text(0.75, 0.75, f"약점\n{swot_data['약점 (Weaknesses)']}", ha='center', va='center', fontsize=10)
    ax.text(0.25, 0.25, f"기회\n{swot_data['기회 (Opportunities)']}", ha='center', va='center', fontsize=10)
    ax.text(0.75, 0.25, f"위협\n{swot_data['위협 (Threats)']}", ha='center', va='center', fontsize=10)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    st.pyplot(fig)


def calculate_results(scores):
    """점수를 계산하고 결과를 출력합니다."""
    averages = {tribe: total / 2 for tribe, total in scores.items()}
    sorted_tribes = sorted(averages.items(), key=lambda item: item[1], reverse=True)
    top_tribes = sorted_tribes[:2]
    bottom_tribes = sorted_tribes[-2:]

    st.subheader("설문 결과")
    st.write("최고점 및 최저점 지파 결과를 보여줍니다:")
    for tribe, average in top_tribes:
        st.write(f"**최고점 지파 - {tribe}:** 평균 {average:.2f}점")
    for tribe, average in bottom_tribes:
        st.write(f"**최저점 지파 - {tribe}:** 평균 {average:.2f}점")

    # 사이드바에 전체 지파 정보 표시
    display_sidebar_traits()

    # 설문조사 결과 그래프 출력
    plot_survey_results(scores)

    # SWOT 분석 그래프 출력
    display_swot_analysis_graph(top_tribes, bottom_tribes)


def conduct_survey():
    """설문조사를 통해 사용자가 각 지파에 대해 점수를 입력합니다."""
    st.title("열두 지파 성품 설문조사")
    st.write("각 항목에 대해 1에서 5점 사이로 점수를 입력해주세요.")
    
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

    for tribe, tribe_questions in questions.items():
        st.subheader(tribe)
        for question in tribe_questions:
            scores[tribe] += st.slider(f"{question}", 1, 5, 3)

    if st.button("결과 출력"):
        calculate_results(scores)


if __name__ == "__main__":
    conduct_survey()
