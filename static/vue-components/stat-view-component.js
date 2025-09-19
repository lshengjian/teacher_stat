// stat-view-component.js
import { loadTemplate } from './template-loader.js';

const { ref, onMounted } = Vue;

// 预加载模板
let templateCache = null;
const getTemplate = async () => {
  if (!templateCache) {
    templateCache = await loadTemplate('/static/templates/stat-view.html');
  }
  return templateCache;
};

const StatViewComponent = {
  props: ['state'],
  template: '', // 将在组件注册前动态设置
  setup(props) {
    // 加载统计
    const loadStat = async () => {
      const res = await fetch('/api/stat/age-title');
      const data = await res.json();
      console.log('从API获取的统计数据:', data);
      props.state.statData.value = data;
    };

    // 导出统计Excel
    const exportStatExcel = () => {
      const params = new URLSearchParams();
      window.open(`/api/stat/age-title/export?${params.toString()}`, '_blank');
    };

    // 在组件挂载时加载统计数据
    onMounted(() => {
      // 只有在statData为空时才加载数据
      if (Object.keys(props.state.statData.value).length === 0) {
        loadStat();
      }
    });

    return {
      loadStat,
      exportStatExcel
    };
  }
};

// 动态设置模板
getTemplate().then(template => {
  StatViewComponent.template = template;
});

export { StatViewComponent };