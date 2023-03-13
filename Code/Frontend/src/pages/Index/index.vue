!<!--  -->
<template>
  <div class='container'>
    <div class="header">
      <!--input class="iconfont search_input " type="text" placeholder="search"-->
      <SearchBar :q=q :t=t :key=q :pro=pro />
    </div>
    
    <div class="content">
      <div class="homebtn">
        <router-link to="/">
          <el-button text>
            Home <el-icon style="margin-left: 10px;" color="black" size="25"><HomeFilled /></el-icon>
          </el-button>
        </router-link>
      </div>
      <div class="big-title" v-if="spellchecked.value.length>0">
        Do you mean: 
        <el-space spacer="or ">
          <el-button v-for="(text, index) in spellchecked.value" :key="index" @click="$event => goCorrectedPage(text)" text>
            {{ text }}
          </el-button>
        </el-space>?
      </div>
      <div class="big-title" v-if="querySuggestion.value.length>0">
        You might also like:
        <el-space spacer="or ">
          <el-button v-for="(text, index) in querySuggestion.value" :key="index" @click="$event => goCorrectedPage(text)" text>
            {{ text }}
          </el-button>
        </el-space>
      </div>
      <div class="big-title">
        <p>Wall time in sever side: <i> {{ wallTime }} ms</i>. CPU time in sever side: <i> {{ cpuTime }} ms</i>.</p>
      </div>
      <div class="big-title">
        <p> <i> {{ totalNum }} </i> results are found. Show Top {{ movieList.rel.length }} only. 
          <el-button @click="handleFetchMore" v-if="movieList.rel.length < totalNum && movieList.rel.length != 0" text>
            Show more?
          </el-button>
        </p> 
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
import { useRouter,useRoute} from "vue-router"
import { ElNotification, ElMessageBox} from 'element-plus'
import SearchBar from '../MovieDetail/SearchBar.vue';
// import http from "@/util/http"
const router = useRouter()
const route = useRoute()

let movieList = reactive({value:[],show:[], rel:[]})
let spellchecked = reactive({value:[]})
let querySuggestion = reactive({value:[]})
let wallTime = ref('')
let cpuTime = ref('')
let totalNum = ref('')
let chunck_id = ref(0)
const relevence_ids = ref([])

let q = ref(route.query.q)
let t = ref(route.query.t)
let pro = ref(Boolean(route.query.pro=='true'))
console.log(route.query)
//alert("loading!") //for debug
const state = reactive({
  currentPage:1,
  total:1000,
  pageSize:10
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
        movieList.value = movieList.rel.slice(0,state.pageSize)
      }
      else{
        movieList.value = movieList.rel.slice()
      }
      movieList.show = movieList.rel.slice()

      totalNum.value = res.data.total
      wallTime.value = res.data.wallT
      cpuTime.value = res.data.cpuT
      relevence_ids.value = JSON.parse(JSON.stringify(res.data.ids))
      console.log(relevence_ids.value)
      console.timeEnd("getData");
     })
     .catch(function(error) {
      console.log(error);
      //console.log(additions);
    })
};

const getMoreData=async()=>{
  await proxy.$http
     .get('/api/fetchmore',
     {params:
      {
        ids:JSON.stringify(relevence_ids.value.slice(chunck_id.value*200, chunck_id.value*200+200)),
      }
    })
     .then(function(res){
      console.log(res)
      movieList.rel = movieList.rel.concat(JSON.parse(JSON.stringify(res.data.results)))
      state.total = movieList.rel.length
      movieList.show = movieList.rel.slice()
      console.log(movieList.rel.length)
     })
     .catch(function(error) {
      console.log(error);
    })
};

const getSpellCheck=async()=>{
  await proxy.$http
  .get('/api/spellcheck',
  {params:{input: route.query.q}}
  ).then(function(res){
    console.log("Spellcheck!")
    console.log(res)
    spellchecked.value = JSON.parse(JSON.stringify(res.data.corrected))
    querySuggestion.value = JSON.parse(JSON.stringify(res.data.suggestion))
    console.log(spellchecked)
    console.timeEnd("getSpellCheck");
  }).catch(function(error){
    console.log(error)
  })
}

/**
 *  watch the sort method
 */
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

/**
 * jump to the new page
 * @param {*} val 
 */
const handleCurrentChange=(val)=>{
  state.currentPage = val
  movieList.value = movieList.show.slice((val-1)*state.pageSize,val*state.pageSize)
}

const sliceStr= computed(()=>{
  // to slice a simple discription (no more than 500 chars)
  return function (val,len){
    return val.length>len?val.slice(0,len)+"...":val
  }
})

const arrEtc= computed(()=>{
  // add etc. after long array
  return function (arr,len){
    if(arr.length == 0)
      return "Unknown"
    return arr.length>len?arr[0]+"; "+arr[1]+" etc.":arr.join("; ")
  }
})

const handleFetchMore = () =>{
  ElMessageBox.confirm(
    'Do you want to fetch more? The results will be sorted by relevance.',
    'Search More?',
    {
      confirmButtonText: 'YES',
      cancelButtonText: 'Cancel',
      type: 'info',
    }
  ).then(()=>{
    ElNotification({
      title: 'Fetch more',
      message: "Fetch next 200 results (if exist) and the result will be sorted by relevance",
    })
    sort_by.value = 1
    chunck_id.value++
    getMoreData()
    console.log(chunck_id.value)
  })
  .catch(()=>{
    console.log("Cancelled fetch more!")
  })
}

console.time("getData");
getData()

if(route.query.pro == 'false' && route.query.check != 'false')
{
  console.time("getSpellCheck");
  console.log("SpellCheck");
  getSpellCheck()
}
else{
  console.log("notSpellCheck");
}

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

  .homebtn{
    align-self: flex-end;
  }

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
