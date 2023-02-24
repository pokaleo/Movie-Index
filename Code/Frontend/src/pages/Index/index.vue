!<!--  -->
<template>
  <div class='container'>
    <div class="header">
      <!--input class="iconfont search_input " type="text" placeholder="search"-->
      <SearchBar :q=q :t=t :key=q />
    </div>
    
    <div class="content">
      <div class="big-title" v-if="hasCorrected">
        Did you mean: <i>{{ spellchecked }}</i>?
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
  

  </div>
</template>

<script setup>
import { reactive,watch,onMounted,getCurrentInstance } from 'vue';
import { useRouter,useRoute, onBeforeRouteLeave, onBeforeRouteUpdate } from "vue-router"
import SearchBar from '../MovieDetail/SearchBar.vue';
const router = useRouter()
const route = useRoute()

let movieList = reactive([])
let spellchecked = reactive()
let hasCorrected = false
let q = reactive(route.query.q)
let t = reactive(route.query.t)


/**
 * 跳转电影详情页面
 * @param movieId 
 */
const goMovieDetailPage = (movieId) => {
  router.push("/detail/" + movieId)
}

//alert("New Search: "+route.query.q+route.query.t)
let { proxy } = getCurrentInstance();
const getData=async()=>{
  await proxy.$http
     .post('http://10.124.30.217:8800/search',{
      query:route.query.q,
      type: route.query.t,
      need_check: false
     })
     .then(function(res){
      console.log(res)
      const list = JSON.parse(JSON.stringify(res.data.results))
      spellchecked = res.data.corrected
      if(spellchecked != '')
        hasCorrected = true
      movieList.push(list)
      console.log(movieList[0])
      //console.log(spellchecked)
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
}
.header{
  background-color: black;
  text-align: center;
}

.content {
  width: 600px;
  height: 300px;
  margin: 0 auto;
  margin-top: 30px;

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
      box-sizing: border-box;
      margin: 10px 0;
      background-color: #eee;
      cursor: pointer;

      .movie-name {
        color: blue;
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