!<!--  -->
<template>
  <div class='container'>
    <div class="header">
      <!--input class="iconfont search_input " type="text" placeholder="search"-->
      <SearchBar :q=q :t=t :key=q />
    </div>
    
    <div class="content">
      <div class="big-title" v-if="spellchecked.value.length>0">
        Do you mean: 
        <el-space spacer="or ">
          <el-button v-for="(text, index) in spellchecked.value" :key="index" @click="$event => goCorrectedPage(text)" text>
            {{ text }}
          </el-button>
        </el-space>?
      </div>
      <div class="big-title">
        <p>Wall time in sever side: <i> {{ wallTime }} ms</i>. CPU time in sever side: <i> {{ cpuTime }} ms</i>.</p>
      </div>
      <div class="big-title">
        <p> <i> {{ movieList.rel.length }} </i> results are found.</p>
      </div>
      <el-radio-group v-model="sort_by">
        <el-radio :label="1">By Relevance</el-radio>
        <el-radio :label="2">By Time (New to Old)</el-radio>
        <el-radio :label="3">By Time (Old to New)</el-radio>
        <el-radio :label="4">By Alphabet(A to Z)</el-radio>
        <el-radio :label="5">By Alphabet(Z to A)</el-radio>
      </el-radio-group>
      <!--el-scrollbar-->
        <div class="movie-list">
          <div class="movie-item" v-for="(item, index) in movieList.value" :key="index" @click="goMovieDetailPage(item.id)">
            <div class="movie-name">{{ item.movieName }}</div>
            <div class="movie-description">{{ sliceStr(item.description, 500) }}</div>
            <div class="movie-info">
              <span>Director: {{ arrEtc(item.director,2) }}• </span>
              <span>Year: {{ item.year }} • </span>
              <span>Country: {{ arrEtc(item.country,2) }} </span>
              <!--span>Runtime:{{ item.runtime }}</span-->
            </div>
          </div>
        </div>
      <!--/el-scrollbar-->
      <el-pagination
        @current-change ="handleCurrentChange"
        :page-size="state.pageSize"
        :pager-count="11"
        :current-page = "state.currentPage"
        layout="prev, pager, next,jumper"
        :total="state.total"
        :hide-on-single-page="true"
      />
    </div>
  

  </div>
</template>

<script setup>
import { reactive,watch,getCurrentInstance, ref, h,computed} from 'vue';
import { useRouter,useRoute, onBeforeRouteLeave, onBeforeRouteUpdate } from "vue-router"
import { ElNotification } from 'element-plus'
import SearchBar from '../MovieDetail/SearchBar.vue';
// import http from "@/util/http"
const router = useRouter()
const route = useRoute()

let movieList = reactive({value:[],show:[], rel:[]})
let spellchecked = reactive({value:[]})
let wallTime = ref('')
let cpuTime = ref('')
const relevence_ids = ref([])

let hasCorrected = ref(true)
let q = ref(route.query.q)
let t = ref(route.query.t)
console.log(route.query)
//alert("loading!") //for debug
const state = reactive({
  currentPage:1,
  total:1000,
  pageSize:25
})

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
    more: route.query.more,
    pro: route.query.pro
  }})
}

//alert("New Search: "+route.query.q+route.query.t)
let { proxy } = getCurrentInstance();
const getData=async()=>{
  await proxy.$http
     .get('/api/search',
     {params:
      {
      pro: route.query.pro,
      query:route.query.q,
      by: route.query.t,
      need_check: "",
      from:route.query.from,
      to:route.query.to,
      color:JSON.stringify(route.query.c),
      additions: JSON.stringify(route.query.more),
     }
    })
     .then(function(res){
      console.log(res)
      movieList.rel = JSON.parse(JSON.stringify(res.data.results))
      state.total = movieList.rel.length
      if(movieList.rel.length > state.pageSize){
        movieList.value = movieList.rel.slice(0,25)
      }
      else{
        movieList.value = movieList.rel.slice()
      }
      wallTime.value = res.data.wallT
      cpuTime.value = res.data.cpuT

      movieList.show = movieList.rel.slice()
      //console.log(movieList[0])
      //console.log(spellchecked)
     })
     .catch(function(error) {
      console.log(error);
      //console.log(additions);
    })
};
console.time("getData");
getData()
console.timeLog("getData");

const getSpellCheck=async()=>{
  await proxy.$http
  .get('/api/spellcheck',
  {params:{input: route.query.q}}
  ).then(function(res){
    console.log("Spellcheck!")
    console.log(res)
    spellchecked.value = JSON.parse(JSON.stringify(res.data.corrected))
    console.log(spellchecked)
  }).catch(function(error){
    console.log(error)
  })
}

console.time("getSpellCheck");

if(route.query.pro == 'false')
  getSpellCheck()

console.timeLog("getSpellCheck");

watch(sort_by, (new_data, old_data)=>{
  if(new_data == 1){
    ElNotification({
      title: "Sort by Relevance",
      message:h('i','The results will be sorted by relevance. Loading...')
    })
    movieList.show = movieList.rel.slice()
    movieList.value = movieList.show.slice((state.currentPage-1)*state.pageSize,state.currentPage*state.pageSize)
  }
  else if(new_data == 2){
    ElNotification({
      title: "Sort by Time(New to Old)",
      message:h('i','The results will be sorted by time. Loading...')
    })
    movieList.show.sort((a, b)=>b.year-a.year)
    movieList.value = movieList.show.slice((state.currentPage-1)*state.pageSize,state.currentPage*state.pageSize)
  }else if(new_data == 3){
    ElNotification({
      title: "Sort by Time(Old to New)",
      message:h('i','The results will be sorted by time. Loading...')
    })
    movieList.show.sort((a, b)=>a.year-b.year)
    movieList.value = movieList.show.slice((state.currentPage-1)*state.pageSize,state.currentPage*state.pageSize)
  }else if(new_data == 4){
    ElNotification({
      title: "Sort by Title",
      message:h('i','The results will be sorted by title(A to Z). Loading...')
    })
    movieList.show.sort((a, b)=>a.movieName.localeCompare(b.movieName))
    movieList.value = movieList.show.slice((state.currentPage-1)*state.pageSize,state.currentPage*state.pageSize)
  }else{
    ElNotification({
      title: "Sort by Title",
      message:h('i','The results will be sorted by title(Z to A). Loading...')
    })
    movieList.show.sort((a, b)=>b.movieName.localeCompare(a.movieName))
    movieList.value = movieList.show.slice((state.currentPage-1)*state.pageSize,state.currentPage*state.pageSize)
  }
})

const handleCurrentChange=(val)=>{
  state.currentPage = val
  movieList.value = movieList.show.slice((val-1)*state.pageSize,val*state.pageSize)
}

const sliceStr= computed(()=>{
  return function (val,len){
    return val.length>len?val.slice(0,len)+"...":val
  }
})

const arrEtc= computed(()=>{
  return function (arr,len){
    if(arr.length == 0)
      return "Unknown"
    return arr.length>len?arr[0]+"; "+arr[1]+" etc.":arr.join("; ")
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