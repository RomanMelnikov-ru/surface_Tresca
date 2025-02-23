import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Слайдер для sigma_y
sigma_y = st.slider("Выберите значение σᵧ", min_value=30, max_value=80, step=10, value=50)

# Параметр t для параметрических уравнений ребер
t = np.linspace(-100, 250, 200)  # Ограничиваем пространство от -10 до 200

# Уравнения ребер (исправленные)
# Ребро 1: sigma_1 = t, sigma_2 = t, sigma_3 = -sigma_y + t
edge1_s1 = t
edge1_s2 = t
edge1_s3 = -sigma_y + t

# Ребро 2: sigma_1 = t, sigma_2 = t, sigma_3 = sigma_y + t
edge2_s1 = t
edge2_s2 = t
edge2_s3 = sigma_y + t

# Ребро 3: sigma_1 = -sigma_y + t, sigma_2 = t, sigma_3 = -sigma_y + t
edge3_s1 = -sigma_y + t
edge3_s2 = t
edge3_s3 = -sigma_y + t

# Ребро 4: sigma_1 = sigma_y + t, sigma_2 = t, sigma_3 = sigma_y + t
edge4_s1 = sigma_y + t
edge4_s2 = t
edge4_s3 = sigma_y + t

# Ребро 5: sigma_1 = -sigma_y + t, sigma_2 = t, sigma_3 = t
edge5_s1 = -sigma_y + t
edge5_s2 = t
edge5_s3 = t

# Ребро 6: sigma_1 = t, sigma_2 = -sigma_y + t, sigma_3 = -sigma_y + t
edge6_s1 = t
edge6_s2 = -sigma_y + t
edge6_s3 = -sigma_y + t

# Девиаторные плоскости (перпендикулярные гидростатической оси)
# Плоскость 1: sigma_1 + sigma_2 + sigma_3 = C1
C1 = -10
# Плоскость 2: sigma_1 + sigma_2 + sigma_3 = C2
C2 = 350

# Функция для ограничения данных плоскостями
def clip_by_planes(s1, s2, s3):
    mask = (s1 + s2 + s3 >= C1) & (s1 + s2 + s3 <= C2)
    return s1[mask], s2[mask], s3[mask]

# Создание 3D-графика с использованием Plotly
fig = go.Figure()

# Добавление ребер
def add_edge(fig, s1, s2, s3, name, color):
    s1_clipped, s2_clipped, s3_clipped = clip_by_planes(s1, s2, s3)
    fig.add_trace(go.Scatter3d(
        x=s1_clipped, y=s2_clipped, z=s3_clipped,
        mode='lines',
        line=dict(color=color, width=1),
        name=name,
        showlegend=False  # Скрываем ребра из легенды
    ))

# Ребра (все зеленые)
add_edge(fig, edge1_s1, edge1_s2, edge1_s3, 'Ребро 1', 'green')
add_edge(fig, edge2_s1, edge2_s2, edge2_s3, 'Ребро 2', 'green')
add_edge(fig, edge3_s1, edge3_s2, edge3_s3, 'Ребро 3', 'green')
add_edge(fig, edge4_s1, edge4_s2, edge4_s3, 'Ребро 4', 'green')
add_edge(fig, edge5_s1, edge5_s2, edge5_s3, 'Ребро 5', 'green')
add_edge(fig, edge6_s1, edge6_s2, edge6_s3, 'Ребро 6', 'green')

# Вершины призмы (точки пересечения ребер с плоскостями)
def get_vertices(s1, s2, s3):
    s1_clipped, s2_clipped, s3_clipped = clip_by_planes(s1, s2, s3)
    return s1_clipped[0], s2_clipped[0], s3_clipped[0], s1_clipped[-1], s2_clipped[-1], s3_clipped[-1]

# Получаем вершины для каждого ребра
v1_start, v2_start, v3_start, v1_end, v2_end, v3_end = get_vertices(edge1_s1, edge1_s2, edge1_s3)
v4_start, v5_start, v6_start, v4_end, v5_end, v6_end = get_vertices(edge2_s1, edge2_s2, edge2_s3)
v7_start, v8_start, v9_start, v7_end, v8_end, v9_end = get_vertices(edge3_s1, edge3_s2, edge3_s3)
v10_start, v11_start, v12_start, v10_end, v11_end, v12_end = get_vertices(edge4_s1, edge4_s2, edge4_s3)
v13_start, v14_start, v15_start, v13_end, v14_end, v15_end = get_vertices(edge5_s1, edge5_s2, edge5_s3)
v16_start, v17_start, v18_start, v16_end, v17_end, v18_end = get_vertices(edge6_s1, edge6_s2, edge6_s3)

# Список вершин
vertices = [
    (v1_start, v2_start, v3_start),  # Вершина 0
    (v1_end, v2_end, v3_end),        # Вершина 1
    (v4_start, v5_start, v6_start),  # Вершина 2
    (v4_end, v5_end, v6_end),        # Вершина 3
    (v7_start, v8_start, v9_start),  # Вершина 4
    (v7_end, v8_end, v9_end),        # Вершина 5
    (v10_start, v11_start, v12_start),  # Вершина 6
    (v10_end, v11_end, v12_end),        # Вершина 7
    (v13_start, v14_start, v15_start),  # Вершина 8
    (v13_end, v14_end, v15_end),        # Вершина 9
    (v16_start, v17_start, v18_start),  # Вершина 10
    (v16_end, v17_end, v18_end)         # Вершина 11
]

# Добавление граней через треугольные полигоны
def add_face(fig, vertices_indices, color, opacity, name):
    x = [vertices[i][0] for i in vertices_indices]
    y = [vertices[i][1] for i in vertices_indices]
    z = [vertices[i][2] for i in vertices_indices]
    fig.add_trace(go.Mesh3d(
        x=x, y=y, z=z,
        i=[0, 0, 1, 1],  # Индексы вершин для треугольников
        j=[1, 2, 2, 3],
        k=[2, 3, 3, 0],
        color=color, opacity=opacity,
        name=name,
        showlegend=True if name == "Поверхность Треска" else False # Показываем в легенде
    ))

# Грани (все зеленые, прозрачные)
add_face(fig, [2, 3, 8, 9], 'green', 0.3, "Поверхность Треска")
add_face(fig, [8, 9, 4, 5], 'green', 0.3, "")
add_face(fig, [4, 5, 0, 1], 'green', 0.3, "")
add_face(fig, [0, 1, 10, 11], 'green', 0.3, "")
add_face(fig, [10, 11, 6, 7], 'green', 0.3, "")
add_face(fig, [6, 7, 2, 3], 'green', 0.3, "")

# Гидростатическая ось (sigma_1 = sigma_2 = sigma_3)
hydrostatic_s1 = np.linspace(0, 200, 100)
hydrostatic_s2 = np.linspace(0, 200, 100)
hydrostatic_s3 = np.linspace(0, 200, 100)
fig.add_trace(go.Scatter3d(
    x=hydrostatic_s1, y=hydrostatic_s2, z=hydrostatic_s3,
    mode='lines',
    line=dict(color='grey', width=3, dash='dash'),
    name='Гидростатическая ось'
))

# Добавление осей из начала координат
axis_length = 100
fig.add_trace(go.Scatter3d(
    x=[0, axis_length], y=[0, 0], z=[0, 0],
    mode='lines',
    line=dict(color='red', width=3),
    name='σ₁'
))
fig.add_trace(go.Scatter3d(
    x=[0, 0], y=[0, axis_length], z=[0, 0],
    mode='lines',
    line=dict(color='green', width=3),
    name='σ₂'
))
fig.add_trace(go.Scatter3d(
    x=[0, 0], y=[0, 0], z=[0, axis_length],
    mode='lines',
    line=dict(color='blue', width=3),
    name='σ₃'
))

# Добавление поверхности Мизеса
def plot_mises_criterion(fig, sigma_y):
    # Радиус цилиндра Мизеса
    radius = np.sqrt(2 / 3) * sigma_y
    # Угол для окружности
    theta = np.linspace(0, 2 * np.pi, 100)
    # Ось цилиндра (гидростатическая ось)
    z = np.linspace(C1 / np.sqrt(3), C2/ np.sqrt(3), 100)  # Ограничиваем цилиндр девиаторными плоскостями
    Theta, Z = np.meshgrid(theta, z)
    # Координаты цилиндра в девиаторной плоскости
    X = radius * np.cos(Theta)
    Y = radius * np.sin(Theta)
    # Преобразование в пространство главных напряжений
    sigma1 = X / np.sqrt(2) - Y / np.sqrt(6) + Z / np.sqrt(3)
    sigma2 = -X / np.sqrt(2) - Y / np.sqrt(6) + Z / np.sqrt(3)
    sigma3 = 2 * Y / np.sqrt(6) + Z / np.sqrt(3)
    # Добавление поверхности Мизеса
    fig.add_trace(go.Surface(
        x=sigma1, y=sigma2, z=sigma3,
        colorscale="Blues",
        opacity=0.5,
        showscale=False,
        name="Поверхность Мизеса",
        showlegend=True
    ))

# Добавляем поверхность Мизеса
plot_mises_criterion(fig, sigma_y)

# Настройка макета графика
fig.update_layout(
    scene=dict(
        xaxis=dict(title='σ₂', range=[-70, 200]),  # Заголовок оси X и диапазон
        yaxis=dict(title='σ₃', range=[-70, 200]),  # Заголовок оси Y и диапазон
        zaxis=dict(title='σ₁', range=[-70, 200]),  # Заголовок оси Z и диапазон
        aspectmode='data',  # Сохраняем пропорции осей
        camera=dict(
            projection=dict(type='orthographic')  # Ортогональная проекция
        )
    ),
    title='Визуализация критерия Треска и Мизеса в пространстве главных напряжений',
    margin=dict(l=0, r=0, b=0, t=40),
    showlegend=True  # Показываем легенду
)

# Отображение графика в Streamlit
st.plotly_chart(fig, use_container_width=True)
