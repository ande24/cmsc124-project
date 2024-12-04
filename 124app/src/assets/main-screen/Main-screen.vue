<template>
  <v-app>
    <Navbar />
    <v-card>
      <v-layout>
      
        <v-main style="height: 100vh; background-color: #343434;">
          <!-- Content for each rail -->
          
          <div class="ide-name">
            <h1>PormaCode</h1>
          </div>
          <div class="new-file" @click="newFileClicked">
            <button style="border: 4px solid white; border-radius: 40px;background-color: #02123c; color: white; padding-top: 10px; padding-bottom: 10px; padding-left: 30px; padding-right: 30px;"> New File </button>
          </div>
          <div class = "open-existing-file" @click ="openExistingFile" >
            <button style="border: 4px solid white; border-radius: 40px;background-color: #02123c; color: white; padding-top: 10px; padding-bottom: 10px; padding-left: 30px; padding-right: 30px;"> Open File </button>
          </div>
        </v-main>
      </v-layout>
    </v-card>
  </v-app>
</template>

<script>
import Navbar from './Navbar.vue'

export default {
  components: {
    Navbar
  },
  data() {
    return {
      drawer: true, // Sidebar starts open
      activeRail: '', // Track which rail is currently active
    };
  },
  methods: {
    toggleRail(page) {
      // Toggle the rail; if the same page is clicked, it closes the rail
      if (this.activeRail === page) {
        this.activeRail = ''; // Close the rail if it's already open
      } else {
        this.activeRail = page; // Set the rail to the clicked page
      }
    },
    newFileClicked() {
      console.log("new file clicked");
      this.$emit('newFileClicked');
    },

    openExistingFile(){
      console.log("open existing file clicked");
      this.$emit('openFile');
    }
  },
};
</script>

<style scoped>
h2 {
  padding-top: 60px;
  margin-left: 200px;
  color: white;
}
.sidebar-class {
  background: #202020;
}
.ide-name {
  display: flex;
  justify-content: center;
  padding-top: 200px;
  font-size: 50px;
  color: white;
}
.new-file {
  display: flex;
  justify-content: center;
  padding-top: 40px;
  font-size: 20px;
}

.open-existing-file {
  display: flex;
  justify-content: center;
  padding-top: 40px;
  font-size: 20px;
}
</style>