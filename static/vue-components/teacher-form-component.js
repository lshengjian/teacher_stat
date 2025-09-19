// teacher-form-component.js
import { loadTemplate } from './template-loader.js';

const { ref, onMounted } = Vue;

// 预加载模板
let templateCache = null;
const getTemplate = async () => {
  if (!templateCache) {
    templateCache = await loadTemplate('/static/templates/teacher-form.html');
  }
  return templateCache;
};

const TeacherFormComponent = {
  props: ['state'],
  template: '', // 将在组件注册前动态设置
  setup(props) {
    // 打印表单数据以进行调试
    console.log('TeacherFormComponent - state.form:', props.state.form);
    
    // 重置表单
    const resetForm = () => {
      // 计算默认日期
      const today = new Date();
      const defaultBirthDate = new Date(today.getFullYear() - 30, today.getMonth(), today.getDate());
      const defaultHireDate = new Date(today.getFullYear() - 5, today.getMonth(), today.getDate());
      
      props.state.form.value = {
        employee_id: '', 
        name: '', 
        gender: '男', 
        major: '',
        birth_date: defaultBirthDate.toISOString().split('T')[0], 
        highest_education: '', 
        highest_degree: '',
        degree_major_name: '', 
        degree_institution: '', 
        title: '',
        position: '', 
        has_teaching_cert: false, 
        has_industry_background: false,
        professional_title: '', 
        hire_date: defaultHireDate.toISOString().split('T')[0], 
        work_experience: '', 
        main_courses: ''
      };
      props.state.editing.value = false;
      props.state.currentId.value = null;
    };

    // 保存教师
    const saveTeacher = async () => {
      const url = props.state.editing.value ? `/api/teachers/${props.state.currentId.value}` : '/api/teachers';
      const method = props.state.editing.value ? 'PUT' : 'POST';

      const res = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(props.state.form.value)
      });

      if (res.ok) {
        resetForm();
        // 重新加载教师列表
        const params = new URLSearchParams({
          ...props.state.filters,
          page: props.state.pagination.current_page,
          per_page: props.state.pagination.per_page
        });
        const res2 = await fetch(`/api/teachers?${params.toString()}`);
        const data = await res2.json();
        
        props.state.teachers.value = data.teachers;
        props.state.pagination.total = data.total;
        props.state.pagination.pages = data.pages;
        props.state.pagination.current_page = data.current_page;
        
        // 如果当前在统计页面，则刷新统计数据
        if (props.state.tab.value === 'stat') {
          const res3 = await fetch('/api/stat/age-title');
          props.state.statData.value = await res3.json();
        } else {
          props.state.tab.value = 'list'; // 保存成功后切换到列表视图
        }
      } else {
        const result = await res.json();
        if (result.error) {
          alert('操作失败: ' + result.error);
        } else {
          alert('操作失败');
        }
      }
    };

    return {
      resetForm,
      saveTeacher
    };
  }
};

// 动态设置模板
getTemplate().then(template => {
  TeacherFormComponent.template = template;
});

export { TeacherFormComponent };