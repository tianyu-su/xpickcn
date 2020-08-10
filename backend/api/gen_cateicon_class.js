

        // [{"model": "api.categoryicon", "pk": 1, "fields": {"ci_class": "13324234"}}]
let    linecons=['linecons-music', 'linecons-search', 'linecons-mail', 'linecons-heart', 'linecons-star', 'linecons-user', 'linecons-videocam', 'linecons-camera', 'linecons-photo', 'linecons-attach', 'linecons-lock', 'linecons-eye', 'linecons-tag', 'linecons-thumbs-up', 'linecons-pencil', 'linecons-comment', 'linecons-location', 'linecons-cup', 'linecons-trash', 'linecons-doc', 'linecons-note', 'linecons-cog', 'linecons-params', 'linecons-calendar', 'linecons-sound', 'linecons-clock', 'linecons-lightbulb', 'linecons-tv', 'linecons-desktop', 'linecons-mobile', 'linecons-cd', 'linecons-inbox', 'linecons-globe', 'linecons-cloud', 'linecons-paper-plane', 'linecons-fire', 'linecons-graduation-cap', 'linecons-megaphone', 'linecons-database', 'linecons-key', 'linecons-beaker', 'linecons-truck', 'linecons-money', 'linecons-food', 'linecons-shop', 'linecons-diamond', 'linecons-t-shirt', 'linecons-wallet']
res=[]
for(var i=0,len=linecons.length;i<len;i++){
    res.push({"model": "api.categoryicon", "pk": i+1, "fields": {"ci_class": linecons[i]}})


}

console.log(JSON.stringify(res))