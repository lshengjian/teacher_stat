import streamlit as st
import pandas as pd
from io import BytesIO
import zipfile
from pathlib import Path
from src.config import get_options 
from src.merge_files import merge_teacher_files
from src.utils import ROOT_DIR
from src.stat import age_distribution,title_distribution,yearly_application,teacher_projects,pie_chart

st.set_page_config(page_title="教师基本数据登记与统计", page_icon="🧑‍🏫", layout="wide")

DEP_NAME = get_options("department")
st.title(f"🧑‍🏫 {DEP_NAME} 教师基本数据登记、合并与统计")

# 侧边栏功能选项
with st.sidebar:
    st.header("功能导航")
    page = st.radio(
        "请选择功能",
        [ "上传合并","教师结构", "项目情况",],
        key="main_nav"
    )


# Session state 初始化
for key in ["df_basic", "df_proj"]:
    if key not in st.session_state:
        st.session_state[key] = pd.DataFrame()


if page == "上传合并":
    st.subheader("下载教师个人档案模板")
    template_dir = Path(__file__).parent / "templates"
    template_files = list(template_dir.glob("*.xlsx"))
    if template_files:
        for tf in template_files:
            with open(tf, "rb") as f:
                st.download_button(
                    label=f"下载模板：{tf.name}",
                    data=f.read(),
                    file_name=tf.name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    st.subheader("上传教师个人档案（多个）")
    uploaded = st.file_uploader(
        "请选择 .xlsx 文件（文件名必须为：专业-工号-姓名-个人档案.xlsx）",
        type=["xlsx", "xls"],
        accept_multiple_files=True
    )
    if uploaded:
        upload_dir = ROOT_DIR / "data/uploads"
        upload_dir.mkdir(parents=True, exist_ok=True)
        for up in uploaded:
            with open(upload_dir / up.name, "wb") as f:
                f.write(up.getbuffer())
        st.success(f"已上传 {len(uploaded)} 个文件到服务器。")
        fname,all_base, all_projects=merge_teacher_files()
        st.session_state.df_basic = all_base
        st.session_state.df_proj = all_projects
        st.success(f"汇总文件：{fname}，共 {len(all_base)} 条基本资料，{len(all_projects)} 条项目资料。")
elif page == "教师结构":
    st.subheader("专业教师结构统计")
    dfb = st.session_state.df_basic.copy()
    if  dfb.empty:
        data_dir = ROOT_DIR / "data"
        fname = data_dir / (get_options('department') + '.xlsx')
        st.session_state.df_basic = dfb = pd.read_excel(fname, sheet_name="基本资料")
        st.session_state.df_proj = pd.read_excel(fname, sheet_name="项目资料")


    majors = sorted(dfb["专业"].dropna().unique().tolist())
    sel_majors = st.multiselect("选择专业", options=majors, default=majors, key="stats_major")
    dfb2 = dfb[dfb["专业"].isin(sel_majors)] if sel_majors else dfb

    left, right = st.columns(2)
    with left:
        st.markdown("a) 按年龄段（饼图 + 各年龄段内职称小计）")
        dist_age, pivot_title_by_age = age_distribution(dfb2, get_options("age_bins"))
        st.plotly_chart(pie_chart(dist_age, "年龄段", "人数", "年龄段人数占比"), use_container_width=True)
        st.dataframe(pivot_title_by_age, use_container_width=True)
    with right:
        st.markdown("b) 按职称（饼图 + 各职称下的年龄段小计）")
        dist_title, pivot_age_by_title = title_distribution(dfb2, get_options("title_categories"), get_options("age_bins"))
        st.plotly_chart(pie_chart(dist_title, "职称", "人数", "职称人数占比"), use_container_width=True)
        st.dataframe(pivot_age_by_title, use_container_width=True)

elif page == "项目情况":
    st.subheader("专业教师项目情况")
 
    dfp = st.session_state.df_proj.copy()
    if  dfp.empty:
        data_dir = ROOT_DIR / "data"
        fname = data_dir / (get_options('department') + '.xlsx')
        st.session_state.df_proj = dfp = pd.read_excel(fname, sheet_name="项目资料")

    majors = sorted(dfp["专业"].dropna().unique().tolist())
    sel_majors = st.multiselect("选择专业", options=majors, default=majors, key="proj_major")
    dfp2 = dfp.copy()
    if sel_majors:
        dfp2 = dfp2[dfp2["专业"].isin(sel_majors)]

    st.markdown("a) 每年的申报情况（可多选项目状态）")
    statuses = st.multiselect("选择项目状态", options=get_options("project_statuses"))
    yearly, details = yearly_application(dfp2, statuses)
    c1, c2 = st.columns([1, 3])
    with c1:
        st.metric("总申报数", int(details.shape[0]))
    with c2:
        st.dataframe(yearly, use_container_width=True)

    st.markdown("b) 查指定教师项目情况")
    kw = st.text_input("输入工号或姓名关键字")
    res = teacher_projects(dfp2, kw)
    st.dataframe(res, use_container_width=True)