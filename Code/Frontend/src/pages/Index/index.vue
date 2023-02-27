!<!--  -->
<template>
  <div class='container'>
    <div class="header">
      <!--input class="iconfont search_input " type="text" placeholder="search"-->
      <SearchBar :q=q :t=t :key=q />
    </div>
    <perfect-scrollbar>
      <div class="content">
        <div class="big-title" v-if="hasCorrected">
          Did you mean: <el-button @click="$event => goCorrectedPage(spellchecked)" text>{{ spellchecked }}</el-button>?
        </div>
        <div class="movie-list">
          <div class="movie-item" v-for="(item, index) in movieList[0]" :key="index" @click="goMovieDetailPage(item.id)">
            <div class="movie-name">{{ item.movieName }}</div>
            <div class="movie-description">{{ item.description }}</div>
            <div class="movie-info">
              <span>Director:{{ item.director }} • </span>
              <span>Year: {{ item.year }} • </span>
              <span>Country:{{ item.country }} • </span>
              <span>Runtime:{{ item.runtime }}</span>
            </div>
          </div>
        </div>
      </div>
    </perfect-scrollbar>
  

  </div>
</template>

<script setup>
import { reactive,watch,onMounted,getCurrentInstance, ref } from 'vue';
import { useRouter,useRoute, onBeforeRouteLeave, onBeforeRouteUpdate } from "vue-router"
import SearchBar from '../MovieDetail/SearchBar.vue';
// import http from "@/util/http"
const router = useRouter()
const route = useRoute()

let movieList = reactive([])
let spellchecked = ref('')
let hasCorrected = false
let q = ref(route.query.q)
let t = ref(route.query.t)
let a = ref(route.query.a)
let b = ref(route.query.b)
let c = ref(route.query.c)


/**
 * 跳转电影详情页面
 * @param movieId 
 */
const goMovieDetailPage = (movieId) => {
  router.push("/detail/" + movieId)
}

const goCorrectedPage = (newquery) => {
  //alert(spellchecked.value)
  //router.push('/')
  router.replace({name:"Results",query:{q:newquery, t:t.value,a:a.value,b:b.value,c:c.value}})
}

//alert("New Search: "+route.query.q+route.query.t)
let { proxy } = getCurrentInstance();
const getData=async()=>{
  await proxy.$http
     .get('/api/search',
     {params:
      {
      query:route.query.q,
      type: route.query.t,
      need_check: '',
      before:route.query.b,
      after:route.query.a,
      color:route.query.c
     }
    })
     .then(function(res){
      console.log(res)
      const list = JSON.parse(JSON.stringify(res.data.results))
      spellchecked = res.data.corrected
      if(spellchecked != '')
        hasCorrected = true
      movieList.push(list)
      console.log(movieList[0])
      console.log(spellchecked)
     })
     .catch(function(error) {
      console.log(error);
    })
};

getData()

/*
onMounted(() => {
  console.log(route.params.query)
  
})
*/
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
.header{
  background-color: black;
  text-align: center;
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

  .big-title {
    font-weight: bold;
    padding-left: 20px;
    box-sizing: border-box;

    i {
      color: blue;
    }
  }

  .movie-list {
    height: 400px;
    overflow-y: auto;

    .movie-item {
      border: 1px solid #000;
      padding: 10px 24px;
      border-radius: 10px;
      box-sizing: border-box;
      margin: 10px 0;
      // background-color: #eee;
      cursor: pointer;

      .movie-name {
        color: black;
        font-size: 25px;
        font-weight: bold;
      }

      .movie-description {
        font-size: 12px;
        min-height: 50px;
        padding: 2px 0;
      }

      .movie-info {
        font-weight: bold;
        font-size: 12px;
      }
    }
  }

}
</style>