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
      <el-row class="year">
      <div class="block">
        <span class="demonstration">After</span>
        <el-date-picker
          v-model="after"
          type="year"
          placeholder="Pick a year"
        />
      </div>
      <div class="block">
        <span class="demonstration">Before</span>
        <el-date-picker
          v-model="before"
          type="year"
          placeholder="Pick a year"
        />
      </div>
      </el-row>
  </div>
</template>

<script>
import { defineComponent,ref,reactive, onActivated} from 'vue';
import { useRouter } from "vue-router"
//import { getJson } from "serpapi";

export default defineComponent({
  name: "SearchBar",
  props: {
    q: String,
    t: String,
  },
  //emits: ["update:modelValue"],
  setup(props){
    const router = useRouter()
    var query = reactive({queryMsg:props.q, selected:props.t})
    const before=ref('')
    const after=ref('')
    //console.log("props"+props.q)
    //const activeNames = ref(['1'])
    //const handleChange = (val) => {
      //console.log(val)
    //}

    function goSearchResult(){
      //const params = { q: "Coffeee", hl: "en", gl: "us", api_key: "c12acfe0db8b5121456501187b15bee5050b365fcec0a75660456e14aad16a5e" }; 
      //const response = getJson("google", params);
      //console.log(response["search_information"]);
      router.push({path:"/search",query:{q:query.queryMsg, t:query.selected}})
    }

    onActivated(()=>{
      //const router = useRouter()
      query.queryMsg=props.q
      query.selected=props.t
    })
    return{
      query,
      before,
      after,
      goSearchResult
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
  margin-top: 10px;
}
.block{
  text-align: center;
}
</style>