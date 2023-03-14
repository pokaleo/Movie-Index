!<!--  -->
<template>
  <div class='container'>
    <div class="header">
      <!--input class="iconfont search_input " type="text" placeholder="search"-->
      <div class="logo-container">
        <img src="@/assets/logo.png" alt="logo" class="logo"/>
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

    <div style="background:linear-gradient(to left,#e7e9ee,#5a6794,#e7e9ee);height:2px;margin-top: 2%"></div>
    
    <div class="content">
      <div class="big-title" v-if="spellchecked.value.length>0">
        Do you mean: 
        <el-space spacer="or ">
          <el-button color="#5a6794" v-for="(text, index) in spellchecked.value" :key="index" @click="$event => goCorrectedPage(text)">
            {{ text }}
          </el-button>
        </el-space>?
      </div>
      <div class="big-title" v-if="querySuggestion.value.length>0">
        You might also like:
        <el-space spacer="or ">
          <el-button color="#5a6794" v-for="(text, index) in querySuggestion.value" :key="index" @click="$event => goCorrectedPage(text)">
            {{ text }}
          </el-button>
        </el-space>
      </div>
      <div class="big-title">
        <p>Time consumed: Wall time in sever side: <i> {{ wallTime }} ms</i>. CPU time in sever side: <i> {{ cpuTime }} ms</i>.</p>
      </div>
      <div class="big-title">
        <p> <i> {{ totalNum }} </i> results are found. Show Top {{ movieList.rel.length }} only. 
          <el-button @click="handleFetchMore" v-if="movieList.rel.length < totalNum && movieList.rel.length != 0" text>
            Show more?
          </el-button>
        </p> 
      </div>
      <van-radio-group class="radioBtn" direction="horizontal" v-model="sort_by" >
        <van-radio name="1" checked-color="#333c60">By Relevance</van-radio>
        <van-radio name="2" checked-color="#333c60">By Time (New to Old)</van-radio>
        <van-radio name="3" checked-color="#333c60">By Time (Old to New)</van-radio>
        <van-radio name="4" checked-color="#333c60">By Alphabet(A to Z)</van-radio>
        <van-radio name="5" checked-color="#333c60">By Alphabet(Z to A)</van-radio>
      </van-radio-group>
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
  background-color: transparent;
  text-align: center;
  margin-top: 3%;
  display: flex;
  align-items: center;
  justify-content: space-between;
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
