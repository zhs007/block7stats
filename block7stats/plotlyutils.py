# -*- coding:utf-8 -*-
import plotly.graph_objects as go

def genStagesStats(df, fn):
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['stage'],
        y=df['totalusers'],
        name='参与用户数',
    ))
    fig.add_trace(go.Bar(
        x=df['stage'],
        y=df['winper'],
        name='平均用户通关率',
    ))
    fig.add_trace(go.Bar(
        x=df['stage'],
        y=df['totalnums'],
        name='挑战次数',
    ))
    fig.add_trace(go.Bar(
        x=df['stage'],
        y=df['avgClickTime'],
        name='平均点击时间差',
    ))
    fig.add_trace(go.Bar(
        x=df['stage'],
        y=df['avgWinClickTime'],
        name='平均胜利点击时间差',
    ))    
    fig.add_trace(go.Bar(
        x=df['stage'],
        y=df['avgLoseClickTime'],
        name='平均失败点击时间差',
    ))    
    fig.add_trace(go.Bar(
        x=df['stage'],
        y=df['lostper'],
        name='流失率',
    ))
    fig.add_trace(go.Bar(
        x=df['stage'],
        y=df['stayUsers'],
        name='滞留用户数',
    ))
    fig.add_trace(go.Bar(
        x=df['stage'],
        y=df['stayUsersPer'],
        name='滞留用户比例',
    ))    
    fig.add_trace(go.Bar(
        x=df['stage'],
        y=df['avgLoseProgress'],
        name='平均失败进度',
    ))
    fig.add_trace(go.Bar(
        x=df['stage'],
        y=df['gameWinPer'],
        name='通关率',
    ))    
    fig.add_trace(go.Bar(
        x=df['stage'],
        y=df['avgStars'],
        name='平均星星数',
    ))
    fig.add_trace(go.Bar(
        x=df['stage'],
        y=df['totalStarUserNums'],
        name='获得星星玩家数',
    ))    

    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    # fig.write_html('{}{}'.format(g_fnHead, fn))
    fig.write_html('{}'.format(fn))
    # fig.show()
    
