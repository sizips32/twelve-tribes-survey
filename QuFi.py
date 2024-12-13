import streamlit as st
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")  # 와이드 레이아웃 설정

# 사이드바에 입력 폼 추가
with st.sidebar:
    st.title("Input Parameters")
    ticker = st.text_input("Stock Ticker Symbol (e.g., AAPL, TSLA):", "AAPL")
    period = st.selectbox(
        "Time Period:",
        options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=3  # 기본값 "1y"
    )
    
    # 양자 시뮬레이션 파라미터
    st.subheader("Quantum Simulation Parameters")
    hbar = st.slider("Planck Constant (ℏ)", 0.1, 2.0, 1.0, 0.1)
    m = st.slider("Mass Parameter (m)", 0.1, 2.0, 1.0, 0.1)
    dt = st.slider("Time Step (dt)", 0.001, 0.1, 0.01, 0.001)
    M = st.slider("Number of Time Steps", 50, 200, 100, 10)
    
    calculate = st.button("Calculate Price Distribution")

# 메인 화면 설정
st.title("Quantum Finance: PDE-based Stock Price Distribution Prediction")

if calculate:
    # 데이터 다운로드 및 계산을 메인 화면에 표시
    with st.spinner('Downloading and processing data...'):
        data = yf.download(ticker, period=period)
        
        if len(data) == 0:
            st.error("Could not fetch data. Please check the ticker symbol and try again.")
        else:
            # 기존의 계산 코드는 그대로 유지
            prices = data['Close']
            current_price = float(prices.iloc[-1].item())
            
            # 전체 가격 범위 설정
            price_min = float(prices.min().item())
            price_max = float(prices.max().item())
            price_range = price_max - price_min
            
            # 가격 범위를 여유있게 설정 (20% 마진)
            margin = 0.2
            x_min = price_min - margin * price_range
            x_max = price_max + margin * price_range

            # 변동성 추정
            log_returns = np.log(prices / prices.shift(1)).dropna()
            sigma = float(log_returns.std().iloc[0])
            if np.isclose(sigma, 0) or np.isnan(sigma):
                sigma = 0.01
            mu = float(log_returns.mean().iloc[0])

            # 공간 격자 설정
            N = 200
            x = np.linspace(x_min, x_max, N)
            dx = x[1] - x[0]

            # 초기 파동함수: 실제 가격 분포를 반영한 가우시안 혼합
            psi = np.zeros(N)
            for price in prices.values:
                psi += np.exp(-(x - price)**2/(4*sigma**2))
            
            # 정규화
            psi = psi / np.sqrt(np.sum(np.abs(psi)**2)*dx)
            psi_t = psi.copy()

            # 퍼텐셜 계산: 실제 가격 분포를 반영
            price_hist, bins = np.histogram(prices, bins=50, density=True)
            bin_centers = (bins[:-1] + bins[1:]) / 2
            V = np.interp(x, bin_centers, -np.log(price_hist + 1e-10))
            V = V / np.max(np.abs(V))  # 퍼텐셜 정규화

            # 해밀토니안 관련 계수
            coeff = -(hbar**2)/(2*m*dx**2)
            # 대각/비대각항
            diag = 2*coeff + V
            off = -coeff
            i_factor = 1j*dt/(2*hbar)

            # Crank-Nicolson 행렬 요소 (A, B 행렬)
            # A psi(t+dt) = B psi(t)
            # 주어진 diag, off를 이용해 삼중대각 형태 생성
            # A 행렬
            aA = -i_factor * off * np.ones(N, dtype=complex)
            bA = 1 + i_factor * diag
            cA = -i_factor * off * np.ones(N, dtype=complex)
            aA[0] = 0; cA[-1] = 0  # 경계서 연결 끊기(psi=0처럼)
            
            # B 행렬
            aB = i_factor * off * np.ones(N, dtype=complex)
            bB = 1 - i_factor * diag
            cB = i_factor * off * np.ones(N, dtype=complex)
            aB[0] = 0; cB[-1] = 0

            def tridiag_solve(a, b, c, d):
                # 토마스 알고리즘
                n = len(d)
                c_ = np.zeros(n, dtype=complex)
                d_ = np.zeros(n, dtype=complex)
                x_ = np.zeros(n, dtype=complex)

                c_[0] = c[0]/b[0]
                d_[0] = d[0]/b[0]

                for i in range(1, n):
                    denom = b[i] - a[i]*c_[i-1]
                    if denom == 0:
                        denom = 1e-12
                    c_[i] = c[i]/denom if i < n-1 else 0
                    d_[i] = (d[i]-a[i]*d_[i-1])/denom

                x_[n-1] = d_[n-1]
                for i in range(n-2, -1, -1):
                    x_[i] = d_[i] - c_[i]*x_[i+1]
                return x_

            # 시간 진화
            for _ in range(M):
                # B*psi(t) 계산
                d = np.zeros(N, dtype=complex)
                # d[i] = aB[i]*psi_t[i-1] + bB[i]*psi_t[i] + cB[i]*psi_t[i+1]
                # 인덱스 주의
                for i in range(N):
                    val = bB[i]*psi_t[i]
                    if i > 0:
                        val += aB[i]*psi_t[i-1]
                    if i < N-1:
                        val += cB[i]*psi_t[i+1]
                    d[i] = val

                # A*psi(t+dt) = d
                psi_new = tridiag_solve(aA, bA, cA, d)
                # 정규화
                norm = np.sqrt(np.sum(np.abs(psi_new)**2)*dx)
                if norm != 0:
                    psi_t = psi_new / norm
                else:
                    psi_t = psi_new

            # 시간 진화 후 파동함수 확률밀도
            prob_density = np.abs(psi_t)**2

            # 미래 가격 평균 및 표준편차
            mean_future = np.sum(x * prob_density * dx)
            var_future = np.sum((x - mean_future)**2 * prob_density * dx)
            std_future = np.sqrt(var_future)

            pred_1sigma_min = mean_future - std_future
            pred_1sigma_max = mean_future + std_future
            pred_2sigma_min = mean_future - 2*std_future
            pred_2sigma_max = mean_future + 2*std_future
            pred_3sigma_min = mean_future - 3*std_future
            pred_3sigma_max = mean_future + 3*std_future

            # 결과 표시를 두 컬럼으로 분할
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Price Statistics")
                st.metric("Current Price", f"${current_price:.2f}")
                st.metric("Expected Future Price", f"${mean_future:.2f}")
                st.metric("Price Standard Deviation", f"${std_future:.2f}")
                
                st.subheader("Confidence Intervals")
                st.write(f"1σ Range: ${pred_1sigma_min:.2f} - ${pred_1sigma_max:.2f}")
                st.write(f"2σ Range: ${pred_2sigma_min:.2f} - ${pred_2sigma_max:.2f}")
                st.write(f"3σ Range: ${pred_3sigma_min:.2f} - ${pred_3sigma_max:.2f}")

            with col2:
                st.subheader("Historical Data")
                st.line_chart(data['Close'])
            
            # 확률 분포 그래프는 전체 너비로 표시
            st.subheader("Price Distribution Analysis")
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
            
            # 실제 가격 히스토그램
            ax1.hist(prices, bins=50, density=True, alpha=0.5, color='blue', 
                    label='Historical Price Distribution')
            ax1.set_title(f"{ticker} - Historical Price Distribution")
            ax1.set_xlabel("Price")
            ax1.set_ylabel("Density")
            ax1.legend()
            
            # 예측된 확률 분포
            ax2.plot(x, prob_density, label='Quantum Probability Density')
            ax2.axvspan(pred_1sigma_min, pred_1sigma_max, color='orange', 
                       alpha=0.2, label='1σ Range')
            ax2.axvspan(pred_2sigma_min, pred_2sigma_max, color='green', 
                       alpha=0.1, label='2σ Range')
            ax2.axvspan(pred_3sigma_min, pred_3sigma_max, color='red', 
                       alpha=0.05, label='3σ Range')
            ax2.axvline(x=current_price, color='red', linestyle='--', 
                       label='Current Price')
            ax2.set_title(f"{ticker} - PDE-based Price Distribution Prediction")
            ax2.set_xlabel("Price")
            ax2.set_ylabel("Probability Density")
            ax2.legend()
            
            plt.tight_layout()
            st.pyplot(fig)

else:
    st.info("Please enter parameters in the sidebar and click 'Calculate Price Distribution' to start the analysis.")
