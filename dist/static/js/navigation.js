let BookMark = Vue.extend({
    template: `
        <div class="col-sm-3">
                    <div class="xe-widget xe-conversations box2 label-info" @click="open_url(item.id,item.url)" data-toggle="tooltip" data-placement="bottom" title="" :data-original-title="item.url">
                        <div class="xe-comment-entry">
                            <a class="xe-user-img">
<!--                                <img :src="item.img" class="lozad img-circle" width="40">-->
                                <img v-lazy="item.img" width="40">
                            </a>
                            <div class="xe-comment">
                                <a href="#" class="xe-user-name overflowClip_1">
                                    <strong>{{item.title}}</strong>
                                </a>
                                <p class="overflowClip_2">{{item.desc}}</p>
                            </div>
                        </div>
                    </div>
                </div>
        `,
    props: ['item'],
    methods: {
        "open_url": function (id, url) {
            window.open(url, '_blank');
            $.get("/api/" + id + "/");
        }
    },
});

let CategoryBar = Vue.extend({
    template: `
        <div  class="row" >
        <h4 class="text-gray" style="margin-left: 15px;" ><i class="linecons-tag" style="margin-right: 7px;" :id="category"></i>{{category}} </h4>
                <book-mark v-for="(aitem,index) in items" :item="aitem" :key="index"></book-mark>
        </div>
        `,
    components: {
        BookMark,
    },
    props: ['category', 'items'],
});


let SideBar = Vue.extend({
    template: `
                        <ul id="main-menu" v-cloak class="main-menu">
                         <li>
                        <a href="oauth/qq/login/">
                            <i class="linecons-user"></i>
                            <span class="title">导航管理</span>
                        </a>
                        </li>

                    <li v-for="(items,cate,index) in user_data" :key="index">
                        <a :href="'#'+cate" class="smooth">
                            <i :class="items['icon']"></i>
                            <span class="title" >{{cate}}</span>
                        </a>
                    </li>
                       
                        <li>
                        <a href="static/about.html">
                            <i class="linecons-heart"></i>
                            <span class="title">关于本站</span>
                        </a>
                        </li>
                </ul>
        `,
    props: ['user_data']
});