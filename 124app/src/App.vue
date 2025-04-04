<script setup lang="ts">
import { ref, computed } from 'vue'
import CodeEditor from './assets/CodeEditor.vue';
import Mainscreen from './assets/main-screen/Main-screen.vue';
import Toolbar from './assets/Toolbar.vue';

interface File {
  id: number;
  name: string;
  content: string;
  handle: FileSystemFileHandle | null;
}

const showEditor = ref(false);
const files = ref<File[]>([]);
const activeFileId = ref<number | null>(null);

const activeFile = computed(() => files.value.find(f => f.id === activeFileId.value) || null);

const createNewFile = () => {
  const newFile: File = {
    id: Date.now(),
    name: `Untitled-${files.value.length + 1}`,
    content: '',
    handle: null
  };
  files.value.push(newFile);
  activeFileId.value = newFile.id;
  showEditor.value = true;
};

const openFile = (file: { name: string, content: string, handle: FileSystemFileHandle }) => {
  const newFile: File = {
    id: Date.now(),
    name: file.name,
    content: file.content,
    handle: file.handle
  };
  files.value.push(newFile);
  activeFileId.value = newFile.id;
  showEditor.value = true;
};

const closeFile = (fileId: number) => {
  const index = files.value.findIndex(f => f.id === fileId);
  let flag = 0;
  if (index !== -1) {
    
    if(confirm("Are you sure you want to exit without saving?")){
      flag = 1;
      files.value.splice(index, 1);
    }
    else{
      alert("Cancelled");
    }
    if (files.value.length === 0) {
      showEditor.value = false;
      activeFileId.value = null;
    } else{
      if(flag === 1){
        activeFileId.value = files.value[Math.min(index, files.value.length - 1)].id;
      }
    }
  }
};

const updateFileContent = (fileId: number, content: string) => {
  const file = files.value.find(f => f.id === fileId);
  if (file) {
    file.content = content;
  }
};

const saveAs = async (content: string, handle: FileSystemFileHandle | null) => {

  const newHandle = await window.showSaveFilePicker({
      types: [
        {
          description: 'Spell file',
          accept: {
            'text/plain': ['.spell'],
          },
        },
      ],
    });
  
    const writable = await newHandle.createWritable();
    await writable.write(content);
    await writable.close();
    console.log('File saved as in local directory', newHandle.name);
    return { handle: newHandle, name: newHandle.name };
  
};  

const saveFile = async (content: string, handle: FileSystemFileHandle | null) => {
  if (handle) {
    const writable = await handle.createWritable();
    await writable.write(content);
    await writable.close();
    console.log('File saved:', handle.name);
    // return null;
  } else {
    // If no handle, we need to show the save dialog
    return await saveAs(content);
  }
};

const handleToolbarAction = async (action: string, payload?: any) => {
  switch (action) {
    case 'newFile':
      createNewFile();
      break;
    case 'openFile':
      openFile(payload);
      break;
    case 'saveFile':
      if (activeFile.value) {
        const result = await saveFile(activeFile.value.content, activeFile.value.handle);
        if(result){
          activeFile.value.name = result.name;
          activeFile.value.handle = result.handle;
        }
      }
      break;
    case 'fileSaved':
      if (activeFile.value) {
        activeFile.value.name = payload.name;
        activeFile.value.handle = payload.handle;
      }
      break;
    case 'saveasFile':
      if (activeFile.value) {
        const result = await saveAs(activeFile.value.content, activeFile.value.handle);
        if(result){
          activeFile.value.name = result.name;
          activeFile.value.handle = result.value;
        }
      }
      break;
    case 'updateContent':
      if (activeFileId.value !== null) {
        updateFileContent(activeFileId.value, payload);
      }
      break;
  }
};


</script>

<template>
  <div class="container">
    <template v-if="showEditor">
      <Toolbar @action="handleToolbarAction" />
      <div class="tabs" role="tablist">
        <button
          v-for="file in files"
          :key="file.id"
          @click="activeFileId = file.id"
          :class="{ active: file.id === activeFileId }"
          role="tab"
          :aria-selected="file.id === activeFileId"
        >
          {{ file.name }}
          <span @click.stop="closeFile(file.id)" class="close-tab" aria-label="Close tab">&times;</span>
        </button>
      </div>
      <CodeEditor
        v-if="activeFile"
        :content="activeFile.content"
        @update:content="content => updateFileContent(activeFile.id, content)"
      />
    </template>
    <Mainscreen v-else @newFileClicked="createNewFile" />
    <!-- <Mainscreen v-else @openFile = "openFile"/> -->
  </div>
</template>

<style>
.container {
  display: flex;
  flex-direction: column; 
  height: 100vh; 
  width: 100vw;
}

.tabs {
  display: flex;
  background-color: #252526;
  padding: 5px 5px;
  padding-top: 40;
  overflow-x: auto;
}

.tabs button {
  background-color: #4b0082;
  border: none;
  color: #CCCCCC;
  padding: 8px 16px;
  cursor: pointer;
  margin-right: 2px;
  border-top-left-radius: 3px;
  border-top-right-radius: 3px;
}

.tabs button.active {
  background-color: #4b0082;
}

.close-tab {
  margin-left: 8px;
  font-size: 14px;
}

.close-tab:hover {
  color: #FF5555;
}

.CodeEditor {
  flex-grow: 1; 
}

.tabs {
  display: flex;
  padding: 0;
  margin: 5;
  list-style-type: none;
}

.tabs button {
  background: transparent;
  border: none;
  padding: 15px 20px;
  cursor: pointer;
  font-family: 'Fira Code', monospace; /* Change font family here */
  font-size: 16px; /* Change font size here */
  color: #ffffff; /* Set the text color */
  text-align: center;
  transition: color 0.3s, background-color 0.3s;
}

.tabs button:hover {
  background-color: #444444; /* Background color on hover */
  color: #fff; /* Text color on hover */
}

@font-face {
  font-family: 'Anigira';
  src: url('/fonts/Anigira - Display.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'Starlight';
  src: url('/fonts/StarlightRune-Personal Use.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'Mistic';
  src: url('/fonts/Mistic-Regular.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'MagicalWorld';
  src: url('/fonts/Magical World.ttf') format('truetype');
  font-weight: lighter;
  font-style: normal;
}

@font-face {
  font-family: 'MagicalSource';
  src: url('/fonts/MagicalSource_Demo.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'DragonFire';
  src: url('/fonts/Dragon Fire.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}
</style>