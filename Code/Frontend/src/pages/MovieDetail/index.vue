<!--  -->
<template>
  <div class="MovieView">
      <el-container class = page>
          <el-header class="header"><SearchBar class="searchbar"/></el-header>

          <el-container class="body">
              <el-main class="movieBody">
              <h1 class="title">{{info.title}}</h1>
              <el-space spacer="|">
                  <div><el-icon><Calendar /></el-icon></div>{{ info.year }}
                  <el-icon><Location /></el-icon>
                  <div v-for= "(c, index) in info.countries" :key="index">
                      {{ c }} 
                  </div>
              </el-space>
              <el-space spacer="|">
                  <el-icon><CollectionTag /></el-icon>
                  <div v-for="(genre, index) in info.genres" :key="index">
                      {{ genre }} 
                  </div>
              </el-space>
              <el-space spacer="|">
                <el-icon><VideoCameraFilled /></el-icon>
                <div v-for="(c, index) in info.colorinfos" :key="index">
                    {{ c }} 
                </div>
              </el-space>
              <el-space spacer="|">
                <el-icon><Stopwatch /></el-icon>
                <div v-for="(r, index) in info.runningtimes" :key="index">
                    {{ r[0] }}: {{ r[1] }} mins
                </div>
              </el-space>
              <el-space spacer="|">
                <el-icon><ChatDotSquare /></el-icon>
                <div v-for="(l, index) in info.languages" :key="index">
                    {{ l }}
                </div>
              </el-space>
              <div class="fields">  
                  <h2>Description</h2>
                  <p>{{info.plot}}</p>
                  <h2>Directors</h2>
                  <el-space spacer='|'>
                    <div v-for="(director, index) in info.directors" :key="index">
                      <el-icon style='padding-right: 10px'><Avatar /></el-icon>{{ director }} 
                    </div>
                  </el-space>
                  <h2>Writers</h2>
                  <el-space spacer='|'>
                    <div v-for="(writer, index) in info.writers" :key="index">
                      <el-icon style='padding-right: 10px'><Avatar /></el-icon>{{ writer }}
                    </div>
                  </el-space>
                  <h2>Editors</h2>
                  <el-space spacer='|'>
                    <div v-for="(editor, index) in info.editors" :key="index">
                      <el-icon style='padding-right: 10px'><Avatar /></el-icon>{{ editor }}
                    </div>
                  </el-space>

                  <h2>Cast</h2>
                      <el-scrollbar class="srollbar" v-if="hasCast">
                          <div class="scrollbar-flex-content">
                          <el-card v-for="item in Object.keys(info.cast)" :key="item" class="card" shadow="hover">
                              <p>{{ item }}</p>
                              <p class="txt">as</p>
                              <p>{{ info.cast[item] }}</p>
                          </el-card>
                          </div>
                      </el-scrollbar>  
                      <p v-else>Unknown</p>
                  <h2>Soundmixes</h2>
                  <el-space spacer='|'>
                    <div v-for="(soundmix, index) in info.soundmixes" :key="index">
                      {{ soundmix }}
                    </div>
                  </el-space>
                  <h2>Composers</h2>
                  <el-space spacer='|'>
                    <div v-for="(composer, index) in info.composers" :key="index">
                      <el-icon style='padding-right: 10px'><Avatar /></el-icon>{{ composer}}
                    </div>
                  </el-space>
                  <h2>Certificates</h2>
                  <div v-for="item in info.certificates" :key="item">
                      <p>{{item[0]}}: {{ item[1]}}</p>
                  </div>
                  <h2>Release Dates</h2>
                  <div v-for="item in info.releasedates" :key="item">
                      <p>{{item[0]}}: {{ item[1]}}</p>
                  </div>

              </div> 
                  <el-divider><h2 class="end">END</h2></el-divider>
              </el-main>
              <el-aside><KeyWordsBar class="sidebar" :keywords="info.keywords" v-if="info.keywords.length>0"/></el-aside>
          </el-container>
      </el-container>
  
  </div>
</template>

<script setup>
import KeyWordsBar from './KeyWordsBar.vue';
import SearchBar from './SearchBar.vue';
import {ref} from 'vue';
import { reactive, getCurrentInstance, onBeforeMount} from "vue";
import { useRoute } from 'vue-router'
 
let { proxy } = getCurrentInstance();
let hasCast = true;
var info = reactive({
  cast:{},
  certificates:	[],
  colorinfos:[],
  composers:[],
  countries:[],
  directors:[],
  editors:[],
  genres:["None"],
  keywords:["None"],
  languages:[],
  plot:"",
  releasedates:[],
  runningtimes:[],
  soundmixes:[],
  title:"",
  type:"",
  writers:[],
  year:""})

const route = useRoute()
proxy.$http
     .get('/api/movie/'+route.params.id, )
     .then(function(res) {
       if (Object.keys(res.data.cast) == 0)
          hasCast = false
        
       
       info.title = res.data.title
       info.year = res.data.year
       info.plot = res.data.plot
       info.type = res.data.type
       info.genres=JSON.parse(JSON.stringify(res.data.genres));
       info.keywords=JSON.parse(JSON.stringify(res.data.keywords));
       info.cast=JSON.parse(JSON.stringify(res.data.cast));
       info.certificates = JSON.parse(JSON.stringify(res.data.certificates));
       info.colorinfos=JSON.parse(JSON.stringify(res.data.colorinfos));
       info.composers=JSON.parse(JSON.stringify(res.data.composers));
       info.countries=JSON.parse(JSON.stringify(res.data.countries));
       info.directors=JSON.parse(JSON.stringify(res.data.directors));
       info.editors=JSON.parse(JSON.stringify(res.data.editors));
       info.languages = JSON.parse(JSON.stringify(res.data.languages));
       info.releasedates=JSON.parse(JSON.stringify(res.data.releasedates));
       info.runningtimes=JSON.parse(JSON.stringify(res.data.runningtimes));
       info.soundmixes=JSON.parse(JSON.stringify(res.data.soundmixes))
       info.writers = JSON.parse(JSON.stringify(res.data.writers))

       
       //info.genres.push(...res.data.genres)
       //info.certificates.push(...res.data.certificates)
       //info.keywords.push(...res.data.keywords)
       info=res.data
       
       //console.log(info)
       //console.log(Object.keys(info.cast))
     })
     .catch(function(error) {
       console.log(error);
     })

/*
 onBeforeMount(() => {
   const route = useRoute()
   proxy.$http
     .get('http://10.124.30.217:8800/movie/'+route.params.id, )
     .then(function(res) {
       info.genres.push(...res.data.genres)
       info.certificates.push(...res.data.certificates)
       info.keywords.push(...res.data.keywords)
       
       console.log(info)
       console.log(info.genres)
     })
     .catch(function(error) {
       console.log(error);
     });
 });
*/
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
  z-index: 100;
}

.searchbar{
  margin-top: 12px;
}

.movieBody{
  display: flex;
  flex-direction: column;
  margin-left: 5%;
  margin-right: 5%;
}

.fields{
  text-align: left;
}

.sidebar{
  display: flex;
  flex-direction: column;
  margin-top: 10%;
  margin-right: 5%;
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

.txt{
  font-family: cursive;
}
</style>
