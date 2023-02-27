<template>
  <div id="SearchBar" class="searchbar">
      
      <el-input
        class="text"
        placeholder="Please enter a search term"
        v-model="query.queryMsg"
        style="width: 50%">
        <template #append>
          <!--router-link :to="'/result/'+selected+'/'+query"-->
          <el-button
            class="searchButton"
            @click="goSearchResult"
          >
            <img src="@/assets/svg/icons8-search.svg" alt="search">
          </el-button>
          <!-- <el-button :icon="Search" /> -->
        </template>
      </el-input>
      
      <!-- <select v-model="query.selected" class="selected">
        <option value="title">by title</option>
        <option value="general">by general</option>
        <option value="keywords">by keywords</option>
        <option value="genres">by genres</option>
      </select> -->
    
      <!--router-link :to="'/result/'+selected+'/'+query"-->
      <!-- <el-button
        class="searchButton"
        @click="goSearchResult"
      >
        <img src="@/assets/svg/icons8-search.svg" alt="search">
      </el-button> -->


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
          <el-form-item class="demonstration" label="Browse By">
            <el-input
              v-model="query.queryMsg"
              placeholder="Please enter a search term"
              class="input-with-select"
            >
              <template #prepend>
                <el-select class="selectNot" v-model="query.selected" placeholder="Any" style="width: 115px">
                  <el-option value="title">Title</el-option>
                  <el-option value="general">General</el-option>
                  <el-option value="keywords">Keywords</el-option>
                  <el-option value="genres">Genres</el-option>
                </el-select>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item v-for="item in count" :key="item" class="demonstration" label="Alternatives">
            <el-input
              v-model="input3"
              placeholder="Please enter a search term"
              class="input-with-select"
            >
              <template #prepend>
                <el-select class="selectNot" v-model="select" placeholder="AND" style="width: 95px">
                  <el-option label="AND" value="1" />
                  <el-option label="NOT" value="2" />
                </el-select>
                <el-select class="selected" v-model="query.selected" placeholder="Any" style="width: 95px">
                  <el-option value="title">Title</el-option>
                  <el-option value="general">General</el-option>
                  <el-option value="keywords">Keywords</el-option>
                  <el-option value="genres">Genres</el-option>
                </el-select>
              </template>
            </el-input>
          </el-form-item>
          <el-button class="AlterButton" @click="add">Add A New Request Line</el-button>
          <el-button class="AlterButton" @click="onDelete">Delete A Line</el-button>
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
            <el-button class="Advancedbutton" clearable>CLEAR</el-button>
          </el-form-item>
        </el-form>
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
    const count = ref(1)
    const form = reactive({})
    const onSubmit = () => {
      console.log('submit!')
      if (query.color.length == 2)
        query.color='all'
      router.push({path:"/search",query:{q:query.queryMsg, t:query.selected, a: query.after,b: query.before, c: query.color}})
    }
    const add = () => {
      count.value++
    }
    const onDelete = () => {
      if (count.value > 0) {
        count.value--
      }
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
      count,
      add,
      onDelete,
      form,
      onSubmit
    }

    
  }
});
</script>

<style lang="scss" scoped>
.text{
  width: 60%;
  height: 45px;
  outline: hidden;
  margin: auto;
  //border: 1px solid rgb(67, 66, 66);
  background: white;
}
.searchButton{
  background: white;
  height: 45px;
  width: 60px;
}

.selected{
  margin-left: 20px;
}


img{
  width: 20px;
}

.card{
  height: 800px;
  background-color: white;
}

.demonstration{
  font-size: 18px;
  font-style: oblique;
  font-weight: bold;
  margin-right: 10px;
}

.AlterButton{
  margin-bottom: 10px;
  font-style: italic;
}

.range{
  font-size: 15px;
  font-style: italic;
}

.advanced{
  height: 45px;
  font-weight: bold;
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
  height: 45px;
  margin-right: 120px;
  font-size: 15px;
  font-style:oblique;
  font-weight: bold;
}


</style>