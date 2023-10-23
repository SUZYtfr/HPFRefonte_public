# Branche upgrade

Cette branche a pour but de préparer la mise à niveau du projet de NuxtJS à Nuxt 3.
Pour le moment, seules ont été travaillées la page d'index et celle d'auteur et leurs composants pour évaluer la faisabilité de cette mise à niveau.

## node 18
Je n'ai identifié aucun souci à l'utilisation de node 18.

## vue 3
### filtres
Les filtres de rendus sont supprimés, il faut plutôt appeler des méthodes directement depuis \<script> :
https://v3-migration.vuejs.org/breaking-changes/filters.html#_3-x-update
### v-for
:key doit maintenant exclusivement se trouver sur l'élément parent
### simplebar
simplebar-vue, dans template ET dans mounted()?
depuis config, components ? https://nuxt.com/docs/api/nuxt-config#components
ou config, imports ? https://nuxt.com/docs/guide/concepts/auto-imports#auto-import-from-third-party-packages
### buefy-next
Buefy-next est une branche en développement du projet Buefy qui vise l'intégration à Vue 3, ça a l'air de fonctionner dans l'ensemble.
Le module nuxt/buefy ne traitant pas nuxt 3, il faut installer Buefy (next) dans un plugin. J'ai réutilisé plugins/fontawesome.ts pour ça, mais on pourrait séparer en deux modules (penser à l'ordre de montage des plugins dans ce cas)
Problème avec le composant Tabs, qui semble vouloir accéder à window lors du rendu serveur. Comme Buefy-next ne suit pas les mises à jour de la branche principale, c'est peut-être corrigé sur celle-là. En attendant j'ai enveloppé Tabs dans \<ClientOnly>.
### fontawesome
Les icônes de fontawesome sont bien rendues par le client (sauf "star" dans \<b-rate> ??) mais pas trouvées par le serveur ("Could not find one or more icon(s) { prefix: 'fas', iconName: 'comment-alt' } {}"). Ça crée une série d'avertissements lors de l'hydration. Je comprends pas pourquoi, mais c'est un problème mineur, j'imagine.
### bulma-badge
J'ai remplacé par le fork d'un type qui corrige ce satané avertissement de #calc() lors de la compilation
### tiptap et ImageHPF
Passage de @tiptap/vue-2 à @tiptap/vue-3, aucun souci à signaler

## compatibilité des modules
### adios axios
Nuxt 3 intègre $fetch/ofetch, qui est un wrapper autour de JS fetch(), et offre des hooks pratiques comme useAsyncData(), qui remplace (en gros) la logique préalablement implémentée par le hook fetch() de NuxtJS. Axios n'est plus pris en charge. J'ai gardé le même principe de wrapper qu'auparavant, par exemple autour de searchNews(). La "configuration" de useFetch est faite non plus dans un plugin mais dans un composable.
À faire :
- Gérer pending et error.
### @nuxt/auth
Il est annoncé que @nuxt/auth devrait être adapté pour fonctionner avec Nuxt 3 (ou l'inverse) bientôt. En attendant, je n'ai pas réussi à le faire fonctionner. Il n'y a donc pour l'instant pas de gestion de l'authentification. À la place, j'ai créé un faux plugin _auth.ts pour mimer son ancien interface.
À faire :
- Il y a d'autres modules d'authentification déjà disponibles (plus ou moins stables, selon certains) pour Nuxt 3, mais avec d'autres interfaces à implémenter. À voir si on peut pas attendre.
### vuex
Il serait apparemment possible d'intégrer Vuex 4, mais le module sera probablement abandonné pour Nuxt 3. Vuex 5 est "essentiellement Pinia", qui est officiellement pris en charge.
nuxt3-vuex-module permettrait l'injection de $store dans Vue (ce qui n'est plus automatique dans Nuxt 3). Il ne semble pas fonctionner sans @nuxt/typescript-build (ce qui est étrange), il faudra virer ce dernier en même temps.
Par contre, pas moyen de faire fonctionner vuex-module-decorators, les getters fonctionnent mais pas les mutations ("\[vuex] unknown mutation type: modules/ModalsStates/setContactModalActive"). On pourrait virer ce module mais quitte à recoder, autant implémenter Pinia.

## Syntaxe Composition API vs class components
### vue-class-component, vue-property-decorators, nuxt-property-decorators
Remplacés tous trois par vue-facing-decorator qui fonctionne avec Vue 3 et offre la même API. Dans certains cas (par exemple quand il fallait remplacer l'ancien hook fetch()) ça ne semblait pas faire l'affaire et j'ai recodé pour utiliser composition API.
Pour éviter de devoir remplacer le module dans chaque composant avant qu'on passe en Composition API, j'ai aliasé les trois dans packages.json pour rediriger vers vue-facing-decorators. VSCode grogne mais pas les compilateurs. 
### props
Les props sont maintenant pleinement immuables :
https://vuejs.org/guide/components/props.html#one-way-data-flow
Il faudra dans certains cas refaire la logique pour passer par des emits ou des states, par exemple pour les filtres de fictions.

## SSR
### reflect-metadata
Nécessaire à l'utilisation de class-transformer, doit être importé globalement, mais ce n'est plus possible via un middleware. Pour l'instant je dois le cas échéant l'importer dans les modèles, qui utilisent les decorateurs.
Il y a forcément un moyen d'importer reflect-metadata globablement comme avant, j'ai essayé ça (link) (modules dans config) mais ça ne marche pas.
### @SerialiseClass
Ne peut pas être utilisé avec composition API, j'ai donc opté pour un plugin serialise.ts pour indiquer quelles données sérialiser / déserialiser. C'est pas très beau, il faut entrer chaque classe à sérialiser / désérialiser. Il faudrait chercher une meilleure façon de procéder.

## plugins/middleware
/middleware traite maintenant exclusivement le routage. Si j'ai bien compris, tout ce qui ne porte pas strictement sur le routage devrait devenir un plugin.
/plugins change de syntaxe, sans gros problème.

## vite
Vite remplace Webpack par défaut, mais il est toujours possible de remettre ce dernier si besoin.

## typescript intégré
Nuxt 3 intègre typescript pleinement. J'ai pas très bien compris ce que ça implique exactement, si ce n'est qu'on a plus besoin de @nuxt/types et @nuxt/typescrip-build. Une partie de mes modifications est typée quand j'ai pu sans trop me prendre la tête mais j'ai désactivé le mode strict.

## Packages
J'ai fait le ménage dans les dépendences là où j'ai compris ce que je faisais.

## Divers
- \<Nuxt/> devient \<slot/>
- dans nuxt.config.ts, il fallait virer le paramètre hid de la définition de la balise \<head> : https://nuxt.com/docs/migration/meta#migration
- les variables d'environnement sont copiées dans runtimeConfig par dotenv, avec une syntaxe particulière 

## À faire
- revoir config, dev (sans bundle, minify) vs production
- options esbuild, loaders, etc.
- import css
- plugin classes toujours utile ?
- build et preview
