import pandas as pd
import os
import re
from io import BytesIO
from src.utils import ROOT_DIR,compute_age,label_age_bins
from src.config import get_options

def _parse_filename(filename):
    # 专业-工号-姓名-个人档案.xlsx
    match = re.match(r"(.+)-(\d+)-(.+)-个人档案\.xlsx", filename)
    if match:
        return match.group(1), match.group(2), match.group(3)
    return None, None, None

def _save_merged_as_excel(summary_file:str,df_basic: pd.DataFrame, df_proj: pd.DataFrame) -> bytes:
    """
    将两个表写入同一个Excel内存文件，返回字节流（用于Streamlit下载）
    """
    bio = BytesIO()
    with pd.ExcelWriter(bio, engine="openpyxl") as writer:
        df_basic.to_excel(writer, index=False, sheet_name="基本资料")
        df_proj.to_excel(writer, index=False, sheet_name="项目资料")
    bio.seek(0)
    merged_bytes= bio.getvalue()
    sf=ROOT_DIR / f'data/{summary_file}'
    with open(sf, "wb") as f:
        f.write(merged_bytes)

def merge_teacher_files(folder="data/uploads"):
    base_infos = []
    project_infos = []
    for fname in os.listdir(folder):
        if fname.endswith(".xlsx"):
            major, id_num, name = _parse_filename(fname)
            if not major:
                continue
            #path = os.path.join(folder, fname)
            path=ROOT_DIR / folder /f'{fname}'
            base = pd.read_excel(path, sheet_name="基本资料")
            base["专业"] = major
            base["工号"] = id_num
            base["姓名"] = name
            # 计算年龄与年龄段
            if "生日" in base.columns:
                base["年龄"] = base["生日"].apply(lambda d: compute_age(d))
            else:
                base["年龄"] = None

            age_bins = get_options("age_bins")
            base["年龄段"] = base["年龄"].apply(lambda x: label_age_bins(x, age_bins))
            base_infos.append(base)
            projects = pd.read_excel(path, sheet_name="项目资料")
            projects["专业"] = major
            projects["工号"] = id_num
            projects["姓名"] = name
            project_infos.append(projects)
    all_base = pd.concat(base_infos, ignore_index=True)
    all_base = all_base.sort_values(["工号"]).drop_duplicates(subset=["工号"], keep="first").reset_index(drop=True)
    all_projects = pd.concat(project_infos, ignore_index=True)
    fname = get_options('department') + '.xlsx'
    _save_merged_as_excel(fname, all_base, all_projects)
    return fname,all_base, all_projects