// shared-state.js
const { ref, onMounted, watch } = Vue;

const createState = () => {
  const state = {
    tab: ref('list'),
    teachers: ref([]),
    filters: ref({}),
    dicts: ref({ major: [], education: [], degree: [], title: [] }),
    form: ref({
      employee_id: '', name: '', gender: '男', major: '',
      birth_date: '', highest_education: '', highest_degree: '',
      degree_major_name: '', degree_institution: '', title: '',
      position: '', has_teaching_cert: false, has_industry_background: false,
      professional_title: '', hire_date: '', work_experience: '', main_courses: ''
    }),
    editing: ref(false),
    currentId: ref(null),
    statData: ref({}),
    
    // 分页相关
    pagination: ref({
      total: 0,
      pages: 0,
      current_page: 1,
      per_page: 5
    })
  };

  return state;
};

export { createState };