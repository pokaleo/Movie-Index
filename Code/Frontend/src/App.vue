
<template>
  

    <router-view v-slot="{ Component }">
      <transition>
        <keep-alive>
          <component :is="Component" :key="$route.fullPath"/>
        </keep-alive>
      </transition>
        <!--component :is="Component"  v-if="!$route.meta.keepAlive" :key="$route.fullPath"/-->
    </router-view>

  
</template>

<style >
html,
body,
#app {
  height: 100%;
  width: 100%;
  padding: 0;
  margin: 0;
}
</style>
