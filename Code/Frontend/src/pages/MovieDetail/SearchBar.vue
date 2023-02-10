<template>
  <div id="SearchBar" class="searchbar">
      
      <el-input
        class="text"
        placeholder="Please input your query"
        v-model="query"
        style="width: 40%">
      </el-input>
      
      <select v-model="selected" class="selected">
        <option value="title">by titel</option>
        <option value="cast">by cast</option>
      </select>
    
      <el-button
        @click="handleSearch"
        class="searchButton"
      >
      
      <router-link to="/"><img src="@/assets/svg/icons8-search.svg" alt="search"></router-link>
      </el-button>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import { useRouter } from "vue-router"

const router = useRouter()

const handleSearch=()=>{
      //this.$emit('search-for', this.query)
      router.push("/")
}

export default defineComponent({
  name: "SearchBar",
  //props: ["],
  //emits: ["update:modelValue"],
  data() {
    return{
      query: "",
      selected:"",
    }
  },
  methods: {
    
    
  },
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
</style>