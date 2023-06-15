<template>
    <div class="container">
        <div class="card">
            <header class="card-header">
                <p class="card-header-title">
                    Bientôt ici : {{ $route.params.title ?? 'Quelque chose' }}
                </p>
            </header>
        </div>
    </div>
</template>


<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator";

@Component({
  name: "Patience"
})
export default class extends Vue{
  head() {
    return {
      title: "Travaux en cours"
    };
  }
};
</script>