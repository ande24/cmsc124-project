<template>
    <Navbar />
    <Toolbar />
    <div class="editor"> 
        <vue-monaco-editor
          v-model:value="code"
          theme="vs-dark"
          :options="MONACO_EDITOR_OPTIONS"
          @mount="handleMount"
        />
    </div>
</template>

<script lang="ts" setup>
    import { ref, shallowRef } from 'vue'
    import Toolbar from './Toolbar.vue'
    import Navbar from './main-screen/Navbar.vue'

    const MONACO_EDITOR_OPTIONS = {
    automaticLayout: true,
    formatOnType: true,
    formatOnPaste: true,
    }

    const code = ref('// Enter code here')
    const editorRef = shallowRef()
    const handleMount = editor => (editorRef.value = editor)

    function formatCode() {
    editorRef.value?.getAction('editor.action.formatDocument').run()
    }
</script>

<style>
    .editor {
        height: 100%;
        width: 100%;
        overflow: auto;
    }
</style>