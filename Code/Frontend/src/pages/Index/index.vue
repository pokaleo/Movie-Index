!<!--  -->
<template>
  <div class='container'>
    <div class="header">
      <!--input class="iconfont search_input " type="text" placeholder="search"-->
      <SearchBar :q=q :t=t :key=q />
    </div>
    
    <div class="content">
      <div class="big-title" v-if="hasCorrected">
        Did you mean: <el-button @click="$event => goCorrectedPage(spellchecked)" text>{{ spellchecked }}</el-button>?
      </div>
      <div class="big-title">
        <p>Wall time in sever side: <i> {{ wallTime }} ms</i>. CPU time in sever side: <i> {{ cpuTime }} ms</i>.</p>
      </div>
      <el-radio-group v-model="sort_by">
        <el-radio :label="1">By Relevance</el-radio>
        <el-radio :label="2">By Time</el-radio>
      </el-radio-group>
      <el-scrollbar>
        <div class="movie-list">
          <div class="movie-item" v-for="(item, index) in movieList.value" :key="index" @click="goMovieDetailPage(item.id)">
            <div class="movie-name">{{ item.movieName }}</div>
            <div class="movie-description">{{ item.description }}</div>
            <div class="movie-info">
              <span>Director:{{ item.director }} • </span>
              <span>Year: {{ item.year }} • </span>
              <span>Country:{{ item.country }} • </span>
              <!--span>Runtime:{{ item.runtime }}</span-->
            </div>
          </div>
        </div>
      </el-scrollbar>
    </div>
  

  </div>
</template>

<script setup>
import { reactive,watch,onMounted,getCurrentInstance, ref, h } from 'vue';
import { useRouter,useRoute, onBeforeRouteLeave, onBeforeRouteUpdate } from "vue-router"
import { ElNotification } from 'element-plus'
import SearchBar from '../MovieDetail/SearchBar.vue';
// import http from "@/util/http"
const router = useRouter()
const route = useRoute()

let movieList = reactive({value: [],time:[], rel:[]})
let spellchecked = ref('')
let wallTime = ref('')
let cpuTime = ref('')
const relevence_ids = ref([])

let hasCorrected = false
let q = ref(route.query.q)
let t = ref(route.query.t)
console.log(route.query)
//alert("loading!") //for debug

const sort_by = ref(1)

/**
 * go to movie detail page
 * @param movieId 
 */
const goMovieDetailPage = (movieId) => {
  router.push("/detail/" + movieId)
}

/**
 * go to new search page(query with spellecked)
 * @param newquery 
 */
const goCorrectedPage = (newquery) => {
  router.replace({name:"Results",
  query:
   {q:newquery, 
    t:t.value, 
    from: route.query.from, 
    to:route.query.to, 
    c:route.query.c,
    more: route.query.more
  }})
}

//alert("New Search: "+route.query.q+route.query.t)
let { proxy } = getCurrentInstance();
const getData=async()=>{
  await proxy.$http
     .get('/api/search',
     {params:
      {
      query:route.query.q,
      by: route.query.t,
      need_check: "",
      from:route.query.from,
      to:route.query.to,
      color:JSON.stringify(route.query.c),
      additions: JSON.stringify(route.query.more)
     }
    })
     .then(function(res){
      console.log(res)
      movieList.value = JSON.parse(JSON.stringify(res.data.results))
      spellchecked = res.data.corrected
      if(spellchecked != '' && spellchecked != route.query.q)
        hasCorrected = true
      else
        hasCorrected = false
      //movieList.push(list)
      //movieList = list
      wallTime.value = res.data.wallT
      cpuTime.value = res.data.cpuT
      console.log(movieList[0])
      console.log(spellchecked)
     })
     .catch(function(error) {
      console.log(error);
    })
};

getData()

const sort_results=()=>{
  movieList.value.sort((a, b)=>b.year-a.year)
}

watch(sort_by, (new_data, old_data)=>{
  if(movieList.rel.length == 0)
      movieList.rel = movieList.value.slice()
  if(new_data == 1){
    ElNotification({
      title: "Sort by Relevance",
      message:h('i','The results will be sorted by relevance. Loading...')
    })
    movieList.value = movieList.rel
  }
  else{
    ElNotification({
      title: "Sort by Time",
      message:h('i','The results will be sorted by time. Loading...')
    })
    if(movieList.time.length == 0)
      movieList.time = movieList.value.slice().sort((a, b)=>b.year-a.year)
    movieList.value = movieList.time
  }
})

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