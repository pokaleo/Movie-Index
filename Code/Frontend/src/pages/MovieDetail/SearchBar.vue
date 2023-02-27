<template>
  <div id="SearchBar" class="searchbar">
      
      <el-input
        class="text"
        placeholder="Please input your query"
        v-model="query.queryMsg"
        style="width: 40%">
      </el-input>
      
      <select v-model="query.selected" class="selected">
        <option value="title">by title</option>
        <option value="general">by general</option>
        <option value="keywords">by keywords</option>
        <option value="genres">by genres</option>
      </select>
    
      <!--router-link :to="'/result/'+selected+'/'+query"-->
      <el-button
        class="searchButton"
        @click="goSearchResult"
      >
        <img src="@/assets/svg/icons8-search.svg" alt="search">
      </el-button>
      <!--/router-link-->
      <!--el-collapse v-model="activeNames" @change="handleChange" style="width: 40%">
        <el-collapse-item title="Advance" name="1">  
        </el-collapse-item>
      </el-collapse-->
      <el-button class='advanced' @click="() => toggleBotton('clickT')">
        ADVANCED SEARCH
      </el-button>
      <el-card class="card" v-if="filterTrigger.clickT">
        <template #header>
          <div class="card-header">
            <span>Search Filters</span>
            <el-button class="Advancedbutton" text>SEARCH</el-button>
          </div>
        </template>
        <el-row class="year" style="width: 50%">
          <div class="block">
            <el-input
              v-model="query.after"
              placeholder="YYYY"
            >
            <template #prefix>
              <span class="demonstration">Start Year</span>
            </template>
            </el-input>
          </div>
        </el-row>
        <el-row class="year" style="width: 50%">
          <div class="block">
            <el-input
              v-model="query.before"
              type="year"
              placeholder="YYYY"
            >
            <template #prefix>
              <span class="demonstration">End Year</span>
            </template>
            </el-input>
          </div>
        </el-row>
        <el-row class="genre" style="width:50%">
          <div class="block">
            <span class="demonstration">Genre</span>
            <el-cascader
              v-model="value"
              :options="options"
              :props="props"
              @change="handleChange"
            />
          </div>
        </el-row>
        <el-row class="filmColor" style="width:50%">
          <div class="block">
            <span class="demonstration">Film Color</span>
            <el-cascader
              v-model="query.color"
              :options="options"
              :props="props"
              @change="handleChange"
            />
          </div>
        </el-row>    
      </el-card>
  </div>
</template>

<script>
import { defineComponent,ref,reactive, onActivated} from 'vue';
import { useRouter } from "vue-router";
// import {advancedsearch} from "./advancedSearch"

//import { getJson } from "serpapi";

export default defineComponent({
  name: "SearchBar",
  props: {
    q: String,
    t: String,
    a: String,
    b: String,
    c: String
  },
  //emits: ["update:modelValue"],
  setup(props){
    const router = useRouter()
    var query = reactive({queryMsg:"", selected:"", before: "", after:"", color:""})
    const filterTrigger = ref({
      clickT: false
    })
    //console.log("props"+props.q)
    //const activeNames = ref(['1'])
    //const handleChange = (val) => {
      //console.log(val)
    //}
    const toggleBotton = (trigger) => {
      filterTrigger.value[trigger] = !filterTrigger.value[trigger]
    }
    
    function goSearchResult(){
      //const params = { q: "Coffeee", hl: "en", gl: "us", api_key: "c12acfe0db8b5121456501187b15bee5050b365fcec0a75660456e14aad16a5e" }; 
      //const response = getJson("google", params);
      //console.log(response["search_information"]);
      router.push({path:"/search",query:{q:query.queryMsg, t:query.selected, b: query.before, a: query.after, c: query.color}})
    }

    onActivated(()=>{
      //const router = useRouter()
      query.queryMsg=props.q
      query.selected=props.t
      query.after = props.a
      query.before = props.b
      query.color = props.c
    })
    return{
      query,
      goSearchResult,
      filterTrigger,
      toggleBotton
    }

    
  }
});
</script>

<style lang="scss" scoped>
.text{
  width: 40%;
  height: 35px;
  outline: hidden;
  margin: auto;
  border: 1px solid black;
  background: white;
}
.searchButton{
  background: white;
  height: 40px;
  margin-left: 10px;
}

.selected{
  height: 35px;
  background-color: white;
}

img{
  width: 20px;
}
.year{
  width: 40%;
  left: 30%;
  margin-top: 20px;
  //margin-left: 10px;
  //margin-right: 10px;
}
.card{
  height: 300px;
  background-color: white;
}

.genre{
  width: 40%;
  left: 30%;
  margin-top: 30px;
  margin-left: 10px;
  margin-right: 10px;
}

.filmColor{
  width: 40%;
  left: 30%;
  margin-top: 30px;
  margin-left: 10px;
  margin-right: 10px;
}

.demonstration{
  font-size: 18px;
  font-style: oblique;
  font-weight: bold;
  margin-right: 10px;
}
.block{
  width:50%;
  text-align: center;
  height: 20px;
}
.advanced{
  height: 40px;
}
.card-header {
  font-size: 20px;
  font-style: oblique;
  font-weight: bold;
  margin-left: 100px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.Advancedbutton{
  width: 200px;
  height: 40px;
  margin-right: 120px;
  font-size: 15px;
  font-style:oblique;
  font-weight: bold;
}


</style>