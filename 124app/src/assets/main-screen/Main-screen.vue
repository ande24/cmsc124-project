<template>
  <v-app>
    <v-card>
      <v-layout>
        <v-main style="height: 100vh; background-color: #1a1a1a;">
          <!-- Content for each rail -->
          <div class="ide-name">
            <h1 id="title">CODEX</h1>
          </div>
          <div class="new-file">
            <button class="button" @click="newFileClicked">Create a new spell</button>
          </div>
          <div class = "open-existing-file"  >
            <button class="button" @click ="openExistingFile">Invoke an existing spell</button>
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


#title {
  margin-top: 5px;
  font-family: 'Starlight';
  transform: scaleX(1.5); 
  letter-spacing: 5px;
  font-size: 175px;
  color: #e0e0e0;
  text-shadow: 0 0 0px #a26ee2, 0 0 5px #a26ee2, 0 0 10px #a26ee2; /* Initial glow */
  animation: glowingPulse 5s infinite ease-in-out; /* Glowing pulse effect */
}

@keyframes glowingPulse {
  0% {
    text-shadow: 0 0 2px #a26ee2, 0 0 4px #a26ee2, 0 0 8px #a26ee2;
  }
  50% {
    text-shadow: 0 0 8px #a26ee2, 0 0 16px #a26ee2, 0 0 24px #a26ee2;
  }
  100% {
    text-shadow: 0 0 2px #a26ee2, 0 0 4px #a26ee2, 0 0 8px #a26ee2;
  }
}

.button {
  margin-bottom: 25px;
  background-color: #1a1a1a; /* Dark background */
  color: #e0e0e0; /* White text */
  border: none; /* No border by default */
  padding: 10px 20px;
  font-size: 45px;
  transform: scaleX(1.3); 
  letter-spacing: 3px;
  font-family: 'Starlight', sans-serif;
  cursor: pointer;
  border-radius: 30px;
  position: relative;
  box-shadow: none; /* No glow initially */
  text-shadow: none; /* No glow initially */
  transition: all 0.3s ease;
}

.button:hover {
  background-color: #9b4dca; /* Lighter purple background on hover */
  color: #1a1a1a; /* Dark text */
  box-shadow: 0 0 20px #a26ee2, 0 0 30px #a26ee2, 0 0 40px #a26ee2; /* Glowing effect */
  text-shadow: 0 0 10px #a26ee2, 0 0 20px #a26ee2, 0 0 30px #a26ee2; /* Glow effect only on hover */
}

.button:active {
  transform: scale(0.98); /* Slight shrink on click */
}


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