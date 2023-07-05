import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import xgboost
import json
import seaborn as sns
import streamlit as st

sns.set_style("darkgrid")
st.title("Прогнозирование производительности самосвалов")

st.markdown("""Модель прогнозирования производительности самосвала по заданным эксплуатационным показателям. 
            Модель базируется на алгоритме __XGBoost__  и на одноименной библиотеке __python__.""")

with open('xgb.pkl', mode='rb') as m:
    model = pickle.load(m)

breed = list(set(json.load(open('breed.json')).values()))
model_ex = ['WK-35.', 'Погрузчики.', 'ЭКГ-10.', 'ЭКГ-12К.', 'ЭКГ-15.', 'ЭКГ-15М.', 'ЭКГ-18.', 
            'ЭКГ-20.', 'ЭКГ-20КМ.', 'ЭКГ-8УC.']

with st.sidebar:
    st.markdown(
        f"""
            Производительность автосамосвалов БелАЗ является основой для расчета
    количества парка автомобилей при планировании разработки карьеров, при планировании
    выполнения производственных задач по транспортированию горной массы на годовом, месячном,
    недельно-суточном горизонтах.<br>
    {st.divider()}
    На данный момент задача предсказания производительности
    самосвалов с учетом условий горнотранспортного комплекса, су учетом отсутствия
    автоматизированных программных комплексов планирования перевозок горной массы в
    рассматриваемом аспекте является актуальной, а применение методов машинного обучения в
    горной промышленности, на уровне рассматриваемых данных, является достаточно новым для
    предприятия мероприятием и заключает в себе предпосылки к дальнейшему развитию в
    представленной области.
        """
    )
col1, col2 = st.columns(2)

with col1:
    st.subheader("Планируемые горнотехнические показатели карьера")
    length = st.number_input('Значение плеча откатки: ') # 1
    height = st.number_input('Перепад высот: ')          # 2

    ei_breed = st.selectbox("Укажите единицу измерения породы: ", ['т', 'м3']) # 4
    if ei_breed == 'т':
        ei_breed = 1
    else:
        ei_breed = 0

    choice_bread = st.radio("Выберете код породы", [b for b in breed]) # 3



with col2:
    st.subheader("Планируемые эксплуатационные показатели")
    time_in_job = st.number_input('Время рейса: ')
    smena = st.selectbox("Выбираем смену: ", [1, 2])
    choice_model_ex = st.selectbox("Выберете модель экскаватора: ", [ex for ex in model_ex])
    choice_model_ex = "МОДЕЛЬ_ЭКСКАВАТОРА_" + choice_model_ex

    choice_model_auto = st.radio('Модель самосвала', ['Белаз-75309.', 'Белаз-75131.'])
    choice_model_auto = 'Модель_самосвала_'+choice_model_auto

# =========================================================================================

dict_feauters = {'СМЕНА': [int(smena)], 'Расстояние, км': [float(length)], 
                 'Перепад_высот, м': [float(height)], 'Код_породы': [choice_bread],
                 'Время_работы, ч': [float(time_in_job)], 'Модель_самосвала_Белаз-75131.': [0],
                 'Модель_самосвала_Белаз-75309.': [0], 'ЕИ_породы_тн.': [ei_breed],
                 'МОДЕЛЬ_ЭКСКАВАТОРА_WK-35.': [0], 'МОДЕЛЬ_ЭКСКАВАТОРА_Погрузчики.': [0],
                 'МОДЕЛЬ_ЭКСКАВАТОРА_ЭКГ-10.': [0], 'МОДЕЛЬ_ЭКСКАВАТОРА_ЭКГ-12К.': [0],
                 'МОДЕЛЬ_ЭКСКАВАТОРА_ЭКГ-15.': [0], 'МОДЕЛЬ_ЭКСКАВАТОРА_ЭКГ-15М.': [0],
                 'МОДЕЛЬ_ЭКСКАВАТОРА_ЭКГ-18.': [0], 'МОДЕЛЬ_ЭКСКАВАТОРА_ЭКГ-20.': [0],
                 'МОДЕЛЬ_ЭКСКАВАТОРА_ЭКГ-20КМ.': [0], 'МОДЕЛЬ_ЭКСКАВАТОРА_ЭКГ-8УC.': [0]}

dict_feauters[choice_model_ex] = 1
dict_feauters[choice_model_auto] = 1

data = pd.DataFrame(dict_feauters)
X = data.values

pred = np.exp(model.predict(X))

if choice_bread == 1: 
    d = 'т.'  
else:
    d = 'м3'

if st.button('Рассчитать производительность'):
    st.markdown(f'**Производительность смосвала в данных условиях составит - {pred[0]:.2f} {d}/час**')
