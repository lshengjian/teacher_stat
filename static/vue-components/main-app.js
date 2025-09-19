// main-app.js
import { createState } from './shared-state.js';
import { TeacherListComponent } from './teacher-list-component.js';
import { TeacherFormComponent } from './teacher-form-component.js';
import { StatViewComponent } from './stat-view-component.js';
import { loadTemplate } from './template-loader.js';

const { createApp, ref, onMounted, watch } = Vue;

// 预加载模板
let templateCache = null;
const getTemplate = async () => {
  if (!templateCache) {
    templateCache = await loadTemplate('/static/templates/main-app.html');
  }
  return templateCache;
};

const MainApp = {
  components: {
    'teacher-list': TeacherListComponent,
    'teacher-form': TeacherFormComponent,
    'stat-view': StatViewComponent
  },
  template: '', // 将在组件注册前动态设置
  setup() {
    const state = createState();
    
    // 获取字典
    const loadDicts = async () => {
      const types = ['major', 'education', 'degree', 'title'];
      for (let type of types) {
        const res = await fetch(`/api/dict/${type}`);
        state.dicts[type] = await res.json();
      }
    };

    // 获取教师列表
    const loadTeachers = async (page = 1) => {
      // 将filters对象转换为普通对象
      const filtersObj = {};
      for (const key in state.filters) {
        if (state.filters.hasOwnProperty(key)) {
          filtersObj[key] = state.filters[key];
        }
      }
      
      const params = new URLSearchParams({
        ...filtersObj,
        page: page,
        per_page: state.pagination.per_page
      });
      const res = await fetch(`/api/teachers?${params.toString()}`);
      const data = await res.json();
      
      //console.log('从API获取的教师数据:', data);
      
      state.teachers.value = data.teachers;
      state.pagination.total = data.total;
      state.pagination.pages = data.pages;
      state.pagination.current_page = data.current_page;
    };

    // 重置表单
    const resetForm = () => {
      // 计算默认日期
      const today = new Date();
      const defaultBirthDate = new Date(today.getFullYear() - 30, today.getMonth(), today.getDate());
      const defaultHireDate = new Date(today.getFullYear() - 5, today.getMonth(), today.getDate());
      
      state.form.value = {
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
      state.editing.value = false;
      state.currentId.value = null;
    };

    onMounted(() => {
      loadDicts().then(() => {
        //console.log('字典数据已加载:', state.dicts);
      });
      loadTeachers().then(() => {
        //console.log('教师数据已加载:', state.teachers);
      });
    });

    return {
      state,
      resetForm
    };
  }
};

// 动态设置模板
getTemplate().then(template => {
  MainApp.template = template;
});

export { MainApp };