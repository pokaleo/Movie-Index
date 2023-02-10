<!--  -->
<template>
  <div class="LoadingView">
      <el-container class = page>
          <el-header class="header"><SearchBar class="searchbar"/></el-header>

          <el-container class="body">
              <el-main class="movieBody">
              <h1 class="title">{{title}}</h1>
                  
              <el-space spacer="|">
                  <el-icon><CollectionTag /></el-icon>
                  <div v-for="genre in genres" :key="genre">
                      {{ genre }} 
                  </div>
              </el-space>
              <div class="fields">  
                  <h2>Description</h2>
                  <p>{{plot}}</p>
                  <h2>Director</h2>
                  <p>{{director}}</p>
                  <h2>Cast</h2>
                      <el-scrollbar class="srollbar">
                          <div class="scrollbar-flex-content">
                          <el-card v-for="item in cast" :key="item" class="card" shadow="hover">
                              <p>{{ item.actor }}</p>
                              <p class="txt">plays</p>
                              <p>{{ item.role }}</p>
                          </el-card>
                          </div>
                      </el-scrollbar>  
              </div> 
              <el-divider><h2 class="end">END</h2></el-divider>
              </el-main>
              <el-aside><KeyWordsBar class="sidebar" :keywords="keywords"/></el-aside>
          </el-container>
      </el-container>
  
  </div>
</template>

<script>
import KeyWordsBar from './KeyWordsBar.vue';
import SearchBar from './SearchBar.vue';

export default{
  name: "LoadingView",

  components:{
      KeyWordsBar,
      SearchBar
  },

  //props:["id"],

  data() {
      return{
          title: "Monsieur Vincent",
          plot:"St. Vincent de Paul struggles to bring about peace and harmony among the peasant and the nobles in the midst of the Black Death in Europe, carrying on his charitable work in the face of all obstacles.",
          director:"Cloche, Maurice",
          cast:[{actor:"Bouquet, Michel", role:"Le tuberculeux"}, {actor:"Bouquet, Michel", role:"Le tuberculeux"},{actor:"Bouquet, Michel", role:"Le tuberculeux"},{actor:"Bouquet, Michel", role:"Le tuberculeux"},{actor:"Bouquet, Michel", role:"Le tuberculeux"},{actor:"Bouquet, Michel", role:"Le tuberculeux"},{actor:"Bouquet, Michel", role:"Le tuberculeux"},{actor:"Bouquet, Michel", role:"Le tuberculeux"},],
          keywords:["misery","door-knocker","wealth","village","megaphone"],
          genres:["Drama","History","Biography"]
      }
  }
}
</script>

<style scoped>
.page{
  padding-top: 0%;
}
.MovieView{
  top: 0px;
  align-items: flex-start;
  align-content: flex-start;

}
.body{
  align-items: flex-start;
}
.header{
  background-color: black;
  text-align: center;
}

.searchbar{
  margin-top: 12px;
}

.movieBody{
  display: flex;
  flex-direction: column;
}

.fields{
  text-align: left;
}

.sidebar{
  top: 25%;
  left: 0%;
}
.srollbar{
  height: 200px;
}
.scrollbar-flex-content {
display: flex;
}
.card {
flex-shrink: 0;
display: flex;
align-items: center;
justify-content: center;
width: 200px;
height: 150px;
margin: 10px;
text-align: center;
border-radius: 4px;
background: white;
color: black;
}

.title{
  text-align: left;
  font-size: 36px;
  font-family: Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
}

.end{
  font-family: cursive;
}
</style>
