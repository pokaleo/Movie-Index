<!--  -->
<template>
  <div class="MovieView">
      <el-container class = page>
          <el-header class="header"> 
            <SearchBar class="searchbar"/>
          </el-header>
          <el-row class="go">
          <el-button  text>
              <el-icon @click="jumpBack" color="black" size="25"><Back /></el-icon>
            </el-button>
            <router-link to="/">
              <el-button text>
                <el-icon color="black" size="25"><HomeFilled /></el-icon>
              </el-button>
            </router-link>
          </el-row>
          <el-container class="body">
              <el-main class="movieBody">
                <div class="brief">
                  <div class="poster">
                    <el-image style="height: 384px; width:290px;padding-right: 30px;" :src="info.img" fit="contain" >
                      <template #error>
                        <div class="image-slot"> 
                          <img src="../../assets/unsplash.jpg" style="height: 384px; width:290px;"/>
                        </div>
                      </template>
                    </el-image>
                  </div>
                  <div class="text">
                    <h1 class="title">{{info.title}}</h1>
                    <el-space spacer="|">
                        <div><el-icon><Calendar /></el-icon></div>
                        {{ info.year }}
                    </el-space> 
                    <el-space spacer="|">
                        <el-icon><Location /></el-icon>
                        <div v-for= "(c, index) in info.countries" :key="index">
                            {{ c }} 
                        </div>
                        <div v-if="info.countries.length==0">Unknown</div>
                    </el-space>
                    <el-space spacer="|">
                        <el-icon><CollectionTag /></el-icon>
                        <div 
                            v-for="(genre, index) in info.genres" 
                            :key="index" 
                            @click="jumpLink(genre)"
                            @mouseover="handleHoverStart(genre)"
                            @mouseleave="handleHoverLeft()"
                            style="text-decoration: underline;"
                            >
                            <div :class="{active: genre==hover}">{{ genre }} </div>
                        </div>
                        <div v-if="info.genres.length==0">Unknown</div>
                    </el-space>
                    <el-space spacer="|">
                      <el-icon><VideoCameraFilled /></el-icon>
                      <div v-for="(c, index) in info.colorinfos" :key="index">
                          {{ c }} 
                      </div>
                      <div v-if="info.colorinfos.length==0">Unknown</div>
                    </el-space>
                    <el-space spacer="|">
                      <el-icon><Stopwatch /></el-icon>
                      <div v-for="(r, index) in info.runningtimes" :key="index">
                          {{ r[0] }}: {{ r[1] }} mins
                      </div>
                      <div v-if="info.runningtimes.length==0">Unknown</div>
                    </el-space>
                    <el-space spacer="|">
                      <el-icon><ChatDotSquare /></el-icon>
                        <div v-for="(l, index) in info.languages" :key="index">
                            {{ l }}
                        </div>
                        <div v-if="info.languages.length==0">Unknown</div>
                    </el-space>
                  </div>
                </div>
              <div class="fields">  
                  <h2>Description</h2>
                  <p>{{info.plot}}</p>

                  <h2>Directors</h2>
                  <el-scrollbar class="srollbar" v-if="info.directors.length>0" always>
                    <el-space spacer='|'>
                      <div v-for="(director, index) in info.directors" :key="index">
                        <el-icon style='padding-right:10px'><Avatar /></el-icon>{{ director }} 
                      </div>
                    </el-space>
                  </el-scrollbar>
                  <p v-else>Unknown</p>

                  <h2>Writers</h2>
                  <el-scrollbar class="srollbar" v-if="info.writers.length>0"  always>
                    <el-space spacer='|'>
                      <div v-for="(writer, index) in info.writers" :key="index">
                        <el-icon style='padding-right:10px'><Avatar /></el-icon>{{ writer }}
                      </div>
                    </el-space>
                  </el-scrollbar>
                  <p v-else>Unknown</p>

                  <h2>Editors</h2>
                    <el-scrollbar class="srollbar" v-if="info.editors.length>0" always>
                      <el-space spacer='|'>
                        <div v-for="(editor, index) in info.editors" :key="index">
                          <el-icon style='padding-right:10px'><Avatar /></el-icon>{{ editor }}
                        </div>
                      </el-space>
                    </el-scrollbar>
                    <p v-else>Unknown</p>

                  <h2>Cast</h2>
                    <el-scrollbar class="srollbar" v-if="hasCast"  always>
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
                    <el-space spacer='|' v-if="info.soundmixes.length>0">
                      <div v-for="(soundmix, index) in info.soundmixes" :key="index">
                        {{ soundmix }}
                      </div>
                    </el-space>
                    <p v-else>Unknown</p>
                    
                  <h2>Composers</h2>
                    <el-scrollbar class="srollbar" v-if="info.composers.length>0" always>
                      <el-space spacer='|'>
                        <div v-for="(composer, index) in info.composers" :key="index">
                          <el-icon style='padding-right: 10px'><Avatar /></el-icon>{{ composer }}
                        </div>
                      </el-space>
                    </el-scrollbar>
                    <p v-else>Unknown</p>
                  <h2>Certificates</h2>
                  <div v-for="item in info.certificates" v-if="info.certificates.length>0" :key="item">
                      <p>{{item[0]}}: {{ item[1]}}</p>
                  </div>
                  <p v-else>Unknown</p>
                  <h2>Release Dates</h2>
                  <div v-for="item in info.releasedates" v-if="info.releasedates.length>0" :key="item">
                      <p>{{item[0]}}: {{ item[1]}}</p>
                  </div>
                  <p v-else>Unknown</p>
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
import { reactive, getCurrentInstance,ref} from "vue";
import { useRoute, useRouter } from 'vue-router';
import { ElMessageBox} from 'element-plus'
 
let { proxy } = getCurrentInstance();
let hasCast = true;
let hover = ref("");
const router = useRouter()
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
  year:"",
  img: ""})

const route = useRoute()
const fetchData=async()=>{
    await proxy.$http
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
    })
    .catch(function(error) {
      console.log(error);
    })
}

const fetchImg=async()=>{
    await proxy.$http
    .get('/api/img/'+route.params.id, )
    .then(function(res) {
        info.img=res.data.img
    })
    .catch(function(error) {
      console.log(error);
    })
}

/**
 * jump to genre results
 * @param genre 
 */
 const jumpLink = (genre) => {
  ElMessageBox.confirm(
          'Do you want to search results of "'+genre+'"?',
          'Search',
          {
            confirmButtonText: 'YES',
            cancelButtonText: 'Cancel',
            type: 'info',
          })
          .then(()=>{
            router.push({path:"/search",query:{q:genre, t:"genre", pro:false, check:false}})
          })
          .catch(()=>{
            console.log("Jump Cancel!")
          })
}

const jumpBack=()=>{
  router.back()
}

function handleHoverStart(genre){
  hover.value=genre
}

function handleHoverLeft(){
  hover.value=""
}

fetchData()
fetchImg()

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
  text-align: center;
  background-color: black;
  z-index: 100;
}

.header .searchbar{
  margin-top: 12px;
}

.go{
  margin-left: 5%;
  margin-top: 2%;
  margin-bottom: 2%;
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
  height: auto;
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
  font-size: 48px;
  font-family: Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
}

.end{
  font-family: cursive;
}

.txt{
  font-family: cursive;
}

.brief{
  display: flex;
  flex-direction: row;
  align-items: stretch;
}

.brief .text{
  display: flex;
  flex-direction: column;
}

.active{
  background-color:rgb(114, 217, 254);
  font-style: italic;
}

</style>
