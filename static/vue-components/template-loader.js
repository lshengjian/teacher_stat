// template-loader.js
const loadTemplate = async (templatePath) => {
  try {
    const response = await fetch(templatePath);
    if (!response.ok) {
      throw new Error(`Failed to load template: ${templatePath}`);
    }
    return await response.text();
  } catch (error) {
    console.error('Error loading template:', error);
    return ''; // 返回空字符串作为默认模板
  }
};

export { loadTemplate };