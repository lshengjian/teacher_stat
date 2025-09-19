// app.js
import { MainApp } from './vue-components/main-app.js';

const { createApp } = Vue;

// 等待所有组件的模板加载完成后再挂载应用
Promise.all([
  // 等待主应用模板加载
  new Promise(resolve => {
    const checkMainAppTemplate = () => {
      if (MainApp.template && MainApp.template.length > 0) {
        resolve();
      } else {
        setTimeout(checkMainAppTemplate, 10);
      }
    };
    checkMainAppTemplate();
  })
]).then(() => {
  // 创建Vue应用
  const app = createApp(MainApp);
  
  // 挂载Vue应用
  app.mount('#app');
});