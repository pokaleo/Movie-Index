<!--  -->
<template>
  <div class='container'>
    <div class="header">
      <!--input class="iconfont search_input " type="text" placeholder="search"-->
      <div class="logo-container">
        <el-button color="#8794c0" style="margin-right: 20px">
          <el-icon @click="jumpBack" color="#1c2135" size="25"><Back /></el-icon>
        </el-button>
      </div>
      <SearchBar :q=q :t=t :key=q :pro=pro />
      <div class="homebtn">
        <router-link to="/">
          <el-button color="#5a6794">
            Home <el-icon style=" margin-left: 10px" color="#e7e9ee" size="35"><HomeFilled /></el-icon>
          </el-button>
        </router-link>
      </div>
    </div>

    <div class="MovieView">
      <div style="background:linear-gradient(to left,#e7e9ee,#5a6794,#e7e9ee);height:2px;margin-top: 2%"></div>
      <el-container class = page>
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
            <div style="background:linear-gradient(to left,#e7e9ee,#5a6794,#e7e9ee);height:2px;margin-top: 2%"></div>
          </el-main>
          <el-aside><KeyWordsBar class="sidebar" :keywords="info.keywords" v-if="info.keywords.length>0"/></el-aside>
        </el-container>
      </el-container>
    </div>
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
          'Do you want to see all other films in the "'+genre+'" genre?',
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

<style scoped lang="less">
.container {
  height: 100%;
  width: 100%;
  padding-top: 0px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
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
  background-color: transparent;
  text-align: center;
  margin-top: 3%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.movieBody{
  display: flex;
  flex-direction: column;
  margin-left: 5%;
  margin-right: 5%;
}
.homebtn {
  background-color: #5a6794;
  margin-right: 8%;
  border: 1.5px solid #8794c0;
  border-radius: 5px;
  padding: 5px 10px;
  -moz-box-shadow:2px 2px 10px rgba(46, 53, 59, 0.2);
  -webkit-box-shadow:2px 2px 10px rgba(46, 53, 59, 0.2);
  box-shadow:2px 2px 10px rgba(46, 53, 59, 0.2);
}
.go{
  margin-left: 5%;
  margin-top: 2%;
  margin-bottom: 2%;
}
.page{
  padding-top: 0%;
}
.content {
  width: 100%;
  flex: 1;
  margin: 0 auto;
  padding-top: 30px;
  padding-right: 5%;
  padding-left: 5%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;

  .homebtn{
    align-self: flex-end;
  }

  .big-title {
    font-weight: bold;
    padding-left: 20px;
    box-sizing: border-box;

    i {
      color: #5a6794;
    }
  }

  .movie-list {
    overflow-y: auto;

    .movie-item {
      //border: 1px solid gray;
      padding: 10px 24px;
      border-radius: 10px;
      box-sizing: border-box;
      margin-bottom: 15px;
      margin-top: 15px;
      margin-right: 15px;
      //background-color: #eee;
      cursor: pointer;
      padding: 20px;
      box-shadow:
       inset 0 -3em 5em rgba(94, 70, 70, 0.1),
             0.3em 0.3em 0.3em rgba(90, 103, 148, 0.63);


      .movie-name {
        font-size: 25px;
        font-weight: bold;
        color: #1c2135;
      }

      .movie-description {
        font-size: 12px;
        min-height: 50px;
        padding: 2px 0;
        color: #1c2135;
      }

      .movie-info {
        font-weight: bold;
        font-size: 12px;
      }
    }

    .movie-item:hover {
      background-color: #8794c0;
    }
  }

}
.logo{
  height: 70px;
  display: inline-block;
}
.logo-container{
  margin-left: 8%;
  width: 8%;
}
.fields{
  animation: animated-border 1.5s infinite;
  margin-top: 20px;
  font-family: Arial;
  font-size: 18px;
  line-height: 30px;
  font-weight: bold;
  color: #1C2135;
  border: 2px solid;
  border-radius: 10px;
  padding: 15px;
}
.fields{
  text-align: left;
  padding: 2em;
}
.title{
  text-align: left;
  font-size: 48px;
  font-family: Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
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
.txt{
  font-family: cursive;
}
.brief{
  display: flex;
  flex-direction: row;
  align-items: stretch;
  border-radius: 8% / 50%;
  /*background-color: #5a6794;*/
  background-color: rgba(90, 103, 148, 0.3);
  padding: 1px 3% 1px 7%;
  margin-top: 10px;
  -moz-box-shadow:20px 2px 10px #5a6794;
  -webkit-box-shadow:20px 2px 10px #5a6794;
  box-shadow:5px 5px 10px #5a6794;
}
.brief .text{
  display: flex;
  flex-direction: column;
}
.active{
  background-color:#5a6794;
  font-style: italic;
  cursor: pointer;
}
@keyframes animated-border {
  0% {
    box-shadow: 0 0 0 0 #3c4564;
  }
  100% {
     box-shadow: 0 0 0 15px rgba(255,255,255,0);
  }
}
@media only screen and (max-width: 767px) {
  .header {
    align-items: flex-start;
    flex-direction: column-reverse;
  }

  .homebtn {
    margin: 2% auto;
  }
  .logo-container {
    order: 2;
    margin-top: 10px;
  }

  .search-bar-container {
    order: 1;
    margin-bottom: 10px;
  }
}
</style>
