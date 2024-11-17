import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Параметры интерфейса
st.title("Моделирование и Визуализация Здоровья на Основе Параметров")
st.sidebar.header("Настройки моделирования")
M = st.sidebar.slider("Количество выборок (M)", 50, 500, 100, 50)
sigma = st.sidebar.slider("Стандартное отклонение шума (σ)", 0.01, 1.0, 0.1, 0.01)
tau = st.sidebar.slider("Порог для классификации (τ)", 10.0, 40.0, 25.0, 0.5)


if "data_initialized" not in st.session_state:
    # Создание матрицы данных X
    D = 4
    X = np.zeros((D, M))

    # Генерация роста и веса
    X[0, :] = np.round(np.random.normal(165, 15, M))  # Рост: N(165, 225) (среднее 165, std=15)
    X[1, :] = np.random.normal(62, 10, M)  # Вес: N(62, 100) (среднее 62, std=10)

    st.session_state["X"] = X
    st.session_state["data_initialized"] = True

if st.sidebar.button("Сгенерировать данные"):
    D = 4
    X = np.zeros((D, M))

    # Генерация роста и веса
    X[0, :] = np.round(np.random.normal(165, 15, M))  # Рост: N(165, 225) (среднее 165, std=15)
    X[1, :] = np.random.normal(62, 10, M)  # Вес: N(62, 100) (среднее 62, std=10)

    st.session_state["X"] = X

X = st.session_state["X"]

# Кнопка для очистки данных
if st.button("Очистить данные"):
    # Ограничение диапазона роста и веса
    bmi = X[1, :] / (X[0, :] / 100) ** 2
    reasonable_indices = (
            (X[0, :] >= 165) & (X[0, :] <= 225) &
            (X[1, :] >= 65) & (X[1, :] <= 100) &
            (bmi >= 14) & (bmi <= 60)
    )
    X = X[:, reasonable_indices]
    st.session_state["X"] = X
    bmi = bmi[reasonable_indices]

# ИМТ
bmi = X[1, :] / (X[0, :] / 100) ** 2

# Добавление шума и уровня глюкозы
noise = np.random.normal(0, sigma, X.shape[1])
X[2, :] = bmi + noise  # Уровень глюкозы с шумом

# Классификация здоровья на основе уровня глюкозы
X[3, :] = (X[2, :] >= tau).astype(int)

# Отображение данных в интерфейсе
st.subheader("Сгенерированные данные")
data_df = pd.DataFrame({
    "Рост (см)": X[0, :],
    "Вес (кг)": X[1, :],
    "ИМТ": bmi,
    "Уровень глюкозы": X[2, :],
    "Метка (0=Здоров, 1=Диабет)": X[3, :]
})
st.write(data_df)

# Гистограмма ИМТ
st.subheader("Гистограмма ИМТ")
fig, ax = plt.subplots()
bins = np.arange(int(bmi.min()), int(bmi.max()) + 1, 2)
#binsy = np.arange(int(bmi.min()), int(bmi.max()) + 1, 2)
ax.hist(bmi, bins=bins, color='skyblue', edgecolor='black', align='left')
ax.set_xticks(bins)
#ax.set_yticks(bins)
ax.set_xlabel("Индекс Массы Тела (ИМТ)")
ax.set_ylabel("Частота")
st.pyplot(fig)

# Гистограмма уровня глюкозы
st.subheader("Гистограмма уровня глюкозы с шумом")
fig, ax = plt.subplots()
ax.hist(X[2, :], bins=15, color='salmon', edgecolor='black', alpha=0.7)
ax.axvline(tau, color='red', linestyle='--', label=f"Порог τ = {tau}")
ax.set_xlabel("Уровень глюкозы")
ax.set_ylabel("Частота")
ax.legend()
st.pyplot(fig)

# Визуализация по меткам здоровья
st.subheader("Визуализация по меткам здоровья")
fig, ax = plt.subplots()
healthy = X[:, X[3, :] == 0]
diabetic = X[:, X[3, :] == 1]
ax.scatter(healthy[0, :], healthy[1, :], color='blue', label="Здоровые", alpha=0.6)
ax.scatter(diabetic[0, :], diabetic[1, :], color='red', label="Диабетики", alpha=0.6)
ax.set_xlabel("Рост (см)")
ax.set_ylabel("Вес (кг)")
ax.legend()
st.pyplot(fig)

# Слайдеры параметров
st.sidebar.subheader("Информация:")
st.sidebar.write("**σ** (Стандартное отклонение шума): Управляет разбросом уровня глюкозы.")
st.sidebar.write("**τ** (Порог классификации): Управляет разделением на метки здоровья.")