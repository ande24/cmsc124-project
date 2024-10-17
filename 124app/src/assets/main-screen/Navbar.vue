<template>
    <nav class="navbar">
      <ul class="navbar-nav">
        <li v-for="menu in menus" :key="menu.name" class="nav-item dropdown">
          <a href="#" class="nav-link dropdown-toggle" @click="toggleDropdown(menu)">
            {{ menu.name }}
          </a>
          <ul class="dropdown-menu" v-show="menu.isOpen">
            <li v-for="item in menu.items" :key="item">
              <a href="#" class="dropdown-item">{{ item }}</a>
            </li>
          </ul>
        </li>
      </ul>
    </nav>
  </template>
  
  <script>
  export default {
    data() {
      return {
        menus: [
          { name: 'File', isOpen: false, items: ['New', 'Open', 'Save', 'Exit'] },
          { name: 'Edit', isOpen: false, items: ['Undo', 'Redo', 'Cut', 'Copy', 'Paste'] },
          { name: 'Selection', isOpen: false, items: ['Select All', 'Expand Selection', 'Shrink Selection'] },
          { name: 'View', isOpen: false, items: ['Zoom In', 'Zoom Out', 'Toggle Sidebar'] },
          { name: 'Run', isOpen: false, items: ['Start Debugging', 'Run Without Debugging', 'Stop'] },
          { name: 'Terminal', isOpen: false, items: ['New Terminal', 'Split Terminal', 'Close Terminal'] },
        ],
      };
    },
    methods: {
      toggleDropdown(menu) {
        menu.isOpen = !menu.isOpen;
        // Close other open dropdowns
        this.menus.forEach(m => {
          if (m !== menu) m.isOpen = false;
        });
      },
    },
  };
  </script>
  
  <style scoped>
  .navbar {
    background-color: #4d4d4d;
    padding: 10px;
  }
  
  .navbar-nav {
    display: flex;
    list-style-type: none;
    margin: 0;
    padding: 0;
  }
  
  .nav-item {
    margin-right: 20px;
    position: relative;
  }
  
  .nav-link {
    color: white;
    text-decoration: none;
  }
  
  .dropdown-menu {
    position: absolute;
    background-color: #4d4d4d;
    border: 1px solid white;
    border-radius: 4px;
    padding: 10px 0;
    min-width: 150px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    z-index: 1000;
  }
  
  .dropdown-item {
    display: block;
    padding: 5px 15px;
    color: white;
    text-decoration: none;
  }
  
  .dropdown-item:hover {
    background-color: #f8f9fa;
  }
  </style>