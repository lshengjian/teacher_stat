// teacher-list-component.js
import { loadTemplate } from './template-loader.js';

const { ref, onMounted } = Vue;

// 预加载模板
let templateCache = null;
const getTemplate = async () => {
  if (!templateCache) {
    templateCache = await loadTemplate('/static/templates/teacher-list.html');
  }
  return templateCache;
};

const TeacherListComponent = {
  props: ['state'],
  template: '', // 将在组件注册前动态设置
  setup(props) {
    // 获取教师列表
    const loadTeachers = async (page = 1) => {
      // 将filters对象转换为普通对象
      const filtersObj = {};
      for (const key in props.state.filters) {
        if (props.state.filters.hasOwnProperty(key)) {
          filtersObj[key] = props.state.filters[key];
        }
      }
      
      const params = new URLSearchParams({
        ...filtersObj,
        page: page,
        per_page: props.state.pagination.per_page
      });
      const res = await fetch(`/api/teachers?${params.toString()}`);
      const data = await res.json();
      
      console.log('从API获取的教师数据:', data);
      
      props.state.teachers.value = data.teachers;
      props.state.pagination.total = data.total;
      props.state.pagination.pages = data.pages;
      props.state.pagination.current_page = data.current_page;
    };

    // 编辑教师
    const editTeacher = (teacher) => {
      // 深拷贝教师对象，避免直接修改原对象
      const teacherCopy = { ...teacher };
      
      // 格式化日期字段
      if (teacherCopy.birth_date) {
        teacherCopy.birth_date = teacherCopy.birth_date.split('T')[0];
      }
      if (teacherCopy.hire_date) {
        teacherCopy.hire_date = teacherCopy.hire_date.split('T')[0];
      }
      
      props.state.form.value = teacherCopy;
      props.state.editing.value = true;
      props.state.currentId.value = teacher.id;
      props.state.tab.value = 'form';
    };

    // 确认删除教师
    const confirmDelete = (teacher) => {
      if (confirm(`确定要删除教师 ${teacher.name} (${teacher.employee_id}) 吗？`)) {
        deleteTeacher(teacher.id);
      }
    };

    // 删除教师
    const deleteTeacher = async (teacherId) => {
      try {
        const res = await fetch(`/api/teachers/${teacherId}`, {
          method: 'DELETE'
        });
        
        if (res.ok) {
          // 不再提醒删除成功
          // 重新加载教师列表
          loadTeachers(props.state.pagination.current_page);
        } else {
          const result = await res.json();
          alert('删除失败: ' + (result.error || '未知错误'));
        }
      } catch (error) {
        console.error('删除教师时出错:', error);
        alert('删除失败: 网络错误');
      }
    };

    // 导出 Excel
    const exportExcel = () => {
      // 将filters对象转换为普通对象
      const filtersObj = {};
      for (const key in props.state.filters) {
        if (props.state.filters.hasOwnProperty(key)) {
          filtersObj[key] = props.state.filters[key];
        }
      }
      
      const params = new URLSearchParams(filtersObj);
      window.open(`/api/teachers/export?${params.toString()}`, '_blank');
    };

    // 分页相关方法
    const changePage = (page) => {
      if (page >= 1 && page <= props.state.pagination.pages) {
        loadTeachers(page);
      }
    };

    const changePerPage = (per_page) => {
      props.state.pagination.per_page = per_page;
      loadTeachers(1); // 重置到第一页
    };

    return {
      loadTeachers,
      editTeacher,
      confirmDelete,
      deleteTeacher,
      exportExcel,
      changePage,
      changePerPage
    };
  }
};

// 动态设置模板
getTemplate().then(template => {
  TeacherListComponent.template = template;
});

export { TeacherListComponent };