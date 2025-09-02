import pandas as pd
from typing import Tuple, List, Dict
import plotly.express as px
import pandas as pd

def pie_chart(df: pd.DataFrame, names_col: str, values_col: str, title: str):
    if df.empty:
        return px.scatter()  # 空图防报错
    fig = px.pie(df, names=names_col, values=values_col, title=title, hole=0.35)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(legend_title_text="", margin=dict(l=10, r=10, t=40, b=10))
    return fig

def age_distribution(df_basic: pd.DataFrame, age_bins: List[List[int]]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    返回：
    - dist: 各年龄段人数与占比
    - pivot_title_by_age: 透视表（行：年龄段，列：职称）
    """
    total = len(df_basic)
    # 保证年龄段为有序分类
    labels =  [f"<{age_bins[0][0]}"]+[f"{s}-{e}" for s, e in age_bins] + [f">{age_bins[-1][1]}"]
    cat = pd.Categorical(df_basic["年龄段"], categories=labels, ordered=True)
    dist = pd.DataFrame(cat.value_counts()).reset_index()
    dist.columns = ["年龄段", "人数"]
    dist["占比"] = (dist["人数"] / total).round(4) if total > 0 else 0

    pivot = pd.pivot_table(df_basic, index="年龄段", columns="职称", values="工号", aggfunc="count", fill_value=0)
    # 重排索引
    pivot = pivot.reindex(labels, fill_value=0)
    pivot = pivot.reset_index()
    return dist, pivot

def title_distribution(df_basic: pd.DataFrame, title_order: List[str], age_bins: List[List[int]]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    返回：
    - dist: 各职称人数与占比
    - pivot_age_by_title: 透视表（行：职称，列：年龄段）
    """
    total = len(df_basic)
    counts = df_basic["职称"].value_counts()
    counts = counts.reindex(title_order, fill_value=0)
    dist = counts.reset_index()
    dist.columns = ["职称", "人数"]
    dist["占比"] = (dist["人数"] / total).round(4) if total > 0 else 0

    labels =  [f"<{age_bins[0][0]}"]+[f"{s}-{e}" for s, e in age_bins] + [f">{age_bins[-1][1]}"]
    df_basic["年龄段"] = pd.Categorical(df_basic["年龄段"], categories=labels, ordered=True)
    pivot = pd.pivot_table(df_basic, index="职称", columns="年龄段", values="工号", aggfunc="count", fill_value=0)
    pivot = pivot.reindex(title_order, fill_value=0).reset_index()
    return dist, pivot

def yearly_application(df_proj: pd.DataFrame, statuses: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    根据选择的状态过滤，返回：
    - yearly_counts: 每年的申报数量（按申报日期年份）
    - details: 过滤后的明细
    """
    df = df_proj.copy()
    if statuses:
        df = df[df["状态"].isin(statuses)]
    df["申报年度"] = pd.to_datetime(df["申报日期"], errors="coerce").dt.year
    details = df.sort_values(["申报年度", "工号", "课题编号"]).reset_index(drop=True)
    yearly_counts = df.groupby("申报年度")["课题编号"].count().reset_index().rename(columns={"课题编号": "数量"})
    yearly_counts = yearly_counts.sort_values("申报年度").reset_index(drop=True)
    return yearly_counts, details

def teacher_projects(df_proj: pd.DataFrame, keyword: str) -> pd.DataFrame:
    """
    根据工号或姓名关键字查询项目明细
    """
    if not keyword:
        return df_proj.head(0)
    kw = str(keyword).strip()
    m = (df_proj["工号"].astype(str).str.contains(kw, na=False)) | (df_proj["姓名"].astype(str).str.contains(kw, na=False))
    return df_proj[m].sort_values(["申报日期", "工号"]).reset_index(drop=True)