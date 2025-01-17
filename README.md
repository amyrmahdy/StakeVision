# StakeVision

StakeVision is a project focused on predicting staking trends. It uses advanced time-series modeling and machine learning techniques to forecast staking behaviors, optimize staking strategies, and maximize rewards. In the future, the project will explore reinforcement learning (RL) for dynamic strategy optimization.

---

## **Key Objectives**
1. **Forecast Staking Trends**: Build a predictive model to forecast staking metrics (e.g., stake amount, rewards) using historical and real-time data.
2. **Optimize Staking Strategies**: Develop actionable insights to optimize staking decisions based on predictions.
3. **Backtest Strategies**: Validate the effectiveness of predictive models and strategies using historical data.
4. **Future Expansion**: Lay the groundwork for reinforcement learning (RL) to optimize strategies dynamically.

---

## **Minimal OKRs (Objectives and Key Results)**

### **Objective 1: Predict Staking Metrics**
- **KR 1.1**: Collect and preprocess historical staking data, including network metrics and external factors.
- **KR 1.2**: Build a time-series forecasting model using ARIMA, LSTM, or Transformer-based approaches.
- **KR 1.3**: Achieve a mean absolute percentage error (MAPE) of less than 5% on validation data.

### **Objective 2: Optimize Staking Insights**
- **KR 2.1**: Develop a framework for converting predictions into actionable staking strategies (e.g., when to stake/unstake).
- **KR 2.2**: Test strategies on historical data and compare returns with baseline methods (e.g., constant staking).

### **Objective 3: Backtesting Framework**
- **KR 3.1**: Implement a backtesting environment to simulate staking strategies using historical data.
- **KR 3.2**: Evaluate strategies based on key performance metrics (e.g., cumulative rewards, risk-adjusted returns).

### **Objective 4: Prepare for RL Expansion**
- **KR 4.1**: Define potential RL state-action-reward structures for dynamic strategy optimization.
- **KR 4.2**: Document prerequisites and benchmarks for RL integration in the future.

---

## **Tools Overview**

### **Data Engineering**
| Task                  | Tool Options              |
|-----------------------|---------------------------|
| Data Ingestion        | APIs (market data)   |
| Data Pipeline         | Apache Airflow, Apache NiFi   |
| Storage               | InfluxDB, TimescaleDB     |
| Cloud Storage         | AWS S3, Google Cloud      |

### **Data Science**
| Task                  | Tool Options                  |
|-----------------------|-------------------------------|
| Time-Series Models    | Statsmodels, TensorFlow, PyTorch |
| Feature Engineering   | Pandas, NumPy                |
| Model Tuning          | Optuna, Ray Tune             |

### **Backtesting**
| Task                  | Tool Options       |
|-----------------------|--------------------|
| Simulations           | Backtrader         |
| Performance Metrics   | Custom Framework   |

---

## **Help**

App can be run by:
```
uvicorn main:app --reload
```

Post request can be send to fetch and write by:
```
curl --location '127.0.0.1:8000/fetch_and_write/' \
--header 'Content-Type: application/json' \
--data '{
    "since": "2023-08-01"
}'
```

Dockerfile build:
```
docker buildx build --tag stakevision:1.0.0 .
```

Run docker container:
```
docker run --name sv -p 8001:8000 -d stakevision:1.0.0
```