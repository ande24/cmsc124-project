<template>
    <v-toolbar app dense>
      <v-btn id="openNewFile" @click="openNewFile" icon>
        <v-icon class="icons">mdi-file-plus</v-icon>
      </v-btn>
      <v-btn id="openOldFile" @click="openExistingFile" icon>
        <v-icon class="icons">mdi-folder-open</v-icon>
      </v-btn>
      <v-btn id="saveFile" @click="saveFile" icon :disabled="isFileSaved">
        <v-icon class="icons">mdi-content-save</v-icon>
      </v-btn>
      <v-btn id="saveAsNewFile" @click="saveAsNewFile" icon>
        <v-icon class="icons">mdi-content-save-settings</v-icon>
      </v-btn>
      <v-btn id="cut" @click="cut" icon>
        <v-icon class="icons">mdi-content-cut</v-icon>
      </v-btn>
      <v-btn id="paste" @click="paste" icon>
        <v-icon class="icons">mdi-content-paste</v-icon>
      </v-btn>
      <v-btn id="undo" @click="undo" icon>
        <v-icon class="icons">mdi-undo</v-icon>
      </v-btn>
      <v-btn id="redo" @click="redo" icon>
        <v-icon class="icons">mdi-redo</v-icon>
      </v-btn>
      
      <!-- Spacer pushes the compile and execute buttons to the right -->
      <v-spacer></v-spacer>
  
      <!-- Compile button -->
      <v-btn id="compile" @click="compileCode" icon>
        <v-icon class="icons">mdi-play-box-outline</v-icon>
      </v-btn>
  
      <!-- Execute button -->
      <v-btn id="execute" @click="executeCode" icon>
        <v-icon class="icons">mdi-play-circle-outline</v-icon>
      </v-btn>
    </v-toolbar>
  </template>
  
  <script>
    /*functions here*/
  </script>
  
<style>
  .v-toolbar {
    background-color: #1e1e1e;
    width: 100%;
    padding-right: 16px;
  }
  
  /* Shrink the icons to 75% */
  .v-btn {
    transform: scale(0.75); 
    transform-origin: center;/* Shrink the buttons (and icons inside) to 75% */
  }
  
  .icons {
    color: white; /* Icon color */
    padding-right: 12px;
    padding-left: 12px;
  }
  
  /* Shrink the icons to 75% */
  .v-btn {
    transform: scale(0.75); /* Shrink the buttons (and icons inside) to 75% */
  }
  
  .icons {
    color: white; /* Icon color */
  }
  
  .custom-divider {
    width: 1px;
    height: 24px;
    border-left: 1px solid white;
  }

    .icons {
        color: white;
    }
  </style>
  