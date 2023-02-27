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
          </div>
        </template>
        <el-form :model="form" label-width="120px">
          <!-- <el-form-item class="demonstration" label="Genre">
            <el-select v-model="value" placeholder="please select a genre">
              <el-option label="Zone one" value="shanghai" />
              <el-option label="Zone two" value="beijing" />
            </el-select>
          </el-form-item> -->
          <el-form-item class="demonstration" label="Year Range">
            <el-col :span="11">
              <el-input
              v-model="query.after"
              type="year"
              placeholder="YYYY">
              <template #prefix>
                <span class="range">From</span>
              </template>
              </el-input>
            </el-col>
            <el-col :span="2" class="text-center">
              <span class="text-gray-500">-</span>
            </el-col>
            <el-col :span="11">
              <el-input
                v-model="query.before"
                type="year"
                placeholder="YYYY">
                <template #prefix>
                  <span class="range">To</span>
                </template>
              </el-input>
            </el-col>
          </el-form-item>
          <el-form-item class="demonstration" label="Film Color">
            <el-checkbox-group v-model="query.color">
              <el-checkbox label="Black/White"/>
              <el-checkbox label="Colored"/>
            </el-checkbox-group>
          </el-form-item>
          <el-form-item>
            <el-button class="Advancedbutton" type="primary" @click="onSubmit">SEARCH</el-button>
            <el-button class="Advancedbutton">Cancel</el-button>
          </el-form-item>
        </el-form>

        <!-- version 1 -->
        <!-- <el-row class="year" style="width: 50%">
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
            <el-select v-model="value" placeholder="Select" style="height: 20px; width: 350px;">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
              <template #prefix>
                <span class="demonstration">Genre</span>
              </template>
            </el-select>
          </div>
        </el-row>

        <el-row class="filmColor" style="width:50%">
          <div class="block">
            <el-select v-model="query.color" placeholder="Select" style="height: 20px; width: 350px;">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
              <template #prefix>
                <span class="demonstration">Film Color</span>
              </template>
            </el-select>
          </div>
        </el-row> -->
      </el-card>
  </div>
</template>

<script>
import { all } from 'axios';
import { defineComponent,ref,reactive, onActivated} from 'vue';
import { useRouter } from "vue-router";

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
    var query = reactive({queryMsg:"", selected:"", before: "", after:"", color:[]})
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
    const form = reactive({})
    const onSubmit = () => {
      console.log('submit!')
      if (query.color.length == 2)
        query.color='all'
      router.push({path:"/search",query:{q:query.queryMsg, t:query.selected, a: query.after,b: query.before, c: query.color}})
    }
    
    
    function goSearchResult(){
      onSubmit()
      //router.push({path:"/search",query:{q:query.queryMsg, t:query.selected, a: query.after,b: query.before, c: query.color}})
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
      toggleBotton,
      form,
      onSubmit
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
  height: 800px;
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

.range{
  font-size: 15px;
  font-style: italic;
}
.block{
  width:50%;
  text-align: center;
  height: 20px;
}

.blockG{
  width: 350px;
  //text-align: center;
  //height: 20px;
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