<template>
    <div class="editor-container">
      <div class="editor"> 
        <vue-monaco-editor
          v-model:value="code"
          theme="vs-dark"
          :options="MONACO_EDITOR_OPTIONS"
          @mount="handleMount"
          @change="handleChange"
        />
      </div>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { ref, shallowRef, watch } from 'vue'
  
  const props = defineProps(['content']);
  const emit = defineEmits(['update:content']);
  
  const MONACO_EDITOR_OPTIONS = {
    automaticLayout: true,
    formatOnType: true,
    formatOnPaste: true,
  }
  
  const code = ref(props.content);
  const editorRef = shallowRef();
  
  watch(() => props.content, (newContent) => {
    if (newContent !== code.value) {
      code.value = newContent;
    }
  });
  
  const handleMount = (editor) => {
    editorRef.value = editor;
  };
  
  const handleChange = (value) => {
    emit('update:content', value);
  };
  
  function formatCode() {
    editorRef.value?.getAction('editor.action.formatDocument').run();
  }
  
  defineExpose({
    formatCode,
    undo: () => editorRef.value?.trigger('undo'),
    redo: () => editorRef.value?.trigger('redo'),
    cut: () => editorRef.value?.trigger('cut'),
    paste: () => editorRef.value?.trigger('paste'),
  });
  </script>
  
  <style scoped>
  .editor-container {
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  
  .editor {
    flex-grow: 1;
    overflow: auto;
  }
  </style>