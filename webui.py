import streamlit as st
from utils.security import sha256_encode
from utils import request_utils
from config import config

# 初始化 session_state 中的登录状态
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def show_page():
    # 设置初始值
    index_name = ""
    index_id = ""
    segmentation_mode = "自定义"
    max_length = 200  # 假设默认最大长度为5200
    overlap_length = 30  # 假设默认重叠长度为30
    segment_id = "word"  # 默认分段标识符

    # 应用布局
    st.title("知识库管理页面")

    st.text('                                ')
    st.text('-------------------知识库列表------------------')
    st.text('                                 ')

    store_list = request_utils.get_store_list()
    st.json(store_list.json()['data']['vector_stores'])

    st.text('                                ')
    st.text('-------------------创建知识库------------------')
    st.text('                                 ')

    # 输入框
    index_name = st.text_input("请输入知识库名称(创建):", value=index_name)

    # 单选按钮
    segmentation_modes = ["自定义", "自动分段与清洗"]
    segmentation_mode = st.radio("选择分段模式:", segmentation_modes, index=1)

    # 根据分段模式显示额外输入
    if segmentation_mode == "自定义":
        max_length = st.number_input("分段最大长度:", value=max_length)
        overlap_length = st.number_input("分段重叠长度:", value=overlap_length)
        segment_id = st.text_input("分段标识符:", value=segment_id)

    # 文件上传
    uploaded_files = st.file_uploader("请上传文件:", type=["txt", "docx", "pdf"], accept_multiple_files=True, key="uploaded_files")

    # 创建数据库按钮
    if st.button('创建知识库'):
        # 调用接口1
        result = request_utils.create_kb(uploaded_files, index_name, max_length, overlap_length, segment_id)
        # 删除uploads下的文件
        # TODO
        st.json(result.json()['data'])

    st.text('                                ')
    st.text('-------------------知识库上传文件------------------')
    st.text('                                 ')

    # 输入框
    index_id = st.text_input("请输入知识库id(更新):", value=index_id)

    # 文件上传
    uploaded_files1 = st.file_uploader("请上传文件:", type=["txt", "docx", "pdf"], accept_multiple_files=True, key="uploaded_files1")

    if st.button('上传/更新文件'):
        # 调用接口2
        result = request_utils.upload_files(uploaded_files1, index_id, max_length, overlap_length, segment_id)
        st.json(result.json()['data'])

    st.text('                                ')
    st.text('-------------------查询文件------------------')
    st.text('                                 ')

    reload_index_id = ""
    reload_index_id = st.text_input("请输入知识库id(查询所有文件):", value=reload_index_id)

    if st.button('查询'):
        # 调用接口2
        result = request_utils.reload_files(reload_index_id)
        st.json(result.json()["data"]["documents"])

    st.text('                                ')
    st.text('-------------------删除文件------------------')
    st.text('                                 ')
    delete_index_id = ""
    delete_index_id = st.text_input("请输入知识库id(删除文件):", value=delete_index_id)

    delete_file_id = ""
    delete_file_id = st.text_input("请输入文件doc_id(删除文件):", value=delete_file_id)

    if st.button('删除'):
        result = request_utils.delete_file(delete_index_id, delete_file_id)
        st.json(result.json())

# 登录逻辑
def login():
    st.title("用户登录")
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")

    if st.button("登录"):
        if username == config['auth_username'] and sha256_encode(password) == config['auth_password']:
            st.session_state.logged_in = True
            st.success("登录成功！")
            st.rerun()  # 重新运行脚本以显示主页面
        else:
            st.error("用户名或密码错误")

# 根据登录状态决定显示登录界面还是主页面
if not st.session_state.logged_in:
    login()
else:
    show_page()